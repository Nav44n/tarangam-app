# The Web and HTTP: Architecture, Connections, and Caching

> **Course Code:** PCCST501 / CST303 — Computer Networks  
> **Target Audience:** APJ Abdul Kalam Technological University (KTU) B.Tech Computer Science & Engineering  
> **Module Coverage:** Module 1 (Lecture 4) — HTTP Overview, Non-Persistent vs. Persistent Connections, Request/Response Messages, Cookies, and Web Caching  

---

## Quick Navigation Anchors
- [The Intuition](#the-intuition)
- [HTTP Protocol Foundations & Message Formats](#http-foundations)
- [HTTP Status Codes Reference](#status-codes)
- [Non-Persistent vs. Persistent Connections](#connection-types)
- [Timing Ladder Analysis](#timing-ladders)
- [User-Server State: Cookies](#cookies)
- [Web Caching & The Conditional GET](#web-caching)
- [KTU Exam Focus & Numerical Pitfalls](#exam-focus-pitfalls)
- [Active Recall Checkpoint](#self-check)

---

## The Intuition

::: callout-intuition Core Mental Model: The Stateless Cashier & The Loyalty Stamp Card
Imagine ordering coffee every morning at a busy train station espresso kiosk:
1. **The Stateless Cashier (Raw HTTP):**
   * The barista suffers from total amnesia between transactions.
   * You order a Cappuccino. The barista accepts your money, slides you the cup, and immediately forgets your face, name, and order.
   * If you step up five seconds later asking, *"Can I get that with oat milk instead?"*, the barista stares blankly: *"I have never seen you before in my life. What drink are you talking about?"*
   * **The Trade-Off:** The kiosk is remarkably fast and light on resources. It does not maintain filing cabinets full of customer dossiers, allowing it to serve thousands of commuters per hour without running out of memory.
2. **The Loyalty Stamp Card (The Cookie):**
   * To build an ongoing relationship without burdening the barista's brain, the kiosk hands you a small numbered stamp card: `ID: 9842` (`Set-Cookie`).
   * You place the card in your pocket (browser cookie storage).
   * Every time you step up to the counter, you flash the card (`Cookie: 9842`).
   * The barista uses `9842` to query a backend computerized inventory database to retrieve your name, previous drink preferences, and reward balance. The transaction feels continuous and personalized, even though the barista's brain remains entirely stateless.
:::

---

<div id="http-foundations"></div>

## HTTP Protocol Foundations

The **Hypertext Transfer Protocol (HTTP)** is the Web's application-layer protocol, standardized under various RFCs (e.g., RFC 1945 for HTTP/1.0, RFC 2616 / RFC 7230-7235 for HTTP/1.1).

### 1. Architectural Characteristics
* **Client-Server Paradigm:** The **client** (browser or user agent) sends request messages; the **server** (web server software like Apache, NGINX) serves response messages containing objects (HTML documents, JPEG images, CSS stylesheets, JavaScript files).
* **Statelessness:** An HTTP server maintains **no state** information about past client requests. If a client requests the same object thirty times in thirty seconds, the server serves it thirty times without recording that the client recently asked for it.
* **Underlying Transport:** HTTP relies on **TCP** for reliable byte-stream transfer. By default, unencrypted HTTP traffic flows over **Port 80**, while encrypted HTTPS (HTTP over TLS) operates over **Port 443**. Before an HTTP client can send a request, a TCP three-way handshake must first be established.

---

### 2. HTTP Message Formats

HTTP messages are human-readable ASCII text strings structured into distinct sections.

#### A. HTTP Request Message
An HTTP request consists of a **Request Line**, followed by **Header Lines**, a blank line containing a carriage return and line feed (`\r\n`), and an optional **Entity Body**.

```http
GET /somedir/page.html HTTP/1.1\r\n
Host: www.someschool.edu\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n
Accept: text/html,application/xhtml+xml\r\n
Accept-Language: en-US,en;q=0.9\r\n
Connection: keep-alive\r\n
\r\n
[Entity Body - Empty for standard GET requests]
```

* **Request Line Components:**
  * **Method:** Action verb (`GET` to retrieve an object, `POST` to upload user input/form data in the entity body, `HEAD` to retrieve headers only for debugging/caching checks, `PUT` to upload an object to a specific path, `DELETE` to remove a resource).
  * **URL (Uniform Resource Locator):** The path to the requested resource (`/somedir/page.html`).
  * **Version:** Protocol dialect (`HTTP/1.1`).
* **Header Lines:**
  * `Host:` **Mandatory in HTTP/1.1**. Specifies the domain name of the host. Required so that virtual hosting environments (multiple websites sharing a single physical IP address) know which site is being targeted.
  * `User-Agent:` Identifies the browser type and operating system generating the request.
  * `Connection:` Dictates whether the underlying TCP connection should be kept open (`keep-alive`) or terminated (`close`) after the transfer.

#### B. HTTP Response Message
An HTTP response consists of a **Status Line**, **Header Lines**, a blank line (`\r\n`), and the requested **Entity Body**.

```http
HTTP/1.1 200 OK\r\n
Date: Fri, 04 Sep 2026 08:30:00 GMT\r\n
Server: Apache/2.4.52 (Ubuntu)\r\n
Last-Modified: Thu, 03 Sep 2026 14:20:10 GMT\r\n
ETag: "68-5d2b78b0"\r\n
Content-Length: 2596\r\n
Content-Type: text/html; charset=UTF-8\r\n
Connection: keep-alive\r\n
\r\n
<!DOCTYPE html>
<html>
  <head><title>Welcome</title></head>
  <body><h1>Academic Portal</h1>...</body>
</html>
```

* **Status Line Components:** Protocol Version (`HTTP/1.1`), numeric Status Code (`200`), and human-readable Status Phrase (`OK`).
* **Header Lines:**
  * `Date:` Timestamp indicating when the response was generated by the server.
  * `Server:` Software banner of the issuing server.
  * `Last-Modified:` Timestamp indicating when the resource was last altered on the server's storage disk (critical for web caching).
  * `Content-Length:` Size of the payload object in bytes.
  * `Content-Type:` MIME type describing the format of the entity body (`text/html`, `image/jpeg`, `application/json`).

---

<div id="status-codes"></div>

## Status Codes

HTTP response status codes are 3-digit integers partitioned into functional classes:

| Code | Status Phrase | Meaning & Technical Consequence |
| :--- | :--- | :--- |
| **`200`** | **OK** | The request succeeded, and the requested payload is delivered in the response entity body. |
| **`301`** | **Moved Permanently** | The requested resource has permanently relocated to a new URL, specified in the `Location:` response header. Client browsers automatically update their bookmarks and reissue the request to the new URL. |
| **`304`** | **Not Modified** | Response to a **Conditional GET**. Informs the client/proxy that the cached version of the object is still fresh and can be rendered directly from cache; the entity body is deliberately left empty to save bandwidth. |
| **`400`** | **Bad Request** | Generic client error code indicating that the server could not parse the request syntax. |
| **`403`** | **Forbidden** | The server understood the request, but refuses to authorize access, regardless of authentication credentials. |
| **`404`** | **Not Found** | The server cannot locate any document matching the requested Uniform Resource Identifier (URI). |
| **`500`** | **Internal Server Error** | The server encountered an unhandled exception or software failure preventing it from fulfilling the request. |
| **`503`** | **Service Unavailable** | The server is currently unable to handle the request due to temporary system overloading or scheduled maintenance. |

---

<div id="connection-types"></div>

## Connection Types

A core architectural evolution across HTTP revisions centers on how TCP connections are utilized to retrieve web pages containing multiple referenced objects.

```
Base HTML Page: index.html
   |
   +---> References: image1.png
   +---> References: image2.png
   +---> References: script.js
```

### 1. Non-Persistent Connections (HTTP/1.0 Default)
* In a non-persistent connection, **at most one TCP connection is opened per object**.
* When fetching a page containing a base HTML document and $M$ referenced objects, a total of $M + 1$ separate, sequential TCP connections must be opened, used, and torn down.
* **Overhead & Drawbacks:**
  1. **Connection Setup Overhead:** Every object requires a brand-new TCP three-way handshake, consuming at least 1 Round-Trip Time (RTT) before the actual data request can be delivered.
  2. **TCP Slow-Start Penalty:** Each new TCP connection starts in the congestion-avoidance **Slow Start** phase, meaning small windows restrict throughput for every single object.
  3. **Server Resource Drain:** The server OS kernel must allocate buffers and manage Transmission Control Blocks (TCBs) for dozens of fleeting connections, causing high CPU and memory thrashing.

### 2. Persistent Connections without Pipelining (HTTP/1.1 Default)
* The server leaves the TCP connection **open** after sending a response.
* Subsequent requests and responses between the same client and server reuse the existing established TCP connection (`Connection: keep-alive`).
* The client sends a new request only **after** the response for the previous request has been completely received.
* **Performance:** Saves the 1 RTT TCP handshake penalty for every referenced object. Each referenced object now costs **1 RTT** (request-to-response) plus object transmission time.

### 3. Persistent Connections with Pipelining
* The client issues requests for all referenced objects **back-to-back**, as soon as it discovers their URLs in the base HTML, without waiting for intervening responses.
* The server fulfills the requests in the exact order they were received.
* **Performance:** All referenced objects can conceptually be requested in a single RTT burst, minimizing cumulative idle line time.
* *Practical Limitation:* Pipelining suffered severely from **Head-of-Line (HoL) Blocking** (if an early object took a long time to generate on disk, all subsequent responses queued behind it). As a result, pipelining was rarely enabled by default in web browsers and was ultimately superseded by binary framing and stream multiplexing in **HTTP/2**.

---

<div id="timing-ladders"></div>

## Timing Ladders

To compute total latency, we define the **Round-Trip Time (RTT)**: the duration required for a small control packet to travel from client to server and back again.

### Non-Persistent HTTP Timing Ladder (Per Object)
Fetching a single object over non-persistent HTTP requires **$2\text{ RTT} + \text{Transmission Time}$**:

```
CLIENT                                                           SERVER
  |                                                                 |
  | ----------- Step 1: TCP SYN (Initiate Handshake) -------------> |  \
  | <---------- Step 2: TCP SYN-ACK (Handshake Ack) --------------- |   |- RTT_1 (TCP Connection)
  |                                                                 |  /
  | ----------- Step 3: HTTP GET Request (Piggbacked on ACK) -----> |  \
  |                                                                 |   |
  |                                                  [File Access]  |   |- RTT_2 (HTTP Transaction)
  |                                                                 |   |
  | <---------- Step 4: HTTP Response (Base Object Data) ---------- |  /
  |             ======================================              |  \
  |             ======== (Object Transmission Time) ==              |   |- File Transmission (L/R)
  |             ======================================              |  /
  | ----------- TCP FIN (Connection Teardown) --------------------> |
  v                                                                 v
```

### Cumulative Latency Comparison
Suppose a web page contains a base HTML document and $M$ embedded JPEG images.

* **Non-Persistent HTTP (Sequential):**
  $$\text{Total Delay} = \underbrace{2 \cdot \text{RTT} + \frac{L_{\text{base}}}{R}}_{\text{Base HTML Page}} + \sum_{i=1}^{M} \left( 2 \cdot \text{RTT} + \frac{L_i}{R} \right) = 2(M + 1)\text{RTT} + \sum_{i=0}^{M} \frac{L_i}{R}$$
* **Persistent HTTP without Pipelining:**
  $$\text{Total Delay} = \underbrace{2 \cdot \text{RTT} + \frac{L_{\text{base}}}{R}}_{\text{Handshake + Base HTML}} + \sum_{i=1}^{M} \left( 1 \cdot \text{RTT} + \frac{L_i}{R} \right) = (M + 2)\text{RTT} + \sum_{i=0}^{M} \frac{L_i}{R}$$
* **Persistent HTTP with Pipelining:**
  $$\text{Total Delay} \approx 2 \cdot \text{RTT} + \frac{L_{\text{base}}}{R} + 1 \cdot \text{RTT} + \sum_{i=1}^{M} \frac{L_i}{R} = 3 \cdot \text{RTT} + \sum_{i=0}^{M} \frac{L_i}{R}$$

---

<div id="cookies"></div>

## Cookies

Because the HTTP protocol is entirely stateless, websites utilize **Cookies** to maintain session identity, track shopping carts, and preserve user preferences across multiple transactions.

```
CLIENT (Browser)                                        SERVER (e.g., E-Commerce)
  |                                                                 |
  | 1. Initial HTTP GET Request ----------------------------------> |
  |    (No cookie header)                                           | [Generates Unique ID: 1684]
  |                                                                 | [Creates DB Record: 1684]
  | <----------------- 2. HTTP Response --------------------------- |
  |    Set-Cookie: session_id=1684                                  |
  |                                                                 |
  | [Appends 1684 to Cookie file for server]                        |
  |                                                                 |
  | 3. Subsequent HTTP GET Request -------------------------------> |
  |    Cookie: session_id=1684                                      | [Looks up DB Record 1684]
  |                                                                 | [Loads cart, user profile]
  | <----------------- 4. HTTP Response --------------------------- |
  v                                                                 v
```

### The 4 Structural Components of the Cookie Architecture
1. **Response Header:** The `Set-Cookie:` header line included in the HTTP response message from the server (e.g., `Set-Cookie: user_id=98765; Domain=.amazon.com; Path=/; Secure; HttpOnly`).
2. **Request Header:** The `Cookie:` header line included in subsequent HTTP request messages sent by the client's browser (e.g., `Cookie: user_id=98765`).
3. **Client Cookie Store:** A managed file or SQLite database stored on the client host, indexed by server domain name and managed by the web browser.
4. **Backend Database:** An authoritative database maintained by the web server that stores shopping carts, historical preferences, authorization credentials, and profile attributes mapped against the unique cookie key.

### Privacy Implications
While cookies enable essential features like persistent authentication and state tracking, **Third-Party Tracking Cookies** raise significant privacy concerns. When multiple websites embed banner ads or tracking scripts hosted by a common advertising network, that ad broker can read and correlate its own cookies across completely different domains, constructing a detailed behavioral profile of a user's web browsing activity across the entire Internet without explicit user consent.

---

<div id="web-caching"></div>

## Web Caching

A **Web Cache** (also known as a **Proxy Server**) is an intermediary network entity that satisfies HTTP requests on behalf of an origin web server.

```
                                  INSTITUTIONAL NETWORK
                               +---------------------------+
                               |  [ Client 1 ]             |
                               |       \                   |
                               |        v                  |
                               |   [ Web Cache / ] ======= | ======> [ Bottleneck Link ] ===> ( Internet Core )
                               |   [ Proxy Serv. ]         |             (15 Mbps)                     |
                               |        ^                  |                                           v
                               |       /                   |                                  [ Origin Web Server ]
                               |  [ Client 2 ]             |                                    www.university.edu
                               +---------------------------+
```

### 1. The Role of the Web Cache
* When a user requests an object, the browser directs the request directly to the local Web Cache.
* **Cache Hit:** If the cache stores a fresh copy of the object, it immediately delivers it to the client over the fast local area network ($100\text{ Mbps} - 1\text{ Gbps}$), bypassing the slower, costly wide-area link entirely.
* **Cache Miss:** If the object is not cached, the proxy server establishes its own connection to the origin web server, fetches the object, caches a copy locally, and delivers the object to the client.
* **Systemic Benefits:** Substantially reduces the response time experienced by users; decreases traffic on an institution's expensive bottleneck access link to the ISP; prevents popular origin servers from crashing during traffic spikes.

---

### 2. Cache Consistency: The Conditional GET

A major architectural problem arises: *What happens if the origin web server updates the document while a stale copy resides in the web cache?*

The HTTP protocol resolves this problem using the **Conditional GET** mechanism.

```
WEB CACHE / PROXY                                               ORIGIN SERVER
  |                                                                 |
  | 1. HTTP GET (Conditional Request) ----------------------------> |
  |    If-Modified-Since: Thu, 03 Sep 2026 14:20:10 GMT             |
  |                                                                 |
  |                                           [Check Disk Timestamp]
  |                                           [Case A: File has NOT changed]
  | <--- 2a. HTTP/1.1 304 Not Modified ---------------------------- |
  |      (Body is completely empty! Saves bandwidth)                |
  |                                                                 |
  |                                           [Case B: File HAS changed]
  | <--- 2b. HTTP/1.1 200 OK -------------------------------------- |
  |      Last-Modified: Fri, 04 Sep 2026 09:00:00 GMT               |
  |      [Full Updated Object Body Included]                        |
  v                                                                 v
```

1. When a cache receives an object for the first time, it stores the payload and records the timestamp found in the response's `Last-Modified:` header (e.g., `Thu, 03 Sep 2026 14:20:10 GMT`).
2. When a subsequent client requests this object after its local expiration interval, the cache issues a **Conditional GET** to the origin server, appending the `If-Modified-Since:` request header carrying that recorded timestamp:
   ```http
   GET /curriculum/syllabus.pdf HTTP/1.1
   Host: www.ktu.edu.in
   If-Modified-Since: Thu, 03 Sep 2026 14:20:10 GMT
   ```
3. If the resource has **not changed** since that date:
   * The server sends a lightweight response: `HTTP/1.1 304 Not Modified`.
   * The response body is entirely omitted, saving bandwidth across the bottleneck link.
   * The cache serves its existing local copy to the client.
4. If the resource **has changed**:
   * The server responds with `HTTP/1.1 200 OK`, attaching the new `Last-Modified` timestamp and the complete, updated object payload.
   * The cache replaces its stale copy with the newly delivered object.

---

<div id="exam-focus-pitfalls"></div>

## Exam Focus & Pitfalls

::: callout-formula Total Response Time Formula
When computing the cumulative delay to download an HTML file containing $M$ referenced objects over a network link with transmission rate $R$, Round-Trip Time $\text{RTT}$, and negligible processing/queueing delays:

$$\text{Non-Persistent (Sequential): } T = 2(M + 1)\text{RTT} + \frac{L_{\text{base}}}{R} + \sum_{i=1}^{M} \frac{L_i}{R}$$

$$\text{Persistent (Non-Pipelined): } T = (M + 2)\text{RTT} + \frac{L_{\text{base}}}{R} + \sum_{i=1}^{M} \frac{L_i}{R}$$

$$\text{Persistent (Pipelined): } T \approx 3\text{ RTT} + \frac{L_{\text{base}}}{R} + \sum_{i=1}^{M} \frac{L_i}{R}$$
:::

::: callout-pitfall RTT Calculation Mistakes
* **Mistake 1: Forgetting the initial TCP handshake RTT.**
  * *Trap:* Students often calculate non-persistent delay as $1\text{ RTT}$ per object.
  * *Correction:* Every new non-persistent object requires an explicit TCP 3-way handshake ($\text{SYN} \rightarrow \text{SYN-ACK}$), which costs $1\text{ RTT}$ before the HTTP GET can even leave the client. Therefore, every non-persistent object requires **at minimum $2\text{ RTTs}$** ($1\text{ RTT}$ for TCP connection setup $+ 1\text{ RTT}$ for the HTTP GET/response).
* **Mistake 2: Assuming 304 Not Modified contains payload data.**
  * *Trap:* Including file transmission delay $\frac{L}{R}$ when a Conditional GET returns a `304 Not Modified`.
  * *Correction:* A `304 Not Modified` status line carries only header metadata. Its entity body is zero bytes. The transmission delay for the body is exactly zero.
* **Mistake 3: Confusing Persistent without Pipelining with Pipelining.**
  * *Correction:* Without pipelining, the client waits for the response of image $k$ before asking for image $k+1$, accumulating $1\text{ RTT}$ per referenced object. With pipelining, all $M$ requests are fired immediately back-to-back, incurring only $\approx 1\text{ RTT}$ collectively for all referenced requests.
:::

::: callout-exam KTU Standard Numerical Pattern
**Typical 7-Mark KTU Question:** *A client browser downloads a base HTML file of size $20\text{ KB}$ containing references to $4$ JPEG images, each of size $50\text{ KB}$. The available link bandwidth between client and server is $10\text{ Mbps}$, and the one-way propagation delay is $25\text{ ms}$. Assuming zero queuing and processing delays, calculate the total retrieval time under:* *(a) Non-persistent HTTP with sequential connections.* *(b) Persistent HTTP without pipelining.* **Model Solution Framework:**
1. Compute Round-Trip Time:
   $$\text{RTT} = 2 \times 25\text{ ms} = 50\text{ ms} = 0.05\text{ s}$$
2. Calculate total data to transmit:
   $$L_{\text{total}} = 20\text{ KB} + (4 \times 50\text{ KB}) = 220\text{ KB} = 220 \times 1024 \times 8\text{ bits} = 1,802,240\text{ bits}$$
3. Compute total transmission time:
   $$T_{\text{trans}} = \frac{1,802,240\text{ bits}}{10 \times 10^6\text{ bps}} \approx 0.1802\text{ s} = 180.2\text{ ms}$$
4. **Part (a): Non-persistent (Sequential)**
   * Objects: $M = 4 \implies M + 1 = 5$ objects total.
   * Total RTT Delay: $2 \times (4 + 1) \times \text{RTT} = 10 \times 50\text{ ms} = 500\text{ ms}$.
   * Total Retrieval Time: $500\text{ ms} + 180.2\text{ ms} = \mathbf{680.2\text{ ms}}$.
5. **Part (b): Persistent without Pipelining**
   * Total RTT Delay: $(M + 2) \times \text{RTT} = (4 + 2) \times 50\text{ ms} = 6 \times 50\text{ ms} = 300\text{ ms}$.
   * Total Retrieval Time: $300\text{ ms} + 180.2\text{ ms} = \mathbf{480.2\text{ ms}}$.
:::

---

<div id="self-check"></div>

## Self-Check

::: quiz RTT Calculation Under Non-Persistent Connections
A web browser fetches an HTML document referencing 3 external CSS and image files. Assuming the browser opens only one sequential TCP connection at a time and transmission times are negligible, what is the minimum round-trip time (RTT) overhead incurred using non-persistent HTTP?
(A) $4\text{ RTT}$
(B) $6\text{ RTT}$
(*C) $8\text{ RTT}$
(D) $3\text{ RTT}$
::: explanation
The total number of objects fetched is $1$ base HTML file $+ 3$ referenced files $= 4$ objects total. Under non-persistent HTTP, each object requires an independent TCP connection. Each connection requires $1\text{ RTT}$ for the TCP three-way handshake, followed by $1\text{ RTT}$ to issue the HTTP GET and receive the first bytes of the response.
$$\text{Total RTT Delay} = 4 \times 2\text{ RTT} = 8\text{ RTT}$$
Therefore, Option (C) is correct.
:::

::: quiz Web Cache Consistency
When an intermediary proxy server checks whether an existing cached web page is still fresh, which request header and expected success status code are utilized?
(A) Header: `Cache-Control: revalidate`; Status: `200 OK`
(*B) Header: `If-Modified-Since`; Status: `304 Not Modified`
(C) Header: `ETag-Verify`; Status: `204 No Content`
(D) Header: `Set-Cookie`; Status: `301 Moved Permanently`
::: explanation
A web proxy issues a **Conditional GET** appending the `If-Modified-Since:` header containing the timestamp from the object's previous retrieval. If the origin server verifies that the file on disk has not been altered since that timestamp, it replies with `304 Not Modified` with an empty entity body, instructing the cache to serve its stored copy.
:::

::: quiz Cookie Mechanics
Where does the unique identification token that forms the heart of an HTTP stateful session originate, and where is it subsequently stored?
(A) Generated by the client browser; stored permanently in the router's forwarding table
(B) Generated by the local DNS server; stored in the operating system's ARP table
(*C) Generated by the web server in a `Set-Cookie:` header; stored in the client browser's local cookie file
(D) Generated by the network switch; stored in the HTML document body
::: explanation
Cookies are created on the **server side**. When a client connects without identity metadata, the server allocates a session record in its backend database, generates a unique identification string, and transmits it to the browser via the `Set-Cookie:` response header. The client's web browser then persists this value locally and re-attaches it as a `Cookie:` request header in all subsequent requests back to that same domain.
:::
