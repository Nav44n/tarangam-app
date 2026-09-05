# Universal Serial Bus (USB) Interface and HID Device Emulation

**USB 2.0 Physical Layer, Endpoint Architectures, Standard Device Descriptors, and Implementing HID Keyboard / Mouse Emulation on STM32.**

<a id="the-intuition"></a>
## 1. Universal Serial Bus (USB) Architecture

::: callout-intuition Host-Centric Master-Slave Bus
<!-- Conceptual intuition syntax block: USB Host polls endpoints; peripherals never initiate unscheduled transfers -->
:::

* **USB Speed Classes**:
  <!-- Low Speed (1.5 Mbps), Full Speed (12 Mbps), High Speed (480 Mbps) -->
* **Differential Signaling & Physical Lines**:
  <!-- D+ and D- lines, NRZI encoding, bit stuffing, 1.5k pull-up resistor detection -->

---

<a id="the-dimensions"></a>
## 2. USB Transfer Types & Endpoint Topologies

<div class="table-wrap">

| Transfer Type | Bandwidth Guarantee | Error Recovery | Typical Application |
| :--- | :--- | :--- | :--- |
| **Control** | Guaranteed fair access | Handshake & retry | <!-- Device configuration, enumeration (Endpoint 0) --> |
| **Interrupt** | Guaranteed bounded latency | Handshake & retry | <!-- Keyboards, mice, gamepads (HID devices) --> |
| **Bulk** | Uses available bandwidth | Handshake & retry | <!-- Flash drives, printers (mass storage) --> |
| **Isochronous** | Guaranteed fixed rate | No retry (real-time) | <!-- Audio/video streaming headsets, webcams --> |

</div>

---

<a id="foundations"></a>
## 3. The USB Descriptor Hierarchy

::: callout-exam KTU High-Yield Focus: Standard Descriptor Chain
<!-- KTU Exam Focus syntax block: Device Descriptor -> Configuration Descriptor -> Interface Descriptor -> Endpoint Descriptor -->
:::

```c
// [USB HID Report Descriptor Syntax Template: 8-Byte Keyboard Report]
__ALIGN_BEGIN static uint8_t HID_Keyboard_ReportDesc[] __ALIGN_END = {
    0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
    0x09, 0x06,                    // USAGE (Keyboard)
    0xa1, 0x01,                    // COLLECTION (Application)
    // Modifier byte (Ctrl, Shift, Alt, GUI)
    // Reserved padding byte
    // 6 Key-code array bytes (6KRO)
    0xc0                           // END_COLLECTION
};
```

---

<a id="history"></a>
## 4. Human Interface Device (HID) Mouse & Keyboard Emulation

* **HID Class Advantages**:
  <!-- Native OS driver support without custom installation on Windows/macOS/Linux -->
* **Report Descriptors & Input Reports**:
  <!-- Formatting 4-byte mouse report (buttons, X delta, Y delta, wheel) -->
* **STM32 USB Device Library (USBD) Workflow**:
  <!-- Sending HID reports using USBD_HID_SendReport API on STM32U575 -->

```c
// [STM32 USB HID Send Report Syntax Template]
typedef struct {
    uint8_t buttons;
    int8_t  x_delta;
    int8_t  y_delta;
    int8_t  wheel;
} MouseReport_t;

void send_mouse_move(int8_t dx, int8_t dy) {
    MouseReport_t report = {0, dx, dy, 0};
    USBD_HID_SendReport(&hUsbDeviceFS, (uint8_t *)&report, sizeof(report));
}
```

---

<a id="self-check"></a>
## 5. Self-Check Interactive Quiz

::: quiz USB Endpoint 0
In the USB protocol specification, what is the mandatory transfer type and role assigned to **Endpoint 0** across all USB peripherals?
(*) Bidirectional Control Transfer used during device enumeration and configuration.
( ) Unidirectional Interrupt Transfer for high-speed sensor streaming.
( ) Bulk Out Transfer for firmware upgrades.
( ) Isochronous In Transfer for real-time audio samples.
::: explanation
**Endpoint 0** is always a **bidirectional control endpoint** reserved for host enumeration, reading descriptors, and assigning device bus addresses.
:::
