---
id: m1_05_file_transfer_protocol_ftp
title: "File Transfer Protocol (FTP)"
sidebar_label: "1.5 FTP"
description: "Understanding the out-of-band control and data mechanisms of the File Transfer Protocol."
---

# File Transfer Protocol (FTP)

Before the Web became dominant, downloading and uploading files over the Internet was primarily handled by the **File Transfer Protocol (FTP)**. While HTTP is used to transfer web pages (which are also files), FTP is optimized for bulk file transfers, directory navigation, and account management.

---

## 1. The Dual-Connection Architecture

The defining characteristic of FTP is that it uses **two separate parallel TCP connections** to transfer a file. This is fundamentally different from HTTP, which sends control headers and data over the exact same connection.

* **Control Connection (Port 21):** Used for sending control information between the two hosts—such as user identification, passwords, commands to change remote directories (`CWD`), and commands to upload (`STOR`) or download (`RETR`) files.
* **Data Connection (Port 20):** Used strictly for transmitting the actual file data.

### The "Out-of-Band" Analogy

Because FTP sends its control information over a separate connection, FTP is said to use **out-of-band** control.

> **Analogy:** Imagine ordering a refrigerator. You call the store on the telephone (the **Control Connection / Port 21**) to place the order and verify your identity. The store then dispatches a large delivery truck (the **Data Connection / Port 20**) carrying the actual refrigerator to your house. The conversation and the heavy lifting occur over two entirely separate channels.
> 
> *HTTP, by contrast, uses **in-band** control, placing both the request headers and payload data within the same channel.*

---

## 2. How an FTP Session Works

1. **Establishing Control:** The client contacts the server on port 21 to establish a TCP control connection.
2. **Authentication:** The client sends the user ID and password over the control connection.
3. **Issuing Commands:** The client browses remote directories (using commands like `LIST` or `CWD`) over the control connection.
4. **Opening Data Connection:** When the server receives a transfer command (e.g., `RETR` for get, `STOR` for put), a TCP data connection is initiated.
5. **Transfer & Closure:** The server sends exactly one file over the data connection and closes it immediately after completion.
6. **Subsequent Transfers:** If the client requests another file, a brand new TCP data connection is established.

> **Key Rule:** The **Control Connection** remains open for the entire duration of the user session, whereas a separate **Data Connection** is opened and closed for every individual file transferred.

---

## 3. Active vs. Passive FTP

Because firewalls block unsolicited incoming connections, FTP's original design caused connectivity issues with modern security configurations.

* **Active Mode:** The client opens a random port for data and instructs the server to connect back to it. Firewalls on the client side typically block this incoming connection attempt from the server.
* **Passive Mode (`PASV`):** The client requests a passive connection. The server opens a random high-order port (e.g., Port 5050) and informs the client to connect to it. Because the client initiates the connection outbound, client firewalls allow the traffic.

---

## 4. FTP State

Unlike HTTP, which is stateless, FTP is **stateful**.

The FTP server maintains state information for each connected user throughout their session. It tracks:
* The user's current working directory (enabling relative paths).
* The user's authentication and authorization state.

*Trade-off: Maintaining state limits the total number of simultaneous active sessions an FTP server can sustain compared to a stateless HTTP server.*

---

## 5. Active Recall Quiz

* **Question 1:** What does it mean when we say FTP uses "out-of-band" control?
* **Question 2:** Why did FTP introduce "Passive Mode"?