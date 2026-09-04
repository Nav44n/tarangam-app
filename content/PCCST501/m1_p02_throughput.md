# Progressive Problems: Network Throughput and Bottleneck Links

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: Single Connection Bottleneck

### Problem 1.1: Tracing a 50 MB File Transfer Through a Three-Link Path

A user sits at a laptop (Client) and downloads a file from a remote data center (Server).  
The path between the Server and Client consists of three physical links connected in series by two intermediate routers ($R_1$ and $R_2$):
$$\text{Server} \xrightarrow{\quad\text{Link 1}\quad} R_1 \xrightarrow{\quad\text{Link 2}\quad} R_2 \xrightarrow{\quad\text{Link 3}\quad} \text{Client}$$

The transmission rates (capacities) of the individual links are:
- **Link 1 (Server to $R_1$):** $R_1 = 100\text{ Mbps}$
- **Link 2 ($R_1$ to $R_2$):** $R_2 = 10\text{ Mbps}$
- **Link 3 ($R_2$ to Client):** $R_3 = 50\text{ Mbps}$

The file to be downloaded has a total size of $F = 50\text{ MB}$ (Megabytes).

You must:
1. Identify the **Bottleneck Link** and determine the maximum sustained **End-to-End Throughput**.
2. Convert the file size $F$ from Megabytes into raw bits, showing every single intermediate step and multiplication factor.
3. Convert the bottleneck link rate into raw bits per second (bps).
4. Calculate the total time required to transfer the file across the network (assuming ideal transmission without packet loss or protocol overhead).

::: callout-intuition Core Mental Model
Imagine water flowing through three connected garden hoses:
- Hose 1 is a wide firehose that can carry **100 gallons per minute**.
- Hose 2 is a narrow drinking straw that can only carry **10 gallons per minute**.
- Hose 3 is a medium garden hose that can carry **50 gallons per minute**.

If you connect them in a straight line:
$$\text{Wide Firehose (100)} \longrightarrow \text{Drinking Straw (10)} \longrightarrow \text{Medium Hose (50)}$$
How much water can possibly come out of the final hose each minute?
- Even though the first hose can pour $100$ gallons every minute, water gets completely choked as soon as it hits the narrow straw.
- The straw can only pass $10$ gallons each minute.
- That means the third hose only ever receives $10$ gallons each minute to carry to the bucket.
- **The Golden Rule of Throughput:** The maximum speed of any single pipeline is dictated by its **narrowest constriction** (the bottleneck). You can never go faster than your slowest link!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Identify the Bottleneck Link</div>

**What are we doing?** We examine the transmission capacities of all three links along the path and select the minimum value to find the end-to-end throughput.

**Why are we starting here?** Before calculating how long a download will take, we must know the rate at which data can actually flow through the network.

**How do we do it?** 1. List the transmission capacities of all links in the path:
   - Link 1 capacity: $R_1 = 100\text{ Mbps}$
   - Link 2 capacity: $R_2 = 10\text{ Mbps}$
   - Link 3 capacity: $R_3 = 50\text{ Mbps}$
2. Apply the mathematical definition of end-to-end throughput ($T$) for an unshared, single-session path:
   $$T = \min(R_1, R_2, R_3)$$
3. Substitute the values:
   $$T = \min(100\text{ Mbps}, 10\text{ Mbps}, 50\text{ Mbps}) = \mathbf{10\text{ Mbps}}$$

**Where did this concept come from?** In fluid dynamics and network queuing theory, this is known as the **Min-Cut / Bottleneck Capacity Principle**. Bits cannot exit a link faster than they can enter it without generating an infinite backlog. Router $R_1$ will simply buffer incoming bits from Link 1 and feed them out onto Link 2 at a maximum rate of $10\text{ Mbps}$.

**System State:**
- **Bottleneck Link:** Link 2 ($R_1 \to R_2$)
- **Sustained End-to-End Throughput:** $T = 10\text{ Mbps}$
</div>

<div class="step-card">
<div class="step-badge">Step 2: File Size Conversion (Megabytes to Bits)</div>

**What changed from Step 1?** We know our data rate ($10\text{ Mbps}$). Now we must express our file size $F = 50\text{ MB}$ in units of **bits** so that it matches the bits in $\text{Mbps}$.

**What are we doing?** We convert $50\text{ Megabytes (MB)}$ into bits, distinguishing carefully between the capital letter **$\text{B}$** (Bytes) and lowercase **$\text{b}$** (bits).

**Why are we doing this?** One of the most common mistakes in networking is mixing up bytes and bits.
- File storage on your hard drive is measured in **Bytes** ($\text{B}$).
- Network speeds are measured in **bits per second** ($\text{bps}$).
- If you divide Bytes by bits per second without converting, your answer will be off by a factor of $8$!

**How do we do it?** 1. **Step 2a: Convert Megabytes to Bytes.** In standard telecommunications and general networking calculations, the prefix Mega ($\text{M}$) denotes $10^6 = 1{,}000{,}000$:
   $$50\text{ MB} = 50 \times 1{,}000{,}000\text{ Bytes} = 50{,}000{,}000\text{ Bytes}$$
2. **Step 2b: Convert Bytes to Bits.** By definition, every $1\text{ Byte}$ contains exactly $8\text{ bits}$:
   $$50{,}000{,}000\text{ Bytes} \times \frac{8\text{ bits}}{1\text{ Byte}} = 400{,}000{,}000\text{ bits}$$
   In scientific notation:
   $$F = 4 \times 10^8\text{ bits}$$

**Where did this concept come from?**
- $1\text{ Byte} = 8\text{ bits}$ (the fundamental unit of addressable computer memory).
- $\text{SI Prefix Mega (M)} = 10^6 = 1{,}000{,}000$.

**System State:**
- Total Data to Transfer: $F = 400{,}000{,}000\text{ bits}$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Throughput Conversion (Mbps to bps)</div>

**What changed from Step 2?** We have $F$ in raw bits. Now we convert the bottleneck throughput $T = 10\text{ Mbps}$ into raw **bits per second (bps)**.

**What are we doing?** Converting $10\text{ Megabits per second}$ into bits per second.

**Why are we doing this?** To divide data volume by transmission rate, the units must cancel cleanly:
$$\frac{\text{bits}}{\text{bits/second}} = \text{seconds}$$

**How do we do it?** 1. Recall that $1\text{ Mbps} = 1{,}000{,}000\text{ bits per second} = 10^6\text{ bps}$.
2. Multiply:
   $$T = 10\text{ Mbps} \times \frac{1{,}000{,}000\text{ bps}}{1\text{ Mbps}} = 10{,}000{,}000\text{ bits/second}$$
   In scientific notation:
   $$T = 1 \times 10^7\text{ bits/second}$$

**System State:**
- Data Volume: $F = 400{,}000{,}000\text{ bits}$
- Bottleneck Speed: $T = 10{,}000{,}000\text{ bits/second}$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Calculate Transfer Time</div>

**What changed from Step 3?** Both the numerator (file size in bits) and the denominator (throughput in bits per second) are now in identical base units.

**What are we doing?** We compute the time in seconds needed to stream the entire file across the bottleneck link.

**How do we do it?** 1. State the transfer time formula:
   $$\text{Transfer Time} = \frac{\text{File Size (bits)}}{\text{Throughput (bits/second)}} = \frac{F}{T}$$
2. Substitute the converted values:
   $$\text{Transfer Time} = \frac{400{,}000{,}000\text{ bits}}{10{,}000{,}000\text{ bits/second}}$$
3. Cancel the matching zeroes (divide both numerator and denominator by $10{,}000{,}000$):
   $$\text{Transfer Time} = \frac{400}{10}\text{ seconds} = \mathbf{40\text{ seconds}}$$

**Where did this formula come from?** The fundamental kinematic equation of work and rate:
$$\text{Time} = \frac{\text{Total Quantity}}{\text{Rate of Flow}}$$
Because Link 2 can only emit $10{,}000{,}000$ bits each second, pumping all $400{,}000{,}000$ bits through that link requires exactly $40$ seconds.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Conclusion & Physical Verification</div>

**What is the final answer?**
- The bottleneck link is **Link 2** with a capacity of $10\text{ Mbps}$.
- The end-to-end throughput is **$10\text{ Mbps}$**.
- The total time to transfer the $50\text{ MB}$ file is **$40\text{ seconds}$**.

**Why does this answer make sense?**
- Even though the server pushes data onto Link 1 at a blazing $100\text{ Mbps}$, bits cannot travel through Link 2 any faster than $10\text{ Mbps}$.
- Router $R_1$'s input buffer fills up immediately, forcing the server's TCP connection to throttle its transmission rate down to match the $10\text{ Mbps}$ rate of Link 2.
- Even though Link 3 is capable of $50\text{ Mbps}$, it sits largely underutilized, only receiving new bits from Link 2 at a trickle rate of $10\text{ Mbps}$.
- At $10\text{ Mbps}$, the network delivers:
  $$\frac{10\text{ Megabits}}{8\text{ bits per Byte}} = 1.25\text{ Megabytes per second (MB/s)}$$
- Transferring $50\text{ MB}$ at $1.25\text{ MB/s}$:
  $$\frac{50\text{ MB}}{1.25\text{ MB/s}} = 40\text{ seconds}$$
Both calculation methods confirm the exact same result!
</div>

</div>

---

## Level 2: Shared Bottleneck Links

### Problem 2.1: Bandwidth Sharing on a Congested Backbone Link

Now consider a scenario where multiple users must compete for capacity across a shared regional backbone cable.

Three distinct clients ($\text{Client}_1$, $\text{Client}_2$, $\text{Client}_3$) are downloading files simultaneously from three separate servers ($\text{Server}_1$, $\text{Server}_2$, $\text{Server}_3$).  
All three connections pass through their own independent local access links, but they are all routed through the same **shared backbone link** between central routers $R_A$ and $R_B$:

```text
Server 1 ---(Link S1: 100 Mbps)---+                           +---(Link C1: 15 Mbps)---> Client 1
                                   \                         /
Server 2 ---(Link S2: 100 Mbps)----+---> Router RA          +---> Router RB ---(Link C2: 5 Mbps)---> Client 2
                                   /           \           /
Server 3 ---(Link S3: 100 Mbps)---+             \         /   +---(Link C3: 20 Mbps)---> Client 3
                                           [Shared Backbone Link]
                                             Capacity = 24 Mbps
```

System Specifications:
- **Server Access Links:**
  - $R_{S1} = 100\text{ Mbps}$
  - $R_{S2} = 100\text{ Mbps}$
  - $R_{S3} = 100\text{ Mbps}$
- **Central Shared Backbone Link:**
  - Total Capacity $R_{\text{backbone}} = 24\text{ Mbps}$
  - The router uses **Fair Queuing / Equal Sharing** (standard behavior under TCP congestion control), meaning the available backbone bandwidth is split evenly among all active flows competing for it.
- **Client Access Links (Last Mile):**
  - $\text{Client}_1$ access link: $R_{C1} = 15\text{ Mbps}$
  - $\text{Client}_2$ access link: $R_{C2} = 5\text{ Mbps}$
  - $\text{Client}_3$ access link: $R_{C3} = 20\text{ Mbps}$

You must:
1. Determine the slice of backbone bandwidth allocated to each of the $3$ competing sessions.
2. For each individual client, trace the three links along its path (Server Access Link, Shared Backbone Link, and Client Access Link).
3. Identify the specific bottleneck link for each of the three clients.
4. Calculate the resulting end-to-end throughput for each client ($T_1, T_2,$ and $T_3$).

::: callout-intuition Core Mental Model
Imagine a 3-lane highway that passes through a narrow single-lane construction zone:
- Three different drivers want to drive through.
- The construction zone has a total capacity of **24 cars per minute**.
- Since all three drivers arrive at the same time, the flagger lets them take turns fairly. Each driver gets an equal share of the narrow passage:
  $$\frac{24\text{ cars per minute}}{3\text{ drivers}} = 8\text{ cars per minute each}$$
- Now look at what happens when each driver exits the construction zone:
  - Driver 1's local neighborhood road can take up to $15$ cars per minute. But they only got $8$ through the construction zone! So their speed is capped at **$8$**.
  - Driver 2's local driveway has a speed bump that only allows **$5$ cars per minute**. Even though the construction zone granted them an $8$-car slot, their own slow driveway chokes them down to **$5$**!
  - Driver 3's open boulevard can take $20$ cars per minute. But the construction zone only gave them $8$. So their speed is capped at **$8$**.
- A shared link limits your slice of the pie, but your own local connection can still be an even tighter bottleneck!
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Calculate Fair-Share Bandwidth on the Backbone</div>

**What are we doing?** We calculate how much transmission bandwidth the shared backbone link grants to each individual download session.

**Why are we starting here?** The central link is a shared resource. We cannot analyze any client's individual path until we know the maximum bandwidth the backbone provides to that specific flow.

**How do we do it?** 1. Identify the total backbone capacity:
   $$R_{\text{backbone}} = 24\text{ Mbps}$$
2. Identify the number of concurrent, active sessions ($N$):
   $$N = 3 \quad (\text{Session 1, Session 2, Session 3})$$
3. Under ideal TCP max-min fairness / equal queuing, the capacity is divided equally:
   $$R_{\text{shared\_slice}} = \frac{R_{\text{backbone}}}{N} = \frac{24\text{ Mbps}}{3} = \mathbf{8\text{ Mbps per session}}$$

**Where did this concept come from?** TCP's Additive Increase Multiplicative Decrease (AIMD) congestion control algorithm. When multiple TCP connections share a congested bottleneck link, each connection detects packet loss when the buffer overflows and reduces its transmission window. Over time, the flows converge toward equal shares of the bottleneck link's bandwidth.

**System State:**
- Every session is granted at most $8\text{ Mbps}$ across the backbone link ($R_A \to R_B$).
</div>

<div class="step-card">
<div class="step-badge">Step 2: Trace Path & Throughput for Client 1</div>

**What changed from Step 1?** We now have the effective capacity of the middle hop ($8\text{ Mbps}$). We inspect all three hops along Client 1's path.

**What are we doing?** Determine the bottleneck and end-to-end throughput $T_1$ for Client 1.

**How do we do it?** 1. List the transmission capacities of the three hops that Client 1's traffic must cross:
   - Hop 1 (Server 1 Access Link): $R_{S1} = 100\text{ Mbps}$
   - Hop 2 (Backbone Slice): $R_{\text{shared\_slice}} = 8\text{ Mbps}$
   - Hop 3 (Client 1 Access Link): $R_{C1} = 15\text{ Mbps}$
2. Find the minimum link capacity along this path:
   $$T_1 = \min(R_{S1}, R_{\text{shared\_slice}}, R_{C1})$$
   $$T_1 = \min(100\text{ Mbps}, 8\text{ Mbps}, 15\text{ Mbps}) = \mathbf{8\text{ Mbps}}$$

**Where is the bottleneck for Client 1?**
The bottleneck is the **Shared Backbone Link** ($8\text{ Mbps}$). Even though Client 1 pays for a $15\text{ Mbps}$ connection, they can only achieve $8\text{ Mbps}$ because the core network is congested.

**System State:**
- Client 1 Throughput: $T_1 = 8\text{ Mbps}$
- Client 1 Bottleneck: Shared Backbone
</div>

<div class="step-card">
<div class="step-badge">Step 3: Trace Path & Throughput for Client 2</div>

**What changed from Step 2?** We move to the second client, whose local access link has different physical characteristics.

**What are we doing?** Determine the bottleneck and end-to-end throughput $T_2$ for Client 2.

**How do we do it?** 1. List the transmission capacities along Client 2's path:
   - Hop 1 (Server 2 Access Link): $R_{S2} = 100\text{ Mbps}$
   - Hop 2 (Backbone Slice): $R_{\text{shared\_slice}} = 8\text{ Mbps}$
   - Hop 3 (Client 2 Access Link): $R_{C2} = 5\text{ Mbps}$
2. Find the minimum link capacity along this path:
   $$T_2 = \min(R_{S2}, R_{\text{shared\_slice}}, R_{C2})$$
   $$T_2 = \min(100\text{ Mbps}, 8\text{ Mbps}, 5\text{ Mbps}) = \mathbf{5\text{ Mbps}}$$

**Where is the bottleneck for Client 2?**
The bottleneck is **Client 2's own local Access Link (the "Last Mile")**!
- Even though the backbone gave Client 2 enough room to transmit at $8\text{ Mbps}$, Client 2's own cable/DSL line can only physically push $5\text{ Mbps}$.
- Therefore, Client 2's speed drops to $5\text{ Mbps}$.

**System State:**
- Client 2 Throughput: $T_2 = 5\text{ Mbps}$
- Client 2 Bottleneck: Client Access Link ($R_{C2}$)
</div>

<div class="step-card">
<div class="step-badge">Step 4: Trace Path & Throughput for Client 3</div>

**What changed from Step 3?** We evaluate the final client in the network topology.

**What are we doing?** Determine the bottleneck and end-to-end throughput $T_3$ for Client 3.

**How do we do it?** 1. List the transmission capacities along Client 3's path:
   - Hop 1 (Server 3 Access Link): $R_{S3} = 100\text{ Mbps}$
   - Hop 2 (Backbone Slice): $R_{\text{shared\_slice}} = 8\text{ Mbps}$
   - Hop 3 (Client 3 Access Link): $R_{C3} = 20\text{ Mbps}$
2. Find the minimum link capacity along this path:
   $$T_3 = \min(R_{S3}, R_{\text{shared\_slice}}, R_{C3})$$
   $$T_3 = \min(100\text{ Mbps}, 8\text{ Mbps}, 20\text{ Mbps}) = \mathbf{8\text{ Mbps}}$$

**Where is the bottleneck for Client 3?**
The bottleneck is the **Shared Backbone Link** ($8\text{ Mbps}$). Client 3's fast $20\text{ Mbps}$ link is held back by the shared core.

**System State:**
- Client 3 Throughput: $T_3 = 8\text{ Mbps}$
- Client 3 Bottleneck: Shared Backbone
</div>

<div class="step-card">
<div class="step-badge">Final Step: Summary & Key Takeaways</div>

**What are the final throughput results?**
| Session | Server Link | Backbone Allocation | Client Access Link | Bottleneck Location | Final Throughput ($T$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Client 1** | $100\text{ Mbps}$ | $8\text{ Mbps}$ | $15\text{ Mbps}$ | Shared Backbone | **$8\text{ Mbps}$** |
| **Client 2** | $100\text{ Mbps}$ | $8\text{ Mbps}$ | $5\text{ Mbps}$ | Client Access Link | **$5\text{ Mbps}$** |
| **Client 3** | $100\text{ Mbps}$ | $8\text{ Mbps}$ | $20\text{ Mbps}$ | Shared Backbone | **$8\text{ Mbps}$** |

**Why does this answer make sense?**
1. **The Server Links Are Never the Problem:** All three servers sit on $100\text{ Mbps}$ data center links. Since $100\text{ Mbps}$ is far higher than any other link on the path, the server access links are never the bottleneck.
2. **Different Flows, Different Bottlenecks:** Two users sharing the exact same backbone can experience bottlenecks in completely different places:
   - For **Client 1** and **Client 3**, the shared network core is the bottleneck. Upgrading their home internet plans would not make their downloads any faster because the backbone is saturated!
   - For **Client 2**, their own home internet is the bottleneck. The backbone has room to spare ($8\text{ Mbps}$ allocated vs. $5\text{ Mbps}$ used), but Client 2's hardware cannot handle it. Upgrading Client 2's local connection from $5\text{ Mbps}$ to $8\text{ Mbps}$ would directly improve their download speed!
</div>

</div>
