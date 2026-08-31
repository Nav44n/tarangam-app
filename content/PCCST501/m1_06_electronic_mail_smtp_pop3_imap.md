# Electronic Mail Architecture: SMTP, POP3, and IMAP

**Mail User Agents (MUA), Message Transfer Agents (MTA), SMTP push transactions, MIME encoding, and POP3/IMAP access protocols.**

<a id="the-intuition"></a>
## 1. The Intuition

::: callout-intuition Core Mental Model: Postal Delivery vs Private Post Office Boxes
Think of electronic mail as a two-stage postal system:
1. **The Outgoing Courier (Push):** When you write a physical letter, you drop it into your local post office's outgoing slot. The postal service then routes and transports that letter across trucks and planes directly into the recipient’s regional post office holding facility. The letter travels without the recipient needing to be awake, online, or waiting at the door.
2. **The Private Lockbox (Pull):** The letter does *not* fly straight onto the recipient's desk. It sits safely inside their assigned postal box (mailbox) on the destination server until the recipient physically unlocks the box to view, organize, or download their letters.

In computer networking, **SMTP** is the outgoing delivery courier that *pushes* messages across servers, while **POP3** and **IMAP** are the retrieval keys that *pull* stored messages from the mailbox down to your personal screen.
:::

---

<a id="the-math"></a>
## 2. Theoretical Framework & Formalism

### High-Level Architecture & Entity Roles

Electronic mail architecture separates message creation, inter-server transit, and local retrieval across distinct logical agents:

```text
+------------------+                                  +--------------------+
| Alice (Sender)   |                                  |   Bob (Receiver)   |
| User Agent (MUA) |                                  |  User Agent (MUA)  |
+--------+---------+                                  +---------^----------+
|                                                               |
| SMTP (Port 587)                                               | POP3 (995) /
v [Client-to-Server Push]                                       | IMAP (993)
+------------------+                                  +---------+----------+
| Sender Mail      |       SMTP (Port 25)             | Receiver Mail      |
| Server (MTA/MSA) |=================================>| Server (MTA/MDA)   |
|  [Spool Queue]   |    [Server-to-Server Push]       |    [User Mailbox]  |
+------------------+                                  +--------------------+
```

* **Mail User Agent (MUA):** The end-user interface (e.g., Thunderbird, Apple Mail, Outlook) used to compose, read, and manage messages.
* **Message Transfer Agent (MTA):** The server daemon (e.g., Postfix, Sendmail, Exim) that routes messages across the Internet using DNS MX records.
* **Mail Submission Agent (MSA):** Accepts mail from an authenticated MUA on port 587.
* **Mail Delivery Agent (MDA):** Receives the message from the inbound MTA and writes it directly into the user's permanent storage spool (`/var/mail/username` or `Maildir`).
* **Message Access Agent (MAA):** Implements POP3 or IMAP to serve stored messages to the recipient MUA.

---

### Simple Mail Transfer Protocol (SMTP — RFC 5321)

SMTP is an ASCII-text-based, connection-oriented, push protocol running over a reliable TCP stream.

#### Standard Port Allocations

| Port | Service | Encryption | Use Case |
| :--- | :--- | :--- | :--- |
| **25** | Standard SMTP | Plaintext / STARTTLS | Server-to-server relay across the public Internet |
| **587** | Mail Submission (MSA) | Mandatory STARTTLS | Client (MUA) to server (MSA) submission |
| **465** | SMTPS | Implicit SSL/TLS | Legacy secure submission |

#### SMTP Command-Response State Machine

```text
Client (Sender)                         Server (Receiver)
|                                        |
| -------- TCP 3-Way Handshake --------> |
| <------- 220 mail.receiver.org ------- | (Service Ready)
|                                        |
| -------- EHLO mail.sender.org -------> | (Extended Hello)
| <------- 250-SIZE / 250 OK ----------- |
|                                        |
| -------- MAIL FROM:<alice@src.org> --> | (Envelope Sender)
| <------- 250 2.1.0 Originator OK ----- |
|                                        |
| -------- RCPT TO:<bob@dst.org> ------> | (Envelope Recipient)
| <------- 250 2.1.5 Recipient OK ------ |
|                                        |
| -------- DATA -----------------------> | (Begin Message Body)
| <------- 354 End data with .- |
|                                        |
| [Header + Blank Line + Body]           |
| -------- . ---------->                 | (End of Data Token)
| <------- 250 2.0.0 OK: queued -------- |
|                                        |
| -------- QUIT -----------------------> | (Connection Teardown)
| <------- 221 2.0.0 Bye --------------- |
```

---

### Multipurpose Internet Mail Extensions (MIME — RFC 2045)

SMTP was originally constrained strictly to 7-bit ASCII characters (values $0$ to $127$). Binary attachments (images, audio, PDFs) and Unicode characters (e.g., Malayalam, Japanese, emojis) require transformation via MIME headers.

```text
+-------------------------------------------------------------+
| Standard RFC 822 Header: To, From, Subject, Date            |
+-------------------------------------------------------------+
| MIME-Version: 1.0                                           |
| Content-Type: multipart/mixed; boundary="==*BOUNDARY*=="    |
+-------------------------------------------------------------+
| --==*BOUNDARY*==                                            |
| Content-Type: text/plain; charset="utf-8"                   |
| Content-Transfer-Encoding: 7bit                             |
|                                                             |
| Hello Bob, please find the document attached.               |
|                                                             |
| --==*BOUNDARY*==                                            |
| Content-Type: application/pdf; name="report.pdf"            |
| Content-Transfer-Encoding: base64                           |
| Content-Disposition: attachment; filename="report.pdf"      |
|                                                             |
| JVBERi0xLjQKJcTl8uXrp/Og0MTGCjEgMCBvYmoKPDwKL1R5cGUg...     |
| --==*BOUNDARY*==--                                          |
+-------------------------------------------------------------+
```

#### Base64 Encoding Mathematics
Base64 groups binary data into blocks of 3 bytes ($3 \times 8 = 24\text{ bits}$) and partitions them into 4 chunks of 6 bits each ($4 \times 6 = 24\text{ bits}$). Each 6-bit chunk maps to an ASCII printable index ($0 \text{ to } 63 \implies \text{A–Z, a–z, 0–9, +, /}$).

$$\text{Expansion Factor} = \frac{4\text{ output characters}}{3\text{ input bytes}} \approx 1.333 \implies 33.3\%\text{ bandwidth overhead}$$

$$\text{Base64 Size (bytes)} = 4 \times \left\lceil \frac{N}{3} \right\rceil$$

---

### Mail Access Protocols: Pull Mechanism Comparison

Once the receiver's MTA places an email into storage, the recipient uses an access protocol to view messages:

```text
        +------------------------------------------------+
        |        Receiver Server Mailbox Spool           |
        |   [Inbox]  [Drafts]  [Sent]  [Flag: \Seen]     |
        +------------------------------------------------+
                 /                              \
   POP3 (Port 995)                             IMAP (Port 993)
 [Destructive/Atomic]                        [Synchronized/Stateful]
        /                                        \
       v                                          v
+-----------------------+                  +-----------------------+
| Local Disk Storage    |                  | Local Cache View      |
| - Download & Delete   |                  | - Server holds master |
| - Offline inspection  |                  | - Multi-device sync   |
| - Single-client model |                  | - Hierarchy of folders|
+-----------------------+                  +-----------------------+
```

| Dimension | POP3 (Post Office Protocol v3) | IMAP4 (Internet Message Access Protocol) | Webmail (HTTP/HTTPS) |
| :--- | :--- | :--- | :--- |
| **RFC Standard** | RFC 1939 | RFC 3501 | RFC 9110 / Custom REST APIs |
| **Default Ports** | `110` (Plain), `995` (SSL/TLS) | `143` (Plain), `993` (SSL/TLS) | `80` (HTTP), `443` (HTTPS) |
| **Storage Model** | Local storage on client machine | Centralized on remote server | Centralized on cloud server |
| **State Tracking** | Stateless between connections | Stateful (flags: `\Seen`, `\Answered`, `\Deleted`) | Handled via web session/database |
| **Partial Fetch** | Downloads entire message body | Can download headers only, or stream attachments | Streamed via Web UI |
| **Folder Support**| Inbox only | Full hierarchical nested folders | Virtual labels/folders |
| **Multi-Device** | Poor (causes message synchronization conflicts) | Native (all devices see identical state) | Native |

---

<a id="worked-example"></a>
## 3. Worked Example / Step-by-Step Scenario

::: step [Step 1: Setup] Formulating the Transaction
Alice (`alice@univ.edu`) sends a $1.2\text{ MB}$ report to Bob (`bob@tech.com`). Alice's client has already authenticated to her submission agent `smtp.univ.edu` and needs to deliver the message over the network.
:::

::: step [Step 2: Execution] DNS MX Resolution and SMTP Envelope Transfer
1. `smtp.univ.edu` queries DNS for `MX tech.com`. The DNS server returns `mail.tech.com` with priority `10`.
2. `smtp.univ.edu` initiates a TCP connection to `mail.tech.com:25`.
3. The exact ASCII transaction occurs:
```text
S: 220 mail.tech.com ESMTP Postfix
C: EHLO smtp.univ.edu
S: 250-mail.tech.com
S: 250-SIZE 20480000
S: 250 8BITMIME
C: MAIL FROM:<alice@univ.edu>
S: 250 2.1.0 Ok
C: RCPT TO:<bob@tech.com>
S: 250 2.1.5 Ok
C: DATA
S: 354 End data with <CR><LF>.<CR><LF>
C: From: "Alice" <alice@univ.edu>
C: To: "Bob" <bob@tech.com>
C: Subject: Project Review
C: MIME-Version: 1.0
C: Content-Type: text/plain; charset=us-ascii
C: 
C: Hi Bob, please review the uploaded project specifications.
C: .
S: 250 2.0.0 Ok: queued as B4A120F
C: QUIT
S: 221 2.0.0 Bye
```
:::

::: step [Step 3: Conclusion] Final Delivery and Retrieval
`mail.tech.com`'s MDA drops the payload into Bob's physical mailbox directory. Later, Bob opens his phone mail client (MUA). The client connects via **IMAP over TLS (Port 993)**, authenticates, reads the `Project Review` envelope headers without downloading the body until Bob taps the message, and marks the server flag as `\Seen`.
:::

---

## 4. Active Recall Checkpoint

::: quiz Q1: Protocol Directionality
Why can SMTP NOT be used directly by a mobile client to retrieve incoming emails from a mailbox server?
(A) SMTP does not support TCP transport
(*B) SMTP is strictly a push protocol designed to deliver to an active listening daemon; a client device is frequently offline and needs a pull protocol
(C) SMTP is restricted to transmitting numbers rather than text
(D) SMTP cannot route between different domain names
::: explanation
SMTP is a push protocol designed for sending data to always-on listening hosts (mail servers). Client machines (laptops, phones) are frequently powered down or assigned temporary dynamic IP addresses behind NATs, meaning an external server cannot push incoming messages directly to them. A pull protocol (POP3/IMAP) is required.
:::

::: quiz Q2: Base64 Overhead Calculation
If an uncompressed binary attachment has a size of exactly $3\text{ MB}$, what will be its approximate payload size after Base64 encoding for MIME transmission?
(A) $3.0\text{ MB}$
(B) $2.25\text{ MB}$
(*C) $4.0\text{ MB}$
(D) $6.0\text{ MB}$
::: explanation
Base64 encoding expands raw binary data by a factor of $\frac{4}{3}$ (approx $33.3\%$ overhead). Therefore, $3\text{ MB} \times \frac{4}{3} = 4.0\text{ MB}$.
:::

::: quiz Q3: Protocol Comparison
Which of the following operations is possible in IMAP4 but IMPOSSIBLE in standard POP3?
(A) Authenticating using a username and password
(B) Downloading a plaintext message body over a secure TLS channel
(*C) Downloading only the message headers without downloading the accompanying $20\text{ MB}$ attachment
(D) Deleting an email from the local device
::: explanation
IMAP4 supports fine-grained, stateful access and partial fetches—allowing clients to inspect message structures and fetch headers without pulling down large attachments. POP3 is an all-or-nothing protocol that transfers the entire raw message upon retrieval.
:::