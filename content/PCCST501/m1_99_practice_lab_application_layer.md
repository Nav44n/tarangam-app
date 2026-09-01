# Module 1 Practice Lab: Application Layer & Networking Calculations

**Worked calculations for P2P file distribution time, HTTP round-trip latency, DNS query resolution time, and socket/4-tuple addressing.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model: Turning Concepts into Numbers
Every topic in Module 1 has a quantitative side hiding underneath the concepts: P2P's "self-scaling" claim can be measured in seconds, HTTP's "persistent connections are faster" claim can be measured in round-trip times, and DNS's "hierarchy adds latency" claim can be measured in query hops. This lab is a set of worked, numeric problems pulling together File Transfer time, HTTP page-load latency, DNS resolution delay, and socket addressing — the exact style of calculation you should expect to be asked to reproduce on your own, with different numbers, in an exam setting.
:::

---

<a id="the-math"></a>
## 2. Reference Formulas

| Topic | Formula | Notes |
|---|---|---|
| Client-Server distribution time | $D_{CS} \geq \max\left(\frac{NF}{u_s}, \frac{F}{d_{min}}\right)$ | $N$ peers, file size $F$, server upload $u_s$ |
| P2P distribution time | $D_{P2P} \geq \max\left(\frac{F}{u_s}, \frac{F}{d_{min}}, \frac{F}{u_s + \sum u_i}\right)$ | $\sum u_i$ = total peer upload capacity |
| Non-persistent HTTP page load | $\text{Total time} = 2 \times \text{RTT} \times (1 + k)$ (serial) | 1 RTT to open TCP + 1 RTT per object requested; $k$ = number of embedded objects |
| Persistent HTTP (no pipelining) page load | $\text{Total time} = 2 \times \text{RTT}_{setup} + k \times \text{RTT}$ | One TCP setup (2 RTT total incl. first object), then 1 RTT per remaining object |
| DNS resolution (cold cache, full iterative chain) | $\text{Total DNS time} = \text{RTT}_{root} + \text{RTT}_{TLD} + \text{RTT}_{auth}$ | One RTT per hierarchy level walked |
| Base64 (MIME) size expansion | $\text{Encoded size} = \frac{4}{3} \times \text{Original size}$ | ~33% overhead |

---

<a id="worked-example"></a>
## 3. Worked Problems

::: step [Problem 1: P2P vs. Client-Server Distribution Time] Setup
A file of size $F = 4$ Gbits is shared with $N = 20$ peers. Server upload rate $u_s = 20$ Mbps. Every peer has download rate $d_i = 4$ Mbps and upload rate $u_i = 0.5$ Mbps. Compute $D_{CS}$ and $D_{P2P}$.
:::

::: step [Problem 1: Execution] Applying the Formulas
**Client-Server:**
$$D_{CS} \geq \max\left(\frac{20 \times 4000}{20}, \frac{4000}{4}\right) = \max(4000, 1000) = 4000 \text{ s}$$

**P2P:** total peer upload = $20 \times 0.5 = 10$ Mbps.
$$D_{P2P} \geq \max\left(\frac{4000}{20}, \frac{4000}{4}, \frac{4000}{20+10}\right) = \max(200, 1000, 133.3) = 1000 \text{ s}$$
:::

::: step [Problem 1: Conclusion] Result
$D_{CS} = 4000$s vs. $D_{P2P} = 1000$s — **P2P is 4× faster** here because the server-load term ($\frac{NF}{u_s} = 4000$s) dominates Client-Server, while under P2P the bottleneck shifts entirely to each peer's own download rate ($\frac{F}{d_{min}} = 1000$s), which no additional server or peer bandwidth can improve. This is the textbook case where P2P's advantage is largest: many peers, and a server that would otherwise be badly overloaded.
:::

---

::: step [Problem 2: Non-Persistent vs. Persistent HTTP Latency] Setup
A web page consists of 1 base HTML file plus 8 embedded images (9 objects total). The RTT between client and server is $20$ ms. Assume negligible transmission/processing time. Compute total page-load time under Non-Persistent HTTP (serial, one connection per object) vs. Persistent HTTP (one connection, no pipelining — must wait for each response before requesting the next).
:::

::: step [Problem 2: Execution] Counting Round Trips
**Non-Persistent (serial):** each of the 9 objects requires its own TCP handshake (1 RTT) + the actual GET/response (1 RTT) = 2 RTTs per object.
$$\text{Total} = 9 \times 2 \times 20\text{ms} = 360 \text{ ms}$$

**Persistent (no pipelining):** one TCP handshake overall (1 RTT), then the first object's GET/response (1 RTT), then each of the remaining 8 objects only needs 1 RTT each (connection is already open).
$$\text{Total} = (1 + 1) \times 20\text{ms} + 8 \times 20\text{ms} = 40\text{ms} + 160\text{ms} = 200 \text{ ms}$$
:::

::: step [Problem 2: Conclusion] Result
Persistent HTTP finishes in **200 ms** vs. **360 ms** for Non-Persistent — a 44% latency reduction, purely from avoiding 8 redundant TCP handshakes. This gap grows even larger as either the RTT increases (e.g., a distant server) or the number of embedded objects increases (a richer, more image-heavy page).
:::

---

::: step [Problem 3: DNS Resolution Latency] Setup
A client's local DNS cache is completely empty (a "cold cache"). Resolving `www.example.edu` requires the Local DNS Resolver to walk the full hierarchy: Root → `.edu` TLD → `example.edu` Authoritative server. Each hop has a measured RTT of Root = 8ms, TLD = 12ms, Authoritative = 10ms. The client-to-Local-DNS RTT is a separate 5ms. Compute the total time before the client receives the resolved IP address.
:::

::: step [Problem 3: Execution] Summing the Chain
The client's request to its Local DNS Resolver: $5$ms (one-way is often modeled as included in the resolver's total, but here we count the client↔resolver RTT once at the start).
The resolver then performs three **iterative** queries in sequence, each requiring a full RTT before the next can begin (since each answer determines who to ask next):
$$\text{DNS chain} = 8\text{ms (Root)} + 12\text{ms (TLD)} + 10\text{ms (Authoritative)} = 30 \text{ ms}$$
Adding the client-to-resolver leg:
$$\text{Total} = 5\text{ms} + 30\text{ms} = 35 \text{ ms}$$
:::

::: step [Problem 3: Conclusion] Result
The client waits **35 ms** total before it even knows the destination's IP address — and this entire delay happens *before* the actual HTTP request to `www.example.edu` can even begin. This is precisely why DNS caching (honoring the TTL of each resource record) matters so much in practice: every subsequent request for the same hostname, from any user of that same Local DNS Resolver, can skip straight to a cached answer and avoid repeating this 30ms hierarchy walk.
:::

---

::: step [Problem 4: Socket / 4-Tuple Addressing] Setup
A web server at IP `10.0.0.5`, port `80`, is simultaneously handling three connections: Connection X from `192.168.1.10:51000`, Connection Y from `192.168.1.10:51001`, and Connection Z from `192.168.1.20:51000`. Determine whether TCP can correctly distinguish all three as separate sockets, and identify which two connections would be indistinguishable if this were UDP instead of TCP.
:::

::: step [Problem 4: Execution] Comparing Demultiplexing Rules
**TCP (uses full 4-tuple: src IP, src port, dst IP, dst port):**
* X: `(192.168.1.10, 51000, 10.0.0.5, 80)`
* Y: `(192.168.1.10, 51001, 10.0.0.5, 80)`
* Z: `(192.168.1.20, 51000, 10.0.0.5, 80)`

All three 4-tuples are distinct (X and Y differ in source port; X and Z differ in source IP), so TCP correctly demultiplexes all three into separate sockets.

**UDP (uses only destination port, ignoring source entirely):** every one of X, Y, and Z arrives at the same destination port (80), and UDP demultiplexing does not look at source IP/port at all — so a UDP-based server would deliver *all three* to the exact same single socket, unable to distinguish which packet came from whom without inspecting the payload itself.
:::

::: step [Problem 4: Conclusion] Result
TCP's 4-tuple demultiplexing correctly separates all three connections into distinct sockets, which is exactly how one web server on port 80 can serve many simultaneous clients. If the same scenario used UDP, all three would collapse into one shared socket — illustrating precisely why connection-oriented applications (requiring per-client session state) are built on TCP rather than UDP.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Applied Calculation
A file of size $F = 8$ Gbits is distributed to $N = 40$ peers, server upload $u_s = 10$ Mbps, slowest peer download $d_{min} = 5$ Mbps, total peer upload $\sum u_i = 20$ Mbps. What is the minimum P2P distribution time?
(A) 800 seconds
(*B) 1600 seconds
(C) 267 seconds
(D) 8000 seconds
::: explanation
$D_{P2P} \geq \max\left(\frac{8000}{10}, \frac{8000}{5}, \frac{8000}{10+20}\right) = \max(800, 1600, 267) = 1600$ seconds. The slowest peer's own download rate is the binding constraint here, not the server or aggregate upload capacity.
:::

::: quiz Q2: Applied Calculation
With an RTT of 50ms, how much total time does Non-Persistent HTTP need to fetch an HTML page plus 3 embedded images (4 objects total), assuming serial connections and negligible transmission time?
(A) 50 ms
(B) 200 ms
(*C) 400 ms
(D) 800 ms
::: explanation
Each of the 4 objects needs its own TCP handshake (1 RTT) plus its own request/response (1 RTT) = 2 RTT per object. Total = $4 \times 2 \times 50\text{ms} = 400$ ms.
:::

::: quiz Q3: Applied Calculation
Two UDP datagrams both arrive at a server's port 9000 — one from Client A (`203.0.113.1:40000`) and one from Client B (`203.0.113.2:40000`). How does the server's UDP demultiplexing handle these two datagrams?
(A) It creates two separate sockets, one per client, using the full 4-tuple
(*B) It delivers both to the same single socket bound to port 9000, since UDP demultiplexing only examines the destination port and ignores source IP/port
(C) It rejects both datagrams because the source ports match
(D) It automatically upgrades the connection to TCP to distinguish the clients
::: explanation
UDP is connectionless and demultiplexes using only the destination port — every datagram arriving at port 9000 goes to whichever single socket is bound there, regardless of which source IP or source port sent it. Any need to distinguish individual senders must be handled by the application reading the payload itself.
:::
