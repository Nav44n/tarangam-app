# Progressive Problems: Sliding Window Protocols & Channel Utilization

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped unit conversions, and full line-by-line mathematical proofs.

---

## Level 1: Stop-and-Wait Efficiency & The Bandwidth-Delay Product

### Problem 1.1: Transmission Delay, Propagation Delay, and Channel Utilization in Stop-and-Wait

**Problem Statement:** A ground station transmits a data packet of size $L = 1{,}000\text{ bytes}$ to a satellite over a wireless link with bandwidth $B = 2\text{ Mbps}$ ($2\text{ Megabits per second}$). The one-way propagation delay between the ground station and the satellite is $T_p = 120\text{ ms}$.  
Assume acknowledgment packets (ACKs) are tiny (negligible transmission time) and processing time at the satellite is negligible ($0\text{ ms}$).  
1. Calculate the transmission delay ($T_t$) in milliseconds, showing all unit conversions explicitly.  
2. Calculate the total Round-Trip Time ($RTT$) and the total cycle time for one Stop-and-Wait frame.  
3. Calculate the sender utilization ($\eta$) under the Stop-and-Wait protocol, showing why it drops below $2\%$.  
4. Calculate the ratio $a = T_p / T_t$, and determine the minimum sender window size $N$ needed to achieve $100\%$ link utilization.

::: callout-intuition Core Mental Model
Imagine you are standing at the edge of a deep canyon, mailing physical letters to a friend across the canyon using a tiny zipline rope.  
- **Transmission Delay ($T_t$):** The time it takes your hand to push the envelope onto the zipline rope. If the letter is thick, it takes longer to push it out.  
- **Propagation Delay ($T_p$):** The time the envelope spends flying across the air through the canyon to reach your friend.  
- **Stop-and-Wait:** You push one envelope out, wait for it to fly across the canyon, wait for your friend to read it, and wait for your friend to send a tiny thumbs-up flag flying back. During all that waiting time, your hands are completely idle!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Convert Packet Size from Bytes to Bits</div>

**What are we doing?** Converting the packet length $L$ from bytes into individual binary digits (bits).

**Why are we starting here?** Networking bandwidth is measured in *bits per second* (bps), but file and packet sizes are usually quoted in *bytes*. You cannot divide bytes by bits directly without getting an incorrect number by a factor of 8.

**How do we do it?** By international computing definition, exactly $1\text{ byte} = 8\text{ bits}$.  
$$L = 1{,}000\text{ bytes} \times \frac{8\text{ bits}}{1\text{ byte}} = 8{,}000\text{ bits}$$

**Where did this formula/concept come from?** The basic definition of digital storage: 1 byte is a collection of 8 bits.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Convert Bandwidth from Megabits per Second to Bits per Second</div>

**What changed from Step 1?** In Step 1, we converted the numerator (the data size). Now we must convert the denominator (the transmission rate / bandwidth $B$) into base units of bits per second ($\text{bps}$).

**What are we doing?** Converting $B = 2\text{ Mbps}$ into raw bits per second ($\text{bps}$).

**Why are we doing this?** In networking telecommunications standards (data rates), the metric prefix "Mega" ($M$) denotes $10^6$ ($1{,}000{,}000$), not $2^{20}$. To compute time in seconds, the rate must be in pure bits per second.

**How do we do it?** $$1\text{ Mbps} = 10^6\text{ bits per second} = 1{,}000{,}000\text{ bps}$$  
$$B = 2 \times 10^6\text{ bps} = 2{,}000{,}000\text{ bits/second}$$

**Where did this formula/concept come from?** SI metric standard for bandwidth and data transmission speed ($1\text{ kbps} = 10^3\text{ bps}$, $1\text{ Mbps} = 10^6\text{ bps}$, $1\text{ Gbps} = 10^9\text{ bps}$).
</div>

<div class="step-card">
<div class="step-badge">Step 3: Calculate the Transmission Delay ($T_t$)</div>

**What changed from Step 2?** We now have both the packet size ($L$) and the transmission rate ($B$) in matching units of bits. We can now find the exact time needed to push the packet onto the physical wire/channel.

**What are we doing?** Calculating $T_t = \frac{L}{B}$, and converting the resulting time from seconds to milliseconds ($\text{ms}$).

**Why are we doing this?** The physical network adapter pushes bits out onto the medium one bit at a time. The transmission delay tells us how long the sender's network interface card is actively working to pump all 8,000 bits into the link.

**How do we do it?** $$T_t = \frac{L}{B} = \frac{8{,}000\text{ bits}}{2{,}000{,}000\text{ bits/second}}$$  
$$T_t = \frac{8}{2{,}000}\text{ seconds} = \frac{4}{1{,}000}\text{ seconds} = 0.004\text{ seconds}$$  
To convert seconds to milliseconds ($\text{ms}$), multiply by $1{,}000\text{ ms/second}$:  
$$T_t = 0.004\text{ s} \times \frac{1{,}000\text{ ms}}{1\text{ s}} = 4.0\text{ ms}$$

**Where did this formula/concept come from?** Classic physics rate formula: $\text{Time} = \frac{\text{Distance}}{\text{Speed}}$ or $\text{Time} = \frac{\text{Quantity of Work}}{\text{Rate of Work}} = \frac{\text{Packet Size}}{\text{Bandwidth}}$.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Understand and Identify Propagation Delay ($T_p$)</div>

**What changed from Step 3?** $T_t$ measured how long the transmitter *pushed* the bits. Now we identify how long the signal *travels* through space.

**What are we doing?** Recording the one-way transit time $T_p$ across the satellite link.

**Why are we doing this?** Electromagnetic signals travel through space at the speed of light ($c \approx 3 \times 10^8\text{ m/s}$). Even at the speed of light, physical distance introduces a fixed transit time before the first bit physically arrives at the receiver.

**How do we do it?** The problem statement gives this value directly:  
$$T_p = 120\text{ ms}$$

**Where did this formula/concept come from?** $T_p = \frac{\text{Physical Distance } (d)}{\text{Propagation Speed of Signal } (v)}$. For satellite communication in medium/geostationary orbit, distances range from hundreds to thousands of kilometers.
</div>

<div class="step-card">
<div class="step-badge">Step 5: Calculate the Total Cycle Time ($T_{\text{total}}$) for Stop-and-Wait</div>

**What changed from Step 4?** We now combine all phases of a complete communication cycle: pushing the packet, the packet flying out, the receiver sending an ACK, and the ACK flying back.

**What are we doing?** Calculating the total elapsed time between when the sender starts transmitting a packet and when the sender receives the acknowledgment allowing it to transmit the next packet.

**Why are we doing this?** In Stop-and-Wait, the sender is blocked from doing any new work until the ACK for the current packet arrives. The total cycle time represents the full period per packet.

**How do we do it?** The complete cycle consists of:
1. Pushing the data packet onto the wire: $T_t = 4\text{ ms}$
2. Packet traveling to the satellite: $T_p = 120\text{ ms}$
3. Satellite processing: $T_{\text{proc}} = 0\text{ ms}$ (given as negligible)
4. Satellite pushing ACK onto the link: $T_{t,\text{ACK}} \approx 0\text{ ms}$ (given as negligible)
5. ACK traveling back to the ground station: $T_p = 120\text{ ms}$

$$\text{Round-Trip Propagation Time } (RTT) = 2 \times T_p = 2 \times 120\text{ ms} = 240\text{ ms}$$  
$$T_{\text{total}} = T_t + 2 \times T_p = 4\text{ ms} + 240\text{ ms} = 244\text{ ms}$$

**Where did this formula/concept come from?** Stop-and-Wait protocol definition:  
$$T_{\text{total}} = T_t + T_p + T_{\text{proc}} + T_{t,\text{ACK}} + T_p$$  
With negligible ACK size and processing time, this simplifies to $T_{\text{total}} = T_t + 2T_p$.
</div>

<div class="step-card">
<div class="step-badge">Step 6: Calculate Channel Sender Utilization ($\eta$)</div>

**What changed from Step 5?** We know the useful working time ($T_t = 4\text{ ms}$) and the total wasted + working time ($T_{\text{total}} = 244\text{ ms}$). Now we compute efficiency.

**What are we doing?** Computing the utilization ratio $\eta$ (eta) as a fraction and as a percentage.

**Why are we doing this?** To quantify how much of the link's potential capacity is being squandered due to waiting.

**How do we do it?** $$\eta = \frac{\text{Useful Time Spent Transmitting}}{\text{Total Cycle Time}} = \frac{T_t}{T_t + 2T_p}$$  
Substitute our numbers:  
$$\eta = \frac{4\text{ ms}}{244\text{ ms}} = \frac{4}{244} = \frac{1}{61} \approx 0.0163934$$  
Convert to percentage by multiplying by $100\%$:  
$$\eta \approx 0.0163934 \times 100\% \approx 1.64\%$$

**Where did this formula/concept come from?** Standard definition of efficiency: $\text{Efficiency} = \frac{\text{Useful Work Time}}{\text{Total Time Taken}}$.
</div>

<div class="step-card">
<div class="step-badge">Step 7: Derive the Dimensionless Propagation-to-Transmission Ratio ($a$)</div>

**What changed from Step 6?** Instead of working with raw milliseconds, we express the propagation delay as a multiple of the transmission delay.

**What are we doing?** Computing the dimensionless ratio $a = \frac{T_p}{T_t}$.

**Why are we doing this?** $a$ is the fundamental parameter in network protocol analysis. It represents how many packets could fit in the "pipe" in one direction while a single packet is being transmitted.

**How do we do it?** $$a = \frac{T_p}{T_t} = \frac{120\text{ ms}}{4\text{ ms}} = 30$$  
Notice that we can also rewrite utilization $\eta$ using $a$:  
$$\eta = \frac{T_t}{T_t + 2T_p} = \frac{1}{1 + 2\left(\frac{T_p}{T_t}\right)} = \frac{1}{1 + 2a} = \frac{1}{1 + 2(30)} = \frac{1}{1 + 60} = \frac{1}{61} \approx 1.64\%$$

**Where did this formula/concept come from?** Dividing the numerator and denominator of $\frac{T_t}{T_t + 2T_p}$ by $T_t$.
</div>

<div class="step-card">
<div class="step-badge">Step 8: Calculate Minimum Window Size $N$ for $100\%$ Utilization</div>

**What changed from Step 7?** We discovered that a window size of $1$ packet yields only $\frac{1}{1 + 2a} = \frac{1}{61}$ link utilization. We now calculate how many packets we must transmit consecutively without waiting for ACKs to achieve $\eta = 100\% = 1.0$.

**What are we doing?** Solving for the optimal pipeline window size $N$.

**Why are we doing this?** If the sender does not stop and wait, but instead continues transmitting packet after packet continuously until the first ACK returns, the channel will never go idle.

**How do we do it?** For a sliding window protocol with window size $N$, utilization is given by:  
$$\eta = \min\left(1, \frac{N \times T_t}{T_t + 2T_p}\right) = \min\left(1, \frac{N}{1 + 2a}\right)$$  
To achieve $100\%$ utilization ($\eta = 1$):  
$$\frac{N}{1 + 2a} \ge 1 \implies N \ge 1 + 2a$$  
Substitute $a = 30$:  
$$N \ge 1 + 2(30) = 1 + 60 = 61$$

**Where did this formula/concept come from?** The concept of the **Bandwidth-Delay Product (BDP)**:  
The pipe holds $2 \times T_p \times B$ bits of data during one RTT. In packet units, this equals $\frac{2T_p}{T_t} = 2a$ packets in flight. Adding the $1$ packet currently being pushed onto the wire gives $1 + 2a$ total packets needed to keep the sender busy for the entire round trip.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary and Intuitive Sanity Check</div>

**What is the final answer?**
- Packet size in bits: $L = 8{,}000\text{ bits}$  
- Link bandwidth in bps: $B = 2{,}000{,}000\text{ bps}$  
- Transmission delay: $T_t = 4.0\text{ ms}$  
- Propagation delay: $T_p = 120.0\text{ ms}$  
- Total cycle time: $T_{\text{total}} = 244.0\text{ ms}$  
- Stop-and-Wait utilization: $\eta = \frac{1}{61} \approx 1.64\%$  
- Normalized parameter: $a = 30$  
- Minimum window size for $100\%$ utilization: $N = 61\text{ packets}$

**Why does this answer make sense?** It takes only $4\text{ ms}$ to push a packet into space, but it takes $240\text{ ms}$ for the round trip journey. That means for every $244\text{ ms}$ of time, the transmitter works for $4\text{ ms}$ and sleeps for $240\text{ ms}$.  
$240 / 4 = 60$ packet-durations of empty silence. If we send $60$ more packets while waiting for that first ACK (giving a total window of $1 + 60 = 61$ packets), the sender will never have to pause, driving channel efficiency to $100\%$.
</div>

</div>

---

## Level 2: Sequence Number Constraints & Protocol Ambiguity

### Problem 2.1: Deriving Minimum Sequence Number Bits for Go-Back-N and Selective Repeat

**Problem Statement:** From Level 1, we know that to maximize channel utilization over this satellite link, the sender must support a sliding window of size $N = 61$ packets (meaning the sender can transmit up to $61$ unacknowledged packets at any moment: $W_s = 61$).  
Packets in real computer networks must carry a binary sequence number in their header so the receiver can tell them apart. Bits in packet headers cost bandwidth, so we must find the smallest number of bits $k$ required to prevent ambiguity.  
1. For **Go-Back-N (GBN)**, where the receiver window size is $W_r = 1$, use the mathematical condition $W_s + W_r \le 2^k$ to prove that $W_s \le 2^k - 1$. Calculate the minimum integer $k$ for $W_s = 61$.  
2. For **Selective Repeat (SR)**, where the receiver window size equals the sender window size ($W_s = W_r$), use the mathematical condition $W_s + W_r \le 2^k$ to prove that $W_s \le 2^{k-1}$. Calculate the minimum integer $k$ for $W_s = 61$.  
3. Explain, using an intuitive walkie-talkie scenario, why setting $W_s = 2^k$ in Selective Repeat causes catastrophic protocol failure (the "Old Duplicate vs. Brand New Packet" ambiguity).

::: callout-intuition Core Mental Model
Imagine a clock with only numbers 0, 1, 2, and 3 (a 2-bit clock, since $2^2 = 4$).  
If you tell your friend: *"I will send you tasks numbered 0, 1, 2, 3, and then loop back to 0."* If your friend receives a task labeled **0**, did you just send the **very first task again** because your friend's previous ACK was lost? Or did your friend successfully finish tasks 0, 1, 2, and 3, and this is a **brand-new task for tomorrow** that also happens to be numbered 0?  
If the numbers loop around too fast, the receiver cannot tell yesterday's ghost packet from today's fresh packet!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Understand How $k$ Bits Produce Sequence Numbers</div>

**What are we doing?** Determining the total pool of unique identification labels available when using $k$ bits in a binary header field.

**Why are we starting here?** Every packet has a fixed header field for its sequence number. If that field has $k$ binary bits, it can only count up to a finite number before it runs out of combinations and must wrap around to zero (modulo arithmetic).

**How do we do it?** Each bit has 2 possible states ($0$ or $1$).  
With $k$ bits, the total number of unique sequence numbers is:  
$$\text{Total Sequence Numbers } M = 2^k$$  
The sequence numbers generated are integers in the set:  
$$\{0, 1, 2, \dots, 2^k - 1\}$$  
For example:
- If $k = 1$ bit: $2^1 = 2$ sequence numbers $\to \{0, 1\}$
- If $k = 2$ bits: $2^2 = 4$ sequence numbers $\to \{0, 1, 2, 3\}$
- If $k = 3$ bits: $2^3 = 8$ sequence numbers $\to \{0, 1, 2, 3, 4, 5, 6, 7\}$

**Where did this formula/concept come from?** Basic combinatorics of binary representation: an ordered string of $k$ independent binary digits has $2 \times 2 \times \dots \times 2 = 2^k$ possible values.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Derive the Window Size Limit for Go-Back-N ($W_s \le 2^k - 1$)</div>

**What changed from Step 1?** We now connect the available sequence space $2^k$ to the window limits of the Go-Back-N protocol.

**What are we doing?** Proving why Go-Back-N requires the sender window $W_s$ to be strictly less than $2^k$ ($W_s \le 2^k - 1$).

**Why are we doing this?** In Go-Back-N, the receiver only accepts packets **strictly in order**. Therefore, the receiver window size is fixed at $W_r = 1$. The receiver only maintains a single variable: $\text{expected\_frame}$.

**How do we do it?** The fundamental rule to prevent window overlap across wrap-around is:  
$$W_s + W_r \le 2^k$$  
Substitute $W_r = 1$:  
$$W_s + 1 \le 2^k \implies W_s \le 2^k - 1$$  

*Proof by Counterexample (What breaks if $W_s = 2^k$?):* Suppose $k = 2$ bits, so sequence numbers are $\{0, 1, 2, 3\}$ ($2^k = 4$).  
Let $W_s = 2^k = 4$.  
1. Sender transmits frames $0, 1, 2, 3$.
2. Receiver receives all 4 frames successfully in order!  
   The receiver advances its expected pointer: $0 \to 1 \to 2 \to 3 \to 0$. The receiver is now waiting for frame $0$ of the *next* batch.  
   The receiver sends ACKs for $0, 1, 2, 3$.
3. **Catastrophe:** All 4 ACKs get lost in the network due to noise.
4. Sender's timer expires for frame $0$. The sender thinks frame $0$ was never received!
5. Sender retransmits frame $0$ (from the old batch).
6. Receiver sees frame $0$. The receiver says: *"Hooray, frame 0 of the new batch has arrived!"* and accepts the duplicate data as brand-new data.  
The data stream is now permanently corrupted!  

Therefore, $W_s$ cannot exceed $2^k - 1$.

**Where did this formula/concept come from?** Sliding window correctness invariant: The sender's active window and the receiver's active window must never overlap in modulo $2^k$ space.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Calculate Minimum $k$ for Go-Back-N with $W_s = 61$</div>

**What changed from Step 2?** We now apply the derived formula $W_s \le 2^k - 1$ to our satellite link requirement $W_s = 61$.

**What are we doing?** Solving the inequality $61 \le 2^k - 1$ for the smallest integer $k$.

**Why are we doing this?** To find how many bits the network engineer must allocate in the packet header for sequence numbering under GBN.

**How do we do it?** $$2^k - 1 \ge W_s$$  
$$2^k - 1 \ge 61$$  
Add 1 to both sides:  
$$2^k \ge 62$$  
Let us test successive integer powers of 2:  
- If $k = 5$: $2^5 = 32$. Is $32 \ge 62$? **No.** (Too small)  
- If $k = 6$: $2^6 = 64$. Is $64 \ge 62$? **Yes.** ($64 \ge 62$)  

Taking the base-2 logarithm:  
$$k \ge \lceil \log_2(62) \rceil = \lceil 5.954 \rceil = 6\text{ bits}$$

**Where did this formula/concept come from?** Algebraic inversion of powers of 2 using the ceiling function $\lceil \dots \rceil$ because bit counts in headers must be whole integers.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Derive the Window Size Limit for Selective Repeat ($W_s \le 2^{k-1}$)</div>

**What changed from Step 3?** We now analyze **Selective Repeat (SR)**, where the receiver does *not* have a window of size 1. Instead, the receiver has an acceptance buffer of size $W_r = W_s$.

**What are we doing?** Proving why Selective Repeat requires $W_s \le 2^{k-1}$ (which means the window can be at most *half* the sequence number space).

**Why are we doing this?** In Selective Repeat, the receiver accepts out-of-order packets and buffers them. Because the receiver window moves forward independently, both the sender and receiver have dynamic windows of size $W_s$.

**How do we do it?** Apply the general non-overlap invariant:  
$$W_s + W_r \le 2^k$$  
In symmetric Selective Repeat protocols, the receiver buffer size matches the sender window: $W_r = W_s$.  
$$W_s + W_s \le 2^k$$  
$$2W_s \le 2^k$$  
Divide both sides by 2:  
$$W_s \le \frac{2^k}{2} = 2^{k-1}$$

**Where did this formula/concept come from?** In SR, the receiver window can advance by up to $W_s$ positions before the sender learns about it. If the ACKs are delayed or lost, the sender's window is still at the old positions while the receiver's window has slid forward by $W_s$. To guarantee that the old sender window and the new receiver window do not cover any identical sequence numbers, the sum of their widths cannot exceed the total circle size $2^k$.
</div>

<div class="step-card">
<div class="step-badge">Step 5: The "Walkie-Talkie" Ambiguity Failure Demonstration</div>

**What changed from Step 4?** Let us trace an explicit step-by-step failure to prove why $W_s > 2^{k-1}$ breaks Selective Repeat.

**What are we doing?** Tracing what happens if we violate the rule and choose $k = 2$ (sequence numbers $\{0, 1, 2, 3\}$, so $2^k = 4$), but we pick $W_s = W_r = 3$ (which is greater than $2^{2-1} = 2$).

**Why are we doing this?** To visualize the ambiguity directly from the receiver's perspective.

**How do we do it?** Let $k = 2 \implies \text{Sequences} = \{0, 1, 2, 3\}$.  
Assume we set $W_s = 3$ and $W_r = 3$.  
1. **Initial State:**
   - Sender window: $[0, 1, 2]$  
   - Receiver window: $[0, 1, 2]$  
2. Sender transmits frames $0, 1, 2$.  
3. Receiver receives frames $0, 1, 2$ perfectly!  
   - Receiver buffers/delivers all 3 frames.  
   - Receiver slides its window forward by 3 slots.  
   - New Receiver Window: $[3, 0, 1]$ (because after 2 comes 3, then 0, then 1).  
   - Receiver transmits ACK 0, ACK 1, ACK 2.  
4. **The Disaster on the Channel:**
   - Every single ACK (0, 1, 2) is destroyed by solar flare interference and lost.  
   - The sender window never moves! Sender window is still: $[0, 1, 2]$.  
5. **Timeout:**
   - Sender's timer for frame $0$ expires.  
   - Sender retransmits the **original old frame 0**.  
6. **The Ambiguity at Receiver:**
   - Receiver receives frame $0$.  
   - Receiver looks at its current window: $[3, \mathbf{0}, 1]$.  
   - Frame $0$ falls inside the window!  
   - The receiver assumes: *"This must be the brand-new frame 0 that comes right after frame 3!"*
   - The receiver accepts duplicate old data as new data! The file is corrupt.

To prevent this overlap between the old sender window and the advanced receiver window, the window size $W_s$ can never be larger than half the sequence space: $W_s \le 2^{k-1}$.
</div>

<div class="step-card">
<div class="step-badge">Step 6: Calculate Minimum $k$ for Selective Repeat with $W_s = 61$</div>

**What changed from Step 5?** Now that we have proven $W_s \le 2^{k-1}$, we calculate the bits needed for our $W_s = 61$ requirement.

**What are we doing?** Solving the inequality $61 \le 2^{k-1}$ for the smallest integer $k$.

**Why are we doing this?** To determine the bit allocation in packet headers when running Selective Repeat instead of Go-Back-N.

**How do we do it?** $$2^{k-1} \ge W_s$$  
$$2^{k-1} \ge 61$$  
Let us test successive values of $k$:  
- If $k = 6$: $2^{6-1} = 2^5 = 32$. Is $32 \ge 61$? **No.**
- If $k = 7$: $2^{7-1} = 2^6 = 64$. Is $64 \ge 61$? **Yes.** ($64 \ge 61$)  

Taking the base-2 logarithm:  
$$k - 1 \ge \lceil \log_2(61) \rceil$$  
Since $2^5 = 32$ and $2^6 = 64$, $\lceil \log_2(61) \rceil = 6$.  
$$k - 1 \ge 6 \implies k \ge 6 + 1 = 7\text{ bits}$$

**Where did this formula/concept come from?** Logarithmic inversion of the Selective Repeat window constraint inequality.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary and Comparison Table</div>

**What is the final answer?** For a required window size of $W_s = 61$:  
- **Go-Back-N:** Requires $W_s \le 2^k - 1 \implies 2^k \ge 62 \implies \mathbf{k = 6\text{ bits}}$ (yielding sequence space $2^6 = 64$, with maximum allowed $W_s = 63$).  
- **Selective Repeat:** Requires $W_s \le 2^{k-1} \implies 2^{k-1} \ge 61 \implies \mathbf{k = 7\text{ bits}}$ (yielding sequence space $2^7 = 128$, with maximum allowed $W_s = 64$).

**Why does this answer make sense?** Selective Repeat needs an extra bit ($k = 7$ vs $k = 6$) because its receiver accepts packets out of order. To prevent the receiver's forward-sliding window from confusing retransmitted old packets with future packets that wrapped around the circle, the sequence number space must be at least twice as large as the window size.
</div>

</div>

---

## Level 3: Packet Loss and Recovery Tracing (Go-Back-N vs. Selective Repeat)

### Problem 3.1: Complete Frame-by-Frame Execution Trace of Go-Back-N vs. Selective Repeat under Packet Loss

**Problem Statement:** A sender transmits a window of $5$ frames: **Frame 0, Frame 1, Frame 2, Frame 3, Frame 4** ($W_s = 5$) back-to-back over a channel.  
- **Frame 0** and **Frame 1** arrive safely at the receiver.  
- **Frame 2 is corrupted by channel noise and completely lost.**
- **Frame 3** and **Frame 4** arrive safely at the receiver immediately afterwards.  
- No ACKs are lost.  

Trace the complete timeline of events for:  
1. **Case A: Go-Back-N (GBN)** — show receiver actions, exact ACKs generated, sender timer expiration, and every retransmitted frame.  
2. **Case B: Selective Repeat (SR)** — show receiver buffering actions, exact individual ACKs generated, sender timeout behavior, and every retransmitted frame.

::: callout-intuition Core Mental Model
Imagine an assembly line building a bicycle:  
- **Go-Back-N is a stubborn perfectionist:** The worker only installs parts in exact order: Part 0 (Frame), Part 1 (Wheels), Part 2 (Chain), Part 3 (Seat), Part 4 (Handlebars). If Part 2 gets lost in the mail, the worker sees Part 3 and screams: *"I can't use a seat without a chain! Throw it in the trash!"* Then Part 4 arrives: *"Throw it in the trash!"* The sender has to re-ship Part 2, Part 3, AND Part 4 all over again!  
- **Selective Repeat is an organized warehouse:** The worker says: *"Part 2 is missing, but Part 3 and 4 are here? Great! I'll put Part 3 and 4 safely in a storage bin on the shelf and sign a delivery receipt specifically for them. Dear sender: ONLY re-ship Part 2!"*
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Understand the Key Protocol Rules of Go-Back-N (GBN)</div>

**What are we doing?** Establishing the operational rules for Go-Back-N before tracing its execution.

**Why are we starting here?** You cannot trace an algorithm without knowing its exact state machine and event handlers.

**How do we do it?** In Go-Back-N:
1. **Receiver Window:** Size is strictly $W_r = 1$. The receiver maintains a single pointer: `expected_frame`.
2. **Acceptance Rule:** The receiver accepts a frame *if and only if* its sequence number exactly matches `expected_frame`. If any other frame arrives (even if valid and uncorrupted), the receiver **discards it completely**!
3. **Acknowledgment Type:** Cumulative ACKs. An `ACK(n)` means: *"I have received all frames up to and including frame $n$ perfectly."* (Some textbooks define `ACK(n)` as "expecting frame $n$"; here we use the universal standard: `ACK(n)` acknowledges frame $n$).
4. **Sender Timer:** The sender maintains a single timer for the oldest unacknowledged frame. If this timer expires, the sender must **go back and retransmit ALL unacknowledged frames currently in the window**, not just the lost one.

**Where did this formula/concept come from?** The standard ARQ (Automatic Repeat reQuest) protocol definition designed for ultra-simple receivers with no memory buffers.
</div>

<div class="step-card">
<div class="step-badge">Step 2: Trace Go-Back-N Execution (Timeline of Events)</div>

**What changed from Step 1?** We now apply these 4 rules to our specific transmission: Frames 0, 1, 2, 3, 4 with Frame 2 lost.

**What are we doing?** Constructing the step-by-step trace of packets and ACKs for Go-Back-N.

**How do we do it?**

```
Sender                                              Receiver (expected = 0)
  | -------- Frame 0 -----------------------------> |  Matches expected! Delivers Frame 0.
  |                                                 |  Advances expected = 1.
  | <------- ACK 0 -------------------------------- |  Sends ACK 0.
  |                                                 |
  | -------- Frame 1 -----------------------------> |  Matches expected! Delivers Frame 1.
  |                                                 |  Advances expected = 2.
  | <------- ACK 1 -------------------------------- |  Sends ACK 1.
  |                                                 |
  | -------- Frame 2 (LOST IN NOISE) ------------ X |  (Never arrives)
  |                                                 |
  | -------- Frame 3 -----------------------------> |  Expected is 2, but got 3!
  |                                                 |  DISCARDS Frame 3!
  | <------- ACK 1 (Duplicate ACK) ---------------- |  Re-sends ACK 1 ("I only have up to 1!")
  |                                                 |
  | -------- Frame 4 -----------------------------> |  Expected is 2, but got 4!
  |                                                 |  DISCARDS Frame 4!
  | <------- ACK 1 (Duplicate ACK) ---------------- |  Re-sends ACK 1 ("I only have up to 1!")
  |                                                 |
  | [Timer for Frame 2 EXPIRES!]                    |
  | Sender must GO BACK to Frame 2!                 |
  | Retransmits: Frame 2, Frame 3, Frame 4          |
  |                                                 |
  | -------- Frame 2 (Retransmit) ----------------> |  Matches expected = 2! Delivers Frame 2.
  |                                                 |  Advances expected = 3.
  | <------- ACK 2 -------------------------------- |  Sends ACK 2.
  |                                                 |
  | -------- Frame 3 (Retransmit) ----------------> |  Matches expected = 3! Delivers Frame 3.
  |                                                 |  Advances expected = 4.
  | <------- ACK 3 -------------------------------- |  Sends ACK 3.
  |                                                 |
  | -------- Frame 4 (Retransmit) ----------------> |  Matches expected = 4! Delivers Frame 4.
  |                                                 |  Advances expected = 5.
  | <------- ACK 4 -------------------------------- |  Sends ACK 4.
```

**Detailed State Breakdown for GBN:**
1. **Frame 0 arrives:** Matches `expected_frame = 0`. Delivered to application layer. Receiver sends `ACK 0`. `expected_frame` becomes $1$.
2. **Frame 1 arrives:** Matches `expected_frame = 1`. Delivered to application layer. Receiver sends `ACK 1`. `expected_frame` becomes $2$.
3. **Frame 2 is lost:** Receiver never sees it. Receiver state remains `expected_frame = 2`.
4. **Frame 3 arrives:** Receiver checks if $3 == \text{expected\_frame } (2)$. False! Receiver **discards** Frame 3. To remind sender where it is, it generates a duplicate `ACK 1`.
5. **Frame 4 arrives:** Receiver checks if $4 == \text{expected\_frame } (2)$. False! Receiver **discards** Frame 4. Generates another duplicate `ACK 1`.
6. **Sender Timeout:** Sender has received `ACK 0` and `ACK 1`. Frames 0 and 1 are cleared from the window. The oldest unacknowledged frame is Frame 2. Its timer expires.
7. **Retransmission:** Sender must retransmit every frame starting from 2 up to the end of the window: **Frame 2, Frame 3, and Frame 4** are all retransmitted.
</div>

<div class="step-card">
<div class="step-badge">Step 3: Understand the Key Protocol Rules of Selective Repeat (SR)</div>

**What changed from Step 2?** We now examine the second protocol: **Selective Repeat**.

**What are we doing?** Establishing the operational rules for Selective Repeat before tracing its execution.

**Why are we doing this?** To contrast Selective Repeat's intelligent buffering against Go-Back-N's discard behavior.

**How do we do it?** In Selective Repeat:
1. **Receiver Window:** Size $W_r > 1$ (matches $W_s$). The receiver possesses an in-memory buffer to hold out-of-order frames.
2. **Acceptance Rule:** If a frame arrives out of order but falls within $[R_{\text{base}}, R_{\text{base}} + W_r - 1]$, the receiver **stores it in the buffer**!
3. **Acknowledgment Type:** **Selective (Individual) ACKs**. An `ACK(n)` acknowledges *only* frame $n$, saying nothing about other frames.
4. **Sender Timers:** The sender maintains an **independent, dedicated timer for EACH individual unacknowledged frame**.
5. **Retransmission Rule:** When a timer expires for frame $n$, the sender retransmits **ONLY frame $n$**.

**Where did this formula/concept come from?** Advanced ARQ protocols designed to avoid wasting network bandwidth on noisy or high-latency links.
</div>

<div class="step-card">
<div class="step-badge">Step 4: Trace Selective Repeat Execution (Timeline of Events)</div>

**What changed from Step 3?** We now apply Selective Repeat rules to the identical scenario: Frames 0, 1, 2, 3, 4 sent, Frame 2 lost.

**What are we doing?** Constructing the step-by-step trace of packets and ACKs for Selective Repeat.

**How do we do it?**

```
Sender                                              Receiver (Base = 0, Window: [0, 1, 2, 3, 4])
  | -------- Frame 0 -----------------------------> |  In window! Delivers Frame 0.
  |                                                 |  Advances base = 1. Window: [1, 2, 3, 4, 5]
  | <------- ACK 0 -------------------------------- |  Sends individual ACK 0.
  |                                                 |
  | -------- Frame 1 -----------------------------> |  In window! Delivers Frame 1.
  |                                                 |  Advances base = 2. Window: [2, 3, 4, 5, 6]
  | <------- ACK 1 -------------------------------- |  Sends individual ACK 1.
  |                                                 |
  | -------- Frame 2 (LOST IN NOISE) ------------ X |  (Never arrives)
  |                                                 |
  | -------- Frame 3 -----------------------------> |  In window [2, 3, 4, 5, 6]!
  |                                                 |  BUFFERS Frame 3 in memory (out-of-order).
  | <------- ACK 3 -------------------------------- |  Sends individual ACK 3!
  |                                                 |
  | -------- Frame 4 -----------------------------> |  In window [2, 3, 4, 5, 6]!
  |                                                 |  BUFFERS Frame 4 in memory (out-of-order).
  | <------- ACK 4 -------------------------------- |  Sends individual ACK 4!
  |                                                 |
  | Sender marks Frame 3 as ACKED.                  |
  | Sender marks Frame 4 as ACKED.                  |
  |                                                 |
  | [Timer for Frame 2 ONLY EXPIRES!]               |
  | Sender retransmits ONLY Frame 2!                |
  |                                                 |
  | -------- Frame 2 (Retransmit) ----------------> |  Missing piece arrives!
  |                                                 |  Receiver delivers Frame 2, pulls buffered
  |                                                 |  Frame 3 and Frame 4 from memory,
  |                                                 |  and delivers all three to application!
  |                                                 |  Advances base = 5.
  | <------- ACK 2 -------------------------------- |  Sends individual ACK 2.
```

**Detailed State Breakdown for SR:**
1. **Frame 0 arrives:** In window. Delivered to application. Receiver sends `ACK 0`. Receiver base moves to 1.
2. **Frame 1 arrives:** In window. Delivered to application. Receiver sends `ACK 1`. Receiver base moves to 2.
3. **Frame 2 is lost:** Receiver is waiting for Frame 2. Receiver window remains $[2, 3, 4, 5, 6]$.
4. **Frame 3 arrives:** Falls inside $[2, 3, 4, 5, 6]$. It cannot be delivered yet because Frame 2 is missing. The receiver **stores Frame 3 in a local buffer** and transmits `ACK 3`.
5. **Frame 4 arrives:** Falls inside $[2, 3, 4, 5, 6]$. The receiver **stores Frame 4 in a local buffer** and transmits `ACK 4`.
6. **Sender receives ACK 3 and ACK 4:** Sender marks Frame 3 and Frame 4 as successfully received. Their timers are stopped.
7. **Sender Timeout:** Frame 2's timer expires.
8. **Retransmission:** Sender retransmits **ONLY Frame 2**. Frames 3 and 4 are NOT retransmitted!
9. **Arrival of Retransmitted Frame 2:** The receiver receives Frame 2. It now has contiguous frames: 2 (just arrived), 3 (buffered), and 4 (buffered). It delivers 2, 3, and 4 to the application layer in correct order, and advances its base pointer to 5. Receiver transmits `ACK 2`.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Comparative Side-by-Side Analysis</div>

**What is the final answer?** Let us compare the resource utilization and network waste between the two protocols:

| Feature | Go-Back-N (GBN) | Selective Repeat (SR) |
| :--- | :--- | :--- |
| **Receiver Buffer Needed** | None ($W_r = 1$). Only 1 packet space. | Yes ($W_r = W_s$). Must buffer uncorrupted out-of-order packets. |
| **Frame 3 & 4 Fate on First Pass** | Discarded into the trash by receiver. | Stored safely in receiver memory buffer. |
| **ACKs Generated for 3 & 4** | Duplicate `ACK 1`, `ACK 1` (cumulative). | Explicit individual `ACK 3`, `ACK 4`. |
| **Frames Retransmitted on Timeout** | **3 frames:** Frame 2, Frame 3, Frame 4. | **1 frame:** Frame 2 only. |
| **Bandwidth Wasted** | High (Frames 3 and 4 were transmitted twice across the link). | Zero wasted bandwidth (every transmitted frame was useful). |
| **Implementation Complexity** | Extremely simple logic and low memory. | Complex timer tracking, sorting buffers, and sequence logic. |

**Why does this answer make sense?** Go-Back-N sacrifices network bandwidth to make receiver hardware as cheap and simple as possible (no memory buffers). Selective Repeat uses receiver memory and individual acknowledgments to ensure that not a single bit of wireless bandwidth is wasted on retransmitting packets that the receiver already has.
</div>

</div>

---

<a id="self-check"></a>
## Active Recall Checkpoint

::: quiz Q1: Utilization Ratio
If $T_p = 45\text{ ms}$ and $T_t = 5\text{ ms}$, what is the value of parameter $a$, and what is the minimum sliding window size needed for $100\%$ link efficiency?
(A) $a = 9, N = 10$
(*B) $a = 9, N = 19$
(C) $a = 0.11, N = 2$
(D) $a = 9, N = 9$
::: explanation
$a = \frac{T_p}{T_t} = \frac{45}{5} = 9$.  
Optimal window size $N = 1 + 2a = 1 + 2(9) = 19\text{ frames}$.
:::

::: quiz Q2: Selective Repeat Buffer Requirement
In a Selective Repeat protocol with a 5-bit sequence number, what is the maximum sender window size ($W_s$) and receiver window size ($W_r$) that guarantees error-free operation?
(A) $W_s = 31, W_r = 1$
(B) $W_s = 32, W_r = 32$
(*C) $W_s = 16, W_r = 16$
(D) $W_s = 8, W_r = 8$
::: explanation
With $k = 5$ bits, total sequence numbers $= 2^5 = 32$. In Selective Repeat, $W_s + W_r \le 2^k$. For symmetric windows, $W_s = W_r = 2^{k-1} = 32 / 2 = 16$.
:::
