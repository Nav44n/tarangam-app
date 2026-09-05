# Progressive Problems: Network Delays (Transmission, Propagation, Processing, and Queuing)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: Transmission Delay vs. Propagation Delay

### Problem 1.1: Pushing Bits vs. Flying Bits

A host wants to send a single packet of size $L = 1{,}000\text{ bytes}$ across a point-to-point fiber-optic link.  
The transmission rate (bandwidth) of the network link is $R = 1\text{ Mbps}$ (megabits per second).  
The physical length of the fiber cable connecting the two points is $d = 10{,}000\text{ km}$ (kilometers).  
The speed of light in the fiber cable is $s = 2 \times 10^8\text{ m/s}$ (meters per second).

Calculate:
1. The **Transmission Delay** ($d_{\text{trans}}$) in milliseconds.
2. The **Propagation Delay** ($d_{\text{prop}}$) in milliseconds.
3. The total time taken for the very last bit of the packet to arrive at the destination receiver.

::: callout-intuition Core Mental Model
Imagine a toll booth at the entrance of a long highway leading to a city:
- **Transmission Delay ($d_{\text{trans}}$):** This is the time it takes the toll booth operator to push a 10-car caravan through the gate onto the open road. It depends entirely on how long the caravan is and how fast the toll gate opens and closes. *It has nothing to do with how long the highway is!*
- **Propagation Delay ($d_{\text{prop}}$):** Once a car has passed the toll booth and is rolling on the highway, this is the time it takes that car to travel the physical distance at highway speed from the toll booth to the destination city. *It has nothing to do with how many cars are in the caravan!*
- **Total Delay:** The time between when the first car starts getting processed at the toll booth and when the very last car pulls up to the city parking lot is:
$$\text{Total Time} = d_{\text{trans}} + d_{\text{prop}}$$
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Unit Conversion for Packet Size (Bytes to Bits)</summary>

**What are we doing?** We are converting the packet size $L$ from **bytes** into **bits**.

**Why are we starting here?** Network links transmit data bit-by-bit ($1$s and $0$s). The link rate $R$ is given in **megabits per second (Mbps)**, not megabytes per second. To use mathematical equations involving both $L$ and $R$, their units must match.

**How do we do it?** 1. Recall the fundamental definition: $1\text{ byte} = 8\text{ bits}$.
2. Multiply the number of bytes by $8$:
   $$L = 1{,}000\text{ bytes} \times \frac{8\text{ bits}}{1\text{ byte}} = 8{,}000\text{ bits}$$

**Where did this concept come from?** In standard digital computer architecture, an octet (byte) is defined as a sequence of exactly $8$ binary digits (bits).

**Current Values for Calculation:**
- $L = 8{,}000\text{ bits}$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Unit Conversion for Transmission Rate (Mbps to bps)</summary>

**What changed from Step 1?** We have our packet size in bits. Now we must convert our link speed $R$ into matching base units: **bits per second (bps)**.

**What are we doing?** We convert $1\text{ Mbps}$ into bits per second.

**Why are we doing this?** The prefix "Mega" in telecommunications and networking bandwidth represents $10^6$ ($1{,}000{,}000$), based on the decimal system (metric prefix). We cannot divide bits by *mega*bits without converting to raw bits per second first.

**How do we do it?** 1. Recall the definition: $1\text{ Mbps} = 10^6\text{ bps} = 1{,}000{,}000\text{ bits per second}$.
2. Convert:
   $$R = 1\text{ Mbps} \times \frac{1{,}000{,}000\text{ bps}}{1\text{ Mbps}} = 1{,}000{,}000\text{ bits/second}$$

**Where did this concept come from?** International System of Units (SI) standard for networking bandwidth rates:
- $\text{kilo (k)} = 10^3 = 1{,}000$
- $\text{Mega (M)} = 10^6 = 1{,}000{,}000$
- $\text{Giga (G)} = 10^9 = 1{,}000{,}000{,}000$

**Current Values for Calculation:**
- $L = 8{,}000\text{ bits}$
- $R = 1{,}000{,}000\text{ bits/second}$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Calculate Transmission Delay (d_trans)</summary>

**What changed from Step 2?** Both $L$ and $R$ are now expressed in standard units of bits and bits/second.

**What are we doing?** We calculate the time required for the sender hardware to push all $8{,}000$ bits onto the physical communication wire.

**How do we do it?** 1. State the transmission delay formula:
   $$d_{\text{trans}} = \frac{L}{R}$$
2. Substitute our converted numbers into the formula:
   $$d_{\text{trans}} = \frac{8{,}000\text{ bits}}{1{,}000{,}000\text{ bits/second}}$$
3. Divide the numbers:
   $$d_{\text{trans}} = \frac{8{,}000}{1{,}000{,}000}\text{ seconds} = 0.008\text{ seconds}$$
4. Convert seconds to milliseconds ($\text{ms}$) so the number is easy to read. Recall that $1\text{ second} = 1{,}000\text{ milliseconds}$:
   $$d_{\text{trans}} = 0.008\text{ seconds} \times \frac{1{,}000\text{ ms}}{1\text{ second}} = \mathbf{8\text{ ms}}$$

**Where did this formula come from?** Basic rate equation from elementary algebra:
$$\text{Time} = \frac{\text{Amount of Work}}{\text{Rate of Work}}$$
Here, "Amount of Work" is the total number of bits to push ($L$), and "Rate of Work" is the transmission speed of the network card in bits per second ($R$).
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Unit Conversion for Distance (km to m)</summary>

**What changed from Step 3?** We have calculated the transmission delay ($8\text{ ms}$). Now we must calculate the propagation delay. Before doing so, we must align the units of distance $d$ and propagation speed $s$.

**What are we doing?** We convert distance $d = 10{,}000\text{ km}$ into meters ($\text{m}$).

**Why are we doing this?** The propagation speed $s = 2 \times 10^8\text{ m/s}$ is given in **meters** per second, while distance is given in **kilometers**. To divide distance by speed, the distance must be in meters.

**How do we do it?** 1. Recall that $1\text{ kilometer} = 1{,}000\text{ meters} = 10^3\text{ meters}$.
2. Multiply:
   $$d = 10{,}000\text{ km} \times \frac{1{,}000\text{ m}}{1\text{ km}} = 10{,}000{,}000\text{ meters} = 10^7\text{ meters}$$

**Current Values for Calculation:**
- $d = 10{,}000{,}000\text{ m} = 10^7\text{ m}$
- $s = 200{,}000{,}000\text{ m/s} = 2 \times 10^8\text{ m/s}$
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Calculate Propagation Delay (d_prop)</summary>

**What changed from Step 4?** Both physical distance $d$ and signal speed $s$ are in meters and meters/second.

**What are we doing?** We calculate how long a single electromagnetic signal (a bit) takes to travel across the physical medium from one end of the $10{,}000\text{ km}$ cable to the other.

**How do we do it?** 1. State the propagation delay formula:
   $$d_{\text{prop}} = \frac{d}{s}$$
2. Substitute our converted numbers:
   $$d_{\text{prop}} = \frac{10{,}000{,}000\text{ meters}}{200{,}000{,}000\text{ meters/second}} = \frac{10^7\text{ m}}{2 \times 10^8\text{ m/s}}$$
3. Simplify the fraction:
   $$d_{\text{prop}} = \frac{1}{20}\text{ seconds} = 0.05\text{ seconds}$$
4. Convert seconds to milliseconds:
   $$d_{\text{prop}} = 0.05\text{ seconds} \times \frac{1{,}000\text{ ms}}{1\text{ second}} = \mathbf{50\text{ ms}}$$

**Where did this formula come from?** Classical physics:
$$\text{Time} = \frac{\text{Distance}}{\text{Speed}}$$
A bit traveling through a physical medium (copper wire, fiber glass, or air) travels at a finite speed $s$, which is typically around $2 \times 10^8\text{ m/s}$ in glass (roughly $\frac{2}{3}$ the speed of light in a vacuum).
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Total Latency for Single-Link Arrival</summary>

**What is the final answer?**
The total time elapsed from the instant the sender starts transmitting the first bit until the receiver finishes receiving the very last bit is:
$$\text{Total Delay} = d_{\text{trans}} + d_{\text{prop}} = 8\text{ ms} + 50\text{ ms} = \mathbf{58\text{ ms}}$$

**Why does this answer make sense?**
- At time $t = 0\text{ ms}$, the sender begins pushing bit $1$ onto the wire.
- Bit $1$ immediately starts flying down the wire at speed $s$.
- At time $t = 8\text{ ms}$, the sender finishes pushing bit $8{,}000$ (the last bit) onto the wire. ($d_{\text{trans}}$ is complete).
- The last bit still has to travel the full $10{,}000\text{ km}$ length of the wire, which takes exactly $50\text{ ms}$ ($d_{\text{prop}}$).
- Therefore, the last bit arrives at the destination at time:
$$t = 8\text{ ms} + 50\text{ ms} = 58\text{ ms}$$
Notice how transmission delay ($8\text{ ms}$) and propagation delay ($50\text{ ms}$) measure two completely distinct physical phenomena!
</details>

</div>

---

## Level 2: End-to-End Delay across One Router

### Problem 2.1: The 4 Delay Components and Store-and-Forward Routing

Consider a two-hop network path connecting **Host A** to **Host B** through an intermediate **Router R**:
$$\text{Host A} \xrightarrow{\quad\text{Link 1}\quad} \text{Router R} \xrightarrow{\quad\text{Link 2}\quad} \text{Host B}$$

System Parameters:
- Packet size: $L = 1{,}500\text{ bytes}$
- Link 1 (Host A to Router R):
  - Bandwidth: $R_1 = 10\text{ Mbps}$
  - Distance: $d_1 = 200\text{ km}$
  - Signal propagation speed: $s_1 = 2 \times 10^8\text{ m/s}$
- Router R specifications:
  - Nodal processing delay: $d_{\text{proc}} = 0.5\text{ ms}$
  - Queuing delay: $d_{\text{queue}} = 1.5\text{ ms}$ (due to existing traffic in buffer)
- Link 2 (Router R to Host B):
  - Bandwidth: $R_2 = 100\text{ Mbps}$
  - Distance: $d_2 = 100\text{ km}$
  - Signal propagation speed: $s_2 = 2 \times 10^8\text{ m/s}$

Calculate the total end-to-end delay for a single packet from Host A to Host B, accounting for all four components of delay:
$$d_{\text{nodal}} = d_{\text{proc}} + d_{\text{queue}} + d_{\text{trans}} + d_{\text{prop}}$$
Show explicitly why the router must fully receive the packet before forwarding it (**Store-and-Forward** mechanism).

::: callout-intuition Core Mental Model
Imagine sending a package by postal mail through a regional sorting warehouse:
1. **Transmission 1 ($d_{\text{trans1}}$):** You load the package into the local postal truck.
2. **Propagation 1 ($d_{\text{prop1}}$):** The truck drives on the highway from your house to the sorting warehouse.
3. **Processing ($d_{\text{proc}}$):** At the warehouse, an automated scanner reads the barcode on the box to decide where it needs to go next, and checks for damage.
4. **Queuing ($d_{\text{queue}}$):** The package sits on a conveyor belt behind other boxes waiting for the outgoing truck to arrive.
5. **The Store-and-Forward Rule:** The warehouse cannot put the package on the next truck until the *entire box* has arrived inside the building. You can't ship half a box while the other half is still on the highway!
6. **Transmission 2 ($d_{\text{trans2}}$):** The warehouse loads the package onto the outgoing truck.
7. **Propagation 2 ($d_{\text{prop2}}$):** The second truck drives on the highway from the warehouse to your friend's house.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Calculate Transmission and Propagation on Link 1 (Host A to Router R)</summary>

**What are we doing?** We calculate the time it takes for Host A to transmit the packet onto Link 1, and the time it takes for that packet to travel across Link 1 to Router R.

**Why are we starting here?** The packet begins at Host A. Before Router R can do anything, the packet must first travel across Link 1.

**How do we do it?** 1. Convert packet size $L$:
   $$L = 1{,}500\text{ bytes} \times \frac{8\text{ bits}}{1\text{ byte}} = 12{,}000\text{ bits}$$
2. Convert bandwidth $R_1$:
   $$R_1 = 10\text{ Mbps} = 10 \times 10^6\text{ bps} = 10{,}000{,}000\text{ bps}$$
3. Compute transmission delay on Link 1 ($d_{\text{trans1}}$):
   $$d_{\text{trans1}} = \frac{L}{R_1} = \frac{12{,}000\text{ bits}}{10{,}000{,}000\text{ bits/s}} = 0.0012\text{ s}$$
   $$d_{\text{trans1}} = 0.0012\text{ s} \times 1{,}000 = \mathbf{1.2\text{ ms}}$$
4. Convert distance $d_1$:
   $$d_1 = 200\text{ km} = 200 \times 1{,}000\text{ m} = 200{,}000\text{ m} = 2 \times 10^5\text{ m}$$
5. Compute propagation delay on Link 1 ($d_{\text{prop1}}$):
   $$d_{\text{prop1}} = \frac{d_1}{s_1} = \frac{200{,}000\text{ m}}{200{,}000{,}000\text{ m/s}} = 0.001\text{ s}$$
   $$d_{\text{prop1}} = 0.001\text{ s} \times 1{,}000 = \mathbf{1.0\text{ ms}}$$

**System State at Router R Arrival:**
The entire packet has been completely received by Router R at timestamp:
$$t_1 = d_{\text{trans1}} + d_{\text{prop1}} = 1.2\text{ ms} + 1.0\text{ ms} = \mathbf{2.2\text{ ms}}$$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Processing and Queuing Delays at Router R</summary>

**What changed from Step 1?** The entire packet has now entered Router R. The packet now experiences internal delays inside the router's hardware.

**What are we doing?** We account for processing delay ($d_{\text{proc}}$) and queuing delay ($d_{\text{queue}}$).

**Why are these delays occurring?**
- **Processing Delay ($d_{\text{proc}}$):** The router must inspect the packet's IP header, verify the checksum to detect bit errors, and consult its routing table to determine which outgoing interface leads to Host B. This takes microcode computation time ($0.5\text{ ms}$).
- **Queuing Delay ($d_{\text{queue}}$):** Other network packets arrived at the router just before ours did. Router R places our packet into an output buffer (queue). Our packet must wait its turn until earlier packets finish transmitting ($1.5\text{ ms}$).

**How do we do it?** Add the router delays:
$$\text{Router Delay} = d_{\text{proc}} + d_{\text{queue}} = 0.5\text{ ms} + 1.5\text{ ms} = \mathbf{2.0\text{ ms}}$$

**System State when Packet Reaches Head of Queue:**
$$t_2 = t_1 + \text{Router Delay} = 2.2\text{ ms} + 2.0\text{ ms} = \mathbf{4.2\text{ ms}}$$
At $t = 4.2\text{ ms}$, the packet is ready to be transmitted out onto Link 2.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: The Store-and-Forward Rule Explained</summary>

**What are we doing?** We explain why Router R could not begin transmitting bits onto Link 2 earlier (e.g., at $t = 1.5\text{ ms}$).

**Why is this concept critical?** Modern internet routers operate on a **Store-and-Forward** architecture:
- A router must receive ("store") **all $12{,}000$ bits** of the packet before it can begin transmitting ("forwarding") the first bit onto the outbound link.
- Why? Because the error-checking checksum (CRC) is located in the packet trailer/header, and the destination address must be fully verified. If the packet arrived corrupted, the router must discard it immediately rather than wasting bandwidth on Link 2 sending bad data.
- Therefore, Link 2 transmission cannot begin until the full packet is stored, processed, and cleared from the queue ($t = 4.2\text{ ms}$).
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Calculate Transmission and Propagation on Link 2 (Router R to Host B)</summary>

**What changed from Step 3?** The packet has cleared the queue at Router R at $t = 4.2\text{ ms}$. Now Router R pushes the packet onto Link 2 toward Host B.

**What are we doing?** We calculate the transmission delay ($d_{\text{trans2}}$) and propagation delay ($d_{\text{prop2}}$) for Link 2.

**How do we do it?** 1. Convert bandwidth $R_2$:
   $$R_2 = 100\text{ Mbps} = 100 \times 10^6\text{ bps} = 100{,}000{,}000\text{ bps}$$
2. Compute transmission delay on Link 2 ($d_{\text{trans2}}$):
   $$d_{\text{trans2}} = \frac{L}{R_2} = \frac{12{,}000\text{ bits}}{100{,}000{,}000\text{ bits/s}} = 0.00012\text{ s}$$
   $$d_{\text{trans2}} = 0.00012\text{ s} \times 1{,}000 = \mathbf{0.12\text{ ms}}$$
3. Convert distance $d_2$:
   $$d_2 = 100\text{ km} = 100 \times 1{,}000\text{ m} = 100{,}000\text{ m} = 1 \times 10^5\text{ m}$$
4. Compute propagation delay on Link 2 ($d_{\text{prop2}}$):
   $$d_{\text{prop2}} = \frac{d_2}{s_2} = \frac{100{,}000\text{ m}}{200{,}000{,}000\text{ m/s}} = 0.0005\text{ s}$$
   $$d_{\text{prop2}} = 0.0005\text{ s} \times 1{,}000 = \mathbf{0.5\text{ ms}}$$

**Hop 2 Total Delay:**
$$\text{Hop 2 Time} = d_{\text{trans2}} + d_{\text{prop2}} = 0.12\text{ ms} + 0.5\text{ ms} = \mathbf{0.62\text{ ms}}$$
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Total End-to-End Delay Calculation</summary>

**What is the final answer?**
Summing all delay components across the entire path:
$$\begin{aligned}
d_{\text{end-to-end}} &= d_{\text{trans1}} + d_{\text{prop1}} + d_{\text{proc}} + d_{\text{queue}} + d_{\text{trans2}} + d_{\text{prop2}} \\
&= 1.2\text{ ms} + 1.0\text{ ms} + 0.5\text{ ms} + 1.5\text{ ms} + 0.12\text{ ms} + 0.5\text{ ms} \\
&= \mathbf{4.82\text{ ms}}
\end{aligned}$$

**Timeline Breakdown from t = 0:**
- $t = 0.0\text{ ms}$: Host A begins transmitting packet.
- $t = 1.2\text{ ms}$: Host A finishes transmitting last bit.
- $t = 2.2\text{ ms}$: Last bit reaches Router R (Hop 1 complete).
- $t = 2.7\text{ ms}$: Router R finishes header inspection ($d_{\text{proc}}$ done).
- $t = 4.2\text{ ms}$: Packet finishes waiting in queue ($d_{\text{queue}}$ done).
- $t = 4.32\text{ ms}$: Router R finishes transmitting packet onto Link 2 ($d_{\text{trans2}}$ done).
- $t = 4.82\text{ ms}$: Last bit arrives at Host B ($d_{\text{prop2}}$ done).

The packet is completely received at Host B at exactly $t = 4.82\text{ ms}$.
</details>

</div>

---

## Level 3: Pipelining Multiple Packets

### Problem 3.1: Concurrency and Pipelined Overlap across Links

Now suppose Host A wants to send **$3$ identical back-to-back packets** (Packet 1, Packet 2, and Packet 3) to Host B through the intermediate Router R:
$$\text{Host A} \xrightarrow{\quad\text{Link 1}\quad} \text{Router R} \xrightarrow{\quad\text{Link 2}\quad} \text{Host B}$$

To clearly visualize pipelining without distraction, assume idealized link parameters:
- Each packet size: $L$ such that transmission delay on each link is $d_{\text{trans}} = 10\text{ ms}$.
- Both Link 1 and Link 2 have identical bandwidth $R$ (so $d_{\text{trans1}} = d_{\text{trans2}} = 10\text{ ms}$).
- Propagation delay on both links is $d_{\text{prop}} = 5\text{ ms}$ (so $d_{\text{prop1}} = d_{\text{prop2}} = 5\text{ ms}$).
- Router processing delay is negligible: $d_{\text{proc}} = 0\text{ ms}$.
- Initial queue is empty: $d_{\text{queue}} = 0\text{ ms}$ for Packet 1.
- Router enforces **store-and-forward**.

Calculate:
1. The total time for all $3$ packets to be completely received at Host B.
2. Show step-by-step how transmission of Packet 2 overlaps with the flight/forwarding of Packet 1 (**Pipelining**).
3. Compare this total time against what it would take if Host A had to wait for Packet 1 to fully reach Host B before sending Packet 2 (Non-pipelined / Stop-and-Wait).

::: callout-intuition Core Mental Model
Imagine a car manufacturing assembly line with two stations: Station 1 installs the engine, and Station 2 paints the body.
- **Without Pipelining (Stop-and-Wait):** You build Car 1's engine, paint Car 1, deliver Car 1 to the customer, and only *then* start building Car 2. Station 1 sits completely empty and idle while Car 1 is being painted!
- **With Pipelining:** The instant Station 1 finishes installing Car 1's engine and rolls it over to Station 2, Station 1 immediately grabs Car 2 and starts working on its engine!
- Both stations work **at the same time on different cars**.
- In networking, while Link 2 is busy forwarding Packet 1, Link 1 does not sit idle—it is busy transmitting Packet 2!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Trace Packet 1 Through the System</summary>

**What are we doing?** We establish the baseline timeline by tracking Packet 1 from Host A all the way to Host B.

**Why are we starting here?** Packet 1 is first in line. Its milestones dictate when Router R becomes active.

**How do we do it?** Trace the timeline of Packet 1:
- $t = 0\text{ ms}$: Host A begins transmitting Packet 1 onto Link 1.
- $t = 10\text{ ms}$: Host A finishes transmitting Packet 1 ($d_{\text{trans1}} = 10\text{ ms}$).
- $t = 10\text{ ms} + 5\text{ ms} = 15\text{ ms}$: The last bit of Packet 1 propagates across Link 1 and arrives at Router R ($d_{\text{prop1}} = 5\text{ ms}$).
- Store-and-forward condition met: Router R now has the full Packet 1 at $t = 15\text{ ms}$.
- $t = 15\text{ ms}$: Router R immediately begins transmitting Packet 1 onto Link 2.
- $t = 15\text{ ms} + 10\text{ ms} = 25\text{ ms}$: Router R finishes transmitting Packet 1 onto Link 2 ($d_{\text{trans2}} = 10\text{ ms}$).
- $t = 25\text{ ms} + 5\text{ ms} = 30\text{ ms}$: Packet 1 finishes propagating across Link 2 and arrives at Host B ($d_{\text{prop2}} = 5\text{ ms}$).

**Packet 1 Completion:**
Packet 1 is completely received at Host B at **$t = 30\text{ ms}$**.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Trace Packet 2 and Identify the Overlap</summary>

**What changed from Step 1?** Host A does not wait for Packet 1 to reach Host B. The moment Host A finishes pushing the last bit of Packet 1 onto Link 1 at $t = 10\text{ ms}$, Link 1 becomes free!

**What are we doing?** We trace Packet 2 on Link 1 and see how it overlaps in time with Packet 1.

**How do we do it?** 1. **On Link 1:**
   - Host A immediately begins transmitting Packet 2 at $t = 10\text{ ms}$.
   - Host A finishes transmitting Packet 2 at $t = 10 + 10 = \mathbf{20\text{ ms}}$.
   - Packet 2 propagates across Link 1 and arrives completely at Router R at $t = 20 + 5 = \mathbf{25\text{ ms}}$.

2. **The Pipelining Overlap (Look at the clock between $t = 15\text{ ms}$ and $t = 20\text{ ms}$):**
   - On Link 1: Host A is busy transmitting Packet 2.
   - On Link 2: Router R is busy transmitting Packet 1.
   - **Both links are active simultaneously!** Two different packets are being pushed through two different wires in parallel.

3. **On Link 2 for Packet 2:**
   - At $t = 25\text{ ms}$, Packet 2 arrives at Router R.
   - Look at Link 2 at $t = 25\text{ ms}$: Router R just finished transmitting Packet 1 at exactly $t = 25\text{ ms}$!
   - Therefore, the queue delay at Router R is $0\text{ ms}$. Link 2 is immediately free!
   - Router R starts transmitting Packet 2 at $t = 25\text{ ms}$.
   - Router R finishes transmitting Packet 2 at $t = 25 + 10 = \mathbf{35\text{ ms}}$.
   - Packet 2 finishes propagating to Host B at $t = 35 + 5 = \mathbf{40\text{ ms}}$.

**Packet 2 Completion:**
Packet 2 is completely received at Host B at **$t = 40\text{ ms}$**.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Trace Packet 3 Through the Pipeline</summary>

**What changed from Step 2?** Host A finished sending Packet 2 on Link 1 at $t = 20\text{ ms}$. Link 1 is free once more.

**What are we doing?** We trace the third and final packet.

**How do we do it?** 1. **On Link 1:**
   - Host A begins transmitting Packet 3 at $t = 20\text{ ms}$.
   - Host A finishes transmitting Packet 3 at $t = 20 + 10 = \mathbf{30\text{ ms}}$.
   - Packet 3 propagates to Router R at $t = 30 + 5 = \mathbf{35\text{ ms}}$.

2. **On Link 2:**
   - At $t = 35\text{ ms}$, Packet 3 arrives at Router R.
   - Notice that Router R finished transmitting Packet 2 onto Link 2 at exactly $t = 35\text{ ms}$.
   - Link 2 is immediately free! Router R begins transmitting Packet 3 at $t = 35\text{ ms}$.
   - Router R finishes transmitting Packet 3 at $t = 35 + 10 = \mathbf{45\text{ ms}}$.
   - Packet 3 propagates across Link 2 and arrives at Host B at $t = 45 + 5 = \mathbf{50\text{ ms}}$.

**Packet 3 Completion:**
Packet 3 is completely received at Host B at **$t = 50\text{ ms}$**.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Master Pipelining Schedule Chart</summary>

**What are we doing?** We arrange all events on a unified time chart so the parallel execution is clearly visible.

**Pipelined Transmission Grid (Time in ms):**
```text
Time (ms): 0    10   15   20   25   30   35   40   45   50
           |----|----|----|----|----|----|----|----|----|
Link 1:    [ Pkt 1 ][ Pkt 2 ][ Pkt 3 ] (Idle)
Link 2:         (Idle)   [ Pkt 1 ][ Pkt 2 ][ Pkt 3 ]
Arrived:                 Pkt 1    Pkt 2    Pkt 3
```

**Notice the Rhythm:**
- Once the pipeline is full (after Packet 1 arrives at $t = 30\text{ ms}$), a new packet arrives at Host B **every $10\text{ ms}$**!
  - Packet 1 arrives at $t = 30\text{ ms}$
  - Packet 2 arrives at $t = 40\text{ ms}$ ($+10\text{ ms}$)
  - Packet 3 arrives at $t = 50\text{ ms}$ ($+10\text{ ms}$)
- This steady $10\text{ ms}$ arrival interval is determined entirely by the bottleneck transmission delay: $d_{\text{trans}} = 10\text{ ms}$.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Pipelined vs. Non-Pipelined Comparison</summary>

**What is the final answer?**
With pipelining, all $3$ packets arrive at Host B in **$50\text{ ms}$**.

**How much faster is this than a non-pipelined system?**
- **Non-pipelined (Stop-and-Wait):**
  Host A sends Packet 1 and waits for it to fully arrive at Host B before sending Packet 2.
  - Time for 1 packet = $30\text{ ms}$.
  - Time for 3 packets = $3 \times 30\text{ ms} = \mathbf{90\text{ ms}}$.

- **Pipelined:**
  $$\text{Total Time} = \mathbf{50\text{ ms}}$$

**Time Saved:**
$$\text{Time Saved} = 90\text{ ms} - 50\text{ ms} = \mathbf{40\text{ ms}}\quad (44.4\%\text{ reduction in total transfer time!})$$

**General Mathematical Formula for $P$ Packets across $N$ Identical Links:**
If there are $P$ packets, $N$ hops (links), each with transmission delay $d_{\text{trans}}$ and propagation delay $d_{\text{prop}}$:
$$\text{Total Time} = \underbrace{N \times (d_{\text{trans}} + d_{\text{prop}})}_{\text{Time for Packet 1 to traverse all } N \text{ hops}} + \underbrace{(P - 1) \times d_{\text{trans}}}_{\text{Time for remaining } P-1 \text{ packets to drain from pipeline}}$$

Plugging in our values ($P = 3$, $N = 2$, $d_{\text{trans}} = 10$, $d_{\text{prop}} = 5$):
$$\text{Total Time} = 2 \times (10 + 5) + (3 - 1) \times 10 = 2 \times 15 + 2 \times 10 = 30 + 20 = \mathbf{50\text{ ms}}$$
The formula matches our step-by-step trace.
</details>

</div>
