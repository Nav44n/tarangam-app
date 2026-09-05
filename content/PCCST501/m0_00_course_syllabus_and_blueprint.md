# KTU Official Syllabus: Computer Networks (PCCST501)

Welcome to the comprehensive academic and examination blueprint for **Computer Networks (PCCST501)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied engineering branches**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Computer Networks** |
| **Course Code** | `PCCST501` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Common to CS / CD / CM / CR / CA / AD / AI / CB / CN / CU / CI)** |
| **Teaching Hours / Week** | **3:1:0:0** *(Lecture: 3 hrs, Tutorial: 1 hr, Practical: 0, Remedial: 0)* |
| **Total Contact Hours** | **44 Contact Hours** |
| **Course Credits** | **4 Credits** |
| **Course Type** | **Theory (with Linux Hands-on Experiments)** |
| **Continuous Internal Evaluation (CIE)** | **40 Marks** *(Min. 45% / 18 marks required for ESE eligibility)* |
| **End Semester Examination (ESE)** | **60 Marks** *(Min. 40% / 24 marks required to pass)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |
| **Prerequisites** | **None** |

</div>

::: callout-intuition Why Computer Networks is the Cornerstone of Modern Software
Every distributed system, cloud platform, web application, and edge AI deployment relies on the protocol stack studied in this course. From the raw electrical signals that encode bits on fiber-optic cables up through socket buffers in the Linux kernel to HTTP/3 and P2P torrent swarms, understanding networking turns "black box" distributed engineering into transparent, optimizable architecture.
:::

---

## 🎯 Course Objectives

The primary objectives of this course are structured to bridge foundational network architecture with practical Linux systems programming:

1. **Core Networking Foundations**: To introduce the core concepts of computer networking across all layers of the OSI and TCP/IP protocol stacks.
2. **Linux Internetworking Implementation**: To develop a complete, systems-level big picture of internetworking implementation on Linux-based systems, including socket system calls, I/O multiplexing, kernel routing tables, and packet interception.
3. **Network Management & Architecture**: To impart an overview of network management concepts, protocols (SNMP), and abstract data formatting (ASN.1).

---

## 📚 Module-by-Module Syllabus Breakdown

### Module 1: Overview of Internet & Application Layer (6 Contact Hours)

::: callout-exam Module 1 High-Yield Focus
Module 1 carries **15 compulsory/choice marks in ESE** (Two 3-mark questions in Part A + One 9-mark question with choice in Part B). Master HTTP 1.0 vs 1.1 persistence, DNS resolution hierarchy (iterative vs recursive), and P2P BitTorrent choking/unchoking algorithms.
:::

* **Overview of the Internet & Protocol Layering**:
  * Internet infrastructure, network edge, access networks, physical media, packet switching vs circuit switching, network core, ISP hierarchy.
  * Protocol layering concepts, five-layer Internet model vs seven-layer OSI reference model, encapsulation and decapsulation at each tier.
  * *(Reference: Book 1, Chapter 1)*

* **Application Layer Protocols & Paradigms**:
  * Principles of network applications, Application-Layer Paradigms (Client-Server vs Peer-to-Peer).
  * **Client-Server Applications**:
    * **World Wide Web & HTTP**: Persistent vs non-persistent HTTP connections, HTTP request and response message structures, HTTP status codes, cookies, web caching (conditional GET).
    * **File Transfer Protocol (FTP)**: Out-of-band control connection (`port 21`) vs data connection (`port 20`), active vs passive FTP modes.
    * **Electronic Mail**: Mail architecture (User Agents, Mail Servers, SMTP), Message transfer protocol (SMTP), Mail access protocols (POP3, IMAP, HTTP-based webmail).
    * **Domain Name System (DNS)**: Distributed hierarchical database, root servers, TLD servers, authoritative servers, recursive vs iterative name queries, DNS caching, DNS resource records (A, AAAA, CNAME, MX, NS).
  * **Peer-to-Peer (P2P) Paradigm**:
    * P2P file distribution architectures, Client-Server vs P2P file distribution time scaling.
    * **Case Study: BitTorrent**: Torrents, trackers, tit-for-tat incentive mechanism, rarest-first chunk selection, choking/unchoking algorithms, optimistic unchoking.
  * *(Reference: Book 1, Chapter 2)*

---

### Module 2: Transport Layer & Network Layer (18 Contact Hours)

::: callout-exam Module 2 High-Yield Focus
Module 2 is the **largest module in the syllabus (18 contact hours)**. It covers both Transport and Network layers along with critical **Linux systems programming hands-on**. High probability exam questions include: TCP Connection Management (3-way handshake & 4-way teardown), TCP Congestion Control (Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery), Dijkstra/Distance Vector routing, and Linux socket APIs (`select`/`poll`).
:::

* **Transport Layer Services & Protocols**:
  * Transport-layer services, multiplexing and demultiplexing via ports, connectionless transport: **User Datagram Protocol (UDP)**, UDP segment structure, checksum calculation.
  * Principles of Reliable Data Transfer (RDT 1.0 to RDT 3.0), Pipelined protocols: **Go-Back-N (GBN)** vs **Selective Repeat (SR)**, sliding window mechanics.
  * **Transmission Control Protocol (TCP)**:
    * TCP connection-oriented model, TCP segment structure, sequence numbers, acknowledgment numbers, flags (SYN, ACK, FIN, RST, PSH, URG).
    * Round-Trip Time (RTT) estimation and timeout calculation ($SRTT$, $RTTVAR$, $RTO$).
    * TCP connection establishment (Three-Way Handshake) and termination (Four-Way Teardown), connection states and `TIME_WAIT`.
    * TCP Flow Control (Receive Window `rwnd`), TCP Congestion Control (Congestion Window `cwnd`, Slow Start, Congestion Avoidance, Fast Retransmit, Fast Recovery, AIMD).
  * *(Reference: Book 1, Chapter 3)*

* **Hands-on Socket Programming (Linux Systems API)**:
  * **Sockets Introduction**: Berkeley Socket API, socket descriptors, address structures (`sockaddr_in`, `sockaddr_in6`).
  * **Elementary TCP Sockets**: System calls sequence: `socket()`, `bind()`, `listen()`, `accept()`, `connect()`, `read()`, `write()`, `close()`.
  * **TCP Client/Server Architecture**: Iterative vs concurrent servers, handling multiple connections.
  * **I/O Multiplexing**: Synchronous I/O multiplexing using `select()` and `poll()` system calls, descriptor sets, handling read/write readiness.
  * **Elementary UDP Sockets**: `sendto()` and `recvfrom()` APIs, connectionless messaging.
  * **Advanced I/O Functions**: Socket options (`getsockopt()`, `setsockopt()`), non-blocking sockets, timeout handling.
  * *(Reference: Book 2, Chapters 3 to 6, 8, 14)*

* **Network Layer & Routing**:
  * Network-layer services, forwarding vs routing, data plane vs control plane.
  * **Network-layer protocols**: IPv4 datagram format, IPv4 addressing, subnetting, Classless Inter-Domain Routing (CIDR), Network Address Translation (NAT).
  * **Routing Paradigms**:
    * **Unicast Routing**: Link-State routing (Dijkstra's Shortest Path First Algorithm), Distance-Vector routing (Bellman-Ford Algorithm, Count-to-Infinity problem, Split Horizon, Poison Reverse).
    * **Intra-domain and Inter-domain routing**: Hierarchical routing, Autonomous Systems (AS), Intra-AS routing (OSPF, RIP), Inter-AS routing (Border Gateway Protocol - BGP).
    * **Multicast Routing**: Multicasting basics, group management (IGMP), multicast trees (Source-based vs Shared trees), DVMRP, PIM.
  * **Next Generation Internet Protocol (IPv6)**:
    * IPv6 datagram format, 128-bit address representation, header simplifications, flow labeling.
    * Transition from IPv4 to IPv6: Dual-Stack approach, Tunneling, Header translation.
  * **Quality of Service (QoS)**:
    * Principles of QoS, traffic shaping and policing, Leaky Bucket algorithm, Token Bucket algorithm, Packet scheduling (FIFO, Priority Queuing, Round Robin, Weighted Fair Queuing).
  * *(Reference: Book 1, Chapters 4 & 8)*

* **Hands-on Linux Kernel Networking**:
  * Linux Kernel Implementation of Routing Table and Caches (`fib_table`, `rt_hash_table`).
  * Routing Cache Implementation Overview, route lookup workflows inside the kernel networking subsystem.
  * Adding, deleting, and modifying routing table entries using the modern Linux `ip route` command suite (`ip route add`, `ip route show`, `ip route del`).
  * *(Reference: Book 3, Chapter 14)*

---

### Module 3: Data-Link Layer & Wireless Networks (11 Contact Hours)

::: callout-exam Module 3 High-Yield Focus
Key questions from Module 3 include: CRC error detection derivations, CSMA/CD vs CSMA/CA mechanisms, Ethernet IEEE 802.3 frame structure and minimum frame length calculations ($L_{\min} = 2 \times t_{\text{prop}} \times R$), connecting devices comparison, and Mobile IP triangle routing.
:::

* **Data-Link Layer & Data Link Control (DLC)**:
  * Link layer services, node-to-node delivery, framing (character-oriented vs bit-oriented framing, bit stuffing and byte stuffing).
  * Error detection and correction: Parity checks, Two-Dimensional Parity, Checksums, **Cyclic Redundancy Check (CRC)** polynomial division.
  * Flow and error control protocols: Stop-and-Wait ARQ, Go-Back-N ARQ, Selective Repeat ARQ.

* **Multiple Access Protocols (MAC)**:
  * Channel allocation problem, Random Access protocols: Pure ALOHA, Slotted ALOHA, Carrier Sense Multiple Access (CSMA), CSMA with Collision Detection (CSMA/CD), CSMA with Collision Avoidance (CSMA/CA).
  * Controlled access protocols: Reservation, Polling, Token Passing.
  * Channelization: FDMA, TDMA, CDMA (Orthogonal codes, Walsh matrices).

* **Link-Layer Addressing & Local Area Networks**:
  * MAC addresses (IEEE 802 48-bit hex format), Address Resolution Protocol (ARP), ARP cache operation, gratuitous ARP.
  * **Ethernet Protocol (IEEE 802.3)**: Legacy 10 Mbps Ethernet, Fast Ethernet, Gigabit Ethernet, 10-Gigabit Ethernet. Physical layer topologies, Ethernet MAC sublayer frame structure, minimum frame length requirements and derivation.
  * **Connecting Devices**: Physical-layer devices (Repeaters, Hubs), Data-link layer devices (Bridges, Layer-2 Switches, Learning Bridges, Spanning Tree Protocol IEEE 802.1D overview), Network-layer devices (Routers, Layer-3 Switches), Gateways. Virtual LANs (VLANs - IEEE 802.1Q).
  * *(Reference: Book 1, Chapter 5)*

* **Wireless LANs & Mobile IP**:
  * **Wireless LANs (IEEE 802.11 / Wi-Fi)**: Architecture, BSS, ESS, AP, Hidden Station and Exposed Station problems, MACAW, CSMA/CA with RTS/CTS exchange, frame format.
  * **Mobile IP**: Addressing in mobility, Home Agent (HA), Foreign Agent (FA), Home Address, Care-of Address (CoA), Agent Discovery, Registration, Tunneling, Encapsulation, Triangle routing problem and route optimization.
  * *(Reference: Book 1, Chapter 6)*

* **Hands-on Low-Level Link Access**:
  * Datalink Provider Interface (DLPI).
  * Packet sniffing and raw socket creation using `SOCK_PACKET` and `PF_PACKET` in Linux (`socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL))`).
  * *(Reference: Book 2, Chapter 29)*

---

### Module 4: Network Management & Physical Layer (9 Contact Hours)

::: callout-exam Module 4 High-Yield Focus
Module 4 combines network management standards with physical layer transmission theory. Master the Nyquist bit rate ($C = 2B \log_2 M$) vs Shannon capacity ($C = B \log_2(1 + \text{SNR})$), Line Coding schemes (NRZ, Manchester, Differential Manchester, AMI), and SNMP message architecture with ASN.1 encoding.
:::

* **Network Management Architecture & Protocols**:
  * Network management framework, components: Managed devices, Management Agents, Network Management Stations (NMS).
  * **Simple Network Management Protocol (SNMP)**: SNMP architecture, SNMP versions (v1, v2c, v3 security enhancements), Protocol Data Units (PDUs: `GetRequest`, `GetNextRequest`, `GetBulkRequest`, `SetRequest`, `Response`, `Trap`).
  * **Structure of Management Information (SMI)** & **Management Information Base (MIB)**: MIB-II tree hierarchy, object identifiers (OIDs).
  * **Abstract Syntax Notation One (ASN.1)**: Data description language, Basic Encoding Rules (BER) tag-length-value (TLV) representation.
  * *(Reference: Book 1, Chapter 9)*

* **Physical Layer Fundamentals & Transmission**:
  * **Data and Signals**: Analog vs digital signals, time and frequency domains, composite signals, bandwidth, transmission impairment (attenuation, distortion, noise, SNR).
  * **Channel Capacity & Data Rate Limits**: Noiseless channels: Nyquist Theorem ($C = 2B \log_2 L$); Noisy channels: Shannon Capacity theorem ($C = B \log_2(1 + \text{SNR})$).
  * **Digital Transmission**:
    * Line coding schemes: Unipolar, Polar (NRZ-L, NRZ-I, RZ, Manchester, Differential Manchester), Bipolar (AMI, Pseudoternary).
    * Block coding (4B/5B, 8B/10B), Scrambling techniques (B8ZS, HDB3).
    * Pulse Code Modulation (PCM), Delta Modulation (DM).
  * **Analog Transmission**:
    * Digital-to-Analog conversion (Modulation): Amplitude Shift Keying (ASK), Frequency Shift Keying (FSK), Phase Shift Keying (PSK, BPSK, QPSK), Quadrature Amplitude Modulation (QAM).
    * Analog-to-Analog conversion: AM, FM, PM overview.
  * **Bandwidth Utilization**:
    * Multiplexing: Frequency-Division Multiplexing (FDM), Wavelength-Division Multiplexing (WDM), Time-Division Multiplexing (Synchronous TDM vs Statistical TDM).
    * Spread Spectrum: Frequency Hopping Spread Spectrum (FHSS), Direct Sequence Spread Spectrum (DSSS).
  * **Transmission Media**:
    * **Guided Media**: Twisted-Pair cable (UTP, STP, Categories 5e/6), Coaxial cable, Fiber-Optic cable (Step-Index, Graded-Index, Single-Mode vs Multi-Mode).
    * **Unguided (Wireless) Media**: Radio waves, Microwaves, Infrared transmission.
  * *(Reference: Book 1, Chapter 7)*

---

## 📖 Prescribed Reference Books & Textbooks

<div class="table-wrap">

| Label | Complete Textbook Citation & Editions | Syllabus Coverage |
| :---: | :--- | :--- |
| **Book 1** | **Behrouz A. Forouzan**, *Data Communications and Networking with TCP/IP Protocol Suite*, 6th Edition (or 5th/4th), McGraw-Hill Education. *(Core Textbook)* | **Ch 1** (Overview/Layers)<br>**Ch 2** (Application Layer)<br>**Ch 3** (Transport Layer)<br>**Ch 4 & 8** (Network Layer & QoS)<br>**Ch 5** (Data Link Layer)<br>**Ch 6** (Wireless/Mobile IP)<br>**Ch 7** (Physical Layer)<br>**Ch 9** (SNMP & ASN.1) |
| **Book 2** | **W. Richard Stevens, Bill Fenner, Andrew M. Rudoff**, *UNIX Network Programming, Volume 1: The Sockets Networking API*, 3rd Edition, Addison-Wesley / Pearson. *(Systems/Sockets)* | **Ch 3 to 6** (TCP Sockets, Multiplexing `select`/`poll`)<br>**Ch 8** (UDP Sockets)<br>**Ch 14** (Advanced I/O Functions)<br>**Ch 29** (`SOCK_PACKET` / `PF_PACKET`) |
| **Book 3** | **Christian Benvenuti**, *Understanding Linux Network Internals*, 1st Edition, O'Reilly Media. *(Kernel Internals)* | **Ch 14** (Linux Kernel Implementation of Routing Table & Caches, `ip route` operations) |

</div>

::: callout-intuition Supplementary Reference Texts
Students aiming for top competitive scores (GATE CS / KTU S-Grade) are also encouraged to reference **James F. Kurose and Keith W. Ross**, *Computer Networking: A Top-Down Approach*, Pearson, for intuitive protocol diagrams and realistic trace analysis.
:::

---

## ⚖️ Course Assessment Method (CIE & ESE)

The evaluation is split into **40 Marks for Continuous Internal Evaluation (CIE)** and **60 Marks for the University End Semester Examination (ESE)**, totaling 100 Marks.

### Continuous Internal Evaluation (CIE: 40 Marks)

<div class="table-wrap">

| Component | Marks Allocated | Evaluation Criteria & Format |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. Awarded on a sliding scale as per KTU academic regulations. |
| **Assignment / Microproject** | **15 Marks** | Minimum of two rigorous written assignments, or one integrated socket programming microproject (e.g., concurrent TCP chat server, raw packet sniffer, or protocol simulator). |
| **Internal Examination - 1 (Written)** | **10 Marks** | Centralized written test covering **Module 1 and first half of Module 2** (scaled to 10 marks). |
| **Internal Examination - 2 (Written)** | **10 Marks** | Centralized written test covering **second half of Module 2, Module 3, and Module 4** (scaled to 10 marks). |
| **Total CIE Marks** | **40 Marks** | **Eligibility Rule: A student must secure a minimum of 45% (18/40 marks) in CIE to appear for the End Semester Examination.** |

</div>

---

### End Semester Examination (ESE: 60 Marks)

* **Total Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Total Paper Valuation**: **96 Marks** (Students answer for a maximum of **60 Marks**)
* **Passing Requirement**: **Minimum 40% (24/60 marks) in ESE AND minimum 50% aggregate (50/100) combining CIE + ESE**.

<div class="table-wrap">

| Section | Question Format & Mark Distribution | Choice Rules | Total Marks |
| :---: | :--- | :--- | :---: |
| **Part A** | • **2 Questions from each module** (Modules 1, 2, 3, 4).<br>• Total of **8 Questions** (Questions 1 to 8).<br>• Each question carries **3 marks** ($8 \times 3 = 24$). | **Compulsory**<br>*(No internal choice)* | **24 Marks** |
| **Part B** | • **Two full questions from each module** (Questions 9 & 10 from M1, 11 & 12 from M2, 13 & 14 from M3, 15 & 16 from M4).<br>• Each full question carries **9 marks** ($4 \times 9 = 36$).<br>• Each full question can have **maximum 3 subdivisions** (e.g., 5+4, 6+3, or 3+3+3). | **Choice-based**<br>*(Answer any 1 full question from each module)* | **36 Marks** |
| **Total** | **Part A (24 Marks) + Part B (36 Marks)** | | **60 Marks** |

</div>

---

## 🎓 Course Outcomes (COs)

At the completion of the Computer Networks course, the student will demonstrate mastery across the following outcomes evaluated using **Bloom's Revised Taxonomy**:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Understand** the internetworking design in terms of protocol stack and the role of various application layer protocols. | **K2 (Understand)** |
| **CO2** | **Illustrate** the functions of the transport layer from connectionless and connection-oriented perspectives. | **K3 (Apply)** |
| **CO3** | **Identify** how the network layer achieves host-to-host connectivity and caters to the diverse service requirements of the host applications. | **K3 (Apply)** |
| **CO4** | **Explain** the nuances of the data link layer design and **demonstrate** the various data link layer protocols. | **K3 (Apply)** |
| **CO5** | **Describe** the fundamental characteristics of the physical layer and **understand** how the physical layer supports the functionalities of the top layers. | **K2 (Understand)** |

</div>

::: callout-formula Bloom's Revised Taxonomy Levels Key
* **K1 - Remember**: Recalling fundamental definitions, port numbers, frame fields, and RFC standards.
* **K2 - Understand**: Explaining protocol mechanics, comparing sliding window algorithms, summarizing architectural layers.
* **K3 - Apply**: Computing subnet masks, tracing routing tables, writing socket programs, calculating CRC remainders and Nyquist/Shannon bounds.
* **K4 - Analyse**: Diagnosing packet drops, analyzing TCP congestion graphs, identifying network bottlenecks.
* **K5 - Evaluate**: Assessing QoS policies, evaluating security differences between IPv4 vs IPv6 or SNMPv1 vs SNMPv3.
* **K6 - Create**: Designing custom application protocols, engineering resilient multi-homed network topologies.
:::

---

## 🗺️ CO-PO Mapping Table

The Course Outcomes directly map to the **National Board of Accreditation (NBA) Program Outcomes (POs)** for undergraduate computer science and engineering:

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — | — | — |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — | — |
| **CO3** | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-med">2</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — | — |
| **CO5** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — | — | — |

</div>

### CO-PO Mapping Justification & Insights:
* **PO1 (Engineering Knowledge)**: Strongly addressed across all five COs ($\text{Level } 3$) as networking requires applying fundamental mathematics, probability distributions (Poisson/packet arrival), and computing fundamentals.
* **PO2 (Problem Analysis)**: Addressed in CO1, CO2, CO3, CO4, and CO5 through the analysis of throughput, propagation vs transmission delays, count-to-infinity convergence, and channel capacity limits.
* **PO3 (Design/Development of Solutions)**: Addressed in CO2 (Transport Layer socket programming) and CO4 (Link layer protocol design, framing, and CRC polynomial implementation).
* **PO4 (Conduct Investigations of Complex Problems)**: Strongly addressed in CO3 through multicast trees, QoS queuing algorithms, and kernel routing cache evaluations.

---

## ⚡ Interactive Syllabus Self-Check Quiz

::: quiz KTU Examination Scheme Assessment
Under the KTU 2024 scheme for PCCST501 (Computer Networks), how many total questions appear in Part A, what are their individual marks, and are there any choices provided?
(*) 8 questions (2 from each module), each carrying 3 marks (Total 24 marks), all compulsory with no choice.
( ) 5 questions (1 from each module), each carrying 5 marks, with 1 internal choice.
( ) 10 questions, each carrying 2 marks, answer any 8.
( ) 8 questions, each carrying 4 marks, with choice to answer any 6.
::: explanation
According to the official KTU End Semester Examination (ESE) pattern for PCCST501: Part A consists of **8 compulsory questions** (exactly 2 questions selected from each of the 4 modules), each carrying **3 marks**, yielding $8 \times 3 = 24\text{ marks}$. No choice is permitted in Part A. Part B contains the 9-mark questions with 1 out of 2 choice per module.
:::

::: quiz Reference Book & Linux Kernel Systems Topic
Which textbook is specifically designated by the KTU syllabus for studying the Linux Kernel Implementation of Routing Tables, Caches, and the `ip` route command?
(*) Book 3: Christian Benvenuti, Understanding Linux Network Internals (Chapter 14)
( ) Book 1: Behrouz A. Forouzan, Data Communications and Networking
( ) Book 2: W. Richard Stevens, UNIX Network Programming (Chapter 1)
( ) Tanenbaum & Wetherall, Computer Networks
::: explanation
The KTU PCCST501 syllabus explicitly maps Module 2's hands-on Linux networking internals section ("Linux Kernel Implementation of Routing Table and Caches, Routing Cache Implementation Overview, Adding new entry in the Routing Table using ip command") to **Book 3 Chapter 14** (*Christian Benvenuti, Understanding Linux Network Internals*).
:::

---

## 🧭 Next Steps in Your Study Journey

Now that you have reviewed the complete syllabus and examination blueprint:
* Jump straight into **[Module 1: 1.1 Internet Overview & Network Edge](m1_01_internet_overview_and_network_edge.html)** to master protocol layering and network edge fundamentals.
* Practice real-world KTU calculations in the **[Module 1 Workbook: Delays & Throughput](m1_p01_delays.html)**.
* Test your active recall anytime using the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
