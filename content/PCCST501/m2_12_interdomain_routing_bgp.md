# Interdomain Routing: Border Gateway Protocol (BGP)

**Autonomous Systems (AS), intra-AS vs inter-AS routing, path vector routing, and policy-based route selection.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model
The previous topic's routing algorithms (Distance Vector, Link State) work beautifully *within* a single organisation's network — everyone cooperates, sharing information openly, all trying to achieve the same shared goal of globally optimal paths. But the real internet isn't one giant, cooperative network — it's actually a federation of thousands of *independently owned and operated* networks (internet service providers, universities, corporations), each fiercely protective of their own business interests, who must nonetheless somehow agree on paths that cross between each other's territory.

Think of it like international mail: within your own country's postal service, routing decisions are purely about efficiency — the fastest, cheapest internal path. But once a letter needs to cross into another country's postal system, "efficiency" is no longer the only consideration — trade agreements, political relationships, and business contracts between the two countries' postal services matter enormously too; a country might deliberately route mail through a "friendly" neighbouring country's system even if a shorter path exists through a country they have no business relationship with. **BGP (Border Gateway Protocol)** is exactly this: the protocol that lets independently-operated networks (called **Autonomous Systems**, or ASes) exchange routing information *between* each other, where the actual route chosen is often driven as much by business/policy considerations as by pure path length.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

**Autonomous Systems (AS).** An AS is a network (or group of networks) under a single administrative control, using one internal routing policy — e.g., one ISP, one large corporation's network, one university's network. Each AS is identified globally by a unique AS number.

**Intra-AS vs. Inter-AS routing — two different jobs, two different protocol families:**

| | Intra-AS routing | Inter-AS routing |
|---|---|---|
| Scope | Within a single AS | Between different, independently-operated ASes |
| Goal | Pure technical efficiency (shortest/cheapest path) | Efficiency **plus** business policy, contracts, trust relationships |
| Example protocols | OSPF, RIP (the Distance Vector / Link State protocols from the previous topic) | BGP (essentially the only protocol used for this at internet scale) |

**BGP as a path vector protocol.** BGP is often described as a variant of Distance Vector routing, but with a crucial enhancement: instead of each router advertising only a *distance* to a destination, BGP advertises the **entire AS-path** — the complete sequence of AS numbers a route would traverse to reach the destination, e.g. "to reach network X, go through AS 64512, then AS 64513, then AS 64514 (the destination's own AS)." This extra path information solves the count-to-infinity/loop problem inherent to plain distance vector routing directly — a router can immediately detect and reject any advertised route whose AS-path already includes its own AS number, since accepting it would obviously create a loop.

```mermaid
flowchart LR
    AS1["AS 100<br/>(your ISP)"] -->|advertises: "I can reach<br/>Network X via AS-path: 100"| AS2["AS 200<br/>(a transit provider)"]
    AS2 -->|re-advertises: "I can reach<br/>Network X via AS-path: 200, 100"| AS3["AS 300<br/>(another network)"]
    AS3 -.->|"AS 300 now knows a route<br/>to Network X, and knows exactly<br/>which ASes it would pass through"| AS3
```

**Policy-based route selection — why BGP doesn't simply pick the "shortest" AS-path.** Real-world business relationships between ASes typically fall into a few categories: **customer** (pays another AS for internet connectivity), **provider** (the AS being paid), and **peer** (two roughly equal-sized networks agreeing to exchange traffic between each other's customers directly, at no cost to either side, since it mutually benefits both). A common, general policy pattern many ASes follow: **prefer routes learned from a customer** (since the customer is paying, and routing their traffic is directly profitable) **over routes learned from a peer, and prefer routes from a peer over routes learned from a provider** (since sending traffic to a provider typically costs the sending AS money). This means the *shortest* available AS-path is often deliberately **not** the one actually chosen — a longer path through a paying customer can be commercially preferable to a shorter path through an expensive provider.

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
AS 500 learns two possible routes to reach a particular destination network: **Route 1**, a 2-hop AS-path via AS 500's *provider* (whom AS 500 pays for connectivity); and **Route 2**, a 4-hop (longer) AS-path via one of AS 500's *customers* (who pays AS 500). Using typical commercial BGP policy, determine which route AS 500 is likely to actually select, and why.
:::

::: step [Step 2: Execution] Applying Core Algorithm
Apply the standard commercial preference ordering: routes learned from a **customer** are generally preferred over routes learned from a **peer**, which are in turn generally preferred over routes learned from a **provider** — regardless of raw AS-path length. Route 2, despite being longer (4 hops vs. 2), is learned from a customer relationship. Route 1, despite being shorter, is learned from a provider relationship (which typically costs AS 500 money to use).
:::

::: step [Step 3: Conclusion] Final Result
AS 500 is likely to select **Route 2** (the longer, 4-hop path via its paying customer), not the shorter Route 1 — directly contradicting the naive assumption that BGP (or any routing protocol) always picks the "shortest" path. This concretely illustrates the defining feature of interdomain routing: business and policy considerations are woven directly into the route-selection process itself, not treated as an afterthought layered on top of a purely technical shortest-path calculation — a sharp contrast to the intra-AS routing algorithms (Distance Vector/Link State) from the previous topic, which optimise purely for path cost.
:::

---

<a id="self-check"></a>
## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What is an Autonomous System (AS) in the context of interdomain routing?
(A) A single router within a network
(*B) A network (or group of networks) under a single administrative control, operating its own internal routing policy, and identified globally by a unique AS number
(C) A synonym for a single IP address
(D) A protocol used exclusively for intra-AS routing
::: explanation
An AS represents the boundary of independent administrative control — one organisation's network, whether a small company or a massive ISP — and it's precisely the *boundaries between* these independently-controlled ASes where BGP's specialised inter-AS routing becomes necessary, since intra-AS protocols like OSPF assume a single, cooperating administrative authority.
:::

::: quiz Q2: Foundational Concept
How does BGP, as a "path vector" protocol, directly address the routing-loop problem that plain Distance Vector protocols are susceptible to?
(A) It doesn't address loops at all; BGP is equally susceptible to routing loops
(*B) By advertising the complete AS-path (the full sequence of ASes a route would traverse), rather than just a distance value, an AS can immediately detect and reject any route whose AS-path already contains its own AS number, since accepting it would obviously create a loop
(C) By requiring every AS to use Dijkstra's algorithm instead
(D) By limiting the network to a maximum of two ASes
::: explanation
Plain Distance Vector protocols only exchange numeric distance estimates, hiding the actual path taken — which is exactly what enables the count-to-infinity/looping problem. BGP's path vector approach makes the entire path explicit in every advertisement, so any AS can trivially spot (and refuse) a route that would loop back through itself.
:::

::: quiz Q3: Foundational Concept
Why might a network choose a longer AS-path over a shorter one when selecting a BGP route?
(A) BGP always randomly selects among available routes
(*B) Because BGP route selection incorporates business/policy relationships (e.g., preferring routes learned from a paying customer over a route learned from a provider the network itself must pay), which can outweigh pure path length in the decision
(C) Longer paths are always technically faster
(D) Shorter AS-paths are never actually available in real networks
::: explanation
Unlike purely technical intra-AS routing algorithms, BGP explicitly incorporates commercial relationships into route selection — a longer path through a customer relationship (which generates revenue) is commonly preferred over a shorter path through a provider relationship (which costs money), reflecting the genuinely business-driven nature of interdomain routing on the real internet.
:::
