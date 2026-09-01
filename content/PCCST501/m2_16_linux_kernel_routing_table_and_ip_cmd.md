# The Linux Kernel Routing Table & the `ip` Command

**Reading a real routing table, the longest-prefix-match forwarding rule, and hands-on practice with `ip route`, `ip addr`, and related commands.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
Every device that runs Linux — including, quietly, a huge fraction of the internet's actual routers, plus your own laptop if it dual-boots or runs Linux — maintains its own local **routing table**: a small, structured list of rules answering the exact "forwarding" question from earlier in this module: "given a packet destined for IP address X, which network interface (and which next-hop gateway) should it be sent out through?" This isn't an abstract textbook concept — it's a real, inspectable, editable data structure sitting on every Linux machine right now, and the `ip` command (specifically `ip route`, part of the modern `iproute2` toolset) is exactly how you view and manipulate it directly.

Understanding this table hands-on closes the loop on everything theoretical covered so far in this module: subnetting decided *how* address blocks get divided, routing algorithms decided *what the best paths are*, and this routing table is *where that decision actually lives*, consulted by the kernel for literally every single outgoing packet your machine ever sends.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Anatomy of a Linux routing table entry.** Run `ip route show` (or the shorter `ip r`) on any Linux machine, and you'll see output resembling:
```
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.42
10.0.0.0/8 via 192.168.1.254 dev eth0 metric 100
```
Reading each entry:
- **Destination network** (e.g. `192.168.1.0/24`, or the special keyword `default` meaning "everything not matched by any more specific rule" — this is the catch-all default route, typically pointing to your internet gateway).
- **`via <gateway IP>`** — the next-hop router's IP address to forward through (omitted for directly-connected networks, where the destination is reachable without going through any intermediate router).
- **`dev <interface>`** — which local network interface (e.g. `eth0`, `wlan0`) to send the packet out on.
- **`metric <number>`** — a cost value used to choose between multiple matching routes to the same destination, if more than one exists (lower metric preferred).

**The Longest Prefix Match rule — the single most important forwarding principle.** When a packet needs to be forwarded, and *multiple* routing table entries technically match its destination address (because entries with different prefix lengths can overlap — e.g. both a broad `10.0.0.0/8` route and a more specific `10.0.5.0/24` route might both technically cover a destination like `10.0.5.20`), the kernel always selects the entry with the **longest matching prefix** (the most specific match) — not the shortest, and not simply the first one listed. This makes intuitive sense: a more specific route represents more precise, deliberately-configured knowledge about that particular sub-range, and should always take priority over a broader, more general rule that merely happens to also cover it.

**Key practical `ip` command reference:**

| Command | Purpose |
|---|---|
| `ip addr show` (or `ip a`) | List all network interfaces and their assigned IP addresses |
| `ip route show` (or `ip r`) | Display the current routing table |
| `ip route add <network>/<prefix> via <gateway> dev <iface>` | Add a new static route |
| `ip route del <network>/<prefix>` | Remove a route |
| `ip route get <destination-IP>` | Ask the kernel to show exactly which route it *would* use for a specific destination — extremely useful for debugging |
| `ip neigh show` (or `ip n`) | Show the ARP cache (IP-to-MAC mappings, from the earlier ARP topic) |

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
A Linux machine's routing table contains these three entries: `10.0.0.0/8 via 192.168.1.1 dev eth0`, `10.0.5.0/24 via 192.168.1.2 dev eth0`, and `10.0.5.128/25 via 192.168.1.3 dev eth0`. Determine which entry the kernel will actually use to forward a packet destined for `10.0.5.200`.
:::

::: step [Step 2: Execution] Applying Core Algorithm
Check each entry against the destination `10.0.5.200` and identify which ones actually match, and how specifically:
Entry 1, `10.0.0.0/8` (covers `10.0.0.0`–`10.255.255.255`): matches, since `10.0.5.200` falls within this broad range — prefix length 8.
Entry 2, `10.0.5.0/24` (covers `10.0.5.0`–`10.0.5.255`): matches, since `10.0.5.200` falls within this narrower range — prefix length 24.
Entry 3, `10.0.5.128/25` (covers `10.0.5.128`–`10.0.5.255`): matches, since `10.0.5.200` falls within this even narrower range — prefix length 25.
All three entries technically match the destination — apply the Longest Prefix Match rule: compare prefix lengths 8, 24, and 25, and select the **longest**, which is 25.
:::

::: step [Step 3: Conclusion] Final Result
The kernel selects **Entry 3** (`10.0.5.128/25 via 192.168.1.3`) — the most specific matching route — and forwards the packet via gateway `192.168.1.3`, even though two broader routes also technically covered this destination. This is exactly why network administrators can safely add increasingly specific routes for particular sub-ranges (like carving out a special path for one specific /25 subnet) without needing to worry about broader, pre-existing routes accidentally taking priority — the Longest Prefix Match rule guarantees the most specific, deliberately-added rule always wins.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
If a packet's destination address matches both a `/16` route and a `/24` route in the routing table, which one does the Linux kernel actually use to forward the packet?
(A) The `/16` route, because it was likely added first
(*B) The `/24` route, because Longest Prefix Match always selects the most specific (longest prefix) matching entry, regardless of the order routes were added in
(C) Both routes are used simultaneously, splitting the traffic
(D) Neither route is used; the packet is dropped due to ambiguity
::: explanation
The Longest Prefix Match rule is unconditional: whenever multiple routing table entries match a destination, the kernel always selects the one with the longest (most specific) prefix — here, `/24` is more specific than `/16`, so it wins regardless of table ordering or which was configured first.
:::

::: quiz Q2: Foundational Concept
What does the special `default` route (shown as `default via <gateway> dev <iface>` in `ip route show` output) represent, and what is its effective prefix length for Longest-Prefix-Match purposes?
(A) It matches only traffic destined for the local machine itself
(*B) It is a catch-all route matching *any* destination not covered by a more specific entry — effectively equivalent to `0.0.0.0/0`, the shortest possible prefix (0 bits), meaning it is always the *last* choice whenever any more specific route also matches
(C) It always has the highest priority, overriding all other routes
(D) It is only used for IPv6 traffic
::: explanation
`default` represents the broadest possible match (prefix length 0 — matching literally any address), which is precisely why it only gets used as a last resort: any more specific route (any longer prefix) that also matches a given destination will always be preferred over it, per Longest Prefix Match — the default route only "wins" when nothing more specific applies.
:::

::: quiz Q3: Foundational Concept
Which `ip` command would you use to directly ask the kernel exactly which route it would select for a specific destination IP address, without manually working through Longest Prefix Match by hand?
(A) `ip addr show`
(*B) `ip route get <destination-IP>`
(C) `ip neigh show`
(D) `ip route del`
::: explanation
`ip route get <destination-IP>` is specifically designed for this exact debugging task — it directly queries the kernel's own routing logic and reports back which specific route entry (and therefore which gateway/interface) would actually be selected for that destination, saving you from having to manually trace through Longest Prefix Match by hand across potentially many table entries.
:::
