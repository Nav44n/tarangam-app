# Progressive Problems: IPv4 Subnetting, VLSM, and MTU Fragmentation

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps, no skipped bit-level arithmetic, and full line-by-line calculations.

---

## Level 1: Variable Length Subnet Masking (VLSM) Address Planning

### Problem 1.1: Optimal Subnet Allocation for Heterogeneous Networks

**Problem Statement:** You are a network administrator assigned the private base network address block `192.168.1.0/24`.  
You must partition this single address block into subnets to satisfy the host requirements of four distinct departments without wasting address space:
- **Department A:** Needs $100\text{ usable host IP addresses}$.
- **Department B:** Needs $50\text{ usable host IP addresses}$.
- **Department C:** Needs $25\text{ usable host IP addresses}$.
- **Router Link (WAN Link):** Needs $2\text{ usable host IP addresses}$ (point-to-point router connection).

For every department:
1. Sort the requirements using the mandatory VLSM ordering rule.
2. Determine the minimum number of host bits ($h$) required using the formula $2^h - 2 \ge \text{hosts}$.
3. Calculate the allocated block size ($2^h$), the new prefix length ($/x = 32 - h$), and the Subnet Mask in dotted-decimal format.
4. Calculate the **Network Address (Network ID)**, **First Usable Host IP**, **Last Usable Host IP**, and **Broadcast Address**.
5. Verify that no address ranges overlap and determine the total number of unused IP addresses remaining in the original `/24` block.

::: callout-intuition Core Mental Model
Imagine you have a single raw loaf of bread that contains exactly $256$ slices of bread (representing the 256 numerical addresses in a `/24` block).  
You have to feed four different families of different sizes: a huge family (100 people), a medium family (50 people), a small family (25 people), and a pair of twins (2 people).  
- **Rule of Cutting:** Binary powers dictate that you can only cut this loaf into pieces whose sizes are powers of two ($2, 4, 8, 16, 32, 64, 128, 256$).  
- **The Golden Rule of Slicing (Largest First):** If you give a small 4-slice piece to the twins from the middle of the loaf first, you fragment the loaf and you won't have a contiguous chunk of $128$ slices left for the huge family! You **must** cut the biggest chunk first from the left edge, then cut the next biggest chunk from what remains, working down to the smallest.
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Understand the Base Block Structure (192.168.1.0/24)</summary>

**What are we doing?** Analyzing the starting address space and determining the total number of raw IP addresses available.

**Why are we starting here?** Before dividing any resource, we must know our total budget of addresses and what the CIDR prefix notation (`/24`) physically means.

**How do we do it?** An IPv4 address is composed of exactly $32\text{ binary bits}$, broken into four groups of $8\text{ bits}$ called **octets** ($4 \times 8 = 32\text{ bits}$).  
The slash notation `/24` (called CIDR prefix length) means that the first $24\text{ bits}$ are permanently frozen as the **Network Portion** (identifying the street), leaving the remaining bits as the **Host Portion** (identifying house numbers on that street).  

$$\text{Total bits in IPv4} = 32$$  
$$\text{Network bits } (n) = 24$$  
$$\text{Host bits remaining } (h) = 32 - n = 32 - 24 = 8\text{ bits}$$  

Now calculate total available addresses in this block:  
$$\text{Total IP Addresses} = 2^h = 2^8 = 256\text{ addresses}$$  
These $256$ addresses span consecutively from:  
`192.168.1.0` through `192.168.1.255`.

**Where did this formula/concept come from?** RFC 791 (IPv4 standard) and RFC 1519 (Classless Inter-Domain Routing - CIDR). Each bit can be either `0` or `1`, so $h$ binary bits yield $2^h$ unique combinations.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Understand the -2 Subtraction Rule in $2^h - 2 \ge \text{Hosts}$</summary>

**What changed from Step 1?** We know each subnet gets a block of size $2^h$. Now we explain why usable devices cannot use all $2^h$ addresses.

**What are we doing?** Explaining why $2$ addresses are automatically reserved and unusable for assignable host network cards (NICs).

**Why are we doing this?** If a department needs $30$ hosts, and you provide a block of $32$ addresses, a beginner might wonder why only $30$ computers can be plugged in.

**How do we do it?** In every IPv4 subnet:
1. **The First Address (All Host Bits Set to 0):** This is the **Network Address** (or Network ID). It is the official name of the entire subnet itself used by routers to populate routing tables. No individual computer is allowed to use it.
2. **The Last Address (All Host Bits Set to 1):** This is the **Directed Broadcast Address**. Any packet sent to this IP address is automatically copied and delivered to every single device inside that subnet. No single computer can claim it as its personal identity.

$$\text{Usable Hosts} = \text{Total Addresses in Block} - 2 = 2^h - 2$$  
Therefore, for any host requirement, we must satisfy:  
$$2^h - 2 \ge \text{Number of Required Hosts}$$

**Where did this formula/concept come from?** RFC 950 ("Internet Standard Subnetting Procedure").
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Sort the Subnet Requirements from Largest to Smallest</summary>

**What changed from Step 2?** We understand the math constraint. Now we arrange our departmental needs into the mandatory execution sequence.

**What are we doing?** Ordering the four departments in strictly descending order of host count:

1. **Department A:** $100\text{ hosts}$
2. **Department B:** $50\text{ hosts}$
3. **Department C:** $25\text{ hosts}$
4. **Router Link:** $2\text{ hosts}$

**Why are we doing this?** This is the fundamental rule of Variable Length Subnet Masking (VLSM). If you allocate small subnets first, you will place them at arbitrary low address boundaries, splitting the remaining address space into small fragments. Large subnets require boundaries that are multiples of large powers of 2 (e.g., multiples of 128 or 64). Sorting largest-to-smallest guarantees that address boundaries align naturally without overlaps or wasted space.

**How do we do it?** The requirements are already sorted:  
$$100 > 50 > 25 > 2$$
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Design Subnet 1 — Department A (100 Hosts)</summary>

**What changed from Step 3?** We take the first and largest requirement ($100\text{ hosts}$) and allocate its subnet block from the very start of our address space (`192.168.1.0`).

**What are we doing?** Calculating $h$, block size, subnet mask, prefix, and the exact address range for Department A.

**How do we do it?** 1. **Find host bits $h$:** We must solve $2^h - 2 \ge 100$:  
   - If $h = 6 \implies 2^6 - 2 = 64 - 2 = 62\text{ hosts}$ (Too small! $62 < 100$).  
   - If $h = 7 \implies 2^7 - 2 = 128 - 2 = 126\text{ hosts}$ (Satisfies $126 \ge 100$).  
   Therefore, we must allocate **$h = 7\text{ host bits}$**.

2. **Calculate Block Size:** $$\text{Block Size} = 2^h = 2^7 = 128\text{ total addresses}$$

3. **Calculate New Prefix Length ($/x$):** $$x = 32 - h = 32 - 7 = /25$$

4. **Convert $/25$ to Dotted-Decimal Subnet Mask:** $25$ ones followed by $7$ zeros:  
   `11111111 . 11111111 . 11111111 . 10000000`  
   - Octet 1: $11111111_2 = 255$  
   - Octet 2: $11111111_2 = 255$  
   - Octet 3: $11111111_2 = 255$  
   - Octet 4: $10000000_2 = 128$  
   $$\text{Subnet Mask} = 255.255.255.128$$

5. **Determine Address Boundaries (Starting at 192.168.1.0):**
   - **Network Address:** `192.168.1.0`  
   - **First Usable Host IP:** `192.168.1.0 + 1` = `192.168.1.1`  
   - **Block ends at:** $0 + 128 - 1 = 127$  
   - **Broadcast Address:** `192.168.1.127`  
   - **Last Usable Host IP:** `192.168.1.127 - 1` = `192.168.1.126`  

*Department A Usable Range:* `192.168.1.1` to `192.168.1.126` (Capacity: $126$ hosts).
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Design Subnet 2 — Department B (50 Hosts)</summary>

**What changed from Step 4?** Department A consumed addresses `0` through `127`. The very next available unallocated address in our pool is `192.168.1.128`. We now allocate space for Department B ($50\text{ hosts}$).

**What are we doing?** Calculating $h$, block size, subnet mask, prefix, and the address range for Department B starting at `192.168.1.128`.

**How do we do it?** 1. **Find host bits $h$:** We must solve $2^h - 2 \ge 50$:  
   - If $h = 5 \implies 2^5 - 2 = 32 - 2 = 30\text{ hosts}$ (Too small! $30 < 50$).  
   - If $h = 6 \implies 2^6 - 2 = 64 - 2 = 62\text{ hosts}$ (Satisfies $62 \ge 50$).  
   Therefore, we must allocate **$h = 6\text{ host bits}$**.

2. **Calculate Block Size:** $$\text{Block Size} = 2^h = 2^6 = 64\text{ total addresses}$$

3. **Calculate New Prefix Length ($/x$):** $$x = 32 - h = 32 - 6 = /26$$

4. **Convert $/26$ to Dotted-Decimal Subnet Mask:** $26$ ones followed by $6$ zeros:  
   `11111111 . 11111111 . 11111111 . 11000000`  
   - Octet 4: $128 + 64 = 192$  
   $$\text{Subnet Mask} = 255.255.255.192$$

5. **Determine Address Boundaries (Starting at 192.168.1.128):**
   - **Network Address:** `192.168.1.128`  
   - **First Usable Host IP:** `192.168.1.128 + 1` = `192.168.1.129`  
   - **Block ends at:** $128 + 64 - 1 = 191$  
   - **Broadcast Address:** `192.168.1.191`  
   - **Last Usable Host IP:** `192.168.1.191 - 1` = `192.168.1.190`  

*Department B Usable Range:* `192.168.1.129` to `192.168.1.190` (Capacity: $62$ hosts).
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Design Subnet 3 — Department C (25 Hosts)</summary>

**What changed from Step 5?** Department B consumed addresses `128` through `191`. The next free address in line is `192.168.1.192`. We allocate space for Department C ($25\text{ hosts}$).

**What are we doing?** Calculating $h$, block size, subnet mask, prefix, and the address range for Department C starting at `192.168.1.192`.

**How do we do it?** 1. **Find host bits $h$:** We must solve $2^h - 2 \ge 25$:  
   - If $h = 4 \implies 2^4 - 2 = 16 - 2 = 14\text{ hosts}$ (Too small! $14 < 25$).  
   - If $h = 5 \implies 2^5 - 2 = 32 - 2 = 30\text{ hosts}$ (Satisfies $30 \ge 25$).  
   Therefore, we must allocate **$h = 5\text{ host bits}$**.

2. **Calculate Block Size:** $$\text{Block Size} = 2^h = 2^5 = 32\text{ total addresses}$$

3. **Calculate New Prefix Length ($/x$):** $$x = 32 - h = 32 - 5 = /27$$

4. **Convert $/27$ to Dotted-Decimal Subnet Mask:** $27$ ones followed by $5$ zeros:  
   `11111111 . 11111111 . 11111111 . 11100000`  
   - Octet 4: $128 + 64 + 32 = 224$  
   $$\text{Subnet Mask} = 255.255.255.224$$

5. **Determine Address Boundaries (Starting at 192.168.1.192):**
   - **Network Address:** `192.168.1.192`  
   - **First Usable Host IP:** `192.168.1.192 + 1` = `192.168.1.193`  
   - **Block ends at:** $192 + 32 - 1 = 223$  
   - **Broadcast Address:** `192.168.1.223`  
   - **Last Usable Host IP:** `192.168.1.223 - 1` = `192.168.1.222`  

*Department C Usable Range:* `192.168.1.193` to `192.168.1.222` (Capacity: $30$ hosts).
</details>

<details class="step-card">
<summary class="step-badge">Step 7: Design Subnet 4 — Router-to-Router Point-to-Point Link (2 Hosts)</summary>

**What changed from Step 6?** Department C consumed addresses up to `223`. The next free address is `192.168.1.224`. We now allocate space for the point-to-point link between two router interfaces ($2\text{ hosts}$).

**What are we doing?** Calculating $h$, block size, subnet mask, prefix, and the address range for the WAN link starting at `192.168.1.224`.

**How do we do it?** 1. **Find host bits $h$:** We must solve $2^h - 2 \ge 2$:  
   - If $h = 2 \implies 2^2 - 2 = 4 - 2 = 2\text{ hosts}$ (Exact match: $2 \ge 2$).  
   Therefore, we allocate **$h = 2\text{ host bits}$**.

2. **Calculate Block Size:** $$\text{Block Size} = 2^h = 2^2 = 4\text{ total addresses}$$

3. **Calculate New Prefix Length ($/x$):** $$x = 32 - h = 32 - 2 = /30$$

4. **Convert $/30$ to Dotted-Decimal Subnet Mask:** $30$ ones followed by $2$ zeros:  
   `11111111 . 11111111 . 11111111 . 11111100`  
   - Octet 4: $128 + 64 + 32 + 16 + 8 + 4 = 252$  
   $$\text{Subnet Mask} = 255.255.255.252$$

5. **Determine Address Boundaries (Starting at 192.168.1.224):**
   - **Network Address:** `192.168.1.224`  
   - **First Usable Host IP (Router Interface 1):** `192.168.1.225`  
   - **Block ends at:** $224 + 4 - 1 = 227$  
   - **Last Usable Host IP (Router Interface 2):** `192.168.1.226`  
   - **Broadcast Address:** `192.168.1.227`  

*Router Link Usable Range:* `192.168.1.225` to `192.168.1.226` (Capacity: exactly $2$ hosts).
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Complete VLSM Master Table and Free Space Analysis</summary>

**What is the final answer?** Here is the complete, non-overlapping VLSM allocation table:

| Subnet Identifier | Needed | Allocated Size | Prefix & Subnet Mask | Network ID | First Usable IP | Last Usable IP | Broadcast IP |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dept A** | $100$ | $128$ | `/25` (`255.255.255.128`) | `192.168.1.0` | `192.168.1.1` | `192.168.1.126` | `192.168.1.127` |
| **Dept B** | $50$ | $64$ | `/26` (`255.255.255.192`) | `192.168.1.128` | `192.168.1.129` | `192.168.1.190` | `192.168.1.191` |
| **Dept C** | $25$ | $32$ | `/27` (`255.255.255.224`) | `192.168.1.192` | `192.168.1.193` | `192.168.1.222` | `192.168.1.223` |
| **WAN Link** | $2$ | $4$ | `/30` (`255.255.255.252`) | `192.168.1.224` | `192.168.1.225` | `192.168.1.226` | `192.168.1.227` |

**Unallocated Space Remaining:**
- Total addresses allocated = $128 + 64 + 32 + 4 = 228\text{ addresses}$.  
- Total addresses originally available in `/24` = $256\text{ addresses}$.  
- Unused addresses = $256 - 228 = 28\text{ addresses}$ (spanning `192.168.1.228` through `192.168.1.255`), available for future expansion!

**Why does this answer make sense?** Look at the network boundaries: `127` leads seamlessly to `128`; `191` leads seamlessly to `192`; `223` leads seamlessly to `224`; and `227` marks the boundary of the link. Zero addresses overlap, zero addresses are skipped, and every single department's host requirement is completely satisfied.
</details>

</div>

---

## Level 2: IPv4 Datagram Fragmentation Across an MTU Boundary

### Problem 2.1: Fragmenting a 4,000-byte IPv4 Datagram Across an MTU = 1,500 Link

**Problem Statement:** A host computer generates an IPv4 datagram with a **Total Length of $4{,}000\text{ bytes}$**.  
The IP header contains no optional fields, meaning it has a standard base **Header Length of $20\text{ bytes}$**.  
This datagram arrives at an outgoing router interface that leads to an Ethernet network with a **Maximum Transmission Unit ($\text{MTU}$) of $1{,}500\text{ bytes}$**.  
Because the $4{,}000\text{ byte}$ packet is strictly larger than the $1{,}500\text{ byte}$ channel limit, the router must perform **IPv4 Fragmentation**.

1. Calculate the total raw data payload inside the original datagram.
2. Explain why the data payload carried inside every intermediate fragment must be an exact multiple of $8\text{ bytes}$, and determine the maximum allowable data payload per fragment ($P_{\text{max}}$).
3. Calculate the total number of fragments generated.
4. For every generated fragment, explicitly calculate:
   - Header Length (bytes)
   - Data Payload Length (bytes)
   - Total Length field (bytes)
   - More Fragments ($\text{MF}$) flag ($0$ or $1$)
   - Fragment Offset field (both in raw byte offset and in the 8-byte scaled units placed into the IP header).

::: callout-intuition Core Mental Model
Imagine you need to move a giant $4{,}000\text{-page}$ paper report across town, but you only have delivery boxes that can hold at most $1{,}500$ sheets of paper (this is your $\text{MTU}$).  
- **The Box Label (The 20-byte Header):** Every single box must have a shipping invoice taped to the outside that takes up the equivalent of $20$ pages of space. That means inside each box, you only have room for $1{,}500 - 20 = 1{,}480$ pages of actual report!  
- **The Index Card (Fragment Offset):** When the recipient gets the boxes out of order, how do they know which page goes where? Each box has an index number stamped on it: *"This box starts at page number X."*
- **The 8-Byte Scale Factor:** The index number field in the shipping box is so small that the post office rules state: *"You cannot write raw page numbers. You must divide the starting page number by 8 before writing it on the box!"*
:::

<div class="stepped-container">

<details class="step-card">
<summary class="step-badge">Step 1: Calculate the Original Data Payload Size</summary>

**What are we doing?** Separating the original datagram into its two fundamental components: the **IP Header** and the **Data Payload**.

**Why are we starting here?** When a router fragments a packet, it does *not* replicate the original data payload blindly. It slices only the *payload*, and prepends a brand-new IP header to each slice so each fragment can navigate the internet independently.

**How do we do it?** In the IPv4 packet format:  
$$\text{Total Length} = \text{Header Length} + \text{Data Payload}$$  
We are given:  
$$\text{Total Length} = 4{,}000\text{ bytes}$$  
$$\text{Header Length} = 20\text{ bytes}$$  
Subtract header from total length:  
$$\text{Original Data Payload} = 4{,}000\text{ bytes} - 20\text{ bytes} = 3{,}980\text{ bytes}$$

**Where did this formula/concept come from?** RFC 791 ("Internet Protocol"). The Total Length field in the IPv4 header measures the complete datagram size in bytes, including both header and data.
</details>

<details class="step-card">
<summary class="step-badge">Step 2: Understand the 8-Byte Alignment Rule for Fragment Offsets</summary>

**What changed from Step 1?** We know we have $3{,}980\text{ bytes}$ of data to transport across an interface with $\text{MTU} = 1{,}500\text{ bytes}$. Now we derive the mathematical constraint on fragment payload sizing.

**What are we doing?** Proving why the maximum payload of an intermediate fragment cannot simply be $1{,}500 - 20 = 1{,}480\text{ bytes}$ by chance, but **must strictly be a multiple of 8**.

**Why are we doing this?** In the IPv4 header, the **Fragment Offset** field is exactly **$13\text{ bits}$ wide**.  
If the Fragment Offset measured single bytes, a $13\text{-bit}$ number could only count up to:  
$$2^{13} - 1 = 8{,}191\text{ bytes}$$  
However, the maximum possible size of an entire IPv4 datagram is $65{,}535\text{ bytes}$!  
To allow a $13\text{-bit}$ field to point anywhere inside a $65{,}535\text{-byte}$ packet, the designers of IPv4 specified that the Fragment Offset measures data in **units of 8-byte blocks** ($8\text{ octets}$):  
$$\text{Value Written in Offset Field} = \frac{\text{Byte Offset}}{8}$$  
Therefore, every fragment (except the very last one) **must carry a payload length that is evenly divisible by 8**. If it weren't, the starting byte offset of the next fragment would produce a fraction, which cannot be represented as an integer in the 13-bit header field!

**Where did this formula/concept come from?** RFC 791 Section 3.2 ("Fragmentation and Reassembly").
</details>

<details class="step-card">
<summary class="step-badge">Step 3: Calculate the Maximum Data Payload per Fragment ($P_{\text{max}}$)</summary>

**What changed from Step 2?** We know the formula and the 8-byte divisibility constraint. Now we calculate the maximum payload that fits within our $\text{MTU} = 1{,}500\text{ bytes}$.

**What are we doing?** Calculating $P_{\text{max}}$.

**How do we do it?** 1. Maximum total fragment size cannot exceed the MTU:  
   $$\text{Max Total Size} \le 1{,}500\text{ bytes}$$  
2. Every fragment needs its own $20\text{-byte}$ IPv4 header:  
   $$\text{Max Raw Space for Payload} = \text{MTU} - \text{Header Length} = 1{,}500 - 20 = 1{,}480\text{ bytes}$$  
3. Check if $1{,}480$ is divisible by 8:  
   $$\frac{1{,}480}{8} = 185\text{ (Exact whole integer with remainder } 0\text{)}$$  
Because $1{,}480$ is an exact multiple of 8, the maximum payload per fragment is:  
$$P_{\text{max}} = 1{,}480\text{ bytes}$$

*(Instructor Note: If the MTU were $1{,}505\text{ bytes}$, the raw space would be $1{,}485$. We would compute $\lfloor 1{,}485 / 8 \rfloor \times 8 = 185 \times 8 = 1{,}480\text{ bytes}$. The remaining $5\text{ bytes}$ would be left empty to satisfy the 8-byte rule).*
</details>

<details class="step-card">
<summary class="step-badge">Step 4: Determine the Total Number of Fragments</summary>

**What changed from Step 3?** We know we must transport $3{,}980\text{ bytes}$ of payload, and each fragment can hold at most $1{,}480\text{ bytes}$. Now we find how many fragments are needed.

**What are we doing?** Calculating the number of fragments $k$.

**How do we do it?** Divide total payload by $P_{\text{max}}$ and round up using the ceiling function $\lceil \dots \rceil$:  
$$k = \left\lceil \frac{\text{Total Payload}}{P_{\text{max}}} \right\rceil = \left\lceil \frac{3{,}980}{1{,}480} \right\rceil$$  
Let us divide step-by-step:  
$$3{,}980 / 1{,}480 = 2.689189\dots$$  
$$\lceil 2.689189 \rceil = 3\text{ fragments}$$  

Let us see how the $3{,}980\text{ bytes}$ are divided across these 3 fragments:
- **Fragment 1 Payload:** Takes the full capacity = $1{,}480\text{ bytes}$
- **Fragment 2 Payload:** Takes the full capacity = $1{,}480\text{ bytes}$  
- **Cumulative payload so far:** $1{,}480 + 1{,}480 = 2{,}960\text{ bytes}$  
- **Fragment 3 Payload (The Remainder):**
  $$\text{Remaining Data} = 3{,}980 - 2{,}960 = 1{,}020\text{ bytes}$$  
*(Note: The last fragment is allowed to have a payload that is NOT a multiple of 8, because no subsequent fragment follows it).*
</details>

<details class="step-card">
<summary class="step-badge">Step 5: Trace Fragment 1 (First Slice)</summary>

**What changed from Step 4?** We know the payload sizes: $1{,}480$, $1{,}480$, and $1{,}020\text{ bytes}$. Now we compute the exact header fields for Fragment 1.

**What are we doing?** Computing the Data Range, Total Length, More Fragments ($\text{MF}$) flag, and Fragment Offset for Fragment 1.

**How do we do it?** 1. **Data Range:** This fragment carries the very beginning of the original data stream:  
   $$\text{Bytes } 0 \text{ through } 1{,}479 \quad (\text{Total: } 1{,}480\text{ bytes})$$  
2. **Total Length Field:** $$\text{Total Length} = \text{Header Length} + \text{Payload} = 20\text{ bytes} + 1{,}480\text{ bytes} = 1{,}500\text{ bytes}$$  
   *(Notice this perfectly matches the link MTU of $1{,}500$)*.  
3. **More Fragments (MF) Flag:** Are there more fragments coming after this one? **Yes.** $$\text{MF} = 1$$  
4. **Fragment Offset Field:** The starting byte for this fragment is Byte $0$.  
   $$\text{Offset in Header} = \frac{\text{Starting Byte}}{8} = \frac{0}{8} = 0$$
</details>

<details class="step-card">
<summary class="step-badge">Step 6: Trace Fragment 2 (Middle Slice)</summary>

**What changed from Step 5?** Fragment 1 covered bytes $0$ to $1{,}479$. Fragment 2 picks up immediately where Fragment 1 left off.

**What are we doing?** Computing the Data Range, Total Length, More Fragments ($\text{MF}$) flag, and Fragment Offset for Fragment 2.

**How do we do it?** 1. **Data Range:** Starts at Byte $1{,}480$ and carries $1{,}480\text{ bytes}$:  
   $$\text{Ending Byte} = 1{,}480 + 1{,}480 - 1 = 2{,}959$$  
   $$\text{Bytes } 1{,}480 \text{ through } 2{,}959 \quad (\text{Total: } 1{,}480\text{ bytes})$$  
2. **Total Length Field:** $$\text{Total Length} = 20\text{ bytes} + 1{,}480\text{ bytes} = 1{,}500\text{ bytes}$$  
3. **More Fragments (MF) Flag:** Are there more fragments coming after this one? **Yes** (Fragment 3 is still to come).  
   $$\text{MF} = 1$$  
4. **Fragment Offset Field:** The starting byte for this fragment is Byte $1{,}480$.  
   $$\text{Offset in Header} = \frac{\text{Starting Byte}}{8} = \frac{1{,}480}{8} = 185$$  
   The value written into the $13\text{-bit}$ header offset field is **$185$**.
</details>

<details class="step-card">
<summary class="step-badge">Step 7: Trace Fragment 3 (Final Slice / Tail)</summary>

**What changed from Step 6?** Fragment 2 covered bytes up to $2{,}959$. Fragment 3 carries the final remaining bytes.

**What are we doing?** Computing the Data Range, Total Length, More Fragments ($\text{MF}$) flag, and Fragment Offset for Fragment 3.

**How do we do it?** 1. **Data Range:** Starts at Byte $2{,}960$ and carries the remaining $1{,}020\text{ bytes}$:  
   $$\text{Ending Byte} = 2{,}960 + 1{,}020 - 1 = 3{,}979$$  
   $$\text{Bytes } 2{,}960 \text{ through } 3{,}979 \quad (\text{Total: } 1{,}020\text{ bytes})$$  
2. **Total Length Field:** $$\text{Total Length} = \text{Header Length} + \text{Payload} = 20\text{ bytes} + 1{,}020\text{ bytes} = 1{,}040\text{ bytes}$$  
   *(Notice this is well below the MTU limit of $1{,}500$)*.  
3. **More Fragments (MF) Flag:** Are there any more fragments after this? **No**, this is the last fragment.  
   $$\text{MF} = 0$$  
   *(An MF flag of 0 tells the receiving destination reassembly engine: "This is the final piece of the puzzle! Once you have all bytes up to here, assemble the packet!")*.  
4. **Fragment Offset Field:** The starting byte for this fragment is Byte $2{,}960$.  
   $$\text{Offset in Header} = \frac{\text{Starting Byte}}{8} = \frac{2{,}960}{8} = 370$$  
   The value written into the header offset field is **$370$**.
</details>

<details class="step-card">
<summary class="step-badge">Final Step: Complete Fragmentation Master Table and Reassembly Check</summary>

**What is the final answer?** Here is the complete fragmentation breakdown table:

| Fragment # | Header Length | Payload Length | Total Length | Data Byte Range | MF Flag | Offset (Header Value) | Offset (Byte Equivalent) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Fragment 1** | $20\text{ bytes}$ | $1{,}480\text{ bytes}$ | $\mathbf{1{,}500\text{ bytes}}$ | Bytes $0 - 1{,}479$ | $\mathbf{1}$ | $\mathbf{0}$ | $0 \times 8 = 0\text{ bytes}$ |
| **Fragment 2** | $20\text{ bytes}$ | $1{,}480\text{ bytes}$ | $\mathbf{1{,}500\text{ bytes}}$ | Bytes $1{,}480 - 2{,}959$ | $\mathbf{1}$ | $\mathbf{185}$ | $185 \times 8 = 1{,}480\text{ bytes}$ |
| **Fragment 3** | $20\text{ bytes}$ | $1{,}020\text{ bytes}$ | $\mathbf{1{,}040\text{ bytes}}$ | Bytes $2{,}960 - 3{,}979$ | $\mathbf{0}$ | $\mathbf{370}$ | $370 \times 8 = 2{,}960\text{ bytes}$ |

**Verification & Sanity Check:**
1. **Payload Sum:** $1{,}480 + 1{,}480 + 1{,}020 = 3{,}980\text{ bytes of data}$. This matches the original datagram payload ($4{,}000 - 20 = 3{,}980\text{ bytes}$) with $0$ bytes lost.
2. **Reassembly Continuity:**
   - Fragment 1 covers: $0 \to 1{,}479$  
   - Fragment 2 begins at: $185 \times 8 = 1{,}480$ (perfect continuous boundary!)  
   - Fragment 2 covers: $1{,}480 \to 2{,}959$  
   - Fragment 3 begins at: $370 \times 8 = 2{,}960$ (perfect continuous boundary!)  
   - Fragment 3 ends at: $2{,}960 + 1{,}020 - 1 = 3{,}979$  
   - Fragment 3 has $\text{MF} = 0$, signaling the end of the stream.

**Why does this answer make sense?** The router split the oversized $4{,}000\text{-byte}$ packet into two maximal $1{,}500\text{-byte}$ packets and one final $1{,}040\text{-byte}$ tail packet. By ensuring the payloads of Fragments 1 and 2 were multiples of 8, the starting byte offsets ($0$, $185$, $370$) fit cleanly into the 13-bit header offset field without rounding errors or fractional bytes.
</details>

</div>

---

<a id="self-check"></a>
## Active Recall Checkpoint

::: quiz Q1: Subnet Host Capacity
What is the broadcast address for the subnet containing the host IP address `172.16.45.14/20`?
(A) `172.16.45.255`
(*B) `172.16.47.255`
(C) `172.16.255.255`
(D) `172.16.63.255`
::: explanation
Prefix `/20` means $20$ network bits and $12$ host bits.  
In the 3rd octet, the mask has $20 - 16 = 4$ bits: `11110000` ($240$). The block size is $256 - 240 = 16$.  
Multiples of 16 in the 3rd octet: 0, 16, 32, 48.  
The subnet spans from `172.16.32.0` to `172.16.47.255`. Thus, the broadcast address is `172.16.47.255`.
:::

::: quiz Q2: Fragment Offset Decoding
A destination host receives an IPv4 datagram fragment with Fragment Offset = 120 and Total Length = 620 bytes (including a 20-byte IP header). What byte range of the original payload does this fragment represent?
(A) Bytes 120 to 740
(*B) Bytes 960 to 1,559
(C) Bytes 960 to 1,579
(D) Bytes 15 to 75
::: explanation
Starting byte position $= \text{Offset} \times 8 = 120 \times 8 = 960$.  
The payload size is $\text{Total Length} - \text{Header} = 620 - 20 = 600\text{ bytes}$.  
Therefore, the fragment carries bytes from $960$ to $960 + 600 - 1 = 1{,}559$.
:::
