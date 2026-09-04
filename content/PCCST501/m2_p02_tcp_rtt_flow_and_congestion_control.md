# Progressive Problems: TCP Dynamic Timeout Estimation & Karn's Algorithm

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped fraction-to-decimal conversions, and full line-by-line arithmetic.

---

## Level 1: Single RTT Measurement Update

### Problem 1.1: Calculating EstimatedRTT, DevRTT, and RTO from a Single Sample

**Problem Statement:** A running TCP connection has an existing estimated average Round-Trip Time of $\text{EstimatedRTT} = 40.0\text{ ms}$ and an existing estimate of RTT variation of $\text{DevRTT} = 10.0\text{ ms}$.  
A data segment is transmitted, and its acknowledgment (ACK) returns safely, providing a fresh measurement of $\text{SampleRTT} = 60.0\text{ ms}$.  
Using the standard Internet engineering formulas from RFC 6298 with smoothing weight parameters $\alpha = 0.125 = \frac{1}{8}$ and $\beta = 0.25 = \frac{1}{4}$:  
1. Compute the new updated average Round-Trip Time ($\text{EstimatedRTT}_{\text{new}}$).  
2. Compute the current absolute error $|\text{SampleRTT} - \text{EstimatedRTT}_{\text{new}}|$ between the measured sample and the new estimate.  
3. Compute the new updated deviation/jitter estimate ($\text{DevRTT}_{\text{new}}$).  
4. Calculate the newly updated Retransmission Timeout ($\text{RTO}$).

::: callout-intuition Core Mental Model
Think of your computer's TCP timer like a smart digital alarm clock that tries to guess how long pizza delivery will take.  
- **SampleRTT:** You ordered pizza tonight, and it took $60\text{ minutes}$ to arrive. That is tonight's single raw measurement.  
- **EstimatedRTT:** Your historical average delivery time has been $40\text{ minutes}$. Because tonight had unexpected traffic, you do not throw away your entire multi-month history! Instead, you nudge your historical average just a little bit higher.  
- **DevRTT:** The "spread" or "jitter" of delivery times. Sometimes pizza arrives in $30\text{ minutes}$, sometimes in $50\text{ minutes}$. $\text{DevRTT}$ tracks how unpredictable the delivery person is.  
- **RTO (Retransmission Timeout):** How long you will wait before calling the restaurant to scream: *"My pizza is lost! Send another one!"* You do not set this timer to your bare average ($40\text{ minutes}$), or else every time delivery is even slightly delayed by a red light, you would demand a duplicate pizza. You set the timer to:  
$$\text{Average Delivery Time} + 4 \times (\text{Traffic Fluctuation Margin})$$
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Identify Given Variables and Align Units</div>

**What are we doing?** Writing down all given variables and confirming they all share the exact same measurement unit (milliseconds, $\text{ms}$).

**Why are we starting here?** You can never plug numbers into a networking formula without ensuring that times are not mixed between seconds and milliseconds.

**How do we do it?**
- Current baseline average: $\text{EstimatedRTT}_{\text{old}} = 40.0\text{ ms}$  
- Current baseline deviation: $\text{DevRTT}_{\text{old}} = 10.0\text{ ms}$  
- Newly arrived measurement: $\text{SampleRTT} = 60.0\text{ ms}$  
- Weight parameter for average: $\alpha = 0.125$ (which is equal to the fraction $\frac{1}{8}$)  
- Weight parameter for deviation: $\beta = 0.25$ (which is equal to the fraction $\frac{1}{4}$)  
All time values are in milliseconds ($\text{ms}$), so no unit scaling is required.

**Where did this formula/concept come from?** The standard parameters are specified by the Internet Engineering Task Force (IETF) in **RFC 6298** ("Computing TCP's Retransmission Timer").
</div>

<div class="step-card">
<div class="step-badge">Step 2: Understand the EWMA Formula for EstimatedRTT</div>

**What changed from Step 1?** We have listed our inputs. Now we inspect the mathematical engine used to update the average: the **Exponentially Weighted Moving Average (EWMA)**.

**What are we doing?** Breaking down the formula:  
$$\text{EstimatedRTT}_{\text{new}} = (1 - \alpha) \times \text{EstimatedRTT}_{\text{old}} + \alpha \times \text{SampleRTT}$$

**Why are we doing this?** Why doesn't TCP simply average all historical RTTs using normal arithmetic mean $\frac{x_1 + x_2 + \dots + x_n}{n}$? Because network conditions change over time! If you download a huge file today, yesterday's latency is irrelevant. EWMA gives the most weight to recent history while smoothly ignoring short, random spikes.

**How do we do it?** Notice the weights:  
- $(1 - \alpha) = 1.0 - 0.125 = 0.875$ (or $\frac{7}{8}$). This means **$87.5\%$** of the new value comes from our stable past history!  
- $\alpha = 0.125$ (or $\frac{1}{8}$). This means only **$12.5\%$** of the new value is influenced by tonight's new sample.

**Where did this formula/concept come from?** Signal processing and time-series statistics. It is a discrete low-pass filter that lets underlying long-term trends pass through while filtering out rapid, noisy fluctuations.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Calculate the New EstimatedRTT Line-by-Line</div>

**What changed from Step 2?** We understand the equation; now we perform the exact decimal multiplication and addition.

**What are we doing?** Calculating $\text{EstimatedRTT}_{\text{new}}$.

**How do we do it?**
1. Calculate the weight of the historical estimate:  
$$(1 - \alpha) \times \text{EstimatedRTT}_{\text{old}} = 0.875 \times 40.0\text{ ms}$$  
$$0.875 \times 40.0 = \frac{7}{8} \times 40.0 = 7 \times \left(\frac{40.0}{8}\right) = 7 \times 5.0 = 35.0\text{ ms}$$  

2. Calculate the weight of the fresh sample:  
$$\alpha \times \text{SampleRTT} = 0.125 \times 60.0\text{ ms}$$  
$$0.125 \times 60.0 = \frac{1}{8} \times 60.0 = \frac{60.0}{8} = 7.5\text{ ms}$$  

3. Add both partial contributions together:  
$$\text{EstimatedRTT}_{\text{new}} = 35.0\text{ ms} + 7.5\text{ ms} = 42.5\text{ ms}$$  

Notice: The sample spiked dramatically from $40\text{ ms}$ to $60\text{ ms}$ ($+20\text{ ms}$ surge), but our new estimate only nudged up from $40.0\text{ ms}$ to $42.5\text{ ms}$. The EWMA successfully dampened the shock.

**Where did this formula/concept come from?** RFC 6298 Section 2.3.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Compute the Absolute Estimation Error (Difference)</div>

**What changed from Step 3?** We now have $\text{EstimatedRTT}_{\text{new}} = 42.5\text{ ms}$. Before we can calculate deviation, we must figure out how far off our new estimate was from the raw reality of the link.

**What are we doing?** Calculating the absolute difference:  
$$\text{Error} = |\text{SampleRTT} - \text{EstimatedRTT}_{\text{new}}|$$

**Why are we doing this?** In statistics, variation is measured by looking at the distance between an actual observation and the mean. We take the absolute value ($|\dots|$) because an error is equally disruptive whether the packet was unexpectedly late or unexpectedly early.

**How do we do it?**
1. Subtract the newly computed estimate from the sample:  
$$\text{SampleRTT} - \text{EstimatedRTT}_{\text{new}} = 60.0\text{ ms} - 42.5\text{ ms} = +17.5\text{ ms}$$  

2. Take the absolute value:  
$$|+17.5\text{ ms}| = 17.5\text{ ms}$$  

*(Pedagogical Note: Older RFC 793 / Jacobson 1988 texts sometimes computed this error using $\text{EstimatedRTT}_{\text{old}}$, but RFC 6298 formally standardizes computing error against the newly updated $\text{EstimatedRTT}_{\text{new}}$).*

**Where did this formula/concept come from?** Van Jacobson's 1988 seminal paper *"Congestion Avoidance and Control"*, adopted into RFC 6298.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Calculate the New DevRTT (Deviation / Jitter)</div>

**What changed from Step 4?** We have the raw error ($17.5\text{ ms}$). Now we update our running moving average of jitter ($\text{DevRTT}$).

**What are we doing?** Calculating $\text{DevRTT}_{\text{new}}$ using the second EWMA formula:  
$$\text{DevRTT}_{\text{new}} = (1 - \beta) \times \text{DevRTT}_{\text{old}} + \beta \times |\text{SampleRTT} - \text{EstimatedRTT}_{\text{new}}|$$

**Why are we doing this?** If network latency is rock-solid and stable, we don't need a large safety margin. If network latency fluctuates wildly, we need a large safety cushion so we don't time out prematurely. $\text{DevRTT}$ tracks this volatility.

**How do we do it?**
Given $\beta = 0.25 = \frac{1}{4}$, the historical weight is:  
$$(1 - \beta) = 1.0 - 0.25 = 0.75 = \frac{3}{4}$$  

1. Compute historical component:  
$$(1 - \beta) \times \text{DevRTT}_{\text{old}} = 0.75 \times 10.0\text{ ms} = \frac{3}{4} \times 10.0 = \frac{30.0}{4} = 7.5\text{ ms}$$  

2. Compute new error component:  
$$\beta \times |\text{SampleRTT} - \text{EstimatedRTT}_{\text{new}}| = 0.25 \times 17.5\text{ ms} = \frac{1}{4} \times 17.5 = 4.375\text{ ms}$$  

3. Add both components together:  
$$\text{DevRTT}_{\text{new}} = 7.5\text{ ms} + 4.375\text{ ms} = 11.875\text{ ms}$$  

Notice: The deviation expanded from $10.0\text{ ms}$ to $11.875\text{ ms}$ because a sudden $60\text{ ms}$ packet showed the link is experiencing higher variance.

**Where did this formula/concept come from?** RFC 6298 Section 2.3.
</div>

<div class="step-card">
<div class="step-badge">Step 6: Compute the Retransmission Timeout (RTO)</div>

**What changed from Step 5?** We now possess both critical components: the updated center average ($\text{EstimatedRTT}_{\text{new}} = 42.5\text{ ms}$) and the updated safety spread ($\text{DevRTT}_{\text{new}} = 11.875\text{ ms}$).

**What are we doing?** Calculating the actual timer value $\text{RTO}$.

**Why are we doing this?** This is the ultimate objective. The sender's operating system needs an exact millisecond threshold. If an ACK does not arrive within this RTO window, the sender declares the packet lost and triggers a retransmission.

**How do we do it?**
The standard RFC 6298 formula is:  
$$\text{RTO} = \text{EstimatedRTT} + 4 \times \text{DevRTT}$$  

1. Multiply the deviation by the safety factor of $4$:  
$$4 \times \text{DevRTT}_{\text{new}} = 4 \times 11.875\text{ ms}$$  
Let us multiply step-by-step:  
$$4 \times 11 = 44$$  
$$4 \times 0.875 = 4 \times \frac{7}{8} = \frac{28}{8} = 3.5$$  
$$44 + 3.5 = 47.5\text{ ms}$$  

2. Add this safety cushion to the estimated average:  
$$\text{RTO} = 42.5\text{ ms} + 47.5\text{ ms} = 90.0\text{ ms}$$  

*(Rule Check: RFC 6298 states that if $\text{RTO} < 1{,}000\text{ ms}$, some conservative OS implementations clamp it to a minimum of $1\text{ second}$. In textbook theoretical computations, we report the unrounded formula result: $90.0\text{ ms}$).*

**Where did this formula/concept come from?** Chebyshev's Inequality in probability theory. Adding $4$ standard deviations (or $4 \times \text{mean deviation}$) guarantees that over $98\%$ of legitimate packets will arrive safely without causing an accidental, false timeout alarm.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary of Level 1 Calculation</div>

**What is the final answer?**
- Old State: $\text{EstimatedRTT} = 40.0\text{ ms}$, $\text{DevRTT} = 10.0\text{ ms}$, Old $\text{RTO} = 40 + 4(10) = 80.0\text{ ms}$  
- Measured Sample: $\text{SampleRTT} = 60.0\text{ ms}$  
- New EstimatedRTT: $\mathbf{42.5\text{ ms}}$  
- New DevRTT: $\mathbf{11.875\text{ ms}}$  
- New Retransmission Timeout (RTO): $\mathbf{90.0\text{ ms}}$

**Why does this answer make sense?** The incoming sample ($60\text{ ms}$) was slower than expected ($40\text{ ms}$). As a direct result:  
1. The estimated average crept up slightly ($40 \to 42.5\text{ ms}$).  
2. The measured jitter crept up ($10 \to 11.875\text{ ms}$).  
3. The timeout timer widened from $80.0\text{ ms}$ to $90.0\text{ ms}$, giving future packets more breathing room so TCP does not panic unnecessarily.
</div>

</div>

---

## Level 2: Multi-Sample Sequence and Karn's Algorithm

### Problem 2.1: Multi-Step EWMA Trace and the Karn-Partridge Retransmission Ambiguity

**Problem Statement:** Continuing directly from the state achieved at the end of Problem 1.1:  
- Current State: $\text{EstimatedRTT}_1 = 42.5\text{ ms}$, $\text{DevRTT}_1 = 11.875\text{ ms}$, $\text{RTO}_1 = 90.0\text{ ms}$.  
- Standard constants: $\alpha = 0.125 = \frac{1}{8}$, $\beta = 0.25 = \frac{1}{4}$.  

1. **Arrival of Sample 2:** A fast acknowledgment arrives with $\text{SampleRTT}_2 = 30.0\text{ ms}$. Update $\text{EstimatedRTT}_2$, $\text{DevRTT}_2$, and $\text{RTO}_2$.  
2. **Arrival of Sample 3:** An acknowledgment arrives through link congestion with $\text{SampleRTT}_3 = 70.0\text{ ms}$. Update $\text{EstimatedRTT}_3$, $\text{DevRTT}_3$, and $\text{RTO}_3$.  
3. **Karn's Algorithm Scenario:** Suppose a packet times out because its ACK was delayed. The sender retransmits the packet. $20\text{ ms}$ later, an ACK arrives. Explain using an intuitive postal delivery analogy why **Karn's Algorithm** strictly forbids taking an RTT sample from this retransmitted packet, and state what TCP must do to the RTO timer instead.

::: callout-intuition Core Mental Model
Imagine you mail a birthday greeting card to your friend on **Monday morning**.  
By **Wednesday afternoon**, you haven't heard back, so you assume the card was lost in the mail. In a panic, you mail an identical duplicate card on **Wednesday evening**.  
On **Thursday morning**, your friend calls you on the phone saying: *"Thank you so much! I just received your card!"* Here is the billion-dollar question: **Which card is your friend holding?**
- Did the postal service take **3 days** to deliver the Monday card?  
- Or did the postal service take **half a day** to deliver the Wednesday card at supersonic speed?  
You have no way of knowing! If you guess wrong, you will corrupt your entire timer calculation. This is the **ACK Ambiguity Problem**.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Process Sample 2 (SampleRTT2 = 30.0 ms) — Update Average</div>

**What are we doing?** Updating our moving average after receiving a faster-than-average packet ($30.0\text{ ms}$).

**Why are we starting here?** To see how the EWMA responds when a delay drop occurs.

**How do we do it?**
Current state: $\text{EstimatedRTT}_1 = 42.5\text{ ms}$.  
Formula: $\text{EstimatedRTT}_2 = (1 - \alpha) \times \text{EstimatedRTT}_1 + \alpha \times \text{SampleRTT}_2$  

1. Compute history component:  
$$0.875 \times 42.5\text{ ms} = \frac{7}{8} \times 42.5 = \frac{297.5}{8} = 37.1875\text{ ms}$$  

2. Compute sample component:  
$$0.125 \times 30.0\text{ ms} = \frac{1}{8} \times 30.0 = \frac{30.0}{8} = 3.75\text{ ms}$$  

3. Sum together:  
$$\text{EstimatedRTT}_2 = 37.1875\text{ ms} + 3.75\text{ ms} = 40.9375\text{ ms}$$  

The estimated average gracefully floated down from $42.5\text{ ms}$ to $\approx 40.94\text{ ms}$.

**Where did this formula/concept come from?** RFC 6298 EWMA update rule.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Process Sample 2 — Update DevRTT and RTO</div>

**What changed from Step 1?** We have $\text{EstimatedRTT}_2 = 40.9375\text{ ms}$. Now we update the deviation and the timeout timer.

**What are we doing?** Calculating $\text{DevRTT}_2$ and $\text{RTO}_2$.

**How do we do it?**
1. Calculate the error magnitude:  
$$|\text{SampleRTT}_2 - \text{EstimatedRTT}_2| = |30.0 - 40.9375| = |-10.9375| = 10.9375\text{ ms}$$  

2. Compute $\text{DevRTT}_2$ (with previous $\text{DevRTT}_1 = 11.875\text{ ms}$):  
$$\text{DevRTT}_2 = (1 - \beta) \times \text{DevRTT}_1 + \beta \times (\text{Error})$$  
$$(1 - 0.25) \times 11.875 = 0.75 \times 11.875 = \frac{3}{4} \times 11.875 = \frac{35.625}{4} = 8.90625\text{ ms}$$  
$$0.25 \times 10.9375 = \frac{1}{4} \times 10.9375 = 2.734375\text{ ms}$$  
$$\text{DevRTT}_2 = 8.90625 + 2.734375 = 11.640625\text{ ms}$$  

3. Compute $\text{RTO}_2$:  
$$\text{RTO}_2 = \text{EstimatedRTT}_2 + 4 \times \text{DevRTT}_2$$  
$$4 \times 11.640625 = 46.5625\text{ ms}$$  
$$\text{RTO}_2 = 40.9375 + 46.5625 = 87.5\text{ ms}$$  

Summary after Sample 2: Average is $40.9375\text{ ms}$, $\text{RTO}$ tightened from $90.0\text{ ms}$ down to $87.5\text{ ms}$.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Process Sample 3 (SampleRTT3 = 70.0 ms) — Update Average</div>

**What changed from Step 2?** The network suddenly hits a congestion queue. A packet takes $70.0\text{ ms}$ round-trip.

**What are we doing?** Computing $\text{EstimatedRTT}_3$.

**How do we do it?**
Base state: $\text{EstimatedRTT}_2 = 40.9375\text{ ms}$.  
Formula: $\text{EstimatedRTT}_3 = 0.875 \times 40.9375 + 0.125 \times 70.0$  

1. Compute history component:  
$$0.875 \times 40.9375 = \frac{7}{8} \times 40.9375 = \frac{286.5625}{8} = 35.8203125\text{ ms}$$  

2. Compute sample component:  
$$0.125 \times 70.0 = \frac{1}{8} \times 70.0 = 8.75\text{ ms}$$  

3. Sum together:  
$$\text{EstimatedRTT}_3 = 35.8203125 + 8.75 = 44.5703125\text{ ms}$$  

Notice: Despite a massive $70\text{ ms}$ spike, the average only rose from $40.94\text{ ms}$ to $44.57\text{ ms}$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Process Sample 3 — Update DevRTT and RTO</div>

**What changed from Step 3?** We have $\text{EstimatedRTT}_3 = 44.5703125\text{ ms}$. Now we recalculate the deviation and find the new safety threshold.

**What are we doing?** Computing $\text{DevRTT}_3$ and $\text{RTO}_3$.

**How do we do it?**
1. Calculate error magnitude:  
$$|\text{SampleRTT}_3 - \text{EstimatedRTT}_3| = |70.0 - 44.5703125| = 25.4296875\text{ ms}$$  

2. Compute $\text{DevRTT}_3$ (with previous $\text{DevRTT}_2 = 11.640625\text{ ms}$):  
$$\text{DevRTT}_3 = 0.75 \times 11.640625 + 0.25 \times 25.4296875$$  
$$0.75 \times 11.640625 = \frac{3}{4} \times 11.640625 = 8.73046875\text{ ms}$$  
$$0.25 \times 25.4296875 = \frac{1}{4} \times 25.4296875 = 6.357421875\text{ ms}$$  
$$\text{DevRTT}_3 = 8.73046875 + 6.357421875 = 15.087890625\text{ ms}$$  

3. Compute $\text{RTO}_3$:  
$$\text{RTO}_3 = \text{EstimatedRTT}_3 + 4 \times \text{DevRTT}_3$$  
$$4 \times 15.087890625 = 60.3515625\text{ ms}$$  
$$\text{RTO}_3 = 44.5703125 + 60.3515625 = 104.921875\text{ ms}$$  

The timeout timer reacted aggressively to the sudden spike: $\text{RTO}$ jumped from $87.5\text{ ms}$ up to $\approx 104.92\text{ ms}$.
</div>

<div class="step-card">
<div class="step-badge">Step 5: The ACK Ambiguity Problem and Karn's Algorithm</div>

**What changed from Step 4?** We finished calculating normal, healthy packet exchanges. Now we confront a failure condition: **packet retransmissions**.

**What are we doing?** Explaining why we must NEVER compute a SampleRTT for a packet that has been retransmitted.

**Why are we doing this?** In standard TCP, segment headers contain a Sequence Number, and ACK packets acknowledge that Sequence Number. However, TCP ACKs do NOT contain a timestamp saying which transmission attempt they correspond to!

**How do we do it?** Examine the two catastrophic failure modes if you attempt to measure RTT on a retransmitted segment:

```
Case 1: ACK was for the FIRST transmission (First transmission was just delayed)
Sender: --- Transmit 1 (t = 0 ms) ---------------------------------->
Sender: [Timeout expires at t = 90 ms]
Sender: --- Retransmit 2 (t = 90 ms) -------------------------------->
Sender: <--- Receives ACK at t = 95 ms -------------------------------
If Sender assumes ACK belongs to Retransmit 2:
Measured SampleRTT = 95 - 90 = 5 ms!
REALITY: The link is horribly slow (took 95 ms), but TCP falsely records
an ultra-fast 5 ms RTT! This collapses the RTO timer, causing a storm of
premature retransmissions that can crash the network!

Case 2: ACK was for the SECOND transmission (First transmission was lost)
If Sender assumes ACK belongs to Transmit 1:
Measured SampleRTT = 95 - 0 = 95 ms!
REALITY: The second transmission only took 5 ms, but TCP falsely inflates
the sample with the timeout dead-time.
```

**Karn's Rule (Karn & Partridge, 1987):**
1. **Rule 1:** Do NOT update $\text{EstimatedRTT}$ or $\text{DevRTT}$ using samples from retransmitted segments. Discard the measurement completely!  
2. **Rule 2 (Exponential Timer Backoff):** Because a timeout occurred, the network is likely severely congested. Each time a segment times out and is retransmitted, double the timeout timer:  
$$\text{RTO}_{\text{new}} = 2 \times \text{RTO}_{\text{old}}$$  
Only resume normal EWMA calculations after an acknowledgment arrives for a segment that was sent exactly once without retransmission.

**Where did this formula/concept come from?** Phil Karn and Craig Partridge, *"Improving Round-Trip Time Estimates in Reliable Transport Protocols"* (SIGCOMM 1987).
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary Comparison of State Evolution</div>

**What is the final answer?** Let us review the complete numerical journey across the packet sequence:

| Step / Event | SampleRTT | EstimatedRTT | DevRTT | Computed RTO | Action Taken |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Initial Base** | — | $40.000\text{ ms}$ | $10.000\text{ ms}$ | $80.000\text{ ms}$ | Baseline state |
| **After Sample 1** | $60.0\text{ ms}$ | $42.500\text{ ms}$ | $11.875\text{ ms}$ | $90.000\text{ ms}$ | Average & spread expand |
| **After Sample 2** | $30.0\text{ ms}$ | $40.938\text{ ms}$ | $11.641\text{ ms}$ | $87.500\text{ ms}$ | Timer safely tightens |
| **After Sample 3** | $70.0\text{ ms}$ | $44.570\text{ ms}$ | $15.088\text{ ms}$ | $104.922\text{ ms}$ | Timer widens significantly |
| **If Retransmitted**| Ambiguous | **UNCHANGED** | **UNCHANGED** | **DOUBLED ($2 \times \text{RTO}$)** | **Karn's Algorithm applied** |

**Why does this answer make sense?** The EWMA algorithm acts as an intelligent statistical shock absorber. When latency bounces ($60 \to 30 \to 70\text{ ms}$), the estimated center moves smoothly between $40.9\text{ ms}$ and $44.6\text{ ms}$ rather than swinging violently. Meanwhile, the $+4 \times \text{DevRTT}$ term ensures that the moment uncertainty increases, the timeout deadline ($\text{RTO}$) pulls back to give packets ample time to arrive without triggering false duplicate transmissions.
</div>

</div>

---

<a id="self-check"></a>
## Active Recall Checkpoint

::: quiz Q1: Karn's Algorithm
Why does TCP ignore SampleRTT measurements for segments that had to be retransmitted?
(A) Because retransmitted packets use UDP headers
(*B) Because the sender cannot tell whether an arriving ACK was generated in response to the original transmission or the retransmission (ACK Ambiguity)
(C) Because routers change sequence numbers on retransmissions
(D) To reduce CPU usage
::: explanation
If a segment times out and is resent, and an ACK returns shortly after, was the ACK delayed from the first transmission, or was the retransmission remarkably fast? You cannot know. If you misattribute it, your RTT estimate will be wildly inaccurate. Karn's rule solves this by discarding all retransmission timing samples.
:::

::: quiz Q2: Timeout Jitter Scaling
In RFC 6298, what is the mathematical multiplier applied to DevRTT when calculating the Retransmission Timeout (RTO = EstimatedRTT + k * DevRTT)?
(A) $k = 1$
(B) $k = 2$
(*C) $k = 4$
(D) $k = 8$
::: explanation
RFC 6298 dictates a factor of $4$ ($\text{RTO} = \text{EstimatedRTT} + 4 \times \text{DevRTT}$). Based on Chebyshev's inequality, adding 4 mean deviations ensures that less than $2\%$ of packets will experience a spurious timeout under normal random packet delay variations.
:::
