# KTU Official Syllabus: Networks Lab (PCCSL507)

Welcome to the official practical syllabus and laboratory examination blueprint for **Networks Lab (PCCSL507)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied branches (Common to CS/CD/CM/CB/CU/CI)**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Networks Lab** |
| **Course Code** | `PCCSL507` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Common to CS / CD / CM / CB / CU / CI)** |
| **Teaching Hours / Week** | **0:0:3:0** *(Lecture: 0, Tutorial: 0, Practical: 3 hrs/week, Remedial: 0)* |
| **Total Practical Hours** | **36–42 Contact Lab Hours (17 Prescribed Experiments)** |
| **Course Credits** | **2 Credits** |
| **Course Type** | **Laboratory (Practical)** |
| **Prerequisites** | **None** |
| **Continuous Internal Evaluation (CIE)** | **50 Marks** *(Continuous Lab Assessment: 25, Lab Test: 20, Attendance: 5)* |
| **End Semester Examination (ESE)** | **50 Marks** *(External Practical Exam with Certified Record)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |

</div>

::: callout-intuition From Wire to Socket: Hands-On Networking
Theoretical understanding of protocol headers, three-way handshakes, and routing algorithms comes alive in the laboratory. By capturing raw Ethernet frames on Wireshark, constructing client-server daemons using BSD socket system calls in C, and configuring virtual enterprise topologies on Cisco Packet Tracer, this lab trains software and infrastructure engineers to diagnose and build resilient network systems.
:::

---

## 🎯 Course Objectives

The primary pedagogical objectives of the laboratory course are:

1. **Hands-On Network Programming**: To provide practical, hands-on experience in network programming using Linux system calls (`socket`, `bind`, `listen`, `accept`, `connect`, `sendto`, `recvfrom`), raw sockets, and command-line diagnostics tools.
2. **Protocols & Routing Simulators**: To comprehend the practical implementation and dissection of network protocols, algorithms, and configuration of network-layer services (Static Routing, RIPv2, OSPF, Access Control Lists, IPv6 with RIPng) using network simulators.

---

## 🧪 Comprehensive List of Lab Experiments

The laboratory curriculum is organized into **4 structured modules**:

1. **Part I: Warm-Up & Linux Networking Utilities** (Experiment 1)
2. **Part II: Wireshark Packet Inspection & Header Analysis** (Experiments 2 – 4)
3. **Part III: Socket Programming in C / Linux** (Experiments 5 – 10)
4. **Part IV: Cisco Packet Tracer Topology & Routing Protocols** (Experiments 11 – 17)

---

### Part I: Warm-Up & Linux Networking Utilities

#### Experiment 1: Linux Command-Line Networking Diagnostics
* **Objective**: Gain proficiency in Linux network inspection, interface management, path tracing, and real-time socket monitoring.
* **Commands to Master**:
  * `ip` / `ifconfig`: Inspecting IP addresses, netmasks, broadcast addresses, and MAC addresses.
  * `nmcli` / `ifplugstatus`: Network manager CLI and link status verification.
  * `ping` / `traceroute` / `mtr`: ICMP echo latency, TTL hop decrement inspection, combined traceroute with real-time ping statistics.
  * `netstat` / `ss`: Active TCP/UDP listening ports, established sockets, PID to socket mapping (`ss -tulpn`).
  * `whois` / `nslookup` / `dig`: Domain registrar lookup and DNS record resolution.
  * `nmap`: Network port scanning, OS detection, and service enumeration.
  * `tcpdump`: Command-line packet sniffer capturing PCAP traffic on specified interfaces (`tcpdump -i eth0 -w dump.pcap`).
  * `speedtest-cli` / `iftop` / `bmon`: Real-time network throughput and bandwidth utilization monitors.

---

### Part II: Wireshark Packet Analysis

::: callout-exam Wireshark Lab Protocol
Before capturing HTTP, SMTP, or DNS traffic, always clear browser caches and local OS resolver caches (`systemd-resolve --flush-caches` on Linux or `ipconfig /flushdns` on Windows) to prevent local cache hits.
:::

#### Experiment 2: Wireshark Analysis of HTTP Protocol
* **Objective**: Capture and dissect web traffic using HTTP filter (`http`).
* **Analytical Inquiries**:
  1. Determine the source IP and destination IP address of the first HTTP `GET` message.
  2. Inspect HTTP Client Accept headers: MIME types (`Accept`), language (`Accept-Language`), compression (`Accept-Encoding`), and character set (`Accept-Charset`).
  3. Extract Request URL and User-Agent identification string.
  4. Identify the Server Response message, status codes (`200 OK`, `304 Not Modified`, `404 Not Found`).
  5. Locate the `Last-Modified` server header timestamp.
  6. Record the `Content-Length` header value.
  7. Compute Round-Trip Latency: calculate time delta between `GET` request transmission and initial response arrival using Wireshark frame timestamps.
  8. Identify the HTTP protocol version (`HTTP/1.1` vs `HTTP/2`).

#### Experiment 3: Wireshark Analysis of Electronic Mail (SMTP)
* **Objective**: Capture end-to-end SMTP mail transaction packets using filter `smtp`.
* **Analytical Inquiries**:
  1. Correlate IP addresses: identify client workstation IP vs remote SMTP mail transfer agent (MTA) IP.
  2. Port inspection: locate client ephemeral source port vs standard server destination port (`25`, `587`, or `465`).
  3. Protocol handshake trace: verify SMTP commands (`HELO`/`EHLO`, `MAIL FROM`, `RCPT TO`, `DATA`, `QUIT`) and three-digit server status reply codes (`220`, `250`, `354`, `221`).
  4. Internet Message Format (IMF): inspect encapsulated MIME mail headers (`Date`, `From`, `To`, `Subject`) and body payload inside the `DATA` stream.

#### Experiment 4: Wireshark Analysis of the Domain Name System (DNS)
* **Objective**: Inspect DNS query and response messages over UDP port 53 using filter `dns`.
* **Analytical Inquiries**:
  1. Packet identification: identify packet frame numbers for initial college domain resolution query and corresponding response.
  2. Transport layer identification: confirm transport protocol (UDP vs TCP).
  3. Port numbers: inspect source ephemeral port and destination port (53).
  4. Resolver destination IP: identify the configured recursive DNS server IP.
  5. Transaction ID: verify matching 16-bit Query Identification number in request and reply.
  6. DNS Flags dissection:
     * Flag length (16 bits).
     * `QR` bit (0 = Query, 1 = Response).
     * Response-specific flag bits: Authoritative Answer (`AA`), Truncated (`TC`), Recursion Desired (`RD`), Recursion Available (`RA`), Reply code / `RCODE` (0 = No error, 3 = NXDOMAIN).
  7. Section count verification: compare counts for Question Records, Answer Records, Authority Records, and Additional Records across query and response.

---

### Part III: Linux Socket Programming (C / BSD Sockets)

#### Experiment 5: Client-Server TCP Matrix Type Classifier
* **Objective**: Implement a connection-oriented TCP socket application.
* **Specification**:
  * **Client**: Prompts user for matrix order $N$, populates an $N \times N$ matrix with random integers in range $[1, 50]$, serializes and transmits the matrix to the server via TCP socket.
  * **Server**: Reads the matrix stream, analyzes structural properties, classifies the matrix into one of:
    * *Upper Triangular Matrix* ($A[i][j] = 0$ for all $i > j$)
    * *Lower Triangular Matrix* ($A[i][j] = 0$ for all $i < j$)
    * *Diagonal Matrix* ($A[i][j] = 0$ for all $i \neq j$)
    * *General Square Matrix*
  * Server responds with the classification string; Client prints the verified result.

#### Experiment 6: Client-Server UDP Gen-Z Slang-to-Formal English Translator
* **Objective**: Implement a connectionless UDP socket application using `sendto()` and `recvfrom()`.
* **Specification**:
  * **Client**: Takes a conversational informal sentence containing internet acronyms from the user and transmits the datagram to the server.
  * **Server**: Parses tokenized words, cross-references an acronym lookup table, and translates recognized abbreviations to formal English before returning the result.
  * Supported dictionary acronyms: `tbh` (to be honest), `ig` (I guess), `tbf` (to be fair), `atm` (at the moment), `irl` (in real life), `lol` (laugh out loud), `asap` (as soon as possible), `omg` (oh my god), `ttyl` (talk to you later), `idk` (I don't know), `nvm` (never mind).
  * *Example*:
    * Input: `"Really idc about this stupid server as it is of no use irl but atm, I will design one, tbf to the professor."`
    * Output: `"Really I don't care about this stupid server as it is of no use in real life but at the moment, I will design one, to be fair to the professor."`

#### Experiment 7: Multi-User Chat Server using TCP
* **Objective**: Implement a multi-client interactive chatroom daemon.
* **Implementation Strategy**:
  * Use I/O Multiplexing (`select()` or `poll()`) OR POSIX Threads (`pthread_create`) to handle multiple concurrent client connections.
  * Client registration, message broadcast engine (re-transmitting incoming messages to all active connected peers except the sender), and clean disconnect cleanup.

#### Experiment 8: Concurrent Time Server Application using UDP
* **Objective**: Implement a concurrent UDP time synchronization server.
* **Specification**: Client sends an empty datagram probe or timestamp request to the remote server; Server fetches system wall-clock time via `time()` and `ctime()`, and replies with the current ISO/formatted timestamp for the client to display.

#### Experiment 9: Concurrent File Server with Process ID (PID)
* **Objective**: Develop a client-server file retrieval service in C.
* **Specification**:
  * Client sends requested filename string.
  * Server checks local filesystem (`access()` / `fopen()`):
    * If file exists, server reads contents in chunks and streams data along with the server worker Process ID (`getpid()`).
    * If file does not exist, server responds with an error diagnostic and its PID.
  * Client displays server PID alongside file content or error notification.

#### Experiment 10: Packet Capturing Application using Raw Sockets
* **Objective**: Build a low-level packet sniffer bypassing transport layers using raw sockets (`socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL))`).
* **Specification**: Unpack Ethernet header (MAC addresses, EtherType), IP header (version, TTL, protocol, Source/Destination IPs), and TCP/UDP header fields directly from the raw byte stream.

---

### Part IV: Cisco Packet Tracer Network Topologies & Routing

#### Experiment 11: Router CLI Navigation & Interface Configuration
* **Router Modes**:
  * User EXEC Mode (`Router>`) $\rightarrow$ Privileged EXEC Mode (`Router#` via `enable`).
  * Global Configuration Mode (`Router(config)#` via `configure terminal`).
* **Essential Commands**:
  * Device information: `show version`, `show running-config`, `show ip interface brief`, `show interfaces`.
  * Clock and history: `show clock`, `show history`.
  * Controller type: `show controllers serial [slot/port]` to identify DTE vs DCE.
  * Interface setup: `interface fastethernet 0/0`, `ip address <ip> <netmask>`, `no shutdown`, `clock rate 64000` (on DCE serial interfaces).
  * Configuration persistence: `copy running-config startup-config` or `write memory`.

#### Experiment 12: Static Routing Implementation
* **Objective**: Interconnect multi-router subnet topology using explicit static routing.
* **Configuration**: `ip route <destination-network> <subnet-mask> <next-hop-ip / exit-interface>`.
* **Verification**: Display routing table (`show ip route`) and verify end-to-end ping reachability across disparate /24 subnets.

#### Experiment 13: Distance-Vector Dynamic Routing using RIPv2
* **Objective**: Configure Routing Information Protocol version 2 (classless, hop-count metric max 15).
* **Configuration**:
  ```text
  Router(config)# router rip
  Router(config-router)# version 2
  Router(config-router)# no auto-summary
  Router(config-router)# network <classful-network-id>
  ```
* **Verification**: `show ip route rip`, `show ip protocols`, packet tracer simulation mode packet exchange.

#### Experiment 14: Link-State Dynamic Routing using OSPF
* **Objective**: Implement Open Shortest Path First (OSPFv2) single-area link-state protocol.
* **Configuration**:
  ```text
  Router(config)# router ospf 1
  Router(config-router)# network <subnet-ip> <wildcard-mask> area 0
  ```
* **Verification**: Verify neighbor relationships (`show ip ospf neighbor`), shortest path first database (`show ip ospf database`), and convergence routing table.

#### Experiment 15: Standard Access Control Lists (ACL) for Host Restriction
* **Scenario**: Campus network where only `Host_B` is permitted to communicate with secure server subnet `172.16.10.0`, while `Lab_B` and `Lab_C` workstations are blocked.
* **Configuration**:
  ```text
  Router(config)# access-list 10 permit host <Host_B_IP>
  Router(config)# access-list 10 deny any
  Router(config)# interface <target-interface>
  Router(config-if)# ip access-group 10 out
  ```
* **Verification**: Verify ping from Host_B succeeds while pings from Lab_B/Lab_C receive ICMP destination unreachable messages.

#### Experiment 16: Extended Access Control Lists (ACL) for Port-Specific Website Blocking
* **Scenario**: College network `140.80.0.0/20` with 20 subnets. The Central Computing Facility (CCF) is in Subnet 4. An inter-department hackathon registration server is assigned the 7th IP in Subnet 16. Block students in CCF from accessing the hackathon web server (HTTP port 80 / HTTPS 443) while permitting all other services (SSH, Ping, FTP).
* **Calculation & Rule Design**:
  * Calculate CIDR boundaries for Subnet 4 and Subnet 16.
  * Formulate Extended ACL blocking TCP traffic to destination server IP on port 80/443 while adding `permit ip any any` fallback.
* **Verification**: Web browser connection to server IP fails; ICMP ping to server IP continues to succeed.

#### Experiment 17: IPv6 Network Interconnection using RIPng
* **Objective**: Interconnect multi-router IPv6 subnets using Next Generation RIP (RIPng).
* **Configuration**:
  ```text
  Router(config)# ipv6 unicast-routing
  Router(config)# interface <interface-id>
  Router(config-if)# ipv6 address <ipv6-prefix>/64
  Router(config-if)# ipv6 rip MY_RIP enable
  ```
* **Verification**: `show ipv6 route rip`, verify ping across 128-bit IPv6 link-local and global unicast endpoints.

---

## ⚖️ Course Assessment Method (CIE: 50 Marks, ESE: 50 Marks)

### Continuous Internal Evaluation (CIE: 50 Marks)

<div class="table-wrap">

| Component | Marks Allocated | Evaluation Details |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. |
| **Continuous Assessment** | **25 Marks** | Continuous assessment averaged across all 17 lab sessions: |
| ↳ *1. Preparation & Pre-Lab Work* | *(7 Marks)* | Pre-lab assignments, conceptual quizzes, algorithm readiness. |
| ↳ *2. Conduct of Experiments* | *(7 Marks)* | Adherence to procedures, correct coding, troubleshooting skill, teamwork. |
| ↳ *3. Lab Reports & Record Keeping* | *(6 Marks)* | Completeness of rough record, prompt submission of certified fair record. |
| ↳ *4. Lab Viva Voce* | *(5 Marks)* | Oral defense of experiment logic, system calls, and protocol headers. |
| **Internal Lab Examination** | **20 Marks** | Model practical test (programming, execution, packet analysis, viva). |
| **Total CIE Marks** | **50 Marks** | **Minimum 45% (23/50 marks) in CIE required for ESE eligibility.** |

</div>

---

### End Semester Examination (ESE: 50 Marks)

* **Examination Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Certified Record Requirement**: Duly certified laboratory record signed by the faculty-in-charge and external examiner is mandatory for exam entry.

<div class="table-wrap">

| Sl. No. | Evaluation Stage | Marks | Assessment Rubric |
| :---: | :--- | :---: | :--- |
| **1** | **Procedure / Preparatory Work / Design / Algorithm** | **10 Marks** | Clarity of procedure, flowchart/algorithm correctness, network topology sketch, subnetting calculations. |
| **2** | **Conduct of Experiment / Execution / Troubleshooting / Programming** | **15 Marks** | Setup of hardware/Packet Tracer, bug-free C socket code, appropriate system call usage, proper syntax. |
| **3** | **Result with Valid Inference / Quality of Output** | **10 Marks** | Accuracy of packet capture analysis, successful client-server execution, routing convergence verification. |
| **4** | **Viva Voce** | **10 Marks** | Comprehensive oral examination testing theoretical foundations, socket flags, Wireshark headers, and routing protocols. |
| **5** | **Lab Record** | **5 Marks** | Neatness, completeness, and accuracy of endorsed lab record. |
| **Total** | **End Semester Practical Examination** | **50 Marks** | **Minimum 40% (20/50 marks) required in ESE.** |

</div>

---

## 📖 Prescribed Textbooks & Reference Books

### Prescribed Core Textbooks

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Unix Network Programming, Volume 1: The Sockets Networking API** | **W. Richard Stevens, Andrew M. Rudoff, Bill Fenner** | **Pearson Education** | **3rd Edition, 2004** |
| **2** | **CCNA Cisco Certified Network Associate Study Guide** | **Todd Lammle** | **Wiley** | **6th Edition, 2007** |
| **3** | **Beej's Guide to Network Programming: Using Internet Sockets** | **Brian "Beej Jorgensen" Hall** | **Amazon Digital Services** | **2019** |

</div>

### Prescribed Reference Books

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Computer Networks: A Top-Down Approach** | Behrouz A. Forouzan | McGraw Hill | SIE Edition, 2017 |
| **2** | **Computer Networking: A Top-Down Approach Featuring the Internet** | J. F. Kurose, K. W. Ross | Pearson Education | 8th Edition, 2022 |

</div>

---

## 🎥 Video Lectures & Online Lab Tutorials

<div class="table-wrap">

| Platform | Course ID / Link | Focus Areas |
| :---: | :--- | :--- |
| **NPTEL / IIT Kharagpur** | [Computer Networks and Internet Protocol (Course 106106091)](https://nptel.ac.in/courses/106106091) | Wireshark packet traces, socket programming paradigms, and routing algorithms. |

</div>

---

## 🎓 Course Outcomes (COs)

Upon successful completion of the Networks Lab, students will demonstrate mastery across the following outcomes:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Understand** the working of application layer protocols by analyzing the pertinent headers in actual data packets captured using network monitoring tools. | **K3 (Apply)** |
| **CO2** | **Exploit** the client-server paradigm to develop real-time networking applications using transport layer protocols. | **K3 (Apply)** |
| **CO3** | **Employ** IPv4 and IPv6 addressing, subnetting to efficiently design networks. | **K3 (Apply)** |
| **CO4** | **Simulate** core networking concepts using a network simulator. | **K3 (Apply)** |

</div>

---

## 🗺️ CO-PO Mapping Table

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | <span class="matrix-high">3</span> |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-med">2</span> | — | — | — | — | — | — | <span class="matrix-high">3</span> |
| **CO3** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | <span class="matrix-high">3</span> |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | <span class="matrix-high">3</span> |

</div>

---

## ⚡ Interactive Lab Self-Check Quiz

::: quiz Socket Programming: TCP vs UDP Primitives
In Linux BSD socket programming (Experiments 5 & 6), which sequence of system calls is strictly required on the server side for a connection-oriented TCP daemon, compared to a connectionless UDP daemon?
(*) TCP requires socket() -> bind() -> listen() -> accept() -> recv()/send(), whereas UDP only requires socket() -> bind() -> recvfrom()/sendto().
( ) Both TCP and UDP servers require listen() and accept() before receiving data.
( ) UDP servers must execute connect() before calling recvfrom().
( ) TCP servers do not require bind(), only socket() and accept().
::: explanation
A **TCP server** is connection-oriented and must create an endpoint (`socket()`), assign a local port (`bind()`), enter a passive listening state with a connection backlog queue (`listen()`), and block waiting for incoming three-way handshakes (`accept()`), which returns a dedicated connected socket file descriptor. A **UDP server** is connectionless; it simply binds to a port and immediately waits for incoming datagrams using `recvfrom()`, requiring neither `listen()` nor `accept()`.
:::

::: quiz Cisco Packet Tracer: Standard vs Extended ACLs
In Experiments 15 and 16, what is the fundamental technical difference between Standard ACLs (1–99) and Extended ACLs (100–199) when filtering network traffic?
(*) Standard ACLs filter traffic based solely on Source IP address and should be placed close to the destination; Extended ACLs can filter based on Source IP, Destination IP, Protocol (TCP/UDP/ICMP), and Port numbers (e.g., port 80/443), and should be placed close to the source.
( ) Standard ACLs can inspect HTTP payload data, while Extended ACLs only filter MAC addresses.
( ) Standard ACLs are only for IPv6, whereas Extended ACLs are only for IPv4.
( ) Standard ACLs deny all traffic by default, whereas Extended ACLs permit everything unless configured otherwise.
::: explanation
**Standard ACLs** (numbered 1–99 or named standard) inspect only the **source IP address**; because of this coarse granularity, they are placed as close to the destination as possible. **Extended ACLs** (numbered 100–199 or named extended) filter on **source IP, destination IP, protocol type (TCP, UDP, ICMP), and destination port numbers** (such as HTTP port 80 or DNS port 53 in Experiment 16). Extended ACLs are placed as close to the traffic source as possible to save network bandwidth.
:::

---

## 🧭 Next Steps in Your Study Journey

* Master application layer protocols with **[Computer Networks Module 1: Application Layer Protocols](../PCCST501/m1_01_application_layer_paradigms_and_http.html)**.
* Practice socket mechanics with **[Computer Networks Module 2: Socket Programming in C](../PCCST501/m2_04_socket_programming_in_c.html)**.
* Review key commands and protocols in the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
