# Progressive Problems: HTTP Response Times and Round Trip Time (RTT)

> **Instructor Note:** Every problem below is explained for an absolute beginner. We break down the *What*, *When*, *Where*, *How*, and *Why* for every single step. No logical leaps.

---

## Shared Scenario Setup

To clearly observe how network protocols evolve to make the web faster, we will use the exact same webpage across all three levels:
- A user sitting at a browser clicks a link to download a webpage from a web server.
- The webpage consists of:
  1. One **Base HTML text file** (contains the written words and code references).
  2. Two **Embedded Images** (`image1.png` and `image2.png`).
  - Total objects to fetch: **$3$ distinct files**.
- The physical distance between the client and server creates a round-trip delay:
  $$\text{RTT} = 100\text{ ms}$$
  *(One Round Trip Time is the time it takes for a tiny packet to travel from Client $\to$ Server, plus the time for a reply to travel Server $\to$ Client).*
- For clarity and clean comparisons, each object takes a transmission time:
  $$d_{\text{trans}} = 10\text{ ms}$$
  *(The time for the server's network card to push all the bits of one file onto the wire).*
- The client cannot know that `image1.png` and `image2.png` exist until it receives and parses the Base HTML file!

---

## Level 1: Non-Persistent HTTP without Parallel Connections

### Problem 1.1: Sequential Fetching (HTTP/1.0 Default)

Under traditional **Non-Persistent HTTP (HTTP/1.0)**:
1. Every single object requires establishing a brand-new, independent TCP connection.
2. A TCP connection requires a **Three-Way Handshake** before any data can be requested.
3. Once the server finishes sending the requested object, it immediately closes the TCP connection.
4. The client fetches objects purely sequentially (one after another).

Trace the step-by-step timeline to fetch the base HTML file and the two images.  
Calculate the total elapsed time in milliseconds from the moment the user clicks the link until all three objects are fully displayed on screen.

::: callout-intuition Core Mental Model
Imagine you want to buy 3 separate books from a rare book dealer located across the country:
- You cannot just shout your order. First, you must hire a **courier** to deliver a letter saying: *"Hello, I would like to do business with you."*
- The dealer writes back: *"Hello! I am ready to do business with you."* (This courier trip there and back is **1 RTT for the TCP Handshake**).
- Now that your business connection is officially open, you send the courier back with your order: *"Please send me the Catalog (Base HTML)."*
- The dealer gives the courier the catalog. (This courier trip there and back is **1 RTT for the Request/Response**, plus the time to pack the box, which is **$d_{\text{trans}}$**).
- Under Non-Persistent rules, as soon as you receive the catalog, you **tear up the business contract**!
- To order Book 1, you must hire a courier to do the formal greeting handshake all over again!
- To order Book 2, you must do the formal greeting handshake a third time!
- It is safe, but you waste an enormous amount of time sending couriers back and forth just to say hello.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The Three-Way Handshake for the Base HTML File</div>

**What are we doing?** Before our web browser can request the webpage, it must establish a reliable TCP transport connection with the web server.

**Why are we starting here?** The HTTP application protocol runs on top of TCP. In computer networking, you cannot send HTTP data across a "raw" wire without first agreeing on sequence numbers and allocating memory buffers via the TCP Three-Way Handshake.

**How do we do it?** 1. Client sends a tiny synchronization packet called `SYN` to the server. (Takes $\frac{1}{2}\text{ RTT} = 50\text{ ms}$).
2. Server receives `SYN` and replies with a synchronization acknowledgement packet called `SYN-ACK`. (Takes $\frac{1}{2}\text{ RTT} = 50\text{ ms}$).
3. When the `SYN-ACK` arrives at the client, the TCP connection is officially established!
4. Total time elapsed for this greeting step:
   $$\text{Handshake Time} = \frac{1}{2}\text{ RTT} + \frac{1}{2}\text{ RTT} = 1\text{ RTT} = \mathbf{100\text{ ms}}$$

**Where did this concept come from?** Transmission Control Protocol (RFC 793) specification for connection-oriented transport.

**Timeline State:**
- $t = 0\text{ ms}$: User clicks link; Client sends `SYN`.
- $t = 50\text{ ms}$: Server receives `SYN`; sends `SYN-ACK`.
- $t = 100\text{ ms}$: Client receives `SYN-ACK`. TCP Connection 1 is open!
</div>

<div class="step-card">
<div class="step-badge">Step 2: Request and Receive the Base HTML File</div>

**What changed from Step 1?** The TCP connection is open. The client can now ask for the actual webpage file.

**What are we doing?** Client sends an `HTTP GET /index.html` request. The server replies with the file data.

**How do we do it?** 1. Along with its final acknowledgment, the client sends the `HTTP GET` request. It flies across the network to the server:
   $$\text{Travel time to server} = \frac{1}{2}\text{ RTT} = 50\text{ ms}$$
2. The server receives the request, pulls `index.html` from disk, and pushes the bits onto the link:
   $$\text{Server transmission time} = d_{\text{trans}} = 10\text{ ms}$$
3. The bits fly across the network back to the client:
   $$\text{Travel time back to client} = \frac{1}{2}\text{ RTT} = 50\text{ ms}$$
4. Total time for this request/response cycle:
   $$\text{Request-to-Arrival Time} = \frac{1}{2}\text{ RTT} + d_{\text{trans}} + \frac{1}{2}\text{ RTT} = 1\text{ RTT} + d_{\text{trans}} = 100\text{ ms} + 10\text{ ms} = \mathbf{110\text{ ms}}$$
5. Under Non-Persistent HTTP, the server now **closes TCP Connection 1**.

**Timeline State:**
- $t = 100\text{ ms}$: Client sends `HTTP GET /index.html`.
- $t = 150\text{ ms}$: Server receives request; spends $10\text{ ms}$ pushing bits.
- $t = 160\text{ ms}$: Last bit of `index.html` leaves server.
- $t = 210\text{ ms}$: Last bit of `index.html` arrives at client.
- Client reads HTML and discovers: *"Oh! This page contains image1.png and image2.png!"*
- Total time to obtain Base HTML:
  $$\text{Time}_{\text{HTML}} = 1\text{ RTT (Handshake)} + 1\text{ RTT (Data Request)} + d_{\text{trans}} = 2\text{ RTT} + d_{\text{trans}} = \mathbf{210\text{ ms}}$$
</div>

<div class="step-card">
<div class="step-badge">Step 3: Fetch Image 1 (Entirely New TCP Connection)</div>

**What changed from Step 2?** The first TCP connection was closed. The client knows it needs `image1.png`. Because this is sequential non-persistent HTTP, the client must open a brand-new connection specifically for Image 1.

**What are we doing?** We execute a second TCP handshake, send an HTTP GET for Image 1, and wait for the file to arrive.

**How do we do it?** 1. Open new TCP Connection 2:
   - Client sends `SYN`, Server sends `SYN-ACK`.
   - Cost: $1\text{ RTT} = 100\text{ ms}$.
2. Request and receive `image1.png`:
   - Client sends `HTTP GET /image1.png`.
   - Server transmits ($d_{\text{trans}} = 10\text{ ms}$) and data returns.
   - Cost: $1\text{ RTT} + d_{\text{trans}} = 100\text{ ms} + 10\text{ ms} = 110\text{ ms}$.
3. Server closes TCP Connection 2.

**Timeline State:**
- $t = 210\text{ ms}$: Client initiates TCP Handshake 2.
- $t = 310\text{ ms}$: TCP Connection 2 established; Client sends `HTTP GET /image1.png`.
- $t = 420\text{ ms}$: Last bit of `image1.png` arrives at client. TCP Connection 2 closed.
- Additional time for Image 1:
  $$\text{Time}_{\text{Image1}} = 2\text{ RTT} + d_{\text{trans}} = 200\text{ ms} + 10\text{ ms} = \mathbf{210\text{ ms}}$$
</div>

<div class="step-card">
<div class="step-badge">Step 4: Fetch Image 2 (Third Independent TCP Connection)</div>

**What changed from Step 3?** Image 1 has arrived. Because operations are strictly sequential, the client only now begins fetching `image2.png`.

**What are we doing?** We repeat the exact same two-RTT process for Image 2.

**How do we do it?** 1. Open new TCP Connection 3:
   - Client sends `SYN`, Server sends `SYN-ACK`.
   - Cost: $1\text{ RTT} = 100\text{ ms}$.
2. Request and receive `image2.png`:
   - Client sends `HTTP GET /image2.png`.
   - Server transmits ($d_{\text{trans}} = 10\text{ ms}$) and data returns.
   - Cost: $1\text{ RTT} + d_{\text{trans}} = 100\text{ ms} + 10\text{ ms} = 110\text{ ms}$.
3. Server closes TCP Connection 3.

**Timeline State:**
- $t = 420\text{ ms}$: Client initiates TCP Handshake 3.
- $t = 520\text{ ms}$: TCP Connection 3 established; Client sends `HTTP GET /image2.png`.
- $t = 630\text{ ms}$: Last bit of `image2.png` arrives at client. Entire page is now complete!
- Additional time for Image 2:
  $$\text{Time}_{\text{Image2}} = 2\text{ RTT} + d_{\text{trans}} = 200\text{ ms} + 10\text{ ms} = \mathbf{210\text{ ms}}$$
</div>

<div class="step-card">
<div class="step-badge">Final Step: Total Time for Sequential Non-Persistent HTTP</div>

**What is the final answer?**
Summing all three sequential phases:
$$\begin{aligned}
\text{Total Time} &= \text{Time}_{\text{HTML}} + \text{Time}_{\text{Image1}} + \text{Time}_{\text{Image2}} \\
&= (2\text{ RTT} + d_{\text{trans}}) + (2\text{ RTT} + d_{\text{trans}}) + (2\text{ RTT} + d_{\text{trans}}) \\
&= 6\text{ RTT} + 3d_{\text{trans}} \\
&= 6(100\text{ ms}) + 3(10\text{ ms}) = 600\text{ ms} + 30\text{ ms} = \mathbf{630\text{ ms}}
\end{aligned}$$

**General Formula for $N$ Objects (1 HTML + $M$ images, where $N = 1 + M$):**
$$\text{Total Time}_{\text{Sequential Non-Persistent}} = 2N \times \text{RTT} + N \times d_{\text{trans}}$$
For $N = 3$:
$$\text{Total Time} = 2(3) \times 100\text{ ms} + 3 \times 10\text{ ms} = 600\text{ ms} + 30\text{ ms} = \mathbf{630\text{ ms}}$$

**Why does this answer make sense?**
Every single object costs $2\text{ RTT}$ ($1$ to say hello via TCP, $1$ to ask for the data). With $3$ objects fetched back-to-back, you pay $2 \times 3 = 6$ full round trips just waiting for network propagation!
</div>

</div>

---

## Level 2: Non-Persistent HTTP with Parallel TCP Connections

### Problem 2.1: Concurrent Handshakes and Overlapping RTTs

To combat the slowness of sequential downloading, web browser engineers introduced **Parallel Connections**:
- The browser still uses Non-Persistent HTTP (each connection is closed after one file).
- However, as soon as the client parses the Base HTML file and sees that it needs multiple referenced objects (`image1.png` and `image2.png`), the browser opens **two TCP connections at the exact same time in parallel**!

Using the exact same numbers ($\text{RTT} = 100\text{ ms}$, $d_{\text{trans}} = 10\text{ ms}$):
1. Trace how the Base HTML file is fetched.
2. Trace the simultaneous opening of Connection 2 and Connection 3.
3. Show step-by-step how the RTTs of both images overlap in time.
4. Calculate the total time and quantify the speedup over sequential fetching.

::: callout-intuition Core Mental Model
Imagine you read the bookstore catalog and realize you want Book 1 and Book 2:
- Instead of hiring one courier to go fetch Book 1, waiting for them to return, and then hiring another courier for Book 2...
- You hire **two couriers at the exact same second**!
  - Courier A runs to get Book 1.
  - Courier B runs alongside Courier A to get Book 2.
- Both couriers run across the country together.
- When they arrive, the dealer hands Book 1 to Courier A, and Book 2 to Courier B.
- Both couriers run back together and arrive at your doorstep at almost the exact same time!
- You paid the cost of the trip **once**, but you got **two books back simultaneously**.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: Fetch the Base HTML File</div>

**What are we doing?** The client must fetch the Base HTML file first.

**Can the images be fetched in parallel with the HTML file?** **No!** The client does not know what images exist, what their file names are, or what server holds them until it downloads and parses `index.html`. Therefore, the HTML file must always be retrieved alone first.

**How do we do it?** The process is identical to Step 1 and Step 2 of Level 1:
1. TCP Handshake for HTML: $1\text{ RTT} = 100\text{ ms}$.
2. Request and Receive HTML: $1\text{ RTT} + d_{\text{trans}} = 100\text{ ms} + 10\text{ ms} = 110\text{ ms}$.
3. Connection closes.

**Timeline State:**
- $t = 0\text{ ms}$: User clicks link; TCP Connection 1 initiated.
- $t = 100\text{ ms}$: TCP Connection 1 established; `HTTP GET /index.html` sent.
- $t = 210\text{ ms}$: `index.html` arrives at client.
$$\text{Time to receive HTML} = 2\text{ RTT} + d_{\text{trans}} = \mathbf{210\text{ ms}}$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Simultaneous Parallel TCP Handshakes for Images 1 & 2</div>

**What changed from Step 1?** At $t = 210\text{ ms}$, the client reads the HTML file and sees tags for both `image1.png` and `image2.png`.

**What are we doing?** Instead of waiting, the client immediately fires off two `SYN` packets across the wire in parallel:
- Packet A: `SYN` for Connection 2 (Image 1)
- Packet B: `SYN` for Connection 3 (Image 2)

**How do we do it?** 1. Both `SYN` packets fly toward the server simultaneously.
2. The server receives both packets at roughly $t = 260\text{ ms}$ and sends back two `SYN-ACK` packets.
3. Both `SYN-ACK` packets arrive at the client at roughly $t = 310\text{ ms}$.
4. **The Overlap:** Because the signals traveled over the wire at the same time, the time elapsed for *both* handshakes combined is simply:
   $$\text{Parallel Handshake Time} = 1\text{ RTT} = \mathbf{100\text{ ms}}$$

**Timeline State:**
- $t = 210\text{ ms}$: Both Connection 2 and Connection 3 send `SYN`.
- $t = 310\text{ ms}$: Both Connection 2 and Connection 3 receive `SYN-ACK`. Both connections are now simultaneously open!
</div>

<div class="step-card">
<div class="step-badge">Step 3: Simultaneous Parallel Image Requests & Transmissions</div>

**What changed from Step 2?** Both TCP connections are open at $t = 310\text{ ms}$.

**What are we doing?** The client immediately transmits two HTTP requests in parallel:
- On Connection 2: `HTTP GET /image1.png`
- On Connection 3: `HTTP GET /image2.png`

**How do we do it?** 1. Both request packets fly across the network:
   $$\text{Request travel time} = \frac{1}{2}\text{ RTT} = 50\text{ ms}$$
2. Both requests arrive at the server at $t = 310 + 50 = 360\text{ ms}$.
3. **Server Transmission at the Bottleneck:**
   The server's network link must push out the bits for both images. Assuming the server transmits them back-to-back onto its outbound link:
   - Server transmits Image 1: takes $d_{\text{trans}} = 10\text{ ms}$ (from $t = 360\text{ ms}$ to $t = 370\text{ ms}$).
   - Server transmits Image 2: takes $d_{\text{trans}} = 10\text{ ms}$ (from $t = 370\text{ ms}$ to $t = 380\text{ ms}$).
   - Total transmission time for both images: $2 \times d_{\text{trans}} = 20\text{ ms}$.
4. **Propagation back to Client:**
   - Image 1 bits arrive at client at $t = 370 + 50 = 420\text{ ms}$.
   - Image 2 bits arrive at client at $t = 380 + 50 = \mathbf{430\text{ ms}}$.

**Timeline State:**
- At $t = 430\text{ ms}$, the last bit of the second image arrives at the browser. All objects are fully downloaded!
</div>

<div class="step-card">
<div class="step-badge">Final Step: Total Time for Parallel Non-Persistent HTTP</div>

**What is the final answer?**
$$\begin{aligned}
\text{Total Time} &= \text{Time}_{\text{HTML}} + \text{Time}_{\text{Parallel Images}} \\
&= (2\text{ RTT} + d_{\text{trans}}) + (1\text{ RTT for Handshakes} + 1\text{ RTT for Requests} + 2 \times d_{\text{trans}}) \\
&= (200\text{ ms} + 10\text{ ms}) + (100\text{ ms} + 100\text{ ms} + 20\text{ ms}) \\
&= 210\text{ ms} + 220\text{ ms} = \mathbf{430\text{ ms}}
\end{aligned}$$

**Comparison against Level 1 (Sequential):**
- Sequential Non-Persistent: **$630\text{ ms}$**
- Parallel Non-Persistent: **$430\text{ ms}$**
- Time saved:
  $$\Delta t = 630\text{ ms} - 430\text{ ms} = \mathbf{200\text{ ms}}\quad (31.7\%\text{ faster!})$$

**Why did we save exactly 200 ms?**
We saved exactly **$2\text{ RTT}$**! In Level 1, Image 2 had to wait for Image 1's handshake ($1\text{ RTT}$) and Image 1's request travel ($1\text{ RTT}$). By running them in parallel, those two round trips occurred concurrently.
</div>

</div>

---

## Level 3: Persistent HTTP (HTTP/1.1)

### Problem 3.1: Reusing a Single TCP Connection across Objects

While parallel connections are faster, they place heavy stress on web servers:
- Opening dozens of parallel TCP sockets consumes server RAM, file descriptors, and CPU time.
- To solve this, **HTTP/1.1** introduced **Persistent Connections (Keep-Alive)**:
  1. The client opens **one single TCP connection** to the server.
  2. After the base HTML file is delivered, the server **keeps the connection open**!
  3. The client can immediately reuse the existing, already-open connection to request `image1.png` and `image2.png` without performing any additional TCP handshakes.

Trace the timeline under Persistent HTTP (with pipelined/back-to-back requests).  
Calculate the total elapsed time and show why skipping the extra TCP handshakes provides optimal performance while using only one socket.

::: callout-intuition Core Mental Model
Imagine hiring a courier with a **standing daily contract**:
- You send the courier with the initial formal greeting letter once: *"I am opening an active account with you."* (1 RTT Handshake).
- You order the catalog: *"Send the Catalog."*
- The dealer hands the courier the catalog, but you **do not fire the courier**! The courier stands by, waiting for your next instruction.
- The instant you look at the catalog and see that you need Book 1 and Book 2, you tell the standing courier: *"Bring me Book 1 and Book 2!"*
- Because the courier is already standing there and your business account is already open, you **completely skip the greeting trip**!
- You never waste time saying hello twice.
:::

<div class="stepped-container">

<div class="step-card">
<div class="step-badge">Step 1: The One-and-Only TCP Handshake & Base HTML Fetch</div>

**What are we doing?** We open the initial TCP connection and fetch `index.html`.

**How do we do it?** 1. TCP Handshake:
   - Client sends `SYN`, Server replies `SYN-ACK`.
   - Cost: $1\text{ RTT} = 100\text{ ms}$.
2. Request and Receive HTML:
   - Client sends `HTTP GET /index.html`.
   - Server takes $d_{\text{trans}} = 10\text{ ms}$ to push the bits.
   - Total travel and transmission: $1\text{ RTT} + d_{\text{trans}} = 100\text{ ms} + 10\text{ ms} = 110\text{ ms}$.
3. **The Crucial Persistent Difference:**
   Instead of sending a `FIN` packet to tear down the connection, the server includes a response header:
   `Connection: keep-alive`
   The TCP connection **remains open and active**!

**Timeline State:**
- $t = 0\text{ ms}$: Handshake starts.
- $t = 100\text{ ms}$: Handshake completes; HTML requested.
- $t = 210\text{ ms}$: `index.html` arrives at client.
- **Connection status:** OPEN.
$$\text{Time to fetch HTML} = 2\text{ RTT} + d_{\text{trans}} = \mathbf{210\text{ ms}}$$
</div>

<div class="step-card">
<div class="step-badge">Step 2: Requesting Both Images on the Open Connection</div>

**What changed from Step 1?** At $t = 210\text{ ms}$, the client inspects the HTML file. It needs `image1.png` and `image2.png`.

**What are we doing?** Because the TCP connection is already established, the client **does not perform any TCP handshake**! It immediately transmits its HTTP GET requests down the already-open pipe.

**How do we do it?** 1. At $t = 210\text{ ms}$, the client sends the HTTP requests for both images back-to-back (pipelined):
   - `HTTP GET /image1.png`
   - `HTTP GET /image2.png`
2. Both requests travel across the network to the server:
   $$\text{Travel time} = \frac{1}{2}\text{ RTT} = 50\text{ ms}$$
3. The server receives the requests at $t = 210 + 50 = \mathbf{260\text{ ms}}$.
   *(Notice that in Level 2, the server hadn't even finished the TCP handshakes by $t = 260\text{ ms}$!)*
</div>

<div class="step-card">
<div class="step-badge">Step 3: Server Transmits Both Images Back-to-Back</div>

**What changed from Step 2?** The server has received the requests for both images on the existing connection at $t = 260\text{ ms}$.

**What are we doing?** The server serializes and transmits both files down the open connection.

**How do we do it?** 1. Server pushes `image1.png`:
   - Duration: $d_{\text{trans}} = 10\text{ ms}$ (from $t = 260\text{ ms}$ to $t = 270\text{ ms}$).
2. Server immediately pushes `image2.png`:
   - Duration: $d_{\text{trans}} = 10\text{ ms}$ (from $t = 270\text{ ms}$ to $t = 280\text{ ms}$).
3. The data propagates back across the wire to the client:
   $$\text{Propagation time} = \frac{1}{2}\text{ RTT} = 50\text{ ms}$$
4. Arrival at client:
   - First image finishes arriving: $t = 270 + 50 = 320\text{ ms}$.
   - Second image finishes arriving: $t = 280 + 50 = \mathbf{330\text{ ms}}$.

**Timeline State:**
At $t = 330\text{ ms}$, all three objects are completely delivered to the client.
</div>

<div class="step-card">
<div class="step-badge">Final Step: Grand Comparison Across All 3 Architectures</div>

**What is the final answer for Persistent HTTP?**
$$\begin{aligned}
\text{Total Time}_{\text{Persistent}} &= \text{Time}_{\text{HTML}} + \text{Time}_{\text{Images}} \\
&= (2\text{ RTT} + d_{\text{trans}}) + (1\text{ RTT} + 2d_{\text{trans}}) \\
&= 3\text{ RTT} + 3d_{\text{trans}} \\
&= 3(100\text{ ms}) + 3(10\text{ ms}) = 300\text{ ms} + 30\text{ ms} = \mathbf{330\text{ ms}}
\end{aligned}$$

**Master Performance Comparison Table:**

| Metric / Step | Level 1: Sequential Non-Persistent | Level 2: Parallel Non-Persistent | Level 3: Persistent HTTP/1.1 |
| :--- | :---: | :---: | :---: |
| **Number of TCP Sockets Used** | $1$ at a time ($3$ total) | **$2$ simultaneously** ($3$ total) | **Only $1$ socket total!** |
| **TCP Handshakes Performed** | $3$ handshakes ($3\text{ RTT}$) | $3$ handshakes ($2\text{ RTT}$ elapsed) | **Only $1$ handshake ($1\text{ RTT}$)** |
| **RTTs Spent on HTML** | $2\text{ RTT}$ | $2\text{ RTT}$ | $2\text{ RTT}$ |
| **RTTs Spent on Images** | $4\text{ RTT}$ | $2\text{ RTT}$ | **$1\text{ RTT}$** |
| **Total Transmission Time** | $3d_{\text{trans}} = 30\text{ ms}$ | $3d_{\text{trans}} = 30\text{ ms}$ | $3d_{\text{trans}} = 30\text{ ms}$ |
| **Total Page Load Time** | **$630\text{ ms}$** | **$430\text{ ms}$** | **$330\text{ ms}$** |
| **Speedup vs. Sequential** | Baseline ($1.0\times$) | **$1.47\times$ faster** | **$1.91\times$ faster!** |

**Why does Persistent HTTP win?**
1. It is almost **twice as fast** as traditional sequential non-persistent HTTP.
2. It is **$100\text{ ms}$ faster** than parallel non-persistent HTTP, without opening extra sockets or flooding the server with connection state.
3. Every referenced object after the base HTML is fetched at the theoretical minimum possible cost: **just the transmission time plus the physical propagation time of the wire**, with zero overhead wasted on handshakes!
</div>

</div>
