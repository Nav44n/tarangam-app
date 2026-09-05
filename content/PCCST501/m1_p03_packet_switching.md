# Progressive Problems: Packet Switching vs. Circuit Switching Performance

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Level 1: Circuit Switching Capacity & Resource Reservation

### Problem 1.1: Calculating the Hard User Limit on a 1 Mbps Link

A telecommunications company operates a dedicated physical trunk line with a total capacity (transmission rate) of:
$$C = 1\text{ Mbps}$$

The company uses **Circuit Switching** (such as Frequency-Division Multiplexing or Time-Division Multiplexing) to support telephone calls.  
Whenever an individual user places a call, the network reserves a constant, guaranteed bit rate of:
$$r = 100\text{ kbps}$$
exclusively for that user for the entire duration of the call.

You must:
1. Convert both values into the same fundamental base units (bits per second).
2. Calculate the exact maximum number of simultaneous users ($N_{\text{circuit}}$) the link can support.
3. Trace what happens if an $(N_{\text{circuit}} + 1)^{\text{th}}$ user attempts to place a call while the system is full.
4. Analyze what happens to the reserved link capacity when an active caller pauses to listen or is silent.

::: callout-intuition Core Mental Model
Imagine a restaurant that has a dining room with **10 private booths**:
- Under a **Circuit Switching (Reservation)** policy, when you reserve a booth, it belongs *exclusively to you* from 6:00 PM to 8:00 PM.
- Even if you step outside to take a phone call for 45 minutes and your table sits completely empty, nobody else is allowed to sit there. The chair is locked to your name.
- If an 11th customer walks in asking for a table while all 10 booths are reserved, the host turns them away with a **busy signal**, even if 5 of the reserved tables are currently sitting empty with no one eating!
- Circuit switching gives every customer a 100% guaranteed private experience, but it wastes an enormous amount of empty space when people aren't actively using their slots.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Unit Conversion of Link Capacity (Mbps to bps)</summary>

**What are we doing?** We convert the total trunk line capacity $C = 1\text{ Mbps}$ into base units of bits per second ($\text{bps}$).

**Why are we starting here?** The link capacity is given in **Megabits per second (Mbps)**, while the individual user requirement is given in **kilobits per second (kbps)**. We cannot perform arithmetic across different metric prefixes ($1\text{ M}$ vs $100\text{ k}$) without first aligning their units.

**How do we do it?** 1. Recall the standard telecommunications definition for the metric prefix Mega ($\text{M}$):
   $$1\text{ Mbps} = 10^6\text{ bps} = 1{,}000{,}000\text{ bits per second}$$
2. Multiply:
   $$C = 1\text{ Mbps} \times \frac{1{,}000{,}000\text{ bps}}{1\text{ Mbps}} = 1{,}000{,}000\text{ bps}$$

**Where did this concept come from?** The International System of Units (SI) decimal scale used in data communications:
$$\text{Base} \xrightarrow{\times 10^3} \text{kilo (k)} \xrightarrow{\times 10^3} \text{Mega (M)} \xrightarrow{\times 10^3} \text{Giga (G)}$$

**System State:**
- Total Capacity: $C = 1{,}000{,}000\text{ bps}$
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Unit Conversion of User Demand (kbps to bps)</summary>

**What changed from Step 1?** Total link capacity is now in bits per second. Now we must convert the per-user requirement $r = 100\text{ kbps}$ into the same unit.

**What are we doing?** Convert $100\text{ kilobits per second}$ into bits per second ($\text{bps}$).

**How do we do it?** 1. Recall that the metric prefix kilo ($\text{k}$) equals $10^3 = 1{,}000$:
   $$1\text{ kbps} = 1{,}000\text{ bits per second}$$
2. Multiply:
   $$r = 100\text{ kbps} \times \frac{1{,}000\text{ bps}}{1\text{ kbps}} = 100{,}000\text{ bps}$$

**System State:**
- Total Link Capacity: $C = 1{,}000{,}000\text{ bps}$
- Required Rate per User: $r = 100{,}000\text{ bps}$
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Calculate the Maximum Number of Circuit Users</summary>

**What changed from Step 2?** Both $C$ and $r$ are expressed in $\text{bps}$.

**What are we doing?** We calculate how many independent, dedicated slices of $100{,}000\text{ bps}$ fit into a total link of $1{,}000{,}000\text{ bps}$.

**How do we do it?** 1. State the formula for circuit capacity:
   $$N_{\text{circuit}} = \left\lfloor \frac{C}{r} \right\rfloor$$
2. Substitute the values:
   $$N_{\text{circuit}} = \frac{1{,}000{,}000\text{ bps}}{100{,}000\text{ bps}}$$
3. Cancel the zeros (divide both numerator and denominator by $100{,}000$):
   $$N_{\text{circuit}} = \frac{10}{1} = \mathbf{10\text{ simultaneous users}}$$

**Where did this concept come from?** The fundamental definition of **Circuit Switching**: resources (frequencies in FDM, or periodic time slots in TDM) are carved into fixed physical slices and reserved for the entire lifetime of the call.

**System State:**
- The link is divided into exactly $10$ dedicated circuits (slots $1$ through $10$).
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Trace Call Attempt by an 11th User (Blocking/Call Dropping)</summary>

**What changed from Step 3?** All $10$ slots are currently allocated to Users $1$ through $10$. An 11th user now dials a number.

**What are we doing?** We determine what action the circuit switch takes when an 11th user requests a connection.

**How do we do it?** 1. Inspect available unreserved capacity:
   $$\text{Remaining Capacity} = C - (10 \times r) = 1{,}000{,}000 - 1{,}000{,}000 = \mathbf{0\text{ bps}}$$
2. Check admission condition:
   Is $\text{Remaining Capacity} \ge 100{,}000\text{ bps}$?  
   $0 \ge 100{,}000$ is **False**.
3. **Outcome:** The network **blocks** the 11th user. The user receives a busy signal or a "network busy" tone.
4. **Why?** A circuit-switched network strictly refuses to degrade the quality of existing calls. It will never squeeze an 11th user in by giving everyone less bandwidth.

**System State:**
- Active Calls: $10$
- Blocked Calls: $1$
- Link Allocation: $100\%$ full
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Resource Underutilization during Silence Periods</summary>

**What are we doing?** We analyze human conversation patterns and examine what happens when active callers are not speaking.

**Why are we examining this?** Human speech and computer web browsing are naturally **bursty**: people speak for a few seconds, then pause to listen or think.

**How do we analyze it?** 1. Suppose all $10$ callers are currently in active phone calls.
2. In typical voice conversations, each person speaks roughly $50\%$ of the time (or even less when considering pauses).
3. If User 1 is listening quietly to their friend:
   - User 1's microphone produces $0\text{ bits per second}$.
   - However, their dedicated $100\text{ kbps}$ circuit slot remains locked to them.
   - That $100\text{ kbps}$ slot transmits empty dummy padding bits across the physical cable.
4. **The Inefficiency:** Even though the actual information flowing across the link might only be $200\text{ kbps}$ or $300\text{ kbps}$ in total across all callers, the remaining $700\text{ kbps}$ is **wasted**. Nobody else can use those idle frequencies or time slots.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Conclusion for Level 1</summary>

**What is the final answer?**
Under Circuit Switching, a $1\text{ Mbps}$ link can support a hard maximum of **$10$ simultaneous users**.

**Why does this answer make sense?**
Circuit switching provides a **deterministic guarantee**: once your call is accepted, your $100\text{ kbps}$ stream never stutters, never slows down, and never encounters congestion, because the pipe has been physically reserved for you. The trade-off is extreme inefficiency: idle time is wasted, and the 11th user is turned away even if the other 10 users are sitting in total silence.
</details>

</div>

---

## Level 2: Packet Switching & Statistical Multiplexing

### Problem 2.1: Supporting Multiple Users on Demand

Now consider the exact same physical link and user profile:
- Total Link Capacity: $C = 1\text{ Mbps} = 1{,}000\text{ kbps}$
- User Transmission Rate when generating data: $r = 100\text{ kbps}$

However, this network operates using **Packet Switching** (the technology of the Internet):
- Resources are **not** reserved in advance.
- When a user has data to send, their device chops the data into packets and transmits them on demand at the full link speed.
- When a user has nothing to say, they transmit **zero bits**, leaving the link completely free for anyone else.
- Empirical studies show that a typical user is active and generating data only **$10\%$ of the time** ($p = 0.10$ or $\frac{1}{10}$). For the remaining **$90\%$ of the time**, the user is silent (reading a webpage, pausing between sentences, or thinking).

You must:
1. Explain how **Statistical Multiplexing** works in simple, non-mathematical terms.
2. Demonstrate why this $1\text{ Mbps}$ link can easily support **$35$ active users** under packet switching, whereas circuit switching could only support $10$.
3. Analyze the probability of congestion: what condition must occur for the link to become overloaded, and why is that event exceptionally rare?

::: callout-intuition Core Mental Model
Imagine an office with **35 employees** sharing **1 coffee machine**:
- **Circuit Switching approach:** You assign specific time slots. You say: *"Only 10 employees are allowed to drink coffee today, and each of those 10 gets the machine reserved for 6 minutes every hour."* The other 25 employees are completely banned from having coffee! Meanwhile, during those 6 minutes, an employee is often just typing at their desk, leaving the coffee machine sitting idle and unused.
- **Packet Switching approach:** You let all **35 employees** drink coffee whenever they want!
- Why does this work without chaos? Because nobody drinks coffee all day long! A person walks up to the machine for 2 minutes to brew an espresso, and then walks back to their desk for the next 20 minutes.
- Most of the time, the machine is completely empty.
- Occasionally, two people might walk up at the exact same moment. When that happens, the second person simply waits in a short line (**the queue**) for 30 seconds.
- By sharing the machine on demand, you satisfy all 35 employees with one single machine!
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: The Activity Factor of a User</summary>

**What are we doing?** We formally define how often a user actually transmits data.

**Why are we starting here?** In packet switching, link sharing relies entirely on the fact that users do not generate continuous streams of data.

**How do we do it?** 1. Let $p$ be the fraction of time a user is active:
   $$p = 10\% = \frac{10}{100} = 0.10$$
2. Let $q$ be the fraction of time a user is completely idle:
   $$q = 1 - p = 1 - 0.10 = 0.90 = 90\%$$
3. Interpretation:
   - At any random moment you check on a specific user, there is only a **$1$ in $10$ chance** that they are pushing bits onto the network.
   - There is a **$9$ in $10$ chance** that they are doing nothing at all.

**Where did this concept come from?** Real-world computer network traffic is **bursty**: users click a link, receive a page in a burst, and then spend seconds or minutes reading it.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Compare Circuit Switching vs. Packet Switching for 35 Users</summary>

**What changed from Step 1?** We know that each user is silent $90\%$ of the time. Now suppose our customer base grows to **$35$ users**.

**What are we doing?** We compare how Circuit Switching and Packet Switching handle these $35$ users.

**Under Circuit Switching:**
- Maximum allowable users: $N_{\text{circuit}} = 10$.
- To serve $35$ users, the network would need to buy **$4$ separate $1\text{ Mbps}$ trunk lines** ($10 + 10 + 10 + 5$ slots).
- If only $1$ trunk line is available, **$25$ users are rejected immediately**.

**Under Packet Switching:**
- We allow **all $35$ users** to share the single $1\text{ Mbps}$ link.
- Let's compute the **average (expected) demand** generated by all $35$ users combined:
  $$\text{Expected Active Users at any instant} = \text{Total Users} \times p$$
  $$\text{Average Active Users} = 35 \times 0.10 = \mathbf{3.5\text{ users}}$$
- How much bandwidth do $3.5$ active users consume on average?
  $$\text{Average Bandwidth Used} = 3.5 \times 100\text{ kbps} = \mathbf{350\text{ kbps}}$$
- Compare this to the total link capacity ($1{,}000\text{ kbps}$):
  $$\text{Average Link Utilization} = \frac{350\text{ kbps}}{1{,}000\text{ kbps}} = 35\%$$

On average, the link is only **$35\%$ loaded**! The remaining $65\%$ of the link is free headroom.
</details>

<details class="step-card">
<summary class="step-badge">Step 3: What Causes Congestion in Packet Switching?</summary>

**What changed from Step 2?** We know the link is safe on average ($350\text{ kbps} \ll 1{,}000\text{ kbps}$). But what happens during rare bursts?

**What are we doing?** We identify the exact condition under which the packet-switched link becomes overloaded.

**How do we do it?** 1. Total link capacity: $C = 1{,}000\text{ kbps}$.
2. Bandwidth per active user: $r = 100\text{ kbps}$.
3. How many users can transmit simultaneously before the link reaches $100\%$ capacity?
   $$\frac{1{,}000\text{ kbps}}{100\text{ kbps}} = 10\text{ users}$$
4. **The Overload Condition:**
   - If **$10$ or fewer** users transmit at the exact same moment, the total demand is $\le 1{,}000\text{ kbps}$. The link handles all traffic with zero delay!
   - If **$11$ or more** users transmit at the exact same moment, the instantaneous demand exceeds $1{,}000\text{ kbps}$.
   - When this happens, the excess packets are placed into the router's **buffer queue**. The packets do not vanish; they just wait a few milliseconds in line until the burst subsides.

**System State:**
- No congestion if active users $\le 10$.
- Queuing begins only if active users $\ge 11$.
</details>

<details class="step-card">
<summary class="step-badge">Step 4: The Intuition of Rare Overlap (Coin-Flip Analogy)</summary>

**What are we doing?** We build an intuitive understanding of why having $11$ or more users active at the exact same instant is extraordinarily rare among $35$ people.

**Why are we using an analogy instead of complex math?** A complete binomial distribution formula $\sum_{k=11}^{35} \binom{35}{k} p^k (1-p)^{35-k}$ can obscure the fundamental intuition for a beginner.

**The 10-Sided Die Analogy:**
- Imagine each of the $35$ users has a 10-sided die.
- Once every minute, every user rolls their die:
  - If they roll a **$1$**, they generate data (a $10\%$ chance).
  - If they roll anything from **$2$ through $10$**, they remain silent (a $90\%$ chance).
- For the link to overload, **at least $11$ different people out of $35$ must simultaneously roll a $1$ on the exact same roll!**

**How likely is that?**
- Think about how hard it is to get even $3$ or $4$ people to roll a $1$ at the same time.
- Having $11$ or more people all roll a $1$ simultaneously is an extremely rare coincidence.
- In rigorous probability, this chance is roughly:
  $$P(\text{Active Users} \ge 11) \approx 0.00042 = \mathbf{0.042\%}$$
  That is less than **$1$ chance in $2{,}000$**!
- For $99.96\%$ of the time, the network runs smoothly with $10$ or fewer active users, requiring zero buffering.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Summary Comparison & Trade-Offs</summary>

**What is the final comparison?**

| Metric / Feature | Circuit Switching | Packet Switching |
| :--- | :---: | :---: |
| **Total Users Supported** | **$10$ users** (hard limit) | **$35$ users** (easily supported) |
| **Resource Reservation** | Dedicated in advance (TDM/FDM) | On-demand (No pre-reservation) |
| **Handling Inactive Periods** | Capacity wasted on empty slots | Capacity immediately freed for others |
| **Behavior Under Heavy Load** | Blocks new calls (busy signal) | Packets wait in queue (slight delay) |
| **Performance Guarantee** | Predictable, constant latency | Variable latency (jitter) under bursts |

**Why does this answer make sense?**
Packet switching wins by exploiting **Statistical Multiplexing**: because independent users rarely burst at the exact same instant, the network can safely overbook its resources, supporting more than **$3$ times as many users** on the exact same physical wire with minimal delay. This fundamental efficiency is why the entire modern Internet is built on packet switching rather than circuit switching.
</details>

</div>
