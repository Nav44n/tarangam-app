# Serial Communication Protocols: USART, I2C, SPI, and CAN Bus

**Serial Terminal Applications, I2C Sensor Interfacing, SPI EEPROM Data Persistence, and Robust Multi-Node CAN Bus Networking.**

<a id="the-intuition"></a>
## 1. Protocol Comparison Matrix: USART, I2C, SPI, and CAN

::: callout-intuition Synchronous vs Asynchronous Communication
<!-- Conceptual intuition syntax block: Shared clock wire vs agreed baud rate timing -->
:::

<div class="table-wrap">

| Parameter | USART | I2C | SPI | CAN Bus |
| :--- | :--- | :--- | :--- | :--- |
| **Clocking** | Asynchronous / Sync | Synchronous (SCL) | Synchronous (SCK) | Asynchronous (Bit-time) |
| **Wire Count** | 2 (`TX`, `RX`) | 2 (`SDA`, `SCL`) | 4 (`MOSI`, `MISO`, `SCK`, `CS`) | 2 (`CAN_H`, `CAN_L`) |
| **Duplex Mode** | Full-Duplex | Half-Duplex | Full-Duplex | Half-Duplex |
| **Max Bit Rate** | ~1–10 Mbps | 100k / 400k / 1M / 3.4M | 10–50+ Mbps | 1 Mbps (Classic) / 5+M (FD) |
| **Addressing** | Point-to-point | 7-bit or 10-bit address | Dedicated Chip Select ($CS$) | 11-bit or 29-bit Message ID |

</div>

---

<a id="the-dimensions"></a>
## 2. USART & Serial Terminal Interface

::: callout-formula Baud Rate Divisor Formula
<!-- Formula vault syntax block: Baud rate calculation for USART_BRR -->
$$\text{USARTDIV} = \frac{f_{\text{CK}}}{16 \times \text{Baud Rate}}$$
:::

```c
// [STM32 HAL UART Transmit Syntax Template]
void print_serial(UART_HandleTypeDef *huart, const char *msg) {
    HAL_UART_Transmit(huart, (uint8_t *)msg, strlen(msg), HAL_MAX_DELAY);
}
```

---

<a id="foundations"></a>
## 3. I2C Sensor Interfacing & SPI Memory Access

* **I2C Protocol Frame Format**:
  <!-- START condition, 7-bit Slave Address + R/W bit, ACK/NACK, 8-bit Data bytes, STOP condition -->
* **Interfacing I2C Temperature Sensor & I2C Alphanumeric LCD**:
  <!-- PCF8574 I2C expander interfacing to HD44780 LCD -->
* **SPI Protocol & EEPROM Memory (e.g., 25LCxxx)**:
  <!-- CPOL and CPHA clock polarity/phase modes, Instruction opcodes (WREN, WRITE, READ) -->

```c
// [STM32 HAL I2C Memory Read Syntax Template]
HAL_StatusTypeDef read_i2c_sensor(I2C_HandleTypeDef *hi2c, uint16_t dev_addr, uint8_t *buffer, uint16_t size) {
    return HAL_I2C_Master_Receive(hi2c, dev_addr << 1, buffer, size, 100);
}
```

---

<a id="history"></a>
## 4. Controller Area Network (CAN) Bus Architecture

::: callout-exam KTU High-Yield Focus: CAN Differential Signaling & Arbitration
<!-- KTU Exam Focus syntax block: CAN_H vs CAN_L dominant/recessive bit levels, non-destructive bitwise arbitration -->
:::

* **Physical Layer & Transceivers**:
  <!-- 120-ohm termination resistors, differential voltage Vdiff = CAN_H - CAN_L -->
* **Message Frame Anatomy**:
  <!-- SOF, Arbitration ID (11-bit / 29-bit), RTR bit, Control field (DLC), Data (0-8 bytes), CRC, ACK, EOF -->
* **Configuring CAN Communication Between Multiple STM32U575 MCUs**:
  <!-- Bit timing calculation (Sync, Prop, Phase1, Phase2), Filter banks, and Tx/Rx Mailboxes -->

---

<a id="self-check"></a>
## 5. Self-Check Interactive Quiz

::: quiz CAN Bus Arbitration Mechanism
In the Controller Area Network (CAN) protocol, what happens when two nodes begin transmitting message frames simultaneously?
(*) The node transmitting a dominant bit (0) overwrites the recessive bit (1); the node transmitting the recessive bit detects the mismatch and gracefully drops off the bus.
( ) Both nodes experience a collision and abort, retrying after an exponential backoff time.
( ) The node with the higher physical MAC address wins arbitration automatically.
( ) The bus arbiter hardware assigns transmission slots using round-robin scheduling.
::: explanation
CAN implements **non-destructive bitwise arbitration**: the **dominant bit (logic 0)** overrides the **recessive bit (logic 1)** on the physical differential bus, allowing the highest priority message to proceed without corrupting transmission.
:::
