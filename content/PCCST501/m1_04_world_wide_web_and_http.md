---
id: m1_04_world_wide_web_and_http
title: "The Web and HTTP"
sidebar_label: "1.4 Web & HTTP"
description: "Deep dive into the Hypertext Transfer Protocol (HTTP), persistent vs non-persistent connections, and cookies."
---

# The World Wide Web and HTTP

The World Wide Web transformed the Internet from an academic tool into a global mainstream phenomenon. The Web operates on a strict Client-Server paradigm, and its central communication protocol is **HTTP** (Hypertext Transfer Protocol).

---

## 1. Web Terminology Basics

* **Web Page:** A document, usually containing base HTML and several referenced objects (like images, CSS files, JavaScript).
* **Object:** Simply a file (e.g., an HTML file, a JPEG image, a video clip).
* **URL (Uniform Resource Locator):** The address of the object, consisting of a hostname (`www.example.com`) and a path name (`/images/pic.jpg`).

---

## 2. HTTP Overview

HTTP is implemented in two programs: a client program (your web browser) and a server program (e.g., Apache, Nginx). It defines how web clients request web pages from web servers and how servers transfer them to clients.

* **Transport Protocol:** HTTP uses **TCP** as its underlying transport protocol to ensure reliable delivery. It does not use UDP.
* **Statelessness:** HTTP is a **stateless** protocol. The server maintains absolutely no information about past client requests. If you request a page and then request the exact same page 2 seconds later, the server treats it as a completely new request.

---

## 3. Non-Persistent vs. Persistent Connections

How does a client pull down a webpage that contains an HTML file and 10 referenced JPEG images?

### Non-Persistent HTTP (HTTP/1.0)
* A brand new TCP connection must be opened and closed for every single object.
* **Drawback:** High overhead. Fetching an HTML file and 10 images requires opening and closing 11 separate TCP connections, causing significant latency due to the repeated TCP Three-Way Handshake setup time.

### Persistent HTTP (HTTP/1.1)
* The server leaves the TCP connection open after sending a response.
* Subsequent requests and responses between the same client and server can be sent over that same open connection.
* Drastically reduces latency and CPU overhead on the server.

---

## 4. HTTP Request and Response Messages

When your browser communicates with a server, it exchanges plain-text HTTP messages.

### HTTP Request Message
* **Request Line:** Contains the method (`GET`, `POST`, `HEAD`, `PUT`, `DELETE`), the URL path, and the HTTP version (e.g., `GET /index.html HTTP/1.1`).
* **Header Lines:** Metadata such as `Host:`, `User-Agent:` (client browser type), and `Accept-Language:`.
* **Entity Body:** Used primarily in `POST` requests when submitting form data or payloads to the server.

### HTTP Response Message
* **Status Line:** Contains the protocol version, a status code, and a status message (e.g., `HTTP/1.1 200 OK` or `HTTP/1.1 404 Not Found`).
* **Header Lines:** Metadata such as `Date:`, `Server:`, `Content-Length:`, and `Content-Type:`.
* **Data (Body):** The actual requested object payload (the HTML file, image data, etc.).

---

## 5. Cookies: Maintaining State

Because HTTP is stateless, websites use **Cookies** to keep track of sessions, authentication, and shopping carts:

1. **Initial Visit:** You visit a website (e.g., Amazon) for the first time.
2. **Identification:** The server creates a unique identification number (e.g., `1678`) and saves it in a backend database.
3. **Cookie Assignment:** The server responds with an HTTP header: `Set-cookie: 1678`.
4. **Client Storage:** Your browser saves this cookie locally.
5. **Session Continuity:** On your next request to Amazon, your browser automatically includes the header: `Cookie: 1678`. The server reads the ID, looks it up in the database, and retrieves your state.

---

## 6. Active Recall Quiz

* **Question 1:** Why is HTTP referred to as a "stateless" protocol?
* **Question 2:** An HTML page contains text and 5 image references. How many total TCP connections are established to fetch this entire page in Non-Persistent HTTP vs. Persistent HTTP?