---
id: m1_03_application_layer_paradigms
title: "Application Layer Paradigms"
sidebar_label: "1.3 App Layer Paradigms"
description: "An exploration of Client-Server and Peer-to-Peer network application architectures."
---

# Application Layer Paradigms

When a software developer creates a network application, they do not write code for the routers or switches in the network core. They write code that runs on the end systems (hosts). To structure this software, developers choose between two dominant architectural paradigms: Client-Server and Peer-to-Peer (P2P).

---

## 1. The Client-Server Architecture

In a client-server architecture, there is an always-on host, called the server, which services requests from many other hosts, called clients.

### Key Characteristics

* **Asymmetry:** The server provides a service; the client consumes it.
* **Always-on Server:** The server must have a permanent, fixed IP address so clients can always find it.
* **Clients Do Not Communicate Directly:** If Client A wants to talk to Client B (like in early chat rooms), Client A sends the message to the Server, and the Server forwards it to Client B.
* **Scalability Bottleneck:** If millions of clients hit the server at once, the server can crash (this is how a DDoS attack works). To fix this, tech giants use data centers containing hundreds of thousands of servers acting as a single virtual server.

* **Examples:** Web (HTTP), Email (SMTP), File Transfer (FTP), Netflix.

---

## 2. The Peer-to-Peer (P2P) Architecture

In a P2P architecture, there is minimal (or no) reliance on dedicated servers. Instead, direct communication occurs between pairs of intermittently connected hosts, called peers.

Peers are not owned by the service provider but are the users' own desktops and laptops.

### Key Characteristics

* **Symmetry:** Every peer acts as both a client (requesting data) and a server (providing data to others).
* **Self-Scalability:** As new peers join the network, they generate new workload (requests for files), but they also add service capacity to the network (by uploading files to others).
* **Decentralized:** No single point of failure. If one peer turns off their computer, the network survives.
* **Challenges:** Security is difficult, performance is highly variable (depends on user upload speeds), and IP addresses change constantly (dynamic IPs).

* **Examples:** BitTorrent, Blockchain/Bitcoin nodes, Skype (in its early days).

---

## 3. Processes Communicating via Sockets

Regardless of whether it's Client-Server or P2P, the actual communication happens between processes running on the end systems.

When a process wants to send a message to another process on a different machine, it sends it out through a software interface called a **socket**.

* **The Door Analogy:** A process is like a house, and its socket is the door. When a sender process wants to send a message, it shoves the message out the door (socket). The sender assumes that there is a transport infrastructure (the postal service / network layers) on the other side of the door that will deliver the message to the receiver's door.
* **Addressing:** To deliver the message, the network needs two identifiers:
  * **IP Address:** To find the correct destination host computer (like a street address).
  * **Port Number:** To find the correct receiving process running on that computer (like an apartment number). For example, a Web Server process usually listens on Port 80.

---

## 4. Active Recall Quiz

* **Question 1:** Why is P2P considered "self-scaling"?
* **Question 2:** If two processes are communicating over the Internet, why isn't an IP address alone sufficient to get the data to the correct application?