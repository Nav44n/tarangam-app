# File Transfer Protocol (FTP): Dual Connections & State Management

> **Course Code:** PCCST501 / CST303 — Computer Networks  
> **Target Audience:** APJ Abdul Kalam Technological University (KTU) B.Tech Computer Science & Engineering  
> **Module Coverage:** Module 1 (Lecture 5) — Control Connection vs. Data Connection, Out-of-Band Signaling, Active vs. Passive Mode, and State Maintenance  

---

## Quick Navigation Anchors
- [The Intuition](#the-intuition)
- [Dual-Connection Architecture & Out-of-Band Signaling](#dual-connection)
- [FTP Commands & Reply Status Codes](#commands-replies)
- [Active vs. Passive FTP: Mechanics & NAT Traversal](#active-vs-passive)
- [Architectural State: FTP vs. HTTP](#state-management)
- [KTU Exam Focus & Pitfalls](#exam-focus-pitfalls)
- [Active Recall Checkpoint](#self-check)

---

## The Intuition

::: callout-intuition Core Mental Model: The Walkie-Talkie Dispatcher vs. The Cargo Freight Train
Imagine managing the loading and transit of freight across an industrial railyard:
1. **The In-Band Model (HTTP):**
   * You write your loading instructions on a piece of paper, tape it to the front of a 100-car freight train, and send the train down a single track.
   * If an emergency arises while that heavy train is rolling (e.g., *"Stop the transfer immediately!"* or *"What is the directory status?"*), you cannot easily reach the conductor. Your message is stuck behind hundreds of tons of slow-moving cargo on the exact same physical line.
2. **The Out-of-Band Model (FTP):**
   * You equip the railyard dispatcher with a **dedicated walkie-talkie channel** (the Control Connection) that remains open at all times.
   * Freight trains are assembled, loaded, dispatched, and disassembled on completely **separate railway tracks** (the Data Connection).
   * Even if a massive 50-gigabyte data transfer is occupying a data track, the dispatcher can instantly radio commands over the dedicated walkie-talkie channel: aborting the job (`ABOR`), checking transfer progress, or switching the target directory. 
   * The control commands never have to wait in line behind the bulk payload.
:::

---

<div id="dual-connection"></div>

## Dual-Connection Architecture & Out-of-Band Signaling

The **File Transfer Protocol (FTP)**, standardized under **RFC 959**, transfers files between local and remote file systems. Unlike web protocols that multiplex control data and content onto a single channel, FTP utilizes **two parallel TCP connections**:

```
+---------------------------------------------------------------------------------+
|                                 FTP ARCHITECTURE                                |
+---------------------------------------------------------------------------------+

       CLIENT HOST                                            SERVER HOST
+------------------------+                             +------------------------+
|  User Interface        |                             |                        |
|           |            |                             |                        |
|     [Control Process]  | <=== TCP Port 21 (Control) => |  [Server Protocol]     |
|                        |      (Persistent / 7-bit)   |      Interpreter (PI)  |
|                        |                             |           |            |
|     [Data Transfer]    | <=== TCP Port 20 (Data) ===>|  [Data Transfer]       |
|      Process (DTP)     |      (Non-Persistent)       |   Process (DTP)        |
|           |            |                             |           |            |
|      [Local Disk]      |                             |     [Remote Disk]      |
+------------------------+                             +------------------------+
```

### 1. The Control Connection (Port 21)
* **Purpose:** Exchanging administrative control signals—user authentication, navigation of directory structures, transfer commands, and server status codes.
* **Characteristics:**
  * Initiated by the client to **Server Port 21**.
  * **Persistent:** Remains established and open for the entire duration of the client's session.
  * Carries lightweight 7-bit ASCII text commands and 3-digit reply numbers.
  * **Does not carry any file payload or directory listings.**

### 2. The Data Connection (Port 20 in Active Mode)
* **Purpose:** Moving the actual binary or text file payload, as well as multi-line directory listings (`LIST`).
* **Characteristics:**
  * **Non-Persistent:** Spawned dynamically on-demand each time a file transfer or directory listing is invoked.
  * Tears down immediately once the requested object transfer is complete.
  * If a user transfers 10 separate files in a single session, **10 distinct data TCP connections** are opened and closed, while the single control connection remains open throughout.

### 3. Out-of-Band vs. In-Band Signaling
* **In-Band (e.g., HTTP):** Control information (request headers like `GET`, `User-Agent`, and response status codes like `200 OK`) travels inside the exact same TCP stream as the payload data itself. Headers sit directly in front of the object payload.
* **Out-of-Band (FTP):** Control messages are segregated onto a completely independent TCP connection from the data stream. Because control information bypasses the data queue entirely, FTP is categorized as an **Out-of-Band protocol**.

---

<div id="commands-replies"></div>

## FTP Commands & Reply Status Codes

FTP commands and replies are human-readable ASCII text strings transmitted over the control connection, structured similarly to SMTP and HTTP lines terminated by `\r\n`.

### Common Client Control Commands

| Command | Argument | Functional Description |
| :--- | :--- | :--- |
| `USER` | `username` | Identifies the client user to the remote server. |
| `PASS` | `password` | Delivers the authentication secret for the specified user. |
| `LIST` | `[directory]` | Requests a list of files in the current working remote directory (sent over a freshly spawned **data connection**). |
| `RETR` | `filename` | **Retrieve:** Instructs the remote server to transmit a copy of the specified file back to the client via a data connection. |
| `STOR` | `filename` | **Store:** Instructs the remote server to accept data arriving over the data connection and write it to disk under the specified name. |
| `CWD` | `directory` | **Change Working Directory:** Changes the current working directory on the server file system without altering the control link. |
| `PORT` | `h1,h2,h3,h4,p1,p2` | Informs the server of the client's IP and ephemeral port for Active Mode data connections. |
| `PASV` | *None* | Requests the server to enter Passive Mode and listen on an unreserved data port. |
| `QUIT` | *None* | Requests graceful teardown of the persistent control connection. |

### Common Server Reply Codes

Server status responses consist of a 3-digit integer followed by optional human-readable descriptive text:

* **`150 File status okay; about to open data connection.`** — Precedes data transmission.
* **`200 Command okay.`** — Generic operational success.
* **`220 Service ready for new user.`** — Emitted by server upon initial connection to port 21.
* **`226 Closing data connection; requested file action successful.`** — Emitted over the control connection once data transmission terminates on the parallel data connection.
* **`230 User logged in, proceed.`** — Authentication successful.
* **`331 User name okay, need password.`** — Challenges the client to issue the `PASS` command.
* **`425 Can't open data connection.`** — Network/firewall error during data setup.
* **`550 Requested action not taken; file unavailable.`** — File not found or permission denied.

---

<div id="active-vs-passive"></div>

## Active vs. Passive FTP

Because the data connection is created on demand, the protocol must specify which endpoint (client or server) initiates the TCP three-way handshake for the data connection. This distinction separates **Active Mode** from **Passive Mode**.

### 1. Active FTP (The Classic Approach)
In Active Mode, the client initiates the control connection, but the **server initiates the data connection**.

```
ACTIVE FTP ARCHITECTURE
CLIENT (IP: 192.168.1.50)                                       SERVER (IP: 203.0.113.10)
  |                                                                 |
  | 1. Control Connection Setup (Client Port 5150 -> Server Port 21)|
  | -------------------- TCP SYN (Port 21) -----------------------> |
  | <------------------- TCP SYN-ACK ------------------------------ |
  |                                                                 |
  | 2. Client issues PORT command (Listen on Client Port 5151)      |
  | --- PORT 192,168,1,50,20,31 (5151 = 20*256 + 31) -------------> |
  | <------------------- 200 Command OK --------------------------- |
  |                                                                 |
  | 3. Client requests file transfer                                |
  | -------------------- RETR syllabus.pdf -----------------------> |
  | <------------------- 150 Opening Data Connection -------------- |
  |                                                                 |
  | 4. Server INITIATES Data Connection back to client              |
  | <--- TCP SYN (Server Port 20 -> Client Port 5151) ------------- |  <-- BLOCKED BY NAT/FIREWALL!
  | -------------------- TCP SYN-ACK -----------------------------> |
  | <=================== Transmit Payload Over Port 20 ===========> |
  | -------------------- Data TCP FIN ----------------------------> |
  | <------------------- 226 Transfer Complete (Control) ---------- |
  v                                                                 v
```

#### The Port Math in the `PORT` Command
The client encodes its 32-bit IP address and 16-bit ephemeral port number as a comma-separated series of six 8-bit octets: `PORT h1,h2,h3,h4,p1,p2`.
The listening data port is calculated as:
$$\text{Port Number} = (p_1 \times 256) + p_2$$
*Example:* `PORT 192,168,1,50,20,31` translates to port $(20 \times 256) + 31 = 5120 + 31 = \mathbf{5151}$.

#### The Firewall / NAT Breakdown Problem
In modern networks, client machines almost universally sit behind **Network Address Translation (NAT) gateways** and stateful packet inspection **firewalls**.
* The client's firewall monitors outbound connections. It permits the client to connect out to `Server:21`.
* In Step 4 of Active FTP, the **remote server initiates an inbound connection** from its Port 20 targeting the internal client machine at Port 5151.
* The client-side firewall detects an unsolicited inbound connection attempt from an external host. It drops the incoming TCP SYN packet, and **Active FTP fails**.

---

### 2. Passive FTP (PASV Mode — Modern Standard)
To resolve the firewall traversal problem, **Passive Mode** ensures that the **client initiates both connections** (both the control connection and the data connection).

```
PASSIVE FTP ARCHITECTURE
CLIENT (Behind NAT/Firewall)                                    SERVER (Public IP)
  |                                                                 |
  | 1. Control Connection Setup (Client Port 5150 -> Server Port 21)|
  | -------------------- Established -----------------------------> |
  |                                                                 |
  | 2. Client requests Passive Mode                                 |
  | -------------------- PASV ------------------------------------> |
  | <------------------- 227 Entering Passive Mode (h1..h4,p1,p2) - |
  |                      (Server opens ephemeral port, e.g., 30005) |
  |                                                                 |
  | 3. Client INITIATES Data Connection to Server Ephemeral Port    |
  | -------------------- TCP SYN (Client -> Server:30005) --------> |  <-- OUTBOUND: PERMITTED!
  | <------------------- TCP SYN-ACK ------------------------------ |
  |                                                                 |
  | 4. Client issues file request over Control Channel              |
  | -------------------- RETR exam_schedule.pdf ------------------> |
  | <------------------- 150 Opening BINARY mode data connection -- |
  | <=================== Transmit Payload Over Port 30005 ========> |
  | -------------------- Data TCP FIN ----------------------------> |
  | <------------------- 226 Transfer Complete (Control) ---------- |
  v                                                                 v
```

1. The client sends the `PASV` command over the established control connection.
2. The server receives `PASV`, binds an unreserved ephemeral port on its own interface (e.g., Port 30005), and replies with:
   `227 Entering Passive Mode (203,0,113,10,117,53)` where $(117 \times 256) + 53 = 30005$.
3. The client initiates the outbound TCP three-way handshake from an ephemeral port to the server's announced IP and port (`203.0.113.10:30005`).
4. Because this is an **outbound** connection initiated from within the private network, the client-side firewall and NAT permit the traffic, enabling successful transfers without complex gateway reconfiguration.

---

<div id="state-management"></div>

## Stateful vs. Stateless Architecture

A major architectural divergence in application layer protocols is how they manage conversational context.

```
       STATEFUL PROTOCOL (FTP)                     STATELESS PROTOCOL (HTTP)
    +---------------------------+                +---------------------------+
    | Server maintains memory:  |                | Server maintains NO memory|
    | - Current working dir     |                | between transactions:     |
    | - Authenticated identity  |                | - Each request is isolated|
    | - Active transfer state   |                | - Requires Cookies for    |
    | - Control link bindings   |                |   simulated state         |
    +---------------------------+                +---------------------------+
```

### 1. FTP is Strictly Stateful
An FTP server maintains extensive **state** information for every active client throughout the session:
* **Current Working Directory:** If a client executes `CWD /var/www/html` and subsequently issues `RETR index.html`, the server resolves the relative path using its stored session state.
* **Authentication Context:** Once the user successfully authenticates via `USER` and `PASS`, the server associates operating system access privileges with that specific control connection.
* **Connection Association:** The server correlates the ongoing persistent control connection with newly arriving transient data connections.

### 2. The Cost of Statefulness
* **Resource Scaling Limits:** The server must allocate memory buffers and track state objects for every open control connection. As the number of concurrent users increases into the tens of thousands, tracking idle state can exhaust system memory.
* **Failure Vulnerability:** If an FTP server crashes and restarts, all active state is destroyed. Clients cannot simply resend their last command; they must reconnect, re-authenticate, and rebuild their working directory state.
* **Contrast with HTTP:** Standard HTTP is entirely **stateless**. The server tracks no client history across requests. If an HTTP server crashes and reboots, an incoming client request is processed normally without prior connection knowledge.

---

<div id="exam-focus-pitfalls"></div>

## Exam Focus & Pitfalls

::: callout-pitfall Exam Trap: Port Number Confusion
* **The Confusion:** Students often state that *"FTP runs on Port 20 and 21"* without explaining which port does what, or they assume Port 20 is always active.
* **Precise Rule for KTU Examinations:**
  * **Port 21:** Exclusively for the **Control Connection** (always listens on the server; persistent).
  * **Port 20:** Exclusively for the **Data Connection in Active Mode** (server initiates data connection *from* its local Port 20).
  * **Ephemeral Port ($>1023$):** In **Passive Mode**, the server does **not** use Port 20 for data transfer. It dynamically opens an arbitrary unreserved high-order port and communicates that port to the client via the `227` reply.
:::

::: callout-exam KTU Common 5-Mark & 10-Mark Questions
1. **5-Mark Question:**
   * *Why is FTP described as an out-of-band protocol? Differentiate between in-band and out-of-band signaling with suitable examples.*
   * *Compare FTP and HTTP with respect to connection architecture, port usage, and state maintenance.*
2. **10-Mark Comprehensive Question:**
   * *(a) Describe the dual-connection architecture of FTP. Explain why two separate TCP connections are used instead of one.*
   * *(b) Explain Active FTP and Passive FTP with neat message exchange diagrams. Why does Active FTP fail in the presence of Network Address Translation (NAT) and client-side firewalls?*
   * *(c) Decode the following FTP command: `PORT 192,168,10,2,16,128`. Calculate the target IP address and port number.*
:::

::: callout-formula Port Decoding Equation
Given an FTP address parameter string $(h_1, h_2, h_3, h_4, p_1, p_2)$:

$$\text{IPv4 Address} = h_1.h_2.h_3.h_4$$

$$\text{TCP Port} = (p_1 \times 256) + p_2$$

*Sample Calculation:*
$$\text{For } \text{PORT } 172,16,4,12,32,15:$$
$$\text{IP} = 172.16.4.12$$
$$\text{Port} = (32 \times 256) + 15 = 8192 + 15 = \mathbf{8207}$$
:::

---

<div id="self-check"></div>

## Self-Check

::: quiz Dual Connection Architecture
Why does FTP utilize a separate out-of-band Control Connection (Port 21) rather than multiplexing commands and data onto a single TCP stream as HTTP does?
(A) Port 21 provides hardware-level encryption that cannot be decoded on standard data lines.
(*B) It allows administrative commands and abort signals to be processed immediately without queuing behind large data transfers.
(C) Operating systems prohibit binary file transfer over any TCP connection initialized with 7-bit ASCII characters.
(D) Out-of-band connections eliminate the need for TCP three-way handshakes during data movement.
::: explanation
By separating the control channel from the data channel (**out-of-band signaling**), FTP ensures that control commands (such as an abort request `ABOR` or a directory query `LIST`) are processed immediately by the server. If control and data were in-band (on the same stream), an administrative command issued mid-transfer would sit at the back of a multi-megabyte TCP transmission buffer.
:::

::: quiz NAT & Firewall Traversal
Under which condition does standard Active Mode FTP reliably fail when transferring files to a residential client?
(A) When the remote server is running a Linux-based operating system.
(B) When the client transfers text files instead of binary images.
(*C) When the client resides behind a standard residential NAT firewall that blocks unsolicited inbound TCP connections.
(D) When the persistent control connection on Port 21 experiences packet loss.
::: explanation
In Active FTP, the client issues a `PORT` command telling the server which port to reach, and the **server initiates the incoming data connection** from Port 20 to the client. Residential NAT routers and firewalls drop unsolicited inbound connection attempts from external IP addresses. Passive FTP resolves this because the client initiates the outbound connection to an ephemeral port announced by the server.
:::

::: quiz Port Calculation
An FTP client sends the control command `PORT 10,0,0,45,40,10`. On which IP address and TCP port does the client expect the incoming data connection?
(A) IP: `10.0.0.45`, Port: `4010`
(B) IP: `10.0.0.45`, Port: `400`
(*C) IP: `10.0.0.45`, Port: `10250`
(D) IP: `10.0.0.45`, Port: `50`
::: explanation
The port calculation formula is:
$$\text{Port} = (p_1 \times 256) + p_2$$
Substituting $p_1 = 40$ and $p_2 = 10$:
$$\text{Port} = (40 \times 256) + 10 = 10240 + 10 = \mathbf{10250}$$
The IP address is formed directly by the first four octets: `10.0.0.45`. Therefore, Option (C) is correct.
:::
