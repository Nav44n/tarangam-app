# IPv4 Addressing, Subnetting, and CIDR

**Address classes (historical), subnet masks, CIDR notation, and the complete step-by-step subnetting calculation.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
An IPv4 address, like `192.168.1.10`, is really made of two conceptual parts glued together — like a postal address that combines a **city/area code** (which post office should handle this?) and a **house number within that area** (which specific building?). The "area code" part is called the **network portion**, and the "house number" part is the **host portion**. Routers, when forwarding a packet, only ever need to look at the network portion to decide roughly which direction to send it — they don't need to know the exact final host inside a distant network, only which general direction leads toward that network, just like a national postal service only needs to route a letter to the right city's sorting office, letting that local office figure out the exact street address from there.

**Subnetting** is the deliberate act of "borrowing" some bits from the host portion and reassigning them to the network portion — effectively subdividing one large network address block into multiple smaller ones. This is enormously useful in practice: an organisation given one large address block can split it into separate subnets for different departments or buildings, improving security (isolating traffic), reducing broadcast domain size (fewer devices affected by broadcast traffic), and making more efficient use of a limited address space than handing out one giant, mostly-empty block.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Classful addressing (historical context — largely obsolete today, but foundational vocabulary):**

| Class | First bits | Range of first octet | Default network/host split |
|---|---|---|---|
| A | 0 | 1–126 | 8 bits network / 24 bits host |
| B | 10 | 128–191 | 16 bits network / 16 bits host |
| C | 110 | 192–223 | 24 bits network / 8 bits host |
| D (multicast) | 1110 | 224–239 | Not used for host addressing |

Classful addressing rigidly fixed the network/host split based purely on the address's leading bits, which wasted enormous numbers of addresses (a Class C organisation needing 300 hosts had to be given an entire Class B block of 65,534 addresses). This inefficiency directly motivated the shift to CIDR.

**CIDR (Classless Inter-Domain Routing).** Instead of fixed class boundaries, CIDR notation explicitly states how many bits belong to the network portion, written as `address/prefix-length`, e.g. `192.168.1.0/24` means "the first 24 bits are the network portion." This allows the network/host split to be placed *anywhere*, sized exactly to an organisation's actual needs — not forced into one of a few fixed class sizes.

**The subnet mask.** A 32-bit value with 1s marking the network (+ subnet) portion and 0s marking the host portion — functionally equivalent information to the CIDR prefix length, just expressed differently. `/24` corresponds to mask `255.255.255.0`; `/26` corresponds to `255.255.255.192`.

**Key subnetting formulas, given a prefix length $/n$ (network+subnet bits) out of 32 total:**
$$\text{Number of host bits} = 32 - n \qquad \text{Total addresses in subnet} = 2^{(32-n)}$$
$$\text{Usable host addresses} = 2^{(32-n)} - 2$$
(The $-2$ accounts for the **network address** — all host bits 0, reserved to identify the subnet itself — and the **broadcast address** — all host bits 1, reserved for sending to every host on that subnet — neither of which can be assigned to an individual device.)

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
You are given the block `192.168.10.0/24` and asked to subdivide it into 4 equal-sized subnets. For the resulting subnets, determine: the new prefix length, the subnet mask, and — for the **second** subnet specifically — its network address, usable host range, and broadcast address.
:::

::: step [Step 2: Execution] Applying Core Algorithm
To create exactly 4 subnets, you need to "borrow" enough host bits to represent 4 distinct subnet values: $2^k \ge 4 \Rightarrow k=2$ bits borrowed. New prefix length: $24 + 2 = /26$.
New subnet mask for `/26`: the first 26 bits are 1s. In the last (4th) octet, that's 2 bits set to 1 (since 24 bits are already used by the first 3 octets): `11000000` in binary = `192`. So the new mask is `255.255.255.192`.
Each subnet's size: $2^{(32-26)} = 2^6 = 64$ total addresses (including network and broadcast).
The four subnets, by their block boundaries (each 64 addresses wide, starting from `192.168.10.0`):
Subnet 1: `192.168.10.0` – `192.168.10.63`
Subnet 2: `192.168.10.64` – `192.168.10.127`
Subnet 3: `192.168.10.128` – `192.168.10.191`
Subnet 4: `192.168.10.192` – `192.168.10.255`
Focusing on **Subnet 2** (`192.168.10.64` – `192.168.10.127`): the **network address** (all host bits 0) is the very first address in this range, `192.168.10.64`. The **broadcast address** (all host bits 1) is the very last address in this range, `192.168.10.127`. The **usable host range** is everything strictly between these two: `192.168.10.65` to `192.168.10.126`.
:::

::: step [Step 3: Conclusion] Final Result
Subnet 2 is fully described as `192.168.10.64/26`, with network address `192.168.10.64`, usable host range `192.168.10.65`–`192.168.10.126` (that's $64-2=62$ usable addresses, matching the formula $2^{(32-26)}-2 = 64-2=62$), and broadcast address `192.168.10.127`. Any device assigned an IP in the usable range, with subnet mask `255.255.255.192`, will correctly recognise it belongs to this specific subnet and route local vs. remote traffic accordingly.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
Why does CIDR notation (e.g., `/26`) represent an improvement over the older classful (A/B/C) addressing system?
(A) CIDR eliminates the need for subnet masks entirely
(*B) CIDR allows the network/host bit boundary to be placed at any position, sized to an organisation's actual address needs, rather than being forced into one of a few rigid, wasteful class-based sizes
(C) CIDR only works with IPv6, not IPv4
(D) CIDR increases the total number of available IPv4 addresses
::: explanation
Classful addressing forced every organisation into one of a few fixed network-size categories (Class A, B, or C), often wasting huge numbers of addresses. CIDR's flexible, explicitly-stated prefix length lets network/host boundaries be placed exactly where needed, dramatically improving address utilisation efficiency.
:::

::: quiz Q2: Foundational Concept
For a subnet with prefix length `/28`, how many usable host addresses does it provide?
(A) 16
(*B) 14
(C) 28
(D) 32
::: explanation
Host bits = 32−28 = 4, giving $2^4=16$ total addresses in the subnet. Subtracting 2 (for the reserved network address and broadcast address) gives $16-2=14$ usable host addresses.
:::

::: quiz Q3: Foundational Concept
Within any given subnet, what do the "network address" and "broadcast address" specifically represent, and why can neither be assigned to an individual host?
(A) They are simply the first and last IP addresses ever allocated globally
(*B) The network address (all host bits set to 0) identifies the subnet itself as a whole, and the broadcast address (all host bits set to 1) is used to send a message to every host on that subnet simultaneously — since both addresses have special, subnet-wide meanings, assigning either to one specific device would create ambiguity
(C) They are reserved exclusively for the subnet's router, and can never be used for any other purpose including broadcast
(D) They only exist in IPv6, not IPv4
::: explanation
Every subnet reserves exactly these two addresses for structural purposes: the network address (host portion all zeros) names the subnet as a whole (used in routing tables, for instance), and the broadcast address (host portion all ones) is the destination address for "send this to every host in this subnet." Assigning either to a single device would conflict with these subnet-wide meanings, which is why both are always excluded from the usable host range.
:::
