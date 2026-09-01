# Network Layer Overview & IP Protocols

**Forwarding vs routing, the datagram (IPv4) header, and the roles of ICMP, ARP, and IGMP as helper protocols.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
The Transport layer (Module 2 so far) assumed something crucial without explaining it: that data can somehow travel *between any two machines on the entire internet*, not just between two devices plugged into the same cable. That "somehow" is the **Network layer**'s entire job — and it splits neatly into two distinct sub-problems, often confused by beginners but genuinely different: **routing** is the *planning* problem — figuring out, in advance, the best paths through the network (this is a global, big-picture, "draw the map" task, handled by routing protocols and algorithms). **Forwarding** is the *execution* problem — given a packet that has just arrived at one specific router, quickly looking up "which outgoing link should this go out on?" and pushing it there (a fast, local, per-packet, "read the map I already have" task, performed by every router on every single packet). Routing happens occasionally, in the background, updating each router's map (its **forwarding table**); forwarding happens constantly, for every packet, using whatever that map currently says.

The core protocol living at this layer is **IP (Internet Protocol)** — the one thing every single device on the internet must speak, regardless of what's above it (TCP or UDP) or below it (Ethernet, Wi-Fi, fiber). IP itself is deliberately simple and unreliable (much like UDP, but one layer down) — it just does its best to get each packet, independently, toward its destination, with a handful of small helper protocols (ICMP, ARP) picking up specific side-jobs IP itself doesn't handle.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Routing vs. Forwarding — side by side:**

| | Routing | Forwarding |
|---|---|---|
| Question answered | "What's the best overall path to every possible destination?" | "This packet just arrived — which single outgoing link do I send it out on, right now?" |
| Scope | Network-wide (needs information from other routers) | Local to a single router (uses only its own table) |
| Frequency | Occasional (runs in the background, updates when topology changes) | Constant (happens for every single packet) |
| Mechanism | Routing algorithms/protocols (covered in upcoming topics) | A fast table lookup (the forwarding table, built by routing) |

**The IPv4 datagram header (20 bytes minimum):**

| Field | Size | Purpose |
|---|---|---|
| Version | 4 bits | IP version (4, for IPv4) |
| Header Length (IHL) | 4 bits | Header length, accounting for variable-length options |
| Type of Service (ToS) | 8 bits | Traffic priority hints, used in QoS (later topic) |
| Total Length | 16 bits | Entire datagram size (header + data), in bytes |
| Identification, Flags, Fragment Offset | 16+3+13 bits | Support datagram fragmentation/reassembly when a link's MTU is too small |
| Time to Live (TTL) | 8 bits | Decremented by every router hop; datagram discarded when it hits 0, preventing infinite routing loops from consuming resources forever |
| Protocol | 8 bits | Identifies the transport-layer protocol carried inside (6=TCP, 17=UDP) — this is the network-layer analogue of a "port number," but for demultiplexing to the right *transport protocol*, not the right process |
| Header Checksum | 16 bits | Error detection over the header only (not the payload — that's left to upper layers) |
| Source / Destination IP address | 32 + 32 bits | The addresses actually used for routing decisions |
| Options, Padding | variable | Rarely used in practice |

**ICMP (Internet Control Message Protocol) — IP's built-in error-reporting and diagnostic companion.** ICMP messages are carried inside IP datagrams but serve a fundamentally different purpose than user data: they report problems (e.g., "Destination Unreachable," "Time Exceeded" — sent when TTL hits zero) and support diagnostics. Two everyday tools are built directly on ICMP: `ping` (sends ICMP Echo Request, expects ICMP Echo Reply, measuring round-trip time and reachability) and `traceroute`/`tracert` (cleverly sends packets with deliberately increasing TTL values — 1, 2, 3, ... — so that each successive router along the path is the one that finally lets TTL expire and sends back a "Time Exceeded" ICMP message, revealing the path one hop at a time).

**ARP (Address Resolution Protocol) — bridging IP addresses to physical (MAC) addresses.** IP routing decisions operate on IP addresses, but actually delivering a frame on a local network (like Ethernet) requires the *physical (MAC) address* of the next hop. ARP is a local-network-only protocol: a device broadcasts "who has IP address X?" to everyone on the local network, and the device that owns that IP replies with "that's me, here's my MAC address" — this mapping is then cached (in an "ARP table" or "ARP cache") to avoid repeating the broadcast for every single packet.

**IGMP (Internet Group Management Protocol) — brief mention, detailed later.** Used by hosts to inform their local router which multicast groups they wish to receive traffic for — foundational to the multicast routing topic later in this module.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
A datagram is sent with TTL = 3. It passes through Router A, Router B, and Router C before reaching its final destination host. Trace the TTL value at each hop, and explain what would happen if the destination were actually one hop further away (behind a fourth router, Router D).
:::

::: step [Step 2: Execution] Applying Core Algorithm
Datagram leaves source: TTL = 3.
Arrives at Router A: Router A decrements TTL by 1 (now TTL=2), checks it's still greater than 0, forwards it onward.
Arrives at Router B: decrements to TTL=1, still greater than 0, forwards onward.
Arrives at Router C: decrements to TTL=0. Since the destination host is reached at exactly this point (per the original setup), the datagram is delivered successfully — routers only *discard and report* a datagram whose TTL reaches 0 *before* reaching the actual final destination; delivery to the end host itself doesn't require a further decrement-and-check step in the same way.
:::

::: step [Step 3: Conclusion] Final Result
If instead the destination were one hop further away, behind a fourth Router D: the datagram would arrive at Router D with TTL already at 0 (having been decremented to 0 by Router C, one hop too early), and Router D — following the TTL-expiry rule — would **discard** the datagram and send back an ICMP "Time Exceeded" message to the original source, rather than forwarding it any further. This exact mechanism (deliberately setting a small TTL and watching for the resulting "Time Exceeded" replies) is precisely how `traceroute` maps out a path, one router at a time, as mentioned in the theory section above.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What is the essential difference between "routing" and "forwarding" in the network layer?
(A) They are two different names for the exact same process
(*B) Routing is the network-wide, occasional process of determining the best paths and building forwarding tables; forwarding is the fast, local, per-packet process of using an already-built table to decide which outgoing link to send a specific arriving packet on
(C) Forwarding only happens at the source host; routing only happens at the destination host
(D) Routing is done by hosts; forwarding is done only by routers
::: explanation
Routing is the "planning" phase — algorithms and protocols that figure out good paths and populate each router's forwarding table, running occasionally (updating when the network topology changes). Forwarding is the "execution" phase — the fast table lookup every router performs for every single packet that passes through it, using whatever table routing has most recently provided.
:::

::: quiz Q2: Foundational Concept
What is the purpose of the Time to Live (TTL) field in the IPv4 header?
(A) It specifies how long the receiving application should keep the data before deleting it
(*B) It is decremented by each router the datagram passes through, and the datagram is discarded once it reaches zero — preventing a datagram stuck in a routing loop from circulating the network forever
(C) It encrypts the datagram's payload
(D) It indicates the total number of bytes in the datagram
::: explanation
TTL acts as a hop-count safety limit: since routing errors or loops could theoretically cause a datagram to circulate indefinitely, TTL guarantees every datagram is eventually discarded (and its source notified via ICMP) if it doesn't reach its destination within a bounded number of hops.
:::

::: quiz Q3: Foundational Concept
What specific problem does ARP (Address Resolution Protocol) solve?
(A) Translating domain names into IP addresses
(*B) Mapping a known IP address to the corresponding physical (MAC) address needed to actually deliver a frame on the local network
(C) Detecting and reporting network errors
(D) Establishing a TCP connection
::: explanation
Routing and forwarding decisions are made using IP addresses, but delivering data on a local network segment (like Ethernet) ultimately requires the destination's physical (MAC) address. ARP is the local-network broadcast protocol specifically used to discover "which MAC address currently corresponds to this IP address" — a distinct task from DNS, which maps domain names to IP addresses at a different layer entirely.
:::
