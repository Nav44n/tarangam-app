# Internet of Things (IoT) Architecture, Protocols, and Wireless Technologies

**IoT Layered Architecture, Application Layer Protocols (MQTT vs CoAP), IoT Security Principles, GSM, Bluetooth Low Energy (BLE), and LoRa LPWAN Networks.**

<a id="the-intuition"></a>
## 1. IoT System Architecture & Functional Layers

::: callout-intuition Edge-to-Cloud Continuum
<!-- Conceptual intuition syntax block: Sensing at edge -> Gateway aggregation -> Cloud telemetry -->
:::

* **4-Layer IoT Model**:
  <!-- Perception Layer (Sensors/Actuators) -> Network Layer (Gateways/Routers) -> Middleware / Service Management -> Application Layer -->
* **IoT Security Principles & Threat Vectors**:
  <!-- Data confidentiality (TLS/DTLS), device authentication, eavesdropping, botnet exploitation -->

---

<a id="the-dimensions"></a>
## 2. IoT Application Layer Protocols: MQTT vs CoAP

<div class="table-wrap">

| Parameter | MQTT (Message Queuing Telemetry Transport) | CoAP (Constrained Application Protocol) |
| :--- | :--- | :--- |
| **Communication Paradigm** | Publish / Subscribe via Central Broker | Request / Response (RESTful model) |
| **Transport Protocol** | TCP (Connection-oriented, reliable) | UDP (Connectionless, low-overhead) |
| **Header Overhead** | Minimal 2-byte fixed header | Minimal 4-byte base header |
| **Quality of Service (QoS)**| QoS 0 (At most once), QoS 1 (At least once), QoS 2 (Exactly once) | Confirmable (CON) vs Non-Confirmable (NON) |
| **Transport Security** | TLS / SSL | DTLS (Datagram TLS) |

</div>

```text
[MQTT Publish-Subscribe Architecture Scaffold]
Sensor Node (Publisher) ---> Topic: "home/temp" ---> MQTT Broker ---> Dashboard (Subscriber)
```

---

<a id="foundations"></a>
## 3. Wireless Technologies: GSM, BLE, and LoRa LPWAN

* **GSM / Cellular Modules (e.g., SIM800 / SIM900)**:
  <!-- Hayes AT commands: ATD (voice call), AT+CMGS (SMS), AT+CIPSTART (GPRS TCP/IP socket) -->
* **Bluetooth Low Energy (BLE 4.2 / 5.x)**:
  <!-- Generic Access Profile (GAP), Generic Attribute Profile (GATT), Services, and Characteristics -->
* **LoRa & LoRaWAN Long-Range Radio**:
  <!-- Chirp Spread Spectrum (CSS) modulation, Spreading Factor (SF7-SF12), sub-GHz ISM bands (868/915 MHz) -->

```c
// [AT Command Communication Syntax Template]
void send_sms(UART_HandleTypeDef *huart, const char *number, const char *text) {
    char cmd[64];
    sprintf(cmd, "AT+CMGS=\"%s\"\r\n", number);
    HAL_UART_Transmit(huart, (uint8_t *)cmd, strlen(cmd), 1000);
    // Transmit body followed by Ctrl+Z (0x1A)
}
```

---

<a id="history"></a>
## 4. IoT Home Automation Case Study Architecture

* **System Design Blueprint**:
  <!-- STM32 MCU aggregator + Wireless transceiver + Actuator relay bank + Cloud dashboard -->
* **Power Budget & Duty-Cycling**:
  <!-- Wake from Stop mode -> Read sensor -> Transmit LoRa packet -> Re-enter deep sleep -->

---

<a id="self-check"></a>
## 5. Self-Check Interactive Quiz

::: quiz MQTT vs CoAP Transport Layer
Which underlying transport layer protocol is utilized by MQTT for persistent connection-oriented broker communication?
(*) Transmission Control Protocol (TCP)
( ) User Datagram Protocol (UDP)
( ) Internet Control Message Protocol (ICMP)
( ) Raw Ethernet IEEE 802.3
::: explanation
**MQTT** relies on **TCP** to guarantee ordered, reliable byte-stream delivery between distributed IoT clients and the central MQTT broker.
:::
