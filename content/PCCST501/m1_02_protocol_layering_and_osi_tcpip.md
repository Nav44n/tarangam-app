---
id: m1_02_protocol_layering_and_osi_tcpip
title: "Protocol Layering & OSI/TCP/IP Models"
sidebar_label: "1.2 Protocol Layering"
description: "Understanding how network tasks are divided into layers using the OSI and TCP/IP reference models."
---

# Protocol Layering and OSI vs. TCP/IP

## 1. What is a Protocol?

In human communication, protocols dictate how we interact. If you ask, "What is the time?", the protocol dictates that the other person responds with the time, not by singing a song.

In networking, a **protocol** defines the format and the order of messages exchanged between two or more communicating entities, as well as the actions taken on the transmission and/or receipt of a message or other event.

---

## 2. Why Layering? (The Airline Analogy)

Networks are incredibly complex systems. To deal with this complexity, network designers use a layered architecture.

Imagine flying from New York to London:

* **Ticket Layer:** You purchase a ticket.
* **Baggage Layer:** You check your bags.
* **Gate Layer:** You board the plane.
* **Runway Layer:** The plane takes off.

Each layer provides a service to the layer directly above it. The baggage layer relies on the ticket layer (you can't check bags without a ticket). By separating tasks into layers, if the airline decides to change how baggage is handled (e.g., using robots instead of humans), it does not affect the ticketing system or the flight physics. This is called **modularity**.

---

## 3. The OSI Reference Model (7 Layers)

The Open Systems Interconnection (OSI) model was created by ISO as a conceptual framework. While not strictly implemented in modern software, it is the universal language network engineers use to troubleshoot.

* **Layer 7 - Application:** Network process to application (HTTP, FTP, SMTP).
* **Layer 6 - Presentation:** Data representation, encryption, and decryption (SSL/TLS, JPEG).
* **Layer 5 - Session:** Interhost communication, establishing and terminating connections.
* **Layer 4 - Transport:** End-to-end connections and reliability (TCP, UDP).
* **Layer 3 - Network:** Path determination and logical addressing (IP, ICMP).
* **Layer 2 - Data Link:** Physical addressing and MAC (Ethernet, Wi-Fi).
* **Layer 1 - Physical:** Media, signal, and binary transmission (cables, hubs).

> **Mnemonic (Bottom to Top):** **P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way

---

## 4. The TCP/IP Model (5 Layers)

The Internet actually runs on the TCP/IP suite, which simplifies the OSI model into 5 practical layers (often depicted as 4 in older textbooks where Physical and Link are combined).

* **Application Layer:** Combines OSI Layers 5, 6, and 7 *(PDU: Messages)*.
* **Transport Layer:** Same as OSI Layer 4 *(PDU: Segments)*.
* **Network Layer:** Same as OSI Layer 3 *(PDU: Datagrams / Packets)*.
* **Link Layer:** Same as OSI Layer 2 *(PDU: Frames)*.
* **Physical Layer:** Same as OSI Layer 1 *(PDU: Bits)*.

---

## 5. Encapsulation and Decapsulation

When a message is sent from a sender to a receiver, it travels down the layers on the sender's side and up the layers on the receiver's side.

### Encapsulation (Sending)
As the data moves down, each layer adds its own specific header (like placing a letter inside a sequence of increasingly larger envelopes):

1. **Application** creates a **Message**.
2. **Transport** adds a transport header $\rightarrow$ becomes a **Segment**.
3. **Network** adds an IP header $\rightarrow$ becomes a **Datagram**.
4. **Link** adds a MAC header and trailer $\rightarrow$ becomes a **Frame**.

### Decapsulation (Receiving)
As the data moves up the receiver's stack, each layer reads its specific header, strips it off, and passes the remaining payload up to the next layer.

---

## 6. Active Recall Quiz

* **Question 1:** Why is modularity/layering highly beneficial in network design?
* **Question 2:** Match the Protocol Data Unit (PDU) to its corresponding TCP/IP layer: Frame, Segment, Datagram, Message.