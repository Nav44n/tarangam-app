---
id: m1_01_internet_overview_and_network_edge
title: "Internet Overview & The Network Edge"
sidebar_label: "1.1 Internet & Network Edge"
description: "An introduction to the nuts and bolts of the Internet, end systems, and access networks."
---

# Internet Overview & The Network Edge

## 1. The Big Picture: What is the Internet?

When you open an app on your phone to send a message, you are utilizing the largest engineered system in human history. The Internet can be defined in two distinct ways: by its "nuts and bolts" (the physical components) and by its services (what it does for applications).

### The "Nuts and Bolts" View

Imagine the global highway system. The Internet is similar, but instead of moving cars, it moves data.

* **End Systems (Hosts):** Laptops, smartphones, servers, smart TVs, and IoT devices. They sit at the "edge" of the network.
* **Communication Links:** The roads. These include fiber optics, copper wire, radio, and satellite. Different links have different transmission rates (bandwidth).
* **Packet Switches:** The intersections and roundabouts. Routers and switches take chunks of data (packets) arriving on one incoming communication link and forward them to an outgoing communication link.

### The "Services" View

From a software engineering perspective, the Internet is a distributed application platform. It provides a communication infrastructure that enables applications (like web browsers, social media networks, and streaming services) to exchange data.

---

## 2. The Network Edge

The "Network Edge" refers to the devices and systems that sit on the absolute boundary of the Internet. If the Internet is a vast city, the edge consists of the houses and businesses where the trips actually begin and end.

### End Systems (Hosts)

We call them "end systems" because they sit at the edge, and we call them "hosts" because they host (run) application programs such as a web browser or a web server.

Hosts are broadly divided into:

* **Clients:** Desktops, mobile devices, and laptops that request information.
* **Servers:** Powerful machines that store and distribute web pages, stream video, or relay emails. Today, most servers reside in massive data centers.

### Access Networks

How do you connect your laptop (at the edge) to the very first router (the edge router) in the vast network core? This is done via an Access Network.

Common types of access networks include:

* **Home Networks (DSL, Cable, FTTH):** Uses digital subscriber lines (copper telephone wire), cable (coaxial television cable), or Fiber to the Home.
* **Enterprise Networks (Ethernet):** Used in companies and universities. Devices connect to Ethernet switches, which connect to an institutional router.
* **Wireless Access Networks (Wi-Fi, 4G/5G):**
  * **Wireless LANs (Wi-Fi):** Within a building, transmitting to a local base station (access point).
  * **Wide-Area Wireless Networks (Cellular):** Transmitting to a cell tower tens of kilometers away.

---

## 3. Physical Media

Data doesn't teleport; it requires a physical medium to travel from point A to point B. Bits propagate across these media via electromagnetic waves or light pulses.

* **Guided Media:** The waves are guided along a solid medium.
  * **Twisted-Pair Copper Wire:** The oldest and most common. Used in Ethernet cables (Cat5, Cat6).
  * **Coaxial Cable:** Two concentric copper conductors. Can achieve high download speeds.
  * **Fiber Optics:** Thin flexible glass fibers conducting pulses of light. Extremely fast, immune to electromagnetic interference, and used for long-haul transatlantic links.
* **Unguided Media:** The waves propagate in the atmosphere and in outer space.
  * **Terrestrial Radio Channels:** AM/FM radio, Wi-Fi.
  * **Satellite Radio Channels:** Geosynchronous or Low Earth Orbit (LEO, like Starlink) satellites.

---

## 4. Active Recall Quiz

* **Question 1:** Why is a smartphone considered an "end system" or "host"?
* **Question 2:** If you are watching a Netflix movie on a smart TV connected via Wi-Fi, which parts of the "nuts and bolts" are involved?