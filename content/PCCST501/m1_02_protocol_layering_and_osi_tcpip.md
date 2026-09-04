# Protocol Layering, 5-Layer Stack & The OSI Model

> **Course Code:** PCCST501 / CST303 — Computer Networks  
> **Target Audience:** APJ Abdul Kalam Technological University (KTU) B.Tech Computer Science & Engineering  
> **Module Coverage:** Module 1 (Lecture 2) — Abstraction, Encapsulation, Decapsulation, and Protocol Data Units (PDUs)  

---

## Quick Navigation Anchors
- [The Intuition](#the-intuition)
- [The 5-Layer Internet Protocol Stack](#the-5-layer-stack)
- [The 7-Layer OSI Reference Model](#the-7-layer-osi-model)
- [OSI vs. TCP/IP Comparative Architecture](#comparative-matrix)
- [Encapsulation & Decapsulation Mechanics](#encapsulation-decapsulation)
- [Device Inspection Depths: Host vs Router vs Switch](#device-inspection)
- [KTU Exam Focus & Traps](#exam-focus-traps)
- [Active Recall Checkpoint](#self-check)

---

## The Intuition

::: callout-intuition Core Mental Model: International Postal & Diplomatic Baggage
Consider how an ambassador in New Delhi sends a classified treaty to an ambassador in Paris:
1. **Diplomat (Application Layer):** Writes the treaty text in a formal language and requests dispatch.
2. **Confidential Secretary (Presentation & Session Layer):** Translates the text into an agreed cipher (encryption), binds it into a tracked diplomatic session, and places it inside a labeled envelope.
3. **Embassy Dispatch Officer (Transport Layer):** Assigns a sequence number and acknowledgment slip, splitting thick annexures into numbered parcels ($1$ of $3$, $2$ of $3$, $3$ of $3$) to guarantee none are lost in transit.
4. **Chancery Courier (Network Layer):** Affixes global postal routing slips with country/city destination coordinates (logical addresses) and hands them over to international logistics.
5. **Air Cargo Logistics (Data Link Layer):** Places the parcels into an airfreight crate tagged for the direct flight from Indira Gandhi International (DEL) to Charles de Gaulle (CDG) (hop-to-hop physical framing).
6. **Aircraft / Jet Fuel (Physical Layer):** Converts the crate into physical mass transported across aerial geographic space using kinetic energy.

**Why Layering Matters:** If Air France replaces its aircraft fleet with high-speed cargo trains through the Channel Tunnel, the *ambassador does not rewrite the treaty*, nor does the *chancery courier change destination addresses*. Layering decouples high-level service logic from low-level physical implementation. An internal change in one layer does not affect adjacent layers, provided the standardized interface between them remains unchanged.
:::

---

## The 5-Layer Stack

The modern Internet operates on the **5-Layer Internet Protocol Stack** (often termed the TCP/IP or Internet reference model).

```
+--------------------------------------------------------------------+
|  Layer 5: Application Layer  --> Messages                          |
+--------------------------------------------------------------------+
|  Layer 4: Transport Layer    --> Segments (TCP) / Datagrams (UDP)  |
+--------------------------------------------------------------------+
|  Layer 3: Network Layer      --> Datagrams / Packets               |
+--------------------------------------------------------------------+
|  Layer 2: Data Link Layer    --> Frames                            |
+--------------------------------------------------------------------+
|  Layer 1: Physical Layer     --> Raw Bits                          |
+--------------------------------------------------------------------+
```

### 1. Application Layer (Layer 5)
* **Core Responsibility:** Provides the interface for network-aware user applications to exchange messages across distributed systems. Implemented entirely in software within the operating system's user space.
* **Protocol Data Unit (PDU):** **Message**
* **Key Protocols:**
  * $\text{HTTP}$ (HyperText Transfer Protocol) — Web browsing
  * $\text{DNS}$ (Domain Name System) — Hostname-to-IP resolution
  * $\text{SMTP}$ (Simple Mail Transfer Protocol) — Electronic mail transfer
  * $\text{FTP}$ (File Transfer Protocol) — File exchange

### 2. Transport Layer (Layer 4)
* **Core Responsibility:** Provides **process-to-process communication** between running application entities across end systems. Accomplishes this using **Port Numbers** (16-bit identifiers) to direct incoming data to the correct process.
* **Protocol Data Unit (PDU):** **Segment** (for $\text{TCP}$) / **Datagram** (for $\text{UDP}$)
* **Key Protocols:**
  * $\text{TCP}$ (Transmission Control Protocol): Connection-oriented, reliable in-order byte stream delivery, flow control (sliding window), and network congestion control.
  * $\text{UDP}$ (User Datagram Protocol): Connectionless, lightweight, unreliable, unordered datagram delivery with zero connection setup overhead (used by real-time voice, video streaming, and $\text{DNS}$).

### 3. Network Layer (Layer 3)
* **Core Responsibility:** Provides **host-to-host delivery** across multiple heterogeneous network links. Responsible for **logical addressing** ($\text{IP}$ addresses) and **routing** (determining the optimal path packets should follow from source to destination using distributed routing protocols like $\text{OSPF}$, $\text{BGP}$).
* **Protocol Data Unit (PDU):** **Datagram** (or **Packet**)
* **Key Protocols:**
  * $\text{IPv4}$ (32-bit addressing) and $\text{IPv6}$ (128-bit addressing)
  * $\text{ICMP}$ (Internet Control Message Protocol) — Network diagnostics and error notifications (e.g., `ping`, `traceroute`)
  * Routing protocols ($\text{OSPF}$, $\text{RIP}$, $\text{BGP}$)

### 4. Data Link Layer (Layer 2)
* **Core Responsibility:** Moves complete datagrams across an individual communication link from one node (host or router) to the immediately adjacent next node. Handles **physical addressing** ($\text{MAC}$ addresses), **framing**, link-level error detection (via $\text{CRC}$ checksums), and media access control ($\text{MAC}$) on shared broadcast media.
* **Protocol Data Unit (PDU):** **Frame**
* **Key Protocols:** $\text{Ethernet}$ ($\text{IEEE 802.3}$), $\text{Wi-Fi}$ ($\text{IEEE 802.11}$), Point-to-Point Protocol ($\text{PPP}$), High-Level Data Link Control ($\text{HDLC}$).

### 5. Physical Layer (Layer 1)
* **Core Responsibility:** Transmits individual **raw bits** over physical transmission media. Defines the mechanical, electrical, functional, and procedural standards for encoding digital bits ($0$s and $1$s) into physical signals (voltages, optical pulses, or radio waves).
* **Protocol Data Unit (PDU):** **Bit**
* **Key Standards:** $\text{1000BASE-T}$, $\text{10GBASE-LR}$, $\text{EIA/TIA-232}$, $\text{DSL}$, $\text{802.11 physical layer specs}$.

---

## The 7-Layer OSI Model

Developed by the **International Organization for Standardization (ISO)**, the **Open Systems Interconnection (OSI)** model is a theoretical 7-layer framework. While the Internet protocol stack collapsed or offloaded some of these functions, understanding the OSI model is essential for architectural and protocol design.

```
       7-LAYER OSI MODEL                     5-LAYER TCP/IP STACK
+-----------------------------+           +-------------------------+
|  Layer 7: Application       |           |                         |
+-----------------------------+           |                         |
|  Layer 6: Presentation      |  ======>  |  Layer 5: Application   |
+-----------------------------+           |                         |
|  Layer 5: Session           |           |                         |
+-----------------------------+           +-------------------------+
|  Layer 4: Transport         |  ======>  |  Layer 4: Transport     |
+-----------------------------+           +-------------------------+
|  Layer 3: Network           |  ======>  |  Layer 3: Network       |
+-----------------------------+           +-------------------------+
|  Layer 2: Data Link         |  ======>  |  Layer 2: Data Link     |
+-----------------------------+           +-------------------------+
|  Layer 1: Physical          |  ======>  |  Layer 1: Physical      |
+-----------------------------+           +-------------------------+
```

### The Two Additional OSI Layers

#### 1. Presentation Layer (OSI Layer 6)
Focuses on the syntax and semantics of information exchanged between end systems.
* **Data Translation & Formatting:** Translates differing internal character encodings between heterogeneous computer architectures (e.g., $\text{ASCII}$ to $\text{EBCDIC}$, Big-Endian to Little-Endian conversion).
* **Data Compression:** Reduces the volume of bits requiring transmission across the physical medium (e.g., run-length encoding, Huffman coding, lossy image/audio formats).
* **Encryption & Decryption:** Provides cryptographic data protection to ensure confidentiality and integrity (e.g., $\text{TLS/SSL}$ functionality, though modern implementations execute this within the application/transport interface).

#### 2. Session Layer (OSI Layer 5)
Establishes, manages, and terminates dialogs and communication sessions between cooperating network applications.
* **Dialog Control:** Manages whether communication is half-duplex (alternating turns) or full-duplex (simultaneous two-way transmission).
* **Token Management:** Prevents multiple parties from attempting the same critical operation simultaneously by circulating logical authorization tokens.
* **Synchronization Points (Checkpoints):** Injects checkpoints into long data streams (such as multi-gigabyte file transfers). If an underlying network failure crashes the connection midway through a transfer, transmission resumes from the last confirmed checkpoint rather than restarting from byte zero.

---

## Comparative Matrix

| Feature / Dimension | OSI 7-Layer Reference Model | TCP/IP 5-Layer Protocol Model |
| :--- | :--- | :--- |
| **Origin & Genesis** | Developed by ISO as a formal conceptual blueprint prior to widespread protocol deployment. | Developed by DARPA/DoD based on working operational software implementations (ARPANET). |
| **Number of Layers** | 7 Distinct Layers. | 5 Layers (or 4 in classic RFC 1122 categorization). |
| **Presentation & Session** | Distinct, formally isolated architectural layers. | Absent as standalone layers; implemented directly inside user-space application code if required. |
| **Service Decoupling** | Strict distinction between Services, Interfaces, and Protocols. | Looser boundaries; protocols were written first, and the model merely described existing behavior. |
| **Transport Reliability** | Supports both connectionless and connection-oriented services. | Explicit choice between $\text{TCP}$ (reliable/connection-oriented) and $\text{UDP}$ (unreliable/connectionless). |
| **Network Layer Service** | Designed to support both Connectionless (CLNP) and Connection-Oriented (CONS / X.25). | Exclusively **Connectionless** ($\text{IP}$). Every packet is routed independently. |
| **Real-world Adoption** | Historically marginalized; used predominantly as a conceptual teaching and diagnostic reference. | The universally dominant commercial standard driving global telecommunications and the Internet. |

---

## Encapsulation Decapsulation

Data moves down the stack at the sending host, across intermediate networking infrastructure, and up the stack at the receiving host.

### The Encapsulation Lifecycle

```
SENDING HOST                                                   RECEIVING HOST
[ Application ]        Application Message (M)                 [ Application ]
       |                                                              ^
       v                                                              |
[  Transport  ]        [ Ht |          M          ]            [  Transport  ]
       |                      Segment                                 ^
       v                                                              |
[   Network   ]        [ Hn | Ht |     M     ]                 [   Network   ]
       |                      Datagram                                ^
       v                                                              |
[  Data Link  ]  [ Hl | Hn | Ht |      M      | Tl ]           [  Data Link  ]
       |                      Frame                                   ^
       v                                                              |
[  Physical   ]  01101001011000110111010001100101              [  Physical   ]
                         Raw Physical Bits
```

* **Encapsulation (Sender side):**
  1. The **Application Layer** generates an application-specific message $M$.
  2. The **Transport Layer** prepends a transport header $H_t$ containing source and destination port numbers, sequence numbers, and checksums, yielding a **Segment** $[H_t \mid M]$.
  3. The **Network Layer** prepends a network header $H_n$ containing source and destination logical $\text{IP}$ addresses, Time-to-Live ($\text{TTL}$), and protocol flags, yielding a **Datagram** $[H_n \mid H_t \mid M]$.
  4. The **Data Link Layer** prepends a link header $H_l$ containing source and destination physical $\text{MAC}$ addresses and appends a link trailer $T_l$ containing a Cyclic Redundancy Check ($\text{CRC}$) for hardware error detection, yielding a **Frame** $[H_l \mid H_n \mid H_t \mid M \mid T_l]$.
  5. The **Physical Layer** serializes the frame bits into physical waveforms or optical pulses and injects them onto the medium.

* **Decapsulation (Receiver side):** Each ascending layer strips its corresponding header, parses the control fields, verifies integrity, and delivers the payload to the appropriate protocol entity above it.

---

## Device Inspection

Not all network entities process the full 5-layer protocol stack. Devices are categorized by the highest layer header they are designed to inspect and process during standard packet transit.

```
+-------------------------------------------------------------------------------+
|                       DEVICE PROCESSING HIERARCHY                             |
+-------------------------------------------------------------------------------+

  END SYSTEM (HOST)           CORE ROUTER               LINK-LAYER SWITCH
+-------------------+     +-----------------+          +-----------------+
| Application (L5)  |     |                 |          |                 |
| Transport   (L4)  |     |                 |          |                 |
| Network     (L3)  |     | Network    (L3) |          |                 |
| Data Link   (L2)  |     | Data Link  (L2) |          | Data Link  (L2) |
| Physical    (L1)  |     | Physical   (L1) |          | Physical   (L1) |
+-------------------+     +-----------------+          +-----------------+
```

### 1. End Systems (Hosts) — Full 5-Layer Stack
Hosts run application processes. They originate and terminate packets, executing logic across all 5 layers: from generating application messages down to transmitting bits, and vice-versa.

### 2. Routers (Layer 3 Packet Switches)
A standard Internet router operates up through **Layer 3 (Network Layer)**:
* **Layer 1:** Receives physical signals and reconstitutes the incoming link-layer frame.
* **Layer 2:** Strips the Link Layer header $H_l$ and trailer $T_l$, verifying frame integrity via the $\text{CRC}$.
* **Layer 3:** Inspects the destination $\text{IP}$ address in header $H_n$, performs a routing table lookup, decrements the $\text{TTL}$ counter, recalculates the $\text{IPv4}$ header checksum, determines the outbound interface, encapsulates the datagram into a *new* Layer 2 frame with new source and destination $\text{MAC}$ addresses, and queues it for transmission.
* *Note:* Standard routers do **not** inspect or alter Transport headers ($H_t$) or Application payloads ($M$).

### 3. Switches (Layer 2 Link-Layer Switches)
A standard Ethernet switch operates up through **Layer 2 (Data Link Layer)**:
* **Layer 1:** Receives raw electrical/optical bitstreams from a port.
* **Layer 2:** Parses the incoming frame header $H_l$, reads the destination $\text{MAC}$ address, looks up the port mapping in its internal $\text{MAC}$ address table (Forwarding Information Base), and switches the intact frame directly to the designated egress port.
* *Note:* Switches do **not** inspect $\text{IP}$ addresses or alter $\text{IP}$ headers.

---

## Exam Focus & Traps

::: callout-formula Protocol Data Unit Mapping
Remember this exact layer-to-PDU terminology mapping:

$$\begin{aligned}
\text{Application Layer (L5 / L7)} &\iff \mathbf{Message} \\
\text{Transport Layer (L4)} &\iff \mathbf{Segment} \text{ (TCP) / } \mathbf{Datagram} \text{ (UDP)} \\
\text{Network Layer (L3)} &\iff \mathbf{Datagram} \text{ (or Packet)} \\
\text{Data Link Layer (L2)} &\iff \mathbf{Frame} \\
\text{Physical Layer (L1)} &\iff \mathbf{Bit}
\end{aligned}$$
:::

::: callout-pitfall Layer Inversion Trap
* **Trap 1: Claiming standard Layer 2 Switches inspect IP Addresses.**
  * *Error:* "A switch reads the destination IP address to determine which host receives the packet."
  * *Correction:* Layer 2 switches are strictly Link-Layer devices. They inspect **only MAC addresses** found in the Layer 2 frame header $H_l$. They have no awareness of IP datagram structures or IP addresses.
* **Trap 2: Claiming Routers modify Application Payloads.**
  * *Error:* "A router decrypts or compresses the message during transit."
  * *Correction:* Routers inspect up to Layer 3. They strip and rebuild Layer 2 frames and modify select Layer 3 header fields (specifically decrementing $\text{TTL}$ and updating the header checksum). They treat the Transport header and Application data as an opaque, untouchable byte payload.
* **Trap 3: Believing the Data Link Layer only prepends a Header.**
  * *Error:* Forgetting the trailer during encapsulation drawings.
  * *Correction:* The Data Link layer is unique: it prepends a **Header ($H_l$)** containing addressing and control fields *and* appends a **Trailer ($T_l$)** containing the Frame Check Sequence ($\text{FCS}$ / $\text{CRC}$) for error detection.
:::

::: callout-exam KTU Typical 7/14-Mark Questions
1. **7-Mark Architecture Question:**
   * *Draw the 7-layer OSI reference model and explain the primary functions of each layer. State the PDU at each level.*
   * *Explain the concept of protocol encapsulation and decapsulation with a neat diagram tracing an Application message to the Physical medium.*
2. **14-Mark Comprehensive Question:**
   * *(a) Compare and contrast the 7-layer OSI model with the 5-layer TCP/IP protocol stack. Explain why the OSI model failed commercially while TCP/IP succeeded.*
   * *(b) Explain the specific responsibilities of the Presentation and Session layers of the OSI model, detailing why they were omitted from the core TCP/IP stack.*
   * *(c) Trace the path of an HTTP GET request from a client to a server, identifying which layers are processed by intermediate switches, routers, and the destination host.*
:::

---

## Self-Check

::: quiz PDU Terminology
Which of the following correctly pairs the layer with its corresponding Protocol Data Unit (PDU)?
(A) Transport $\rightarrow$ Frame; Network $\rightarrow$ Segment; Data Link $\rightarrow$ Datagram
(*B) Transport $\rightarrow$ Segment; Network $\rightarrow$ Datagram; Data Link $\rightarrow$ Frame
(C) Transport $\rightarrow$ Packet; Network $\rightarrow$ Frame; Data Link $\rightarrow$ Byte
(D) Transport $\rightarrow$ Datagram; Network $\rightarrow$ Message; Data Link $\rightarrow$ Bit
::: explanation
The standard protocol data unit terminology is:
* Application Layer: **Message**
* Transport Layer: **Segment** (TCP) or **Datagram** (UDP)
* Network Layer: **Datagram** or **Packet**
* Data Link Layer: **Frame**
* Physical Layer: **Bit**

Option (B) is the only fully correct mapping.
:::

::: quiz Layer Inspection Depth
When an IP datagram moves across an enterprise local area network through an unmanaged Layer 2 Ethernet switch, what is the highest header level the switch inspects to forward the data?
(A) Layer 3 Network Header ($H_n$) containing the destination IP address
(*B) Layer 2 Data Link Header ($H_l$) containing the destination MAC address
(C) Layer 4 Transport Header ($H_t$) containing the destination TCP port
(D) Layer 1 Physical Preamble bits only
::: explanation
A standard Layer 2 Ethernet switch operates strictly at the Data Link layer. It decapsulates the physical bits into a frame, inspects the **destination MAC address** inside the Layer 2 header ($H_l$), consults its MAC address table, and forwards the frame out the appropriate switch port. It never parses or inspects the Layer 3 IP header ($H_n$).
:::

::: quiz OSI Layer Functionality
A network application requires automated checkpointing and recovery during large data file transfers, so that if a connection drops, transmission can resume from the last known good position. Under the OSI reference model, which layer is conceptually responsible for providing these synchronization checkpoints?
(A) Presentation Layer
(B) Transport Layer
(*C) Session Layer
(D) Data Link Layer
::: explanation
The **Session Layer** (OSI Layer 5) is explicitly responsible for dialog control, token management, and establishing **synchronization points (checkpoints)** within a data stream to facilitate recovery from interruptions. The Presentation layer handles compression/encryption, the Transport layer handles end-to-end reliability and flow control, and the Data Link layer handles adjacent node-to-node framing.
:::
