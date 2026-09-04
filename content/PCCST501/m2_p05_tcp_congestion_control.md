# Progressive Problems: TCP Congestion Control

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped unit conversions, and full line-by-line math.

---

## Level 1: Slow Start and Congestion Avoidance Evolution

### Problem 1.1: Tracing Window Growth from Cold Start to Congestion Avoidance

**Problem Statement:** A newly established TCP connection begins sending data over an unloaded network path.  
- The Maximum Segment Size is $\text{MSS} = 1\text{ packet}$ (for arithmetic clarity, $1\text{ MSS} = 1\text{ full data segment}$).  
- Initial Congestion Window: $\text{cwnd} = 1\text{ MSS}$.  
- Initial Slow Start Threshold: $\text{ssthresh} = 16\text{ MSS}$.  
- Every transmitted packet is acknowledged individually by the receiver (delayed ACKs are turned off).  
- Assume zero packet loss during this period.  

1. Trace the round-by-round value of $\text{cwnd}$ for the first $6\text{ Round-Trip Times (RTTs)}$.  
2. Explicitly show the micro-step calculation within each RTT: how each individual ACK increases $\text{cwnd}$.  
3. Prove why Slow Start produces exponential growth ($2^{\text{RTT}}$) despite its deceptive name "Slow".  
4. Show the exact moment when $\text{cwnd}$ hits $\text{ssthresh}$ and prove why the growth pattern shifts from doubling to adding $+1\text{ MSS}$ per RTT in Congestion Avoidance.

::: callout-intuition Core Mental Model
Imagine you are testing the capacity of an unfamiliar freeway on-ramp with a metered stoplight:  
- **Slow Start is a doubling sprint:** You send $1$ car. It drives through smoothly. You think: *"The road is empty! Let's send $2$ cars next!"* Both arrive safely. You think: *"Great! Send $4$ cars!"* Then $8$, then $16$! It is called "slow" start only because you didn't dump $1{,}000$ cars at second zero; you started with $1$ and ramped up at lightning speed (doubling every round).  
- **ssthresh (The Caution Warning Sign):** At $16\text{ cars}$, a sign on the freeway flashes: *"Warning: Traffic density approaching capacity."*
- **Congestion Avoidance is tiptoeing:** You don't double to $32$ cars anymore, because that might instantly trigger a catastrophic multi-car pileup! Instead, you add only **$1$ extra car per round** ($16 \to 17 \to 18 \dots$), gently probing the asphalt to find the true breaking point without clogging the highway.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Define Key Terms and Units</div>

**What are we doing?** Formally defining the units and control variables before doing any math.

**Why are we starting here?** A beginner cannot follow congestion formulas without understanding what the units ($\text{MSS}$, $\text{cwnd}$, $\text{ssthresh}$) represent in physical reality.

**How do we do it?**
1. **$\text{MSS}$ (Maximum Segment Size):** The largest chunk of application data TCP will place inside a single packet. If $\text{MSS} = 1{,}460\text{ bytes}$, then $1\text{ MSS} = 1\text{ standard data packet}$. In our calculations, we measure window sizes in integer units of $\text{MSS}$.  
2. **$\text{cwnd}$ (Congestion Window):** A state variable maintained locally by the **sender**. It dictates: *"How many unacknowledged packets is the sender allowed to inject into the network pipe at once?"*
3. **$\text{ssthresh}$ (Slow Start Threshold):** A threshold boundary line (in $\text{MSS}$).  
   - If $\text{cwnd} < \text{ssthresh}$: The sender operates in **Slow Start Mode**.  
   - If $\text{cwnd} \ge \text{ssthresh}$: The sender switches to **Congestion Avoidance Mode**.  
4. **$\text{RTT}$ (Round-Trip Time):** The time duration from when a batch of packets is transmitted until their acknowledgments (ACKs) return back to the sender.

**Where did this formula/concept come from?** Van Jacobson's 1988 Congestion Control paper and RFC 5681 ("TCP Congestion Control").
</div>

<div class="step-card">
<div class="step-badge">Step 2: Understand the Micro-Rule for Slow Start Growth</div>

**What changed from Step 1?** We have defined the variables. Now we look at the exact mathematical rule that the sender's operating system executes every time a single ACK packet arrives during Slow Start.

**What are we doing?** Stating the per-ACK update rule:  
$$\text{For every valid ACK received during Slow Start: } \text{cwnd} \leftarrow \text{cwnd} + 1\text{ MSS}$$

**Why are we starting here?** Many students mistakenly believe $\text{cwnd}$ magically doubles at the end of a round. In reality, the sender increases $\text{cwnd}$ piece-by-piece as individual ACKs trickle in.

**How do we do it?**
Suppose the current window is $W$ packets.  
- The sender transmits all $W$ packets into the network.  
- Over the course of $1\text{ RTT}$, exactly $W$ acknowledgments return.  
- Each individual ACK increases $\text{cwnd}$ by $+1\text{ MSS}$.  
- Total increase across the entire RTT:  
$$\Delta \text{cwnd} = W \times (+1\text{ MSS}) = +W\text{ MSS}$$  
- New window at the end of the RTT:  
$$\text{cwnd}_{\text{end}} = \text{cwnd}_{\text{start}} + W = W + W = 2W$$  
Because the window increases by its own size every RTT, the value doubles every single round!

**Where did this formula/concept come from?** RFC 5681 Section 3.1.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Trace Round 1 through Round 4 (Pure Slow Start)</div>

**What changed from Step 2?** We now execute the exact numbers starting from $\text{cwnd} = 1\text{ MSS}$ up through Round 4.

**What are we doing?** Tracing RTT 1, RTT 2, RTT 3, and RTT 4 step-by-step.

**How do we do it?**
- **Round 1 ($\text{RTT}_1$):**
  - Initial state: $\text{cwnd} = 1\text{ MSS}$.  
  - Sender transmits $1$ packet: $[\text{Pkt}_1]$.  
  - Receiver receives $\text{Pkt}_1$ and returns $\text{ACK}_1$.  
  - When $\text{ACK}_1$ arrives: $\text{cwnd} \leftarrow 1 + 1 = 2\text{ MSS}$.  
  - *End of $\text{RTT}_1$: $\text{cwnd} = 2\text{ MSS}$.* (Since $2 < 16$, continue Slow Start).

- **Round 2 ($\text{RTT}_2$):**
  - Initial state: $\text{cwnd} = 2\text{ MSS}$.  
  - Sender transmits $2$ packets: $[\text{Pkt}_2, \text{Pkt}_3]$.  
  - Receiver sends $2$ ACKs: $\text{ACK}_2, \text{ACK}_3$.  
  - When $\text{ACK}_2$ arrives: $\text{cwnd} \leftarrow 2 + 1 = 3\text{ MSS}$.  
  - When $\text{ACK}_3$ arrives: $\text{cwnd} \leftarrow 3 + 1 = 4\text{ MSS}$.  
  - *End of $\text{RTT}_2$: $\text{cwnd} = 4\text{ MSS}$.* (Since $4 < 16$, continue Slow Start).

- **Round 3 ($\text{RTT}_3$):**
  - Initial state: $\text{cwnd} = 4\text{ MSS}$.  
  - Sender transmits $4$ packets: $[\text{Pkt}_4, \text{Pkt}_5, \text{Pkt}_6, \text{Pkt}_7]$.  
  - Receiver sends $4$ ACKs.  
  - Each of the $4$ ACKs adds $+1$: $\text{cwnd} \leftarrow 4 + 4(1) = 8\text{ MSS}$.  
  - *End of $\text{RTT}_3$: $\text{cwnd} = 8\text{ MSS}$.* (Since $8 < 16$, continue Slow Start).

- **Round 4 ($\text{RTT}_4$):**
  - Initial state: $\text{cwnd} = 8\text{ MSS}$.  
  - Sender transmits $8$ packets: $[\text{Pkt}_8 \dots \text{Pkt}_{15}]$.  
  - Receiver sends $8$ ACKs.  
  - Each of the $8$ ACKs adds $+1$: $\text{cwnd} \leftarrow 8 + 8(1) = 16\text{ MSS}$.  
  - *End of $\text{RTT}_4$: $\text{cwnd} = 16\text{ MSS}$.*
  - **CRITICAL MILESTONE:** Notice that $\text{cwnd} = 16\text{ MSS}$, which **exactly equals** $\text{ssthresh} = 16\text{ MSS}$!

**Where did this formula/concept come from?** The exponential formula: $\text{cwnd}(k) = \text{cwnd}(0) \times 2^k = 1 \times 2^k$ for round $k$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: The Transition Rule from Slow Start to Congestion Avoidance</div>

**What changed from Step 3?** $\text{cwnd}$ reached $\text{ssthresh} = 16\text{ MSS}$. The sender must now change its behavior.

**What are we doing?** Explaining the switch from exponential growth to linear growth.

**Why are we doing this?** If the sender continued doubling ($16 \to 32 \to 64$), it would flood the intermediate router buffers and cause widespread packet drops. At $\text{ssthresh}$, TCP switches to a conservative exploration mode called **Congestion Avoidance**.

**How do we do it?** In Congestion Avoidance, the protocol rule states:  
$$\text{Target growth: Increase cwnd by exactly } +1\text{ MSS per complete RTT}$$  
To achieve $+1\text{ MSS}$ over a whole round of $W$ packets, each individual incoming ACK cannot add $+1$ anymore! Instead, each incoming ACK adds only a tiny fractional slice:  
$$\text{Per-ACK rule in Congestion Avoidance: } \text{cwnd} \leftarrow \text{cwnd} + \frac{1\text{ MSS}}{\text{cwnd}} \times \text{MSS}$$  
Let us verify the math:  
If $\text{cwnd} = W$, there will be $W$ ACKs returning during the RTT.  
$$\text{Total increase in 1 RTT} = W \times \left(\frac{1}{W}\text{ MSS}\right) = \frac{W}{W}\text{ MSS} = +1\text{ MSS}$$  
The micro-increments perfectly sum to $+1\text{ MSS}$ per RTT.

**Where did this formula/concept come from?** RFC 5681 Section 3.1: Additive Increase Multiplicative Decrease (AIMD) algorithm.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Trace Round 5 and Round 6 (Congestion Avoidance)</div>

**What changed from Step 4?** We now trace the next two rounds under the new Congestion Avoidance rules.

**What are we doing?** Calculating $\text{cwnd}$ for $\text{RTT}_5$ and $\text{RTT}_6$.

**How do we do it?**
- **Round 5 ($\text{RTT}_5$):**
  - Initial state at start of round: $\text{cwnd} = 16\text{ MSS}$.  
  - State mode: Congestion Avoidance ($\text{cwnd} \ge \text{ssthresh}$).  
  - Sender transmits $16$ packets into the network pipe.  
  - Over the course of the RTT, $16$ ACKs return.  
  - Each individual ACK increases $\text{cwnd}$ by:  
    $$\Delta = \frac{1}{16}\text{ MSS}$$  
  - After all $16$ ACKs arrive:  
    $$\text{cwnd} \leftarrow 16\text{ MSS} + 16 \times \left(\frac{1}{16}\text{ MSS}\right) = 16 + 1.0 = 17\text{ MSS}$$  
  - *End of $\text{RTT}_5$: $\text{cwnd} = 17\text{ MSS}$.*

- **Round 6 ($\text{RTT}_6$):**
  - Initial state at start of round: $\text{cwnd} = 17\text{ MSS}$.  
  - State mode: Congestion Avoidance ($\text{cwnd} \ge \text{ssthresh}$).  
  - Sender transmits $17$ packets.  
  - Over the course of the RTT, $17$ ACKs return.  
  - Each individual ACK increases $\text{cwnd}$ by:  
    $$\Delta = \frac{1}{17}\text{ MSS}$$  
  - After all $17$ ACKs arrive:  
    $$\text{cwnd} \leftarrow 17\text{ MSS} + 17 \times \left(\frac{1}{17}\text{ MSS}\right) = 17 + 1.0 = 18\text{ MSS}$$  
  - *End of $\text{RTT}_6$: $\text{cwnd} = 18\text{ MSS}$.*

**Where did this formula/concept come from?** The linear equation for Additive Increase: $\text{cwnd}(t) = \text{cwnd}_{\text{initial}} + t$ where $t$ is the number of RTTs spent in Congestion Avoidance.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary Table of Window Evolution</div>

**What is the final answer?** The round-by-round progression of $\text{cwnd}$ over the first 6 RTTs is:

| RTT Round | Starting cwnd | Mode | Action during Round | Ending cwnd |
| :---: | :---: | :---: | :--- | :---: |
| **RTT 1** | $1\text{ MSS}$ | Slow Start | 1 ACK arrives; each adds $+1$ | $\mathbf{2\text{ MSS}}$ |
| **RTT 2** | $2\text{ MSS}$ | Slow Start | 2 ACKs arrive; each adds $+1$ | $\mathbf{4\text{ MSS}}$ |
| **RTT 3** | $4\text{ MSS}$ | Slow Start | 4 ACKs arrive; each adds $+1$ | $\mathbf{8\text{ MSS}}$ |
| **RTT 4** | $8\text{ MSS}$ | Slow Start | 8 ACKs arrive; each adds $+1$ | $\mathbf{16\text{ MSS}}$ |
| **RTT 5** | $16\text{ MSS}$ | Congestion Avoidance | 16 ACKs arrive; each adds $+\frac{1}{16}$ | $\mathbf{17\text{ MSS}}$ |
| **RTT 6** | $17\text{ MSS}$ | Congestion Avoidance | 17 ACKs arrive; each adds $+\frac{1}{17}$ | $\mathbf{18\text{ MSS}}$ |

**Why does this answer make sense?** The growth curve has two distinct phases:  
1. **Exponential Phase ($\text{RTT } 1 \to 4$):** Window doubles every round ($1 \to 2 \to 4 \to 8 \to 16$) because the link is presumed completely clear and we need to fill the empty bandwidth-delay product as fast as mathematically possible.  
2. **Linear Phase ($\text{RTT } 5 \to 6$):** Once the historical safe threshold ($\text{ssthresh} = 16$) is reached, the sender switches to linear crawling ($+1\text{ MSS}$ per RTT) to avoid congesting the intermediate bottleneck router.
</div>

</div>

---

## Level 2: Triple Duplicate ACKs vs. Timeout (Tahoe vs. Reno Divergence)

### Problem 2.1: Comparing TCP Tahoe and TCP Reno Under 3 Duplicate ACKs vs. Retransmission Timeout

**Problem Statement:** Following directly from Level 1, the connection enters **RTT 7** with:  
- Current Congestion Window: $\text{cwnd} = 17\text{ MSS}$.  
- Current Threshold: $\text{ssthresh} = 16\text{ MSS}$.  

During RTT 7, severe packet loss occurs due to network buffer overflows.  
Analyze and contrast how **TCP Tahoe (1988)** and **TCP Reno (1990)** respond under two distinct loss events:  
- **Event A:** The sender receives **3 Duplicate ACKs** (indicating a single packet was dropped, but later packets are still crossing the network and triggering responses).  
- **Event B:** A **Retransmission Timeout (RTO)** expires (indicating complete silence; no packets or ACKs are getting through).  

For both protocols and both events:  
1. Calculate the new $\text{ssthresh}$.  
2. Calculate the new $\text{cwnd}$.  
3. Identify the state machine mode entered immediately after the event.  
4. Construct a clear side-by-side comparison table.  
5. Explain why Reno's **Fast Recovery** provides dramatically higher throughput than Tahoe on high-speed internet links.

::: callout-intuition Core Mental Model
Imagine traffic on a three-lane highway:  
- **Event A (3 Duplicate ACKs):** A single car gets a flat tire in the right lane, but cars behind it are successfully squeezing past it in the left two lanes and waving at the toll booth. The highway is NOT completely blocked!  
  - **TCP Tahoe overreacts:** It sees the flat tire, slams on the emergency brakes, brings the entire highway to a dead stop ($0\text{ mph}$), and forces all cars to restart at $1\text{ car per hour}$ (Slow Start from $\text{cwnd} = 1$).  
  - **TCP Reno is smart (Fast Recovery):** It sees the flat tire, quickly tows the broken car away (Fast Retransmit), cuts the speed limit by half because one lane is blocked ($\text{cwnd} = \text{cwnd} / 2$), but **keeps the remaining cars moving at $50\text{ mph}$ without ever stopping the traffic flow!**
- **Event B (Retransmission Timeout):** Complete silence. A massive rockslide has buried all three lanes. Not a single car is getting through. Both Tahoe and Reno agree: *"The road is completely impassable. We have no choice but to stop everything, drop $\text{cwnd}$ to $1\text{ MSS}$, and cautiously start over."*
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Understand What "3 Duplicate ACKs" Physically Means</div>

**What are we doing?** Explaining why exactly 3 duplicate ACKs are used to diagnose a lost packet.

**Why are we starting here?** A beginner needs to understand why 3 duplicate ACKs do not indicate a total network collapse.

**How do we do it?**
Suppose the sender transmits packets $1, 2, 3, 4, 5$.  
- Packet $2$ is dropped by a router.  
- Packets $3, 4, 5$ arrive safely at the receiver.  
- The receiver's rule is: *"I can only acknowledge contiguous bytes received in order."*
- When Packet $3$ arrives: Receiver says: *"I received something, but I am still missing packet 2! Here is another $\text{ACK}(1)$."* (Duplicate ACK 1).  
- When Packet $4$ arrives: Receiver says: *"Still missing packet 2! Here is another $\text{ACK}(1)$."* (Duplicate ACK 2).  
- When Packet $5$ arrives: Receiver says: *"Still missing packet 2! Here is another $\text{ACK}(1)$."* (Duplicate ACK 3).  

**Key Insight:** If the sender receives 3 duplicate ACKs, it proves that at least 3 packets successfully reached the receiver *after* the missing packet! The pipeline is still functioning. Only one packet was lost.

**Where did this formula/concept come from?** RFC 5681: The heuristic choice of $3$ duplicate ACKs prevents premature retransmissions caused by minor out-of-order packet delivery over multi-path internet routing.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Universal Multiplicative Decrease Rule for ssthresh</div>

**What changed from Step 1?** We understand the loss signal. Now we calculate how both protocols set the new threshold ($\text{ssthresh}$).

**What are we doing?** Applying the Multiplicative Decrease formula to update $\text{ssthresh}$.

**Why are we doing this?** When loss occurs at a window size of $\text{cwnd}$, it means the network capacity is roughly near $\text{cwnd}$. TCP records half of this current window as the new safe ceiling ($\text{ssthresh}$) for future linear probing.

**How do we do it?**
The universal standard formula in RFC 5681 is:  
$$\text{ssthresh}_{\text{new}} = \max\left(2, \left\lfloor \frac{\text{cwnd}}{2} \right\rfloor\right)$$  
Given $\text{cwnd} = 17\text{ MSS}$ at the time of loss:  
$$\text{ssthresh}_{\text{new}} = \left\lfloor \frac{17}{2} \right\rfloor = \lfloor 8.5 \rfloor = 8\text{ MSS}$$  
*(Note: Both TCP Tahoe and TCP Reno use this exact same formula for setting $\text{ssthresh}$).*

**Where did this formula/concept come from?** Van Jacobson's principle of Multiplicative Decrease to ensure network stability and avoid congestion collapse.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Analyze Event A (3 Duplicate ACKs) — Tahoe vs. Reno Reaction</div>

**What changed from Step 2?** We know $\text{ssthresh}_{\text{new}} = 8\text{ MSS}$. Now we calculate the new $\text{cwnd}$ and state mode for both protocols under Event A.

**What are we doing?** Contrasting TCP Tahoe and TCP Reno when 3 duplicate ACKs arrive.

**How do we do it?**
- **TCP Tahoe Reaction to 3 Duplicate ACKs:**
  1. Immediately retransmits the missing packet (this is called **Fast Retransmit**).  
  2. Sets threshold: $\text{ssthresh}_{\text{new}} = \lfloor 17 / 2 \rfloor = 8\text{ MSS}$.  
  3. **Drastic Punishment:** Tahoe collapses the congestion window back to the very bottom:  
     $$\text{cwnd}_{\text{new}} = 1\text{ MSS}$$  
  4. Enters **Slow Start** mode. It must rebuild its window all over again ($1 \to 2 \to 4 \to 8 \dots$).

- **TCP Reno Reaction to 3 Duplicate ACKs:**
  1. Immediately retransmits the missing packet (**Fast Retransmit**).  
  2. Sets threshold: $\text{ssthresh}_{\text{new}} = \lfloor 17 / 2 \rfloor = 8\text{ MSS}$.  
  3. **Intelligent Bypass (Fast Recovery):** Reno realizes that packets are still traversing the link. Instead of crashing down to $1$, Reno cuts $\text{cwnd}$ in half:  
     $$\text{cwnd}_{\text{new}} = \text{ssthresh}_{\text{new}} = 8\text{ MSS}$$  
     *(Pedagogical detail: In the temporary Fast Recovery state, Reno temporarily inflates $\text{cwnd} = \text{ssthresh} + 3 = 11\text{ MSS}$ to account for the 3 packets that left the pipe, but as soon as the ACK for the missing packet arrives, it settles cleanly at $\text{cwnd} = \text{ssthresh} = 8\text{ MSS}$).*
  4. Enters **Congestion Avoidance** directly (skipping Slow Start completely!).

**Where did this formula/concept come from?** RFC 2001 and RFC 2581 (TCP Reno Fast Recovery standard).
</div>

<div class="step-card">
<div class="step-badge">Step 4: Analyze Event B (Retransmission Timeout) — Tahoe vs. Reno Reaction</div>

**What changed from Step 3?** We analyzed the mild loss event (3 Duplicate ACKs). Now we examine the severe loss event: a complete **Retransmission Timeout (RTO)**.

**What are we doing?** Determining the behavior of both protocols when the timer expires.

**Why are we doing this?** To show that when congestion is total and catastrophic, both protocols behave identically.

**How do we do it?**
When a timer expires, zero ACKs have returned for an entire RTO duration. The pipeline has completely drained of data.  
1. **ssthresh calculation (both protocols):**
   $$\text{ssthresh}_{\text{new}} = \left\lfloor \frac{\text{cwnd}}{2} \right\rfloor = \left\lfloor \frac{17}{2} \right\rfloor = 8\text{ MSS}$$  
2. **cwnd reset (both protocols):** Because there is no evidence of packets moving, neither protocol can risk sending a burst of data. Both protocols slam the window shut:  
   $$\text{cwnd}_{\text{new}} = 1\text{ MSS}$$  
3. **Next State (both protocols):** Both enter **Slow Start** mode, growing exponentially from $1\text{ MSS}$ until they hit the new threshold of $8\text{ MSS}$, after which they grow linearly.

**Where did this formula/concept come from?** RFC 6298 and RFC 5681: An RTO event represents severe network failure, demanding a total reset to single-packet injection.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Tabular Comparison and Pipeline Analysis</div>

**What changed from Step 4?** We now assemble all results into an exhaustive reference matrix and mathematically demonstrate why Reno achieves superior throughput.

**What are we doing?** Building the final side-by-side comparison table and throughput explanation.

**How do we do it?**
Let us compile the exact numbers resulting from the loss event at $\text{cwnd} = 17\text{ MSS}$:

| Feature / Metric | Initial State | Event A: 3 Duplicate ACKs | Event A: 3 Duplicate ACKs | Event B: Timeout (RTO) | Event B: Timeout (RTO) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Protocol** | — | **TCP Tahoe** | **TCP Reno** | **TCP Tahoe** | **TCP Reno** |
| **New ssthresh** | $16\text{ MSS}$ | $\mathbf{8\text{ MSS}}$ | $\mathbf{8\text{ MSS}}$ | $\mathbf{8\text{ MSS}}$ | $\mathbf{8\text{ MSS}}$ |
| **New cwnd** | $17\text{ MSS}$ | $\mathbf{1\text{ MSS}}$ | $\mathbf{8\text{ MSS}}$ | $\mathbf{1\text{ MSS}}$ | $\mathbf{1\text{ MSS}}$ |
| **Operating Mode** | Congestion Avoidance | **Slow Start** | **Congestion Avoidance** *(via Fast Recovery)* | **Slow Start** | **Slow Start** |
| **Pkt in Next RTT** | $17$ | $1$ | $8$ | $1$ | $1$ |

**Why Reno Dominates Tahoe on High-Speed Links:**
Look at what happens in the next RTT after 3 Duplicate ACKs:  
- **Tahoe** sends only **$1$ single packet**. The pipeline is emptied, and the sender must wait through multiple RTT rounds ($1 \to 2 \to 4 \to 8$) just to get back to where it should be. The link sits idle and wasted.  
- **Reno** immediately sends **$8$ packets**. The pipeline stays half full. Reno avoids the multi-round latency penalty of Slow Start and begins linear probing ($8 \to 9 \to 10 \dots$) right away.  
This difference saves hundreds of milliseconds of idle stall time on modern high-speed broadband connections.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Complete Rule Summary for Beginners</div>

**What is the final answer?**
- **Slow Start Growth:** Increases by $+1\text{ MSS}$ per received ACK $\implies$ doubles every round ($\text{cwnd} \leftarrow 2 \times \text{cwnd}$).  
- **Congestion Avoidance Growth:** Increases by $+1/\text{cwnd}\text{ MSS}$ per received ACK $\implies$ adds $+1\text{ MSS}$ per round ($\text{cwnd} \leftarrow \text{cwnd} + 1$).  
- **On 3 Duplicate ACKs:**
  - **Tahoe:** $\text{ssthresh} = \lfloor \text{cwnd}/2 \rfloor$, $\text{cwnd} = 1\text{ MSS}$, enters **Slow Start**.  
  - **Reno:** $\text{ssthresh} = \lfloor \text{cwnd}/2 \rfloor$, $\text{cwnd} = \text{ssthresh}$, enters **Congestion Avoidance** (Fast Recovery).  
- **On Timeout (RTO):**
  - **Both Tahoe & Reno:** $\text{ssthresh} = \lfloor \text{cwnd}/2 \rfloor$, $\text{cwnd} = 1\text{ MSS}$, enter **Slow Start**.

**Why does this answer make sense?** Congestion control follows the principle of **conserving packet flow**. If duplicate ACKs arrive, data is still flowing through the pipes, so we only need to throttle back gently (Reno's Fast Recovery). But if a timeout occurs, all flow has ceased, requiring an immediate shutdown and careful reboot (Slow Start from $1\text{ MSS}$).
</div>

</div>

---

<a id="self-check"></a>
## Active Recall Checkpoint

::: quiz Q1: Reno Fast Recovery Window
If a TCP Reno connection experiences 3 duplicate ACKs when its congestion window is 24 MSS, what will be the new value of ssthresh and the starting value of cwnd upon entering Congestion Avoidance?
(A) $ssthresh = 12, cwnd = 1$
(*B) $ssthresh = 12, cwnd = 12$
(C) $ssthresh = 24, cwnd = 24$
(D) $ssthresh = 6, cwnd = 12$
::: explanation
On 3 duplicate ACKs, Reno cuts $ssthresh = cwnd / 2 = 24 / 2 = 12\text{ MSS}$. Once the missing segment is confirmed by a fresh ACK, Fast Recovery terminates and sets $cwnd = ssthresh = 12\text{ MSS}$, resuming additive increase (+1 MSS/RTT).
:::

::: quiz Q2: Slow Start vs Congestion Avoidance
Why does Slow Start increase cwnd exponentially while Congestion Avoidance increases it linearly?
(A) Hardware limitations on routers
(B) Slow start uses UDP while congestion avoidance uses TCP
(*C) Slow start adds 1 MSS for every received ACK, doubling cwnd per RTT; congestion avoidance adds 1/cwnd MSS per ACK, adding exactly 1 MSS across an entire RTT
(D) Slow start ignores acknowledgments
::: explanation
During Slow Start, receiving $W$ ACKs adds $W \times 1\text{ MSS} = W$, so $W \to 2W$ (doubling). During Congestion Avoidance, receiving $W$ ACKs adds $W \times \frac{1}{W}\text{ MSS} = 1\text{ MSS}$, growing by exactly $+1\text{ MSS}$ per RTT.
:::
