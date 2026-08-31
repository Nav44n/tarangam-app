# Domain Name System (DNS)

**Hierarchical namespace, root/TLD/authoritative servers, iterative vs recursive queries, resource records, and DNS caching.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model: The Global Contacts App
Humans prefer names (`www.google.com`); routers require 32-bit or 128-bit numbers (`142.250.190.36`). DNS is the Internet’s automated contact book that bridges this gap. 

If the entire Internet relied on a single, centralized DNS server to translate names to IPs, that server would instantly collapse under billions of simultaneous queries, and a single crash would bring down the global web (a Single Point of Failure). To solve this, DNS is designed as a **distributed, hierarchical database**. No single server knows the whole internet; instead, they know *who to ask next*.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

### The DNS Distributed Hierarchy

The DNS namespace is organized as an inverted tree.

```text
                               [ Root DNS Servers ( . ) ]
                               /                        \
           [ .com TLD Servers ]                          [ .in TLD Servers ]
             /              \                               /               \
 [ amazon.com Auth ]  [ google.com Auth ]      [ ktu.edu.in Auth ]  [ amazon.in Auth ]
          |                  |                          |                    |
   [www.amazon.com](https://www.amazon.com)      mail.google.com            www.ktu.edu.in       www.amazon.in
```

* **Root DNS Servers:** 13 logical IP addresses globally. They do not know the IP of `www.amazon.com`, but they know the IP of the TLD servers responsible for `.com`.
* **Top-Level Domain (TLD) Servers:** Responsible for domains like `.com`, `.org`, `.net`, `.edu`, and country codes like `.in`, `.uk`. They know the IP addresses of the authoritative servers for specific domains.
* **Authoritative DNS Servers:** Owned or leased by the organization itself (e.g., Amazon, Google). These servers hold the actual, final IP address mappings for hostnames.
* **Local DNS Resolver:** Provided by your ISP (or services like Google's `8.8.8.8`). It acts as your proxy, performing the complex tree-walking process on your behalf.

### Resolution Mechanisms: Iterative vs. Recursive

When a client queries a Local DNS Resolver, the resolver must navigate the hierarchy. There are two primary traversal strategies:

1. **Recursive Query (Passing the Buck)**
   The queried server takes full responsibility for finding the final answer. If it doesn't know, it queries the next server, waits for the answer, and passes it back down the chain.
   *Typically used between the Client PC and the Local DNS Resolver.*

2. **Iterative Query (I Don't Know, But Ask Him)**
   The queried server replies with the best answer it currently has—usually a referral (the IP address of the next server down the tree). The querying server must then generate a new request to that next server.
   *Typically used between the Local DNS Resolver and the Root/TLD/Authoritative servers to reduce load on the upper-tier servers.*

```text
      [ ITERATIVE QUERY FLOW ]                        [ RECURSIVE QUERY FLOW ]
      
Local DNS                   Root DNS           Local DNS                   Root DNS
    | ---- 1. Who is X? ----> |                    | ---- 1. Who is X? ----> |
    | <--- 2. Ask TLD IP ---- |                    |                         | -- 2. Who is X? -> TLD
    |                                              |                         | <- 3. X is IP ---- TLD
    | ---- 3. Who is X? ----> TLD DNS              | <--- 4. X is IP ------- |
    | <--- 4. Ask Auth IP --- TLD DNS              |
    |                                              |
    | ---- 5. Who is X? ----> Auth DNS             |
    | <--- 6. X is IP ------- Auth DNS             |
```

### DNS Resource Records (RR)

DNS servers store data in Resource Records. A resource record is a 4-tuple: `(Name, Value, Type, TTL)`

| Type | Name | Value | Purpose |
| :--- | :--- | :--- | :--- |
| **A** | Hostname | IPv4 Address | Standard IPv4 resolution. Maps `www.example.com` to `192.0.2.1`. |
| **AAAA** | Hostname | IPv6 Address | Standard IPv6 resolution. |
| **CNAME** | Alias Hostname | Canonical Hostname | Alias mapping. Maps `shop.ibm.com` to its real name `server-east.ibm.com`. |
| **NS** | Domain | Hostname of Auth Server | Identifies the Authoritative DNS server for a domain. |
| **MX** | Domain | Hostname of Mail Server | Identifies the mail server handling emails for the domain (used by SMTP). |

---

## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Problem
Alice attempts to visit `www.ktu.edu.in`. Her PC checks its local browser/OS DNS cache. It is a cache miss. The PC sends a Recursive Query to the ISP's Local DNS Resolver.
:::

::: step [Step 2: Execution] Iterative Traversal by the Local DNS
1. The Local DNS cache is also empty. It sends an Iterative Query to a Root Server.
2. The Root Server replies: "I don't know `www.ktu.edu.in`, but here is the IP for the `.in` TLD Server." (Type NS record).
3. The Local DNS queries the `.in` TLD Server.
4. The TLD Server replies: "I don't know the exact web server, but here is the IP for the Authoritative Server for `ktu.edu.in`."
5. The Local DNS queries the Authoritative Server for `ktu.edu.in`.
6. The Authoritative Server replies with a Type A record: `(www.ktu.edu.in, 14.139.185.34, A, 86400)`.
:::

::: step [Step 3: Conclusion] Caching and Delivery
The Local DNS Resolver receives the IP. It saves this IP in its cache for 86400 seconds (Time-To-Live, TTL) so future queries for `www.ktu.edu.in` from any user can be answered immediately without traversing the tree. Finally, it sends the IP address back to Alice's PC.
:::

---

## 4. Active Recall Checkpoint

::: quiz Q1: Foundational Concept
What is the primary operational difference between a DNS A record and a CNAME record?
(A) An A record is used for IPv6, while a CNAME is used for IPv4.
(*B) An A record maps a hostname directly to an IP address, while a CNAME maps an alias hostname to a canonical (real) hostname.
(C) An A record is strictly for email servers, while CNAME is for web servers.
(D) An A record holds the physical MAC address of the destination.
::: explanation
The A record provides the actual numerical IP address (e.g., `192.168.1.1`), which the network layer requires. A CNAME simply points an alias (like `www.website.com`) to its true name (like `website-server-01.hosting.com`), requiring a second lookup to resolve the true name to an IP.
:::

::: quiz Q2: Foundational Concept
Why do Local DNS Resolvers typically use iterative queries when talking to Root and TLD servers?
(A) Iterative queries are encrypted, whereas recursive queries are plaintext.
(*B) To prevent the Root and TLD servers from being overwhelmed. If they accepted recursive queries, they would have to do the fetching work for billions of global requests simultaneously.
(C) Root servers do not have enough storage space for recursive queries.
(D) Iterative queries traverse the network layer, while recursive queries traverse the transport layer.
::: explanation
Recursive queries force the receiving server to do all the heavy lifting. If the 13 logical Root servers had to recursively hunt down every URL requested globally, they would instantly crash from connection exhaustion. By using iterative queries, Root servers simply reply with a referral and instantly drop the connection, remaining highly available.
:::

::: quiz Q3: Foundational Concept
Which of the following DNS records is strictly necessary to send an email to user@company.com?
(A) AAAA Record
(B) NS Record
(*C) MX Record
(D) PTR Record
::: explanation
The Mail Exchange (MX) record specifically maps a domain name to the hostname of the mail server responsible for accepting emails on behalf of that domain.
:::