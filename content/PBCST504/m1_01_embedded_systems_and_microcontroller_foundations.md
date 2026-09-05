# Introduction to Embedded Systems and Microcontrollers
**What makes a computer "embedded", real-world applications, Microprocessors vs Microcontrollers, and Processor Classification (RISC vs CISC, Harvard vs Von Neumann).**

---

### Quick Navigation
- [Section 1: What is an Embedded System?](#the-intuition)
- [Section 2: Microprocessor vs Microcontroller (The Silicon Difference)](#the-dimensions)
- [Section 3: Processor Classification (RISC/CISC & Harvard/Von Neumann)](#foundations)
- [Section 4: Real-World Applications Across Modern Industries](#history)
- [Section 5: Interactive Self-Check Quiz](#self-check)

---

<a id="the-intuition"></a>
## Section 1: What is an Embedded System?

If you are reading this on a laptop, desktop, or smartphone, you are interacting with a **general-purpose computer**. A general-purpose machine is designed to do almost anything: run a web browser, compile code, stream $4\text{K}$ video, render 3D games, or calculate tax spreadsheets. Because it must do everything, it is large, expensive, power-hungry, and runs a complex operating system with millions of lines of code that can occasionally freeze or crash.

An **embedded system** is the exact opposite.

::: callout-intuition The Chef vs The Microwave Oven
Imagine hiring a world-renowned Michelin-star chef to sit in your kitchen 24/7. This chef can prepare French cuisine, roll Japanese sushi, or bake Italian sourdough. However, hiring this chef costs $\$15,000$ a month, consumes massive amounts of energy, requires a huge workspace, and occasionally takes a 20-minute break when overwhelmed. This is your **General-Purpose Laptop (Microprocessor)**.

Now imagine a simple pop-up toaster or microwave oven. It cannot make sushi. It cannot bake sourdough. It does exactly **one** thing: it heats bread evenly until a mechanical timer trips. It costs $\$20$, draws zero power when idle, boots up in $2\text{ milliseconds}$, never crashes, and will perform identically every morning for twenty years. This is an **Embedded System (Microcontroller)**.
:::

### Formal Definition of an Embedded System

An **Embedded System** is an engineered combination of **specialized hardware** and **dedicated software (firmware)** integrated as part of a larger mechanical or electrical system, designed to execute a **dedicated, fixed function** under strict operational constraints.

```
+-----------------------------------------------------------------------+
|                         PHYSICAL ENVIRONMENT                          |
|             (Temperature, Pressure, Speed, Biological Signals)        |
+-----------------------------------------------------------------------+
          |                                                 ^
          | Physical Phenomenon                             | Physical Action
          v                                                 |
   +--------------+                                  +--------------+
   |   Sensors    |                                  |  Actuators   |
   | (Thermistor, |                                  |   (Motors,   |
   |  Photodiode) |                                  | Solenoids,   |
   +--------------+                                  |   Valves)    |
          |                                                 ^
          | Weak Analog Signal                              | High-Power Drive
          v                                                 |
   +--------------+                                  +--------------+
   | Condition &  |                                  | Power Driver |
   |  ADC Unit    |                                  | / Transistor |
   +--------------+                                  +--------------+
          |                                                 ^
          | Digital Samples (Bits)                          | Control Signals
          v                                                 |
+=======================================================================+
|                     EMBEDDED MICROCONTROLLER                          |
|                                                                       |
|   +-------------------+    Internal Bus    +--------------------+     |
|   |  CPU Core         |<==================>| SRAM               |     |
|   |  (Executes Logic) |                    | (Active Variables) |     |
|   +-------------------+                    +--------------------+     |
|             ^                                       ^                 |
|             |                                       |                 |
|             v                                       v                 |
|   +-------------------+                    +--------------------+     |
|   | Flash Memory      |                    | Hardware Timers    |     |
|   | (Firmware Code)   |                    | & Watchdog Unit    |     |
|   +-------------------+                    +--------------------+     |
|             ^                                       ^                 |
|             +-------------------+-------------------+                 |
|                                 v                                     |
|                      +--------------------+                           |
|                      | GPIO & Peripheral  |                           |
|                      | Registers (PWM/SPI)|                           |
|                      +--------------------+                           |
+=======================================================================+
       ^                                                 |
       | DC Power (e.g., 3.3V / 5V)                      | Status LED / Buzzer
+--------------+                                  +--------------+
| Power Supply |                                  | User Display |
| / Regulators |                                  | (OLED / LCD) |
+--------------+                                  +--------------+
```

### The 5 Core Constraints of Embedded Design

Every embedded engineer must balance five non-negotiable physical constraints:

1. **Real-Time Deadlines (Determinism)**:
   - *Hard Real-Time*: A missed deadline equals catastrophic system failure. If an automotive Airbag Controller or Anti-Lock Braking System (ABS) responds $15\text{ ms}$ too late, human lives are lost.
   - *Soft Real-Time*: Deadlines are desired, but a slight delay degrades quality without causing failure (e.g., a smart TV dropping an audio packet or an air-conditioner display taking an extra $100\text{ ms}$ to update temperature).
2. **Strict Power Budgets**: Many embedded devices operate on small coin-cell batteries (such as a $3\text{V}$ CR2032 with only $220\text{ mAh}$ capacity) or solar energy harvesting. Microcontrollers must spend $99.9\%$ of their life in "Deep Sleep" consuming less than $1\ \mu\text{A}$, waking up for only $500\ \mu\text{s}$ to take a reading and returning to sleep.
3. **Severe Memory Limits**: While your laptop contains $16\text{ GB}$ of RAM ($17,179,869,184\text{ bytes}$), an entry-level microcontroller like an ATmega328P or an ARM Cortex-M0+ might only possess $2\text{ KB}$ to $32\text{ KB}$ of SRAM. Every byte, buffer, and variable must be explicitly accounted for.
4. **Absolute Reliability & Autonomous Operation**: Once an embedded system is deployed—whether buried inside an undersea fiber repeater, soldered into a pacemaker inside a patient's chest, or mounted on a spacecraft—it cannot be rebooted with `Ctrl + Alt + Delete`. It must run for $10$ to $20$ years without human intervention.
5. **Unit Manufacturing Cost**: If you design a microwave controller manufactured for $5,000,000$ units, shaving $\$0.12$ off the cost of the silicon by optimizing code to fit in a smaller ROM saves the manufacturer $\$600,000$ in pure profit.

---

<a id="the-dimensions"></a>
## Section 2: Microprocessor vs Microcontroller (The Core Silicon Difference)

A common point of confusion for engineering beginners is the difference between a **Microprocessor ($\mu\text{P}$)** and a **Microcontroller ($\mu\text{C}$)**. Both contain a Central Processing Unit (CPU) that executes instructions, but their internal physical construction on the silicon die is fundamentally different.

```
MICROPROCESSOR SYSTEM (Board-Level Integration)
Requires dozens of discrete chips routed across a complex PCB:

+-------------------------------------------------------------------+
| Printed Circuit Board (Motherboard)                               |
|                                                                   |
|  +------------------+         High-Speed PCB Traces               |
|  |                  |         (64-bit Address & Data Bus)         |
|  |  MICROPROCESSOR  |==================+======================+   |
|  |  (CPU Core Only) |                  |                      |   |
|  |  e.g., Intel i7  |                  v                      v   |
|  |  Apple M-Series  |        +------------------+   +-----------+ |
|  |                  |        | External RAM     |   | Ext. Flash| |
|  +------------------+        | (DDR4 / DDR5)    |   | (SSD/ROM) | |
|                               +------------------+   +-----------+ |
|                                        |                          |
|                                        v                          |
|                              +--------------------+               |
|                              | External I/O Chip  |               |
|                              | (USB / PCIe / LAN) |               |
|                              +--------------------+               |
+-------------------------------------------------------------------+

=====================================================================

MICROCONTROLLER (Single-Die Monolithic Silicon)
Everything is integrated onto ONE single microscopic piece of silicon:

+-------------------------------------------------------------------+
| Single Silicon Die (e.g., STM32, PIC, ATmega)                     |
|                                                                   |
|   +--------------------+     +--------------------------------+   |
|   | CPU Core           |     | Flash Memory (Program Code)    |   |
|   | (ALU, Regs, PC)    |     | 32 KB - 1 MB                   |   |
|   +--------------------+     +--------------------------------+   |
|            ^                                  ^                   |
|            |      Internal On-Chip Bus        |                   |
|            +==================================+                   |
|            |                                  |                   |
|            v                                  v                   |
|   +--------------------+     +--------------------------------+   |
|   | SRAM (Data Memory) |     | Peripherals: ADC, DAC, Timers, |   |
|   | 2 KB - 256 KB      |     | PWM, UART, SPI, I2C, GPIO      |   |
|   +--------------------+     +--------------------------------+   |
+-------------------------------------------------------------------+
```

### Comprehensive Structural Comparison

<div class="table-wrap">

| Dimension | Microprocessor ($\mu\text{P}$) | Microcontroller ($\mu\text{C}$) |
| :--- | :--- | :--- |
| **Silicon Architecture** | **CPU Only**: Contains solely the Arithmetic Logic Unit (ALU), Control Unit, and Internal Registers on the die. | **System-on-a-Chip**: CPU, SRAM, Flash ROM, Timers, ADC, and I/O integrated on a single die. |
| **Board Footprint** | Large: Needs multi-layer PCB routing to connect CPU to RAM, ROM, and chipset. | Extremely Compact: Needs only a simple 2-layer PCB; can fit in packages as small as $2\text{ mm} \times 2\text{ mm}$. |
| **External Components** | Mandatory external DDR RAM, Flash/BIOS chip, Voltage Regulators, and Bus Controllers. | Minimal: Runs with as little as a bypass capacitor and an internal RC oscillator. |
| **Clock Frequency** | Gigahertz range ($1.5\text{ GHz} - 5.0\text{ GHz}$). | Megahertz range ($8\text{ MHz} - 480\text{ MHz}$). |
| **Power Dissipation** | High: $15\text{ W}$ to over $150\text{ W}$. Requires heat sinks, heat pipes, and cooling fans. | Ultra-Low: $10\ \mu\text{W}$ to $500\text{ mW}$. Operates cold without any heat sink. |
| **Operating System** | Heavy, multi-tasking OS: Windows 11, Linux, macOS (requires virtual memory & paging). | Bare-metal (super-loop C code) or a Real-Time Operating System (FreeRTOS, Zephyr). |
| **Manufacturing Cost** | High: Silicon chip costs $\$50 - \$800$; full motherboard costs $\$100 - \$500$. | Low: Silicon chip costs $\$0.25 - \$5.00$; complete board costs $\$1.50 - \$10$. |
| **Representative Chips** | Intel Core i9, AMD Ryzen, Apple M3, Broadcom BCM2711 (Raspberry Pi 4 CPU). | Microchip ATmega328P (Arduino), STMicroelectronics STM32F4, TI MSP430, ESP32. |

</div>

::: callout-pitfall Why You Cannot Run Windows 11 on a Microcontroller
Beginners frequently ask: *"Can I install Windows 11 or full Ubuntu on an STM32 or ATmega microcontroller?"*

The answer is **strictly no**, due to three architectural barriers:
1. **No MMU (Memory Management Unit)**: General-purpose operating systems depend on an MMU to create "Virtual Memory"—mapping fake address spaces so individual programs don't overwrite each other. Most microcontrollers only have an optional **MPU (Memory Protection Unit)**, which merely sets read/write permissions on raw, physical memory addresses.
2. **RAM Capacity Disparity**: Windows 11 requires a minimum of $4\text{ GB}$ ($4,194,304\text{ KB}$) of RAM to hold system files, services, and dynamic libraries. An STM32F401 microcontroller typically has $96\text{ KB}$ of SRAM—over $40,000\times$ too small!
3. **Instruction Set Architecture (ISA)**: Desktop operating systems are compiled for x86-64 or high-end 64-bit ARMv8-A application processors. Microcontrollers execute embedded instruction subsets (such as 8-bit AVR or 32-bit ARM Cortex-M Thumb-2), which are physically incapable of decoding x86/x64 opcodes.
:::

---

<a id="foundations"></a>
## Section 3: Processor Classification

Processors are categorized using two main metrics:
1. **Instruction Set Architecture (ISA)**: *How are instructions decoded and executed?* $\rightarrow$ **RISC vs CISC**
2. **Memory Bus Organization**: *How are instructions and data physically routed?* $\rightarrow$ **Von Neumann vs Harvard**

### Part A: RISC vs CISC Architecture

During the 1970s and 1980s, memory was extremely expensive. Engineers wanted instructions to be as dense as possible so that a single assembly command could accomplish a huge mathematical or memory task. This led to **CISC**. Later, researchers discovered that compilers only used a small fraction of these complex instructions, and simpler hardware could run dramatically faster. This gave birth to **RISC**.

```
CISC APPROACH: Complex, Variable-Length, Multi-Cycle
Single Instruction: MULT [0x200], [0x204]
Step 1: CPU accesses memory at 0x200 (Takes 3 clock cycles)
Step 2: CPU accesses memory at 0x204 (Takes 3 clock cycles)
Step 3: Internal multiplier calculates product (Takes 2 clock cycles)
Step 4: Result stored back into memory (Takes 3 clock cycles)
Total: 1 instruction, but consumes 11 clock cycles & massive decode hardware!

---------------------------------------------------------------------

RISC APPROACH: Load-Store Architecture, Fixed-Length, Single-Cycle
Must break the operation down into explicit register-only steps:
Step 1: LDR R0, [0x200]    ; Load value 1 into register R0 (1 cycle)
Step 2: LDR R1, [0x204]    ; Load value 2 into register R1 (1 cycle)
Step 3: MUL R2, R0, R1     ; Multiply registers R0 & R1 into R2 (1 cycle)
Step 4: STR R2, [0x200]    ; Store result back to memory (1 cycle)
Total: 4 instructions, highly pipelined, each executes in 1 clock cycle!
```

#### What is "Load-Store" Architecture?
In a pure **RISC** machine, the ALU can **never** operate directly on external memory. 
- You cannot add a register to a memory location.
- You cannot multiply two values sitting in SRAM directly.
- **Rule**: You must explicitly *Load* bytes from memory into CPU internal registers, execute the mathematical calculation *purely between registers*, and then *Store* the final register value back into memory.

<div class="table-wrap">

| Feature | RISC (Reduced Instruction Set Computer) | CISC (Complex Instruction Set Computer) |
| :--- | :--- | :--- |
| **Instruction Size** | **Fixed Length** (typically strictly 32-bit, or 16-bit in ARM Thumb). | **Variable Length** (ranges from 1 byte up to 15 bytes in x86). |
| **Execution Cycles** | Almost all instructions execute in **$1$ clock cycle** (via pipelining). | Instructions vary wildly (from $1$ cycle to $20+$ cycles). |
| **Memory Access** | **Load-Store Architecture**: Only `LDR` and `STR` touch memory. | Direct memory operands allowed in arithmetic (e.g., `ADD EAX, [EBX]`). |
| **Silicon Decoder** | Simple, hardwired decoding logic; uses minimal silicon real estate. | Complex microcode sequencer ROM; occupies substantial die area. |
| **Register Set** | Large general-purpose register bank ($16$ to $32+$ registers). | Smaller register bank ($8$ to $16$ registers); relies heavily on stack/RAM. |
| **Power Efficiency** | Exceptional. Ideal for battery-operated devices. | Lower. High transistor counts and complex decoders leak power. |
| **Dominant Examples** | **ARM Cortex-M**, RISC-V, MIPS, Microchip AVR. | **Intel x86/x64** (Core i3/i5/i7/i9), AMD Ryzen. |

</div>

::: callout-exam KTU Question: Why ARM Uses RISC Architecture Exclusively [KTU PBCST504 - 5 Marks]
**Model Exam Answer Breakdown:**
1. **Single-Cycle Execution & Determinism**: Because RISC instructions are uniform in length, the instruction pipeline can easily schedule instructions such that every pipeline stage advances in exactly one clock cycle. This guarantees cycle-by-cycle timing predictability—critical for hard real-time embedded systems.
2. **Simplified Decoding Logic**: CISC requires vast decoding trees and microcode ROM to parse variable-length instructions ($1$ to $15\text{ bytes}$). RISC instructions are fixed ($32\text{ bits}$), meaning decoding is implemented via simple, low-transistor, hardwired gates.
3. **Ultra-Low Silicon Footprint & Energy Conservation**: Fewer transistors directly translate to lower dynamic capacitance ($P = C \cdot V^2 \cdot f$) and near-zero static leakage current. This allows ARM cores to operate on milliwatts of power without generating heat.
4. **Silicon Area Saved is Reallocated**: The die area saved by omitting complex CISC decoders is repurposed to integrate essential microcontroller peripherals: on-chip Flash, SRAM, ADC, timers, and nested interrupt controllers.
:::

---

### Part B: Harvard vs Von Neumann Architecture

The fundamental question of computer organization is: **Do instructions and data share the same physical wires, or do they have separate highways?**

```
VON NEUMANN ARCHITECTURE (Shared Unified Bus)
=====================================================================
                    +--------------------+
                    |      CPU CORE      |
                    | (ALU & Registers)  |
                    +--------------------+
                              |
               SHARED Data + Address Bus Highway
                              |
                              v
             +----------------------------------+
             |         UNIFIED MEMORY           |
             |  [Instructions] + [Data/SRAM]    |
             +----------------------------------+

THE VON NEUMANN BOTTLENECK:
Clock Cycle 1: CPU fetches an instruction from memory.
Clock Cycle 2: CPU reads a data variable from memory.
*THEY CANNOT HAPPEN SIMULTANEOUSLY! The CPU must wait.*

=====================================================================

HARVARD ARCHITECTURE (Physically Separate Buses)
=====================================================================
                    +--------------------+
                    |      CPU CORE      |
                    | (ALU & Registers)  |
                    +--------------------+
                         |          |
      Instruction Bus    |          |   Data Bus
      (Code Fetch)       |          |   (Variable Read/Write)
                         v          v
        +-------------------+    +-------------------+
        | INSTRUCTION ROM   |    |    DATA SRAM      |
        | (Flash Memory)    |    | (Working Storage) |
        +-------------------+    +-------------------+

PARALLEL MEMORY ACCESS:
Clock Cycle 1: CPU fetches the NEXT instruction from Flash
               WHILE SIMULTANEOUSLY reading/writing a variable in SRAM.
Zero bus collisions! Double the throughput!
```

#### Why Modern ARM Cortex-M Uses a "Modified Harvard" Architecture
Strict Harvard architecture requires completely segregated addressing spaces: Instruction Address $0\text{x}0040$ is physically different from Data Address $0\text{x}0040$. This is clumsy for software developers who need to store constant strings or lookup tables in Flash and read them as data.

Modern microcontrollers (like the **ARM Cortex-M series**) implement a **Modified Harvard Architecture**:
1. **Internally (Silicon Level)**: The processor has separate internal bus matrices—the **I-Code Bus** (fetches opcodes from Flash) and the **D-Code / System Bus** (reads/writes data in SRAM or Peripherals). They run in parallel with zero bus stalls.
2. **Externally (Programmer's Perspective)**: It maps both Flash and SRAM into a single, seamless, continuous **$4\text{ GB}$ Linear Address Space** ($0\text{x}00000000$ to $0\text{xFFFFFFFF}$). You get Harvard speed in hardware, with Von Neumann ease of programming in C.

---

<a id="history"></a>
## Section 4: Real-World Applications Across Modern Industries

To master microcontrollers, you must understand how physical analog reality converts to embedded execution. Here are four mission-critical domains:

```
+--------------------------------------------------------------------------+
|                        AUTOMOTIVE EMBEDDED SYSTEM                        |
|                                                                          |
| Wheel Speed Sensor  --> [Microcontroller] --> CAN Transceiver            |
| (Variable Reluctance)       | (ARM Cortex-M)        | (Differential Bus) |
|                             v                       v                    |
|                      Solves ABS Math         Transmits Wheel Speed       |
|                      in < 5 milliseconds     to Traction Control         |
+--------------------------------------------------------------------------+
```

### 1. Automotive Systems (Engine, Braking, and Networking)
A modern vehicle contains between $70$ and $150$ interconnected microcontrollers called **Electronic Control Units (ECUs)**.
- **Anti-Lock Braking System (ABS)**: Magnetic Hall-effect sensors on each wheel hub send pulses to an MCU. If the MCU detects a wheel has locked up while the vehicle is moving at $100\text{ km/h}$, it triggers high-speed solenoid valves up to $20$ times per second to release and reapply hydraulic brake pressure. This is a **hard real-time loop** executed in under $5\text{ ms}$.
- **CAN Bus (Controller Area Network)**: Rather than running bundles of heavy copper wire from every door lock, wiper, and sensor back to the dashboard, every ECU talks over a single pair of twisted wires (`CAN_H` and `CAN_L`) using prioritized packet arbitration.

### 2. Biomedical & Healthcare Devices
- **Implantable Cardiac Pacemakers**: A battery-operated microcontroller hermetically sealed in titanium, implanted beneath the collarbone. It runs at ultra-low frequencies ($32.768\text{ kHz}$) to conserve power, continuously reading cardiac electrogram voltages. If an intrinsic pulse is missed within an exact programmed window, it fires a controlled electric shock to stimulate ventricular contraction.
- **Continuous Blood Glucose Monitors (CGM)**: Uses an electrochemical filament beneath the skin. An integrated high-precision 16-bit Sigma-Delta ADC measures nanoampere currents produced by enzymatic glucose reactions, converts this to millimoles per liter, and transmits the values via Bluetooth Low Energy (BLE) to an insulin pump.

### 3. Industrial Automation & Robotics
- **Programmable Logic Controllers (PLCs)**: Ruggedized microcontrollers engineered to withstand severe electromagnetic noise, high-voltage spikes, and vibration inside steel factories. They continuously run an infinite scan cycle: Read Inputs $\rightarrow$ Execute Ladder Logic $\rightarrow$ Update High-Power Relays/Pneumatics.
- **Joint Actuator Servo Control**: Microcontrollers reading absolute optical shaft encoders ($14\text{-bit}$ resolution) run proportional-integral-derivative (PID) closed-loop control algorithms to modulate Three-Phase Brushless DC (BLDC) motor currents using Space Vector Pulse Width Modulation (SVPWM).

### 4. Smart Consumer Electronics
- **Quadcopter Flight Controllers**: An inertial measurement unit (IMU) with a 3-axis gyroscope and 3-axis accelerometer measures angular tilt. An onboard ARM Cortex-M4 MCU samples this at $1\text{ kHz}$, calculates orientation via a complementary or Kalman filter, and adjusts four independent high-speed PWM channels feeding Electronic Speed Controllers (ESCs) to stabilize the drone in mid-air.

---

<a id="self-check"></a>
## Section 5: Interactive Self-Check Quiz

Test your understanding of the concepts covered in this topic.

::: quiz Silicon Integration
An engineer needs to design an ultra-compact smart ring that tracks heart rate. The circuit board must measure no larger than $12\text{ mm} \times 12\text{ mm}$ and run on a tiny lithium coin cell for 4 days. Which processing architecture should they select, and why?
( ) A desktop-grade x86 Microprocessor, because its high clock speed calculates heart rate faster.
(*) A single-die ARM Cortex-M Microcontroller, because it integrates CPU, RAM, Flash, ADC, and BLE on one tiny chip consuming milliwatts of power.
( ) A discrete Microprocessor with external DDR4 RAM and external eMMC Flash, because modularity is required.
( ) A CISC-based processor, because variable instruction lengths save battery life.
::: explanation
A microcontroller is an all-in-one computer on a single silicon die. For extreme physical size and power constraints (such as a smart ring), an integrated MCU (like an ARM Cortex-M or Nordic nRF52 BLE SoC) is the only choice. A microprocessor requires external RAM, Flash, and chipset chips that would exceed the physical board size and drain the battery in minutes.
:::

::: quiz Memory Bus Architecture
Why does a true Harvard architecture deliver higher instruction throughput compared to a Von Neumann architecture running at the same clock frequency?
( ) Harvard architecture uses 64-bit instructions, whereas Von Neumann uses 8-bit instructions.
( ) Harvard architecture eliminates the need for an Arithmetic Logic Unit.
(*) Harvard architecture provides physically separate buses for instruction memory and data memory, allowing simultaneous instruction fetch and data read/write in a single clock cycle.
( ) Harvard architecture relies exclusively on microcode ROM to execute operations.
::: explanation
The classical "Von Neumann Bottleneck" occurs because instructions and data share the same address/data bus. If the CPU is reading a variable from data memory, it cannot simultaneously fetch the next instruction. Harvard architecture physically separates the Instruction Bus from the Data Bus, allowing simultaneous parallel memory transactions on every clock cycle.
:::

::: quiz RISC Load-Store Mechanism
Consider a RISC processor (like ARM). Which of the following assembly operations is **strictly illegal** and prohibited by the architecture?
( ) `LDR R1, [0x20000000]` (Load the 32-bit word at memory address 0x20000000 into register R1)
( ) `ADD R3, R1, R2` (Add contents of register R1 and R2, placing the sum in R3)
(*) `ADD [0x20000004], R1` (Directly add the contents of register R1 to the value residing in RAM address 0x20000004)
( ) `STR R3, [0x20000008]` (Store the 32-bit word from register R3 into RAM address 0x20000008)
::: explanation
RISC processors adhere strictly to a **Load-Store Architecture**. Arithmetic and logic operations can **only** occur between internal CPU registers. Direct manipulation of values sitting in external memory is prohibited. To modify memory, the CPU must first load the value into a register (`LDR`), perform the register operation (`ADD`), and then store the result back (`STR`).
:::
