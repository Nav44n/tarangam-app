# KTU Official Syllabus: Microcontrollers (PBCST504)

Welcome to the comprehensive academic and examination blueprint for **Microcontrollers (PBCST504)**, prescribed under the **APJ Abdul Kalam Technological University (KTU) 2024 Scheme for Semester 5 (S5) Computer Science and allied engineering branches (Common to CS/CC)**.

---

## 📋 Course Overview

<div class="table-wrap">

| Parameter | Specification Details |
| :--- | :--- |
| **Course Name** | **Microcontrollers** |
| **Course Code** | `PBCST504` |
| **Semester** | **Semester 5 (S5)** |
| **Degree & Branch** | **B.Tech (Common to CS / CC)** |
| **Teaching Hours / Week** | **3:0:0:1** *(Lecture: 3 hrs, Tutorial: 0, Practical: 0, Project/Remedial: 1 hr with 2 faculty members)* |
| **Total Contact Hours** | **44 Contact Hours (9 + 11 + 10 + 14 Hours)** |
| **Course Credits** | **4 Credits** |
| **Course Type** | **Theory (Project-Based Learning - PBL)** |
| **Prerequisites** | **None** |
| **Continuous Internal Evaluation (CIE)** | **60 Marks** *(Includes 30 Marks Dedicated Project Work)* |
| **End Semester Examination (ESE)** | **40 Marks** *(Part A: 16 Marks + Part B: 24 Marks)* |
| **Total Marks** | **100 Marks** |
| **Examination Duration** | **2 Hours 30 Minutes (150 Minutes)** |

</div>

::: callout-intuition Why ARM Cortex-M & STM32 Dominate Modern Embedded Systems
Modern smart devices, automotive ECUs, IoT nodes, and industrial robotics are powered by 32-bit ARM Cortex-M microcontrollers rather than legacy 8-bit chips. With Harvard architecture, Thumb-2 instruction efficiency, low-power sleep states, nested vector interrupt controllers (NVIC), and hardware security (ARM TrustZone), mastering the STM32 family and FreeRTOS prepares engineers for high-reliability edge computing.
:::

---

## 🎯 Course Objectives

The primary pedagogical objectives of the course are:

1. **ARM Architecture**: To introduce the ARM architecture, Cortex-M series, Armv8-M specifications, core registers, and bus architecture.
2. **STM32 Hardware & Software Development**: To impart practical, hands-on hardware and firmware knowledge to design, interface, and program embedded systems using STM32 microcontrollers, peripheral drivers (HAL), communication protocols, FreeRTOS, and ARM TrustZone security.

---

## 📚 Module-by-Module Syllabus Breakdown

### Module 1: Introduction to ARM Cortex-M Architecture (9 Contact Hours)

::: callout-exam Module 1 High-Yield Focus
Module 1 builds the microprocessor and instruction set foundations. Key exam topics: Microprocessor vs Microcontroller architectural comparison, Harvard vs von Neumann architecture, RISC design principles, ARM Cortex-M profile taxonomy (M0, M3, M4, M23, M33), Armv8-M baseline vs mainline architecture, Cortex-M register organization (R0–R15, MSP/PSP, CONTROL, PRIMASK), and memory map partitioning.
:::

* **Overview of Embedded Systems**:
  * Characteristics, constraints, real-time requirements, and ubiquitous applications (consumer electronics, automotive, biomedical, industrial automation).
  * Introduction to **Embedded C**: Data types, bit manipulation operators (`&`, `|`, `^`, `~`, `<<`, `>>`), register masking, volatile keyword, pointer arithmetic for memory-mapped I/O.
* **Processor Classifications & Architectures**:
  * Microcontrollers vs Microprocessors: On-chip peripherals, integration density, power consumption, cost, and typical application domains.
  * Processor classification: CISC vs RISC, Harvard vs von Neumann, pipelining basics, little-endian vs big-endian memory storage.
* **ARM Cortex-M Series Evolution & Armv8-M Architecture**:
  * Overview of the ARM processor families (Cortex-A application processors, Cortex-R real-time processors, Cortex-M microcontroller processors).
  * Introduction to **Cortex-M23** (ultra-low-power, 2-stage pipeline, Armv8-M Baseline) and **Cortex-M33** (high performance with DSP and FPU, 3-stage pipeline, Armv8-M Mainline).
  * Armv8-M architectural enhancements: Built-in hardware security via TrustZone, enhanced memory protection (MPU), stack limit checking registers (`MSPLIM`, `PSPLIM`).
* **ARM Core Internal Features**:
  * **Register Organization**: General purpose registers ($R_0 - R_{12}$), Stack Pointers ($R_{13}$ / Main Stack Pointer `MSP` and Process Stack Pointer `PSP`), Link Register ($R_{14}$ / `LR`), Program Counter ($R_{15}$ / `PC`).
  * Special Registers: Program Status Register (`xPSR`), Interrupt Mask Registers (`PRIMASK`, `FAULTMASK`, `BASEPRI`), and `CONTROL` register (Privileged vs Unprivileged thread mode).
  * **Memory & Bus Architecture**: Advanced High-performance Bus (AHB-Lite), Advanced Peripheral Bus (APB), System bus, I-code and D-code buses, memory map segments (Code, SRAM, Peripheral, External RAM, System).
  * Comparison with previous generations (Cortex-M0, M0+, M3, M4).

---

### Module 2: STM32 Microcontroller Overview and Peripheral Programming (11 Contact Hours)

::: callout-exam Module 2 High-Yield Focus
Module 2 focuses on peripheral hardware interfacing and firmware drivers. High-yield KTU exam questions: STM32 GPIO configuration registers (MODER, OTYPER, OSPEEDR, PUPDR), HAL driver initialization sequence, SysTick timer & general-purpose timer prescaler/auto-reload math ($f = \frac{f_{\text{CLK}}}{(\text{PSC}+1)(\text{ARR}+1)}$), Interrupt handling via NVIC, Successive Approximation ADC resolution/sampling time, and DAC sine wave generation.
:::

* **Introduction to the STM32 Family**:
  * STMicroelectronics product lines (STM32F, STM32L, STM32G, STM32H, STM32U).
  * **STM32U575 Features and Specifications**: Ultra-low-power Arm Cortex-M33 running up to 160 MHz, embedded Flash up to 2 MB, SRAM up to 786 KB, mathematical accelerators, advanced cryptographic engines.
  * Power Management and Low-Power Operating Modes: Run, Sleep, Stop, Standby, and Shutdown; Autonomous peripherals in low power (LPBAM).
* **Development Ecosystem & Hardware Abstraction Layer (HAL)**:
  * Integrated Development Environment (STM32CubeIDE), STM32CubeMX graphical initialization code generator, and STM32 HAL / LL (Low-Layer) drivers.
  * Firmware structure: `main.c`, `stm32u5xx_it.c`, peripheral initialization functions, and debugging with ST-LINK (SWD interface, breakpoints, live watch).
* **Digital I/O & Display Interfacing**:
  * Writing and debugging LED blinking and switch input interfacing programs.
  * Interfacing Seven-Segment Displays (multiplexed driving), Alphanumeric Character LCD Displays (HD44780 4-bit / 8-bit mode), and Matrix Keypad scanning algorithms.
  * Relay Interfacing: Optocoupler isolation, flyback diode protection, driver transistors (ULN2003 / BJT).
* **Analog-to-Digital Conversion (ADC)**:
  * Principles of Successive Approximation Register (SAR) ADC; Resolution, reference voltage ($V_{\text{REF}}$), sampling rate, channel multiplexing.
  * Sensor Interfacing: Potentiometer reading, analog temperature sensors (LM35 / TMP36), Light Dependent Resistors (LDR), and analog microphone signal acquisition.
* **Digital-to-Analog Conversion (DAC)**:
  * DAC architecture; Simple DC voltage output generation, generating a stepped Sine Wave via lookup tables, audio waveform signal generation.
* **Interrupts & Timer/Counter Subsystems**:
  * **Interrupt Handling**: Nested Vectored Interrupt Controller (NVIC), interrupt priorities (preemption vs sub-priority), Interrupt Service Routines (ISR), EXTI (External Interrupt Controller) line configuration.
  * **Timer and Counter Applications**: Timer clock prescaler (`PSC`), auto-reload register (`ARR`), basic timer configuration, timers in counter mode (pulse counting), Pulse Width Modulation (PWM) generation, and Timer-based Real-Time Clock (RTC) implementation.

---

### Module 3: Communication Protocols and USB (10 Contact Hours)

::: callout-exam Module 3 High-Yield Focus
Module 3 is the serial bus and device communication module. High-frequency exam topics: Comparative analysis of USART vs SPI vs I2C vs CAN (data rates, bus topology, master/slave, wire count, arbitration), I2C START/STOP conditions and ACK/NACK bit timing, SPI 4-wire interface (MOSI, MISO, SCK, CS) and clock polarity/phase (CPOL/CPHA), CAN bus differential signaling (CAN_H, CAN_L) and dominant/recessive bit arbitration, and USB HID descriptor enumeration.
:::

* **Serial Communication Fundamentals**:
  * Asynchronous vs Synchronous communication, simplex, half-duplex, and full-duplex transmission; Baud rate generation and clock synchronization.
  * Serial port terminal applications: PC communication via Virtual COM Port (VCP), UART debugging using `printf` retargeting.
* **USART (Universal Synchronous/Asynchronous Receiver-Transmitter)**:
  * Frame format: Start bit, data bits (7–9), parity bit, stop bits (1–2); Hardware flow control (RTS/CTS); DMA-assisted UART data reception.
* **$I^2C$ (Inter-Integrated Circuit) Protocol**:
  * Bus topology: Two-wire interface ($SDA$ and $SCL$) with open-drain outputs and pull-up resistors.
  * Protocol mechanics: START condition, 7-bit/10-bit slave addressing, Read/Write bit, Acknowledge (ACK) / Not Acknowledge (NACK), data byte transfer, STOP condition; Clock stretching and multi-master arbitration.
  * **Hands-on Application**: Interfacing an $I^2C$ digital temperature sensor (e.g., LM75 / BMP280) and rendering real-time telemetry on an LCD screen.
* **SPI (Serial Peripheral Interface) Protocol**:
  * High-speed synchronous serial data protocol; 4-wire bus: Master Out Slave In ($MOSI$), Master In Slave Out ($MISO$), Serial Clock ($SCK$), and Chip Select / Slave Select ($CS / \overline{SS}$).
  * SPI transmission modes: Clock Polarity ($CPOL$) and Clock Phase ($CPHA$) combinations (Modes 0, 1, 2, 3).
  * **Hands-on Application**: Writing data bytes to and reading data bytes from an SPI-based EEPROM chip (e.g., 25LCxx series).
* **CAN (Controller Area Network) Protocol**:
  * Automotive and industrial robust differential bus: $CAN\_H$ and $CAN\_L$, termination resistors ($120\,\Omega$).
  * Physical layer signaling: Dominant bit (logic 0) vs Recessive bit (logic 1); Carrier Sense Multiple Access with Collision Resolution (CSMA/CR) using non-destructive bitwise arbitration.
  * CAN Standard (11-bit identifier) and Extended (29-bit identifier) frame structures; Cyclic Redundancy Check (CRC), ACK slot.
  * **Hands-on Application**: Configuring and implementing multi-node CAN communication between multiple STM32U575 microcontroller boards.
* **USB (Universal Serial Bus) Architecture & HID Class**:
  * USB network topology (host, hub, functions), differential $D+$ and $D-$ signaling, NRZI encoding with bit stuffing.
  * USB packet hierarchy: Token, Data, Handshake, Special packets; Enumeration process and standard device descriptors.
  * **Hands-on Application**: Implementing a USB Human Interface Device (HID) class on the STM32 to emulate a plug-and-play USB keyboard / mouse.

---

### Module 4: IoT, Wireless Communication, RTOS, and ARM TrustZone (14 Contact Hours)

::: callout-exam Module 4 High-Yield Focus
Module 4 carries extensive advanced content bridging edge IoT, real-time operating systems, and hardware security. High-yield exam topics: IoT protocol comparison (MQTT publish/subscribe vs CoAP client/server REST), FreeRTOS task states (Running, Ready, Blocked, Suspended) and priority-based preemptive scheduling, FreeRTOS synchronization (Binary/Counting Semaphores, Mutex priority inheritance, Queues), ARM TrustZone Secure vs Non-Secure world partitioning, SAU/IDAU configuration, and embedded software memory optimization.
:::

* **Internet of Things (IoT) Architecture & Protocols**:
  * IoT end-to-end architecture: Perception layer, Network layer, Cloud/Middleware layer, Application layer.
  * IoT application protocols:
    * **MQTT (Message Queuing Telemetry Transport)**: Lightweight publish/subscribe architecture, broker, topics, Quality of Service (QoS 0, QoS 1, QoS 2) levels, Keep-Alive ping.
    * **CoAP (Constrained Application Protocol)**: UDP-based RESTful client/server protocol, low header overhead, GET/POST/PUT/DELETE methods.
  * IoT Security Principles: Confidentiality, Integrity, Authentication, secure boot, firmware over-the-air (FOTA) security, and mitigation of side-channel attacks.
* **Wireless Communication Interfaces**:
  * **Cellular GSM/GPRS**: AT command sets, interfacing GSM modules (SIM800/SIM900) for automated voice calls, SMS notifications, and TCP/IP GPRS data uplinks.
  * **Bluetooth Communication**: Classic Bluetooth vs Bluetooth Low Energy (BLE), GAP (Generic Access Profile), GATT (Generic Attribute Profile) services and characteristics.
  * **LoRa (Long Range) Wireless**: Chirp Spread Spectrum (CSS) modulation, ISM sub-GHz bands, LoRaWAN network architecture (end nodes, gateways, network server, application server).
  * **Designing an IoT-based Home Automation System**: System architecture, sensor nodes, relay actuators, wireless gateway, and mobile/cloud dashboard.
* **Real-Time Operating Systems (RTOS) & FreeRTOS**:
  * General-Purpose OS (GPOS) vs Real-Time OS (RTOS); Hard vs Soft real-time constraints; Deterministic execution.
  * **FreeRTOS Integration with STM32**:
    * FreeRTOS kernel architecture, SysTick timer heartbeat, task control block (TCB), task stack allocation.
    * **Task Management**: Task creation (`xTaskCreate`), task states (Running, Ready, Blocked, Suspended), static vs dynamic priority assignment, Preemptive Priority-Based Round-Robin Scheduling.
    * RTOS Software Timers, non-blocking delays (`vTaskDelay`, `vTaskDelayUntil`), and RTC synchronization.
    * **Inter-Task Communication & Synchronization**:
      * **Queues**: Thread-safe FIFO data exchange between tasks and ISRs (`xQueueSend`, `xQueueReceive`).
      * **Semaphores**: Binary semaphores for task synchronization, Counting semaphores for shared resource pools, Mutexes with **Priority Inheritance** to prevent Priority Inversion bugs.
* **ARM TrustZone Technology & Hardware Security**:
  * Introduction to hardware-enforced isolation: Why software-only security fails.
  * **TrustZone Architecture on Armv8-M**:
    * Hardware-enforced separation into two distinct operational execution environments: **Secure World** and **Non-Secure World**.
    * Memory partitioning: Security Attribution Unit (SAU) and Implementation Defined Attribution Unit (IDAU).
    * Non-Secure Callable (NSC) memory region; Secure Gateway (`SG`) instructions for controlled transitions.
    * Implementing TrustZone on STM32U575: Secure boot, cryptographic key isolation, protecting sensitive peripherals and firmware intellectual property.
* **Advanced Debugging & Code Optimization**:
  * Embedded compiler optimization flags (`-O0`, `-O1`, `-O2`, `-Os`, `-O3`); Code size vs execution speed trade-offs.
  * Memory footprint reduction: Stack and heap sizing, RAM data placement, linker script manipulation.
  * Hardware debugging techniques: Serial Wire Debug (SWD), ITM (Instrumentation Trace Macrocell) printf output, fault exception analyzers (HardFault, MemManage, BusFault, UsageFault handlers).

---

## 🛠️ Project-Based Learning (PBL) Course Framework

`PBCST504` is a specialized **Project-Based Learning (PBL)** course under KTU Regulations where **30 Marks out of 60 CIE Marks** are evaluated through a semester-long hardware project.

### PBL Course Structure & Teaching Format

<div class="table-wrap">

| Component | Hours Allocated | Faculty & Pedagogical Execution |
| :--- | :---: | :--- |
| **Lecture ($L$)** | **3 Hours / Week** | Core theoretical instruction, architecture analysis, peripheral programming, protocol deep dives, and algorithm explanations. |
| **Project / Remedial ($R$)** | **1 Hour / Week** | **Supervised by 2 Faculty Members**. Dedicated to hardware project guidance, debugging, testing, and milestone reviews. |
| **PBL Interactive Activities** | — | Project identification, circuit simulation, laboratory prototyping, brainstorming Q&A, progress reviews, guest lectures from embedded industry experts, and video poster presentations. |

</div>

### Project Suggestions & Domains
Students identify real-world embedded challenges and build functional hardware prototypes using ARM Cortex-M/STM32 microcontrollers:
* **IoT & Home Automation**: Smart energy meter, automated climate control node with MQTT, smart lighting with Bluetooth mesh.
* **Smart Security & Surveillance**: Biometric or RFID door access system with TrustZone key storage, GSM intrusion detection alarm with PIR sensors.
* **Industrial & Automotive Telematics**: Multi-node CAN bus vehicle dashboard monitor, LoRa environmental sensor node with solar energy harvesting.
* **Healthcare & Assistive Tech**: Wearable pulse oximeter with FreeRTOS task management and OLED telemetry, ARM-based voice response alert system.

---

## ⚖️ Course Assessment Method (CIE: 60 Marks, ESE: 40 Marks)

The assessment structure reflects a **60:40 ratio** prioritizing continuous practical project evaluation.

### Continuous Internal Evaluation (CIE: 60 Marks)

<div class="table-wrap">

| Component | Marks | Evaluation Details & Rules |
| :--- | :---: | :--- |
| **Attendance** | **5 Marks** | Minimum 75% attendance mandatory. |
| **Course Project Work** | **30 Marks** | **Semester-long embedded hardware project evaluated through 6 rubric stages (see detailed breakdown below).** |
| **Internal Examination - 1** | **12.5 Marks** | Written test covering **Module 1 and first half of Module 2** (scaled to 12.5). |
| **Internal Examination - 2** | **12.5 Marks** | Written test covering **second half of Module 2, Module 3, and Module 4** (scaled to 12.5). |
| **Total CIE Marks** | **60 Marks** | **Eligibility: Minimum 45% (27/60 marks) required in CIE for ESE eligibility.** |

</div>

### Project Evaluation Rubric Breakdown (30 Marks Total)

<div class="table-wrap">

| Sl. No. | Project Evaluation Stage | Marks | Assessment Criteria |
| :---: | :--- | :---: | :--- |
| **1** | **Project Planning & Proposal** | **5** | Clarity, feasibility of the hardware proposal, literature review, defined embedded methodology, and component BOM. |
| **2** | **Progress Presentation & Q&A** | **4** | Quality of milestone presentations, individual technical contribution, and competence during defense Q&A sessions. |
| **3** | **Involvement & Teamwork** | **3** | Active laboratory participation, collaboration, task division, and regular log-book updates. |
| **4** | **Execution & Implementation** | **10** | Adherence to timeline, correct hardware interfacing, firmware architecture, robustness of prototype, and final working results. |
| **5** | **Final Presentation** | **5** | Technical depth of final presentation, clarity of demonstration, live hardware execution, and answering examiner questions. |
| **6** | **Quality, Innovation & Creativity** | **3** | Originality of solution, engineering excellence, power/code optimization, and real-world applicability. |
| **Total** | **Hardware Project Assessment** | **30 Marks** | Continuous multi-tier rubric evaluation conducted by project review committee. |

</div>

---

### End Semester Examination (ESE: 40 Marks)

* **Total Examination Duration**: **2 Hours 30 Minutes (150 Minutes)**
* **Total Question Paper Valuation**: **64 Marks** (Students write for a maximum of **40 Marks**)
* **Passing Requirement**: **Minimum 40% (16/40 marks) in ESE AND minimum 50% aggregate (50/100) combining CIE + ESE**.

<div class="table-wrap">

| Section | Question Distribution & Marks | Choice Rules | Section Marks |
| :---: | :--- | :--- | :---: |
| **Part A** | • **2 Questions from each module** (Modules 1, 2, 3, 4).<br>• Total of **8 Questions** (Questions 1 to 8).<br>• Each question carries **2 marks** ($8 \times 2 = 16$). | **Compulsory**<br>*(No internal choice)* | **16 Marks** |
| **Part B** | • **Two full questions from each module** (Questions 9 & 10 from M1, 11 & 12 from M2, 13 & 14 from M3, 15 & 16 from M4).<br>• Each full question carries **6 marks** ($4 \times 6 = 24$).<br>• Each question can have **maximum 2 subdivisions** (e.g., 3+3 or 4+2). | **Choice-based**<br>*(Answer any 1 full question from each module)* | **24 Marks** |
| **Total** | **Part A (16 Marks) + Part B (24 Marks)** | | **40 Marks** |

</div>

---

## 📖 Prescribed Textbooks & Reference Books

### Prescribed Core Textbooks

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors** | **Joseph Yiu** | **Newnes - Elsevier** | **3rd Edition, 2014** |
| **2** | **Mastering STM32** | **Carmine Noviello** | **Leanpub** | **2nd Edition, 2022** |

</div>

### Prescribed Reference Books

<div class="table-wrap">

| Sl. | Title of the Book | Author(s) | Publisher | Edition & Year |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **ARM System Developer’s Guide** | Andrew N. Sloss, Dominic Symes, Chris Wright | Morgan Kaufmann | 1st Edition, 2008 |
| **2** | **Embedded System Design with Arm Cortex-M Microcontrollers** | Cem Ünsalan, Hüseyin Deniz Gürhan, Mehmet Erkin Yücel | Springer | 1st Edition, 2022 |
| **3** | **Introduction to ARM Cortex-M Microcontrollers** | Jonathan W. Valvano | Self-Published | 5th Edition, 2014 |

</div>

---

## 🎥 Video Lectures & Online Course Resources

<div class="table-wrap">

| Module | Platform | Resource Link | Focus Areas |
| :---: | :---: | :--- | :--- |
| **Module 1** | **NPTEL / IIT Kharagpur** | [Embedded System Design with ARM (Course 106105193)](https://archive.nptel.ac.in/courses/106/105/106105193/) | ARM architecture, registers, memory organization, and Embedded C. |
| **Module 2** | **STMicroelectronics Official** | [STM32U575 Datasheets & Reference Manuals](https://www.st.com/resource/en/datasheet/) | Technical reference manuals, low-power modes, HAL API guides. |

</div>

---

## 🎓 Course Outcomes (COs)

Upon successful completion of the Microcontrollers course, students will demonstrate mastery across the following outcomes:

<div class="table-wrap">

| CO Identifier | Course Outcome (CO) Statement | Bloom's Knowledge Level |
| :---: | :--- | :---: |
| **CO1** | **Explain** the architectural features and instructions of the ARM microcontrollers. | **K2 (Understand)** |
| **CO2** | **Develop** applications involving interfacing of external devices and I/O with ARM microcontroller. | **K3 (Apply)** |
| **CO3** | **Use** various communication protocols of interaction with peer devices and peripherals. | **K3 (Apply)** |
| **CO4** | **Demonstrate** the use of a real time operating system in embedded system applications. | **K3 (Apply)** |
| **CO5** | **Apply** hardware security features of ARM in real world applications. | **K3 (Apply)** |

</div>

---

## 🗺️ CO-PO Mapping Table

The Course Outcomes directly map to the **National Board of Accreditation (NBA) Program Outcomes (POs)**:

*Correlation Scale: **3 = Substantial (High)** | **2 = Moderate (Medium)** | **1 = Slight (Low)** | **— = No Correlation***

<div class="table-wrap">

| Course Outcome | PO1<br><small>Engg Knowledge</small> | PO2<br><small>Problem Analysis</small> | PO3<br><small>Design/Dev</small> | PO4<br><small>Investigations</small> | PO5<br><small>Modern Tools</small> | PO6<br><small>Engineer & Society</small> | PO7<br><small>Environment</small> | PO8<br><small>Ethics</small> | PO9<br><small>Individual/Team</small> | PO10<br><small>Communication</small> | PO11<br><small>Project Mgmt</small> | PO12<br><small>Life-long Learning</small> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CO1** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO2** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — | — |
| **CO3** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — |
| **CO4** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — |
| **CO5** | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | <span class="matrix-high">3</span> | — | — | — | — | — | — | — |

</div>

### CO-PO Mapping Justification & Insights:
* **PO1 to PO4 (Core Engineering, Analysis & Design)**: Addressed at maximum level ($\text{Level } 3$) across all five COs through digital circuit design, register configuration, real-time interrupt analysis, and system debugging.
* **PO5 (Modern Tool Usage)**: Substantially addressed ($\text{Level } 3$) in CO3, CO4, and CO5 through modern IDEs (STM32CubeIDE), hardware debuggers (ST-LINK/SWD), logic analyzers, and FreeRTOS kernel diagnostic tools.
* **PO6 (Engineer and Society)**: Addressed at $\text{Level } 3$ in CO3 and CO4 through societal applications like smart city IoT sensors, home automation, and automotive safety telemetry.

---

## ⚡ Interactive Syllabus Self-Check Quiz

::: quiz FreeRTOS Synchronization: Semaphores vs Mutexes
In Module 4 of the Microcontrollers syllabus, why is a Mutex preferred over a simple Binary Semaphore for protecting shared hardware peripherals (like an I2C bus) in FreeRTOS?
(*) A Mutex incorporates Priority Inheritance to prevent unbounded Priority Inversion, whereas a Binary Semaphore does not have priority inheritance.
( ) A Binary Semaphore cannot be accessed from an interrupt service routine.
( ) A Mutex can only be used by one task for the entire lifetime of the system without being released.
( ) Semaphores only work on 8-bit microcontrollers, not on ARM Cortex-M.
::: explanation
In FreeRTOS, a **Mutex (Mutual Exclusion semaphore)** includes a **Priority Inheritance mechanism**: if a low-priority task holds the mutex and a high-priority task attempts to take it, the low-priority task temporarily inherits the high-priority task's priority level. This prevents intermediate-priority tasks from preempting the low-priority task and causing unbounded **Priority Inversion**. Binary semaphores lack this mechanism and are best suited for task synchronization rather than mutual exclusion.
:::

::: quiz ARM TrustZone Architecture
According to Module 4, what is the fundamental purpose of ARM TrustZone technology implemented in the STM32U575 (Armv8-M architecture)?
(*) To provide hardware-enforced isolation between a Secure World and a Non-Secure World, protecting cryptographic keys and critical peripherals.
( ) To increase the clock frequency of the processor from 160 MHz to 3 GHz.
( ) To replace the operating system with an analog circuit.
( ) To allow the microcontroller to connect directly to WiFi without a radio transceiver.
::: explanation
ARM **TrustZone for Armv8-M** is a system-wide hardware security approach that divides the memory, peripherals, and execution states into **Secure** and **Non-Secure** worlds. The Security Attribution Unit (SAU) and Implementation Defined Attribution Unit (IDAU) enforce memory access boundaries directly in hardware, preventing compromised non-secure firmware (like a third-party IoT networking stack) from accessing secure secrets or cryptographic keys.
:::

---

## 🧭 Next Steps in Your Study Journey

* Explore the **[Module 1: ARM Cortex-M Architecture Foundations](m1_01_arm_cortex_m_architecture.html)**.
* Learn peripheral interfacing in **[Module 2: STM32 Family Architecture, Low-Power Modes, and Ecosystem](m2_01_stm32_family_architecture_and_ecosystem.html)**.
* Master serial protocols in **[Module 3: I2C, SPI, and CAN Bus Interfaces](m3_01_serial_communication_protocols.html)**.
* Dive into real-time multitasking with **[Module 4: FreeRTOS and ARM TrustZone Security](m4_01_freertos_and_trustzone.html)**.
* Review key formulas and hardware pin configurations in the **[Anki-style Spaced Repetition Review Deck](../../review.html)**.
