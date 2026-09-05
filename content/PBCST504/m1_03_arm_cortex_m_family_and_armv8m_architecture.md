# ARM Cortex-M Series and Armv8-M Architecture
**The ARM Licensing Model, Cortex Profiles (A vs R vs M), Evolution from Cortex-M0/M3/M4 to Armv8-M, and Deep Dive into Cortex-M23 vs Cortex-M33.**

---

### Quick-Jump Navigation
* [1. The ARM Revolution & The IP Licensing Model](#the-intuition)
* [2. The Three ARM Profiles: Cortex-A, Cortex-R, and Cortex-M](#the-dimensions)
* [3. Evolution of Cortex-M Families (Armv6-M, Armv7-M to Armv8-M)](#foundations)
* [4. Cortex-M23 vs Cortex-M33 (Armv8-M Deep Dive)](#history)
* [5. Interactive Self-Check Quiz](#self-check)

---

<a id="the-intuition"></a>
## 1. The ARM Revolution & The IP Licensing Model

If you open up an iPhone, a Samsung Galaxy phone, a DJI drone, a Tesla battery manager, an Apple Silicon MacBook, or an industrial automation controller, you will find an ARM processor inside. ARM-based microprocessors and microcontrollers power over **95% of the world's smartphones** and billions of embedded appliances deployed globally every year.

Yet, despite this dominance, **ARM does not own a single chip-fabrication factory (fab), nor do they manufacture or sell physical silicon chips in boxes**.

### Who is ARM, and What Does "Licensing IP" Mean?

ARM (originally *Acorn RISC Machine*, now *Advanced RISC Machines*) is an intellectual property (IP) design house headquartered in Cambridge, United Kingdom. 

ARM creates the **architectural designs, hardware description code (Verilog / VHDL RTL), instruction set specifications, and compiler toolchains**. They package these designs as **Semiconductor Intellectual Property (SIP)** blocks and license them to third-party semiconductor companies.

::: callout-intuition The Formula 1 Engine Blueprint Analogy
Think of **ARM** like a high-performance engine engineering firm (e.g., Cosworth or Ferrari's engine design bureau):
* ARM creates the **master blueprint** for a state-of-the-art engine (the CPU core).
* They do not build or sell cars directly to drivers.
* Instead, car manufacturers (the silicon companies: **STMicroelectronics, NXP, Microchip, Texas Instruments, Apple, Qualcomm, MediaTek**) purchase a license to use that engine blueprint.
* Each car manufacturer then builds their own custom vehicle (the complete System-on-Chip or Microcontroller):
  * **STMicroelectronics** takes an ARM Cortex-M33 core, pairs it with their proprietary low-power Flash memory, 14-bit ADCs, and motor timers, and sells it to you as the **STM32U575**.
  * **NXP** takes the same ARM core, adds high-speed CAN-FD transceivers and automotive safety modules, and sells it as an **S32K** automotive controller.
  * **Apple** licenses the 64-bit ARM architecture, engineers custom multi-core arrangements with neural engines and unified GPU memory, and sells it as the **M-series** chip.

Because thousands of chip manufacturers use the exact same core architecture, software written for an ARM core runs seamlessly across different semiconductor brands without having to reinvent compilers or debuggers from scratch.
:::

```
                        THE ARM SILICON ECOSYSTEM PIPELINE
+-----------------------------------------------------------------------------+
|                          ARM Ltd. (Cambridge, UK)                           |
|  - Defines Instruction Set Architectures (Armv6-M, Armv7-M, Armv8-M)       |
|  - Synthesizes Core RTL Blueprints (Cortex-M0+, Cortex-M4, Cortex-M33)      |
+-----------------------------------------------------------------------------+
                                       |
                   IP Licensing Model  | (Licenses RTL Verilog blueprints)
                                       v
+-----------------------------------------------------------------------------+
|                        Semiconductor Partners                               |
|        STMicroelectronics    |    NXP Semiconductors    |    Microchip      |
|  - Adds SRAM & Flash ROM     |  - Adds CAN-FD Busses    |  - Adds OpAmps    |
|  - Adds Timers, ADCs, DACs   |  - Adds Security Hardware|  - Adds EEPROM    |
+-----------------------------------------------------------------------------+
                                       |
                   Silicon Foundry     | (TSMC, Samsung, GlobalFoundries)
                                       v
+-----------------------------------------------------------------------------+
|                 Physical Microcontroller Chip (Final Silicon)               |
|      e.g., STM32U575 (ARM Cortex-M33 Core + Peripherals + 2MB Flash)        |
+-----------------------------------------------------------------------------+
```

### Why ARM Dominates Mobile and Embedded Systems

1. **Unrivaled Energy Efficiency (Performance-per-Watt):** Traditional desktop processors (x86 architecture) trace their heritage back to 1978 and rely on complex hardware decoders that consume significant power. ARM was designed from day one as a pure, clean RISC machine with single-cycle execution, minimal transistor count, and aggressive clock gating.
2. **Thumb-2 Instruction Set (High Code Density):** Embedded microcontrollers have very small on-chip Flash memory ($16\text{ KB}$ to $2\text{ MB}$). Standard 32-bit instructions consume Flash quickly. ARM engineered the **Thumb-2 technology**, which blends compact 16-bit instructions with full 32-bit instructions. This achieves $35\%$ better code density than pure 32-bit RISC while delivering up to $98\%$ of the performance of uncompressed 32-bit execution.
3. **Massive Ecosystem and CMSIS Standardization:** ARM established the **CMSIS (Cortex Microcontroller Software Interface Standard)**. This common software abstraction layer ensures that interrupt handling, register naming conventions, and mathematical libraries follow identical C signatures, whether you program an ST, NXP, or Silicon Labs microcontroller.

---

<a id="the-dimensions"></a>
## 2. The Three ARM Profiles: Cortex-A, Cortex-R, and Cortex-M

In 2004, ARM consolidated its product lines under the **Cortex** brand name. To address fundamentally different computing markets without diluting core strengths, ARM partitioned its technology into three distinct profiles, often called the **"ARM Trinity"**:

```
                                  ARM ARCHITECTURE
                                         |
         +-------------------------------+-------------------------------+
         |                               |                               |
         v                               v                               v
    [ Cortex-A ]                    [ Cortex-R ]                    [ Cortex-M ]
   "Applications"                    "Real-Time"                 "Microcontroller"
  - Complex OS (Linux)            - Hard Real-Time               - Bare-Metal / RTOS
  - Memory Mgmt Unit (MMU)        - Memory Protection (MPU)      - Deterministic Latency
  - Multi-GHz Multi-Core          - Fault Tolerant / Lock-step   - Ultra-Low Power / Cost
```

<div class="table-wrap">

| Dimension | Cortex-A (Application) | Cortex-R (Real-Time) | Cortex-M (Microcontroller) |
| :--- | :--- | :--- | :--- |
| **Primary Design Goal** | Maximum raw compute throughput & graphics rendering | Deterministic latency, fault tolerance & functional safety | Minimal cost, ultra-low dynamic power & deterministic response |
| **Typical Clock Speed** | $1.0\text{ GHz} - 3.5\text{ GHz}$ | $300\text{ MHz} - 1.0\text{ GHz}$ | $16\text{ MHz} - 250\text{ MHz}$ (up to $500\text{ MHz}$ in Cortex-M7) |
| **Memory Management** | **MMU (Memory Management Unit)** with hardware page tables & virtual memory | **MPU (Memory Protection Unit)** with strict physical memory regions | **MPU (Optional)** or flat physical address space; **No Virtual Memory** |
| **Target Operating Systems** | Rich, monolithic OS: Linux, Android, iOS, Windows on ARM | Deterministic Hard Real-Time OS: SafeRTOS, QNX, VxWorks | Bare-Metal C / Micro-RTOS: FreeRTOS, Zephyr, ThreadX, Keil RTX |
| **Interrupt Latency** | Non-deterministic, variable (tens to hundreds of clock cycles) | Very low, deterministic (typically $< 20$ clock cycles) | **Ultra-low, deterministic** ($12$ cycles on M3/M4/M33, down to $10$ on M23) |
| **Hardware Complexity** | Multi-level out-of-order execution, deep pipelines ($10-15+$ stages) | Dual-core lockstep execution with ECC cache checking | Compact in-order pipeline ($2$ to $3$ stages), very low gate count |
| **Power Budget** | Watts ($0.5\text{ W} - 15\text{ W}+$) | Hundreds of milliwatts ($200\text{ mW} - 2\text{ W}$) | **Microwatts to single-digit milliwatts** ($\mu\text{W} - \text{mW}$) |
| **Representative Applications** | Smartphones, tablet computers, automotive infotainment, smart TVs | Automotive ABS brakes, engine ECUs, aircraft fly-by-wire, hard disk controllers | Smart wearables, pacemakers, IoT sensor nodes, washing machine controllers |

</div>

::: callout-exam KTU Question: Differentiate Cortex-A, Cortex-R, and Cortex-M profiles (Marks: 4 / 6)
**Model Exam Answer Structure:**
1. **Definition & Target Domain:**
   * **Cortex-A (Application):** Designed for performance-intensive systems running rich operating systems (e.g., Linux, Android) requiring virtual memory and multi-core processing.
   * **Cortex-R (Real-Time):** Optimized for mission-critical, time-sensitive applications requiring predictable, deterministic execution and safety redundancy (e.g., aerospace avionics, automotive braking).
   * **Cortex-M (Microcontroller):** Tailored for cost-sensitive, power-constrained embedded applications requiring fast, predictable interrupt servicing and low gate-count silicon.
2. **Key Silicon Differences:**
   * **Memory Management:** Cortex-A features an **MMU** (supporting virtual memory translation); Cortex-R and Cortex-M use an **MPU** (or no protection unit) working strictly on physical addresses.
   * **Interrupt Handling:** Cortex-M incorporates an integrated hardware **NVIC (Nested Vectored Interrupt Controller)** enabling hardware state-saving in $\le 12$ clock cycles. Cortex-A relies on software-vectored interrupt routines with non-deterministic latencies.
:::

---

<a id="foundations"></a>
## 3. Evolution of Cortex-M Families (Armv6-M, Armv7-M to Armv8-M)

Over the past two decades, the Cortex-M processor family has expanded systematically across three core architecture generations.

```
                     EVOLUTION TIMELINE OF THE CORTEX-M FAMILY
  
    Generation 1: Armv6-M                   Generation 2: Armv7-M / Armv7E-M              Generation 3: Armv8-M
   [ Ultra-Low Gate Count ]               [ Mainstream 32-bit Performance ]              [ Connected IoT & Security ]
         (2009-2012)                                 (2004-2010)                                 (2016 - Present)
  
   +--------------------+                     +--------------------+                   +--------------------+
   |     Cortex-M0      |                     |     Cortex-M3      |                   |     Cortex-M23     |
   | - 2-stage pipeline |                     | - 3-stage pipeline |                   | - 2-stage pipeline |
   | - Replaces 8-bit   |                     | - Hardware divide  |                   | - Baseline Armv8-M |
   +--------------------+                     | - Full Thumb-2     |                   | - TrustZone IoT    |
             |                                +--------------------+                   +--------------------+
             v                                          |                                        |
   +--------------------+                               v                                        v
   |     Cortex-M0+     |                     +--------------------+                   +--------------------+
   | - 2-stage pipeline |                     |    Cortex-M4/M7    |                   |     Cortex-M33     |
   | - Low-power champ  |                     | - DSP instructions |                   | - 3-stage pipeline |
   +--------------------+                     | - Hardware FPU     |                   | - Mainline Armv8-M |
                                              +--------------------+                   | - TrustZone + FPU  |
                                                                                       | - **STM32U575** |
                                                                                       +--------------------+
```

### The Legacy Lines: Armv6-M and Armv7-M

#### 1. Armv6-M Architecture: The 8/16-Bit Replacement (Cortex-M0, Cortex-M0+)
* Designed with minimal silicon gate count ($< 12,000$ logic gates).
* Purpose: To allow semiconductor companies to manufacture 32-bit microcontrollers at a lower price point than legacy 8-bit 8051 or PIC microcontrollers.
* Implements a restricted, pure 16-bit Thumb instruction subset (with only 6 basic 32-bit instructions).
* Lacks hardware division, saturation math, and advanced bit-field operations.

#### 2. Armv7-M & Armv7E-M Architecture: The 32-Bit Industry Workhorses (Cortex-M3, M4, M7)
* **Cortex-M3 (Armv7-M):** The standard microcontroller core. Introduced the complete **Thumb-2 instruction set**, dedicated hardware integer division (`SDIV`/`UDIV`), hardware multiply-accumulate (MAC), and an integrated 12-cycle interrupt controller.
* **Cortex-M4 (Armv7E-M):** Enhanced the M3 core with **Digital Signal Processing (DSP)** instruction extensions (SIMD arithmetic, saturation instructions) and an optional single-precision **Floating Point Unit (FPU)** compliant with IEEE-754.
* **Cortex-M7 (Armv7E-M):** Adds double-precision FPU options, 6-stage dual-issue superscalar pipeline, instruction/data L1 caches, and speeds exceeding $400\text{ MHz}$.

---

### Why Armv8-M Was Created: The Connected IoT Security Crisis

During the mid-2010s, billions of embedded microcontrollers were connected to the public Internet to form the **Internet of Things (IoT)**: smart door locks, security cameras, industrial utility meters, and medical sensors.

However, microcontrollers designed under the legacy Armv7-M architecture operated with **flat memory architectures**:
* If a hacker exploited a buffer overflow bug in a third-party open-source MQTT or Wi-Fi network stack, **they gained complete access to the entire microcontroller**.
* The attacker could read private cryptographic encryption keys from SRAM, overwrite Flash firmware sectors, or disable physical safety actuators.

```
LEGACY ARMV7-M SECURITY MODEL (All-or-Nothing Flaw)
+-----------------------------------------------------------------------------+
| UNIFIED PHYSICAL ADDRESS SPACE (No Silicon-Enforced Security Barrier)       |
|                                                                             |
|  [ Wi-Fi / TCP-IP Network Stack ]   <--- Hacker exploits buffer overflow    |
|                 |                        here!                              |
|                 | (Unrestricted access to entire memory!)                   |
|                 v                                                           |
|  [ System Crypto Keys / Flash Memory / Motor Controller / Safety Systems ]  |
+-----------------------------------------------------------------------------+
```

To solve this vulnerability at the silicon level, ARM introduced the **Armv8-M Architecture**. 

The core contribution of Armv8-M is **ARM TrustZone for Microcontrollers**. Unlike legacy architectures, Armv8-M divides the silicon hardware itself into two physically separated execution worlds: **Secure** and **Non-Secure**.

```
ARMV8-M TRUSTZONE ARCHITECTURE (Hardware Silicon Isolation)
+------------------------------------+----------------------------------------+
|          NON-SECURE WORLD          |              SECURE WORLD              |
|                                    |                                        |
|  - Untrusted User Code             |  - Cryptographic Keys & Bootloader     |
|  - Third-Party Wi-Fi / Cloud Stack |  - Critical Sensor Hardware Drivers    |
|  - Real-Time OS Scheduler          |  - Secure Firmware Update Engine       |
|                                    |                                        |
|  [ Non-Secure SRAM & Flash ]       |  [ Secure SRAM & Flash ]               |
+------------------------------------+----------------------------------------+
                  |                                      ^
                  |         Security Attribution Unit    |
                  +--- Non-Secure CANNOT read/write ----->| (Access Blocked by
                       Secure Memory Directly!             Hardware Gate)
```

1. **Non-Secure Software is Blocked at the Bus Level:** The non-secure world (running your RTOS and Wi-Fi stack) cannot read or write to secure memory addresses. If a hacker breaches the network stack, the hardware core triggers a **SecureFault exception** before any crypto keys can be exposed.
2. **Zero-Latency Switching:** Unlike desktop virtualization, TrustZone on Cortex-M does not use a hypervisor. Context switching between Secure and Non-Secure states is handled natively in hardware in just **two to three clock cycles**.

---

<a id="history"></a>
## 4. Cortex-M23 vs Cortex-M33 (Armv8-M Deep Dive)

The Armv8-M architecture specification divides microcontrollers into two distinct profiles:
1. **Armv8-M Baseline:** Ultra-low power, cost-constrained, replacing Cortex-M0/M0+ (embodied by the **Cortex-M23**).
2. **Armv8-M Mainline:** High-performance, feature-rich, replacing Cortex-M3/M4 (embodied by the **Cortex-M33**).

---

### Understanding the Assembly Line: Processor Pipelining

Before comparing the internal designs of these two cores, we need to understand **instruction pipelining**.

::: callout-intuition The Laundry Factory Analogy
Imagine running an industrial laundry service with three steps: **Wash**, **Dry**, and **Fold**. Each step takes 30 minutes.

* **Without a Pipeline (Sequential):** You wash load 1 (30 min), dry load 1 (30 min), fold load 1 (30 min). Total = 90 minutes per load.
* **With a Pipeline:** * At $T=0$: Wash Load 1.
  * At $T=30$: Load 1 moves to the Dryer. Meanwhile, **Load 2 starts in the Washer**.
  * At $T=60$: Load 1 is Folded. Load 2 is in the Dryer. **Load 3 starts in the Washer**.
  
Once the pipeline is full, **one completely clean load emerges every 30 minutes**!
:::

A microprocessor pipeline processes instructions the same way:
* **Fetch:** Read instruction opcode bytes from Flash memory address pointed to by Program Counter ($PC$).
* **Decode:** Translate raw binary opcode into control signals for internal multiplexers and registers.
* **Execute:** Perform the mathematical or logical operation in the Arithmetic Logic Unit (ALU) or access memory.

```
CORTEX-M23: 2-STAGE PIPELINE (Ultra-Compact, Low Gate Count)
================================================================================
 Cycle 1:    [ FETCH Instruction 1 ]
 Cycle 2:    [ DECODE & EXECUTE Inst 1 ]
             [ FETCH Instruction 2     ]
 Cycle 3:                                [ DECODE & EXECUTE Inst 2 ]
                                         [ FETCH Instruction 3     ]

CORTEX-M33: 3-STAGE PIPELINE (High Clock Frequency, Better Branch Handling)
================================================================================
 Cycle 1:    [ FETCH Inst 1 ]
 Cycle 2:    [ DECODE Inst 1 ]
             [ FETCH Inst 2  ]
 Cycle 3:    [ EXECUTE Inst 1 ]
             [ DECODE Inst 2  ]
             [ FETCH Inst 3   ]
```

* **Cortex-M23 uses a 2-stage pipeline:** By folding Decode and Execute together, silicon gate count is reduced to the bare minimum, consuming negligible power.
* **Cortex-M33 uses a 3-stage pipeline:** Separating Decode from Execute simplifies timing paths, allowing the processor to be clocked at much higher speeds (up to $250\text{ MHz}$) without causing timing violations in silicon.

---

### Architectural Feature Comparison: Cortex-M23 vs Cortex-M33

<div class="table-wrap">

| Technical Specification | ARM Cortex-M23 | ARM Cortex-M33 |
| :--- | :--- | :--- |
| **Armv8-M Profile** | **Armv8-M Baseline** | **Armv8-M Mainline** |
| **Pipeline Stages** | **2 stages** (Fetch $\to$ Decode/Execute) | **3 stages** (Fetch $\to$ Decode $\to$ Execute) |
| **Direct Predecessor** | Cortex-M0 / Cortex-M0+ | Cortex-M3 / Cortex-M4 |
| **Instruction Set Architecture (ISA)** | Basic Thumb (mostly 16-bit) + limited 32-bit instructions | Full **Thumb-2 Technology** (rich mix of 16-bit & 32-bit instructions) |
| **Hardware Divide** | Optional (takes up to 32 cycles) | **Standard Hardware Divide** (`SDIV`, `UDIV`, 2 to 12 cycles) |
| **DSP Instruction Extensions** | None | **Full SIMD & DSP extensions** (Single-cycle $16/32$-bit MAC, saturation math) |
| **Floating Point Unit (FPU)** | Not supported | **Optional Single-Precision FPU** (IEEE-754 compliant, hardware float registers `s0`-`s31`) |
| **Hardware Co-Processor Interface** | Not supported | **Supported** (allows custom accelerator hardware instructions) |
| **ARM TrustZone Security** | Supported (Integrated SAU / IDAU) | Supported (Integrated SAU / IDAU) |
| **Memory Protection Units (MPU)** | Up to 2 MPUs (Secure & Non-Secure), max 16 regions each | Up to 2 MPUs (Secure & Non-Secure), max 16 regions each |
| **Interrupt Latency** | **10 to 15 clock cycles** | **12 clock cycles** |
| **Silicon Area & Gate Count** | Extremely small ($\approx 20\text{k} - 35\text{k}$ logic gates) | Medium ($\approx 65\text{k} - 110\text{k}$ logic gates) |
| **Typical Target Microcontroller** | Microchip SAM L11, Nuvoton M261 | **STMicroelectronics STM32U575** (Our course target MCU!) |

</div>

::: callout-pitfall Understanding SAU vs IDAU in Armv8-M
When working with Armv8-M TrustZone, beginners often confuse how memory security states are designated:
* **SAU (Security Attribution Unit):** A software-programmable register block inside the Cortex-M core. Firmware running during early boot configures memory ranges as Secure, Non-Secure, or Non-Secure Callable (NSC).
* **IDAU (Implementation Defined Attribution Unit):** A fixed, hardware-level partition hardwired outside the CPU core by the silicon vendor (e.g., STMicroelectronics).
The CPU computes the final security status of any address by combining both the SAU and IDAU. If either unit declares an address range as Secure, **it is treated as Secure**. Security defaults to the most restrictive policy.
:::

---

<a id="self-check"></a>
## 5. Interactive Self-Check Quiz

::: quiz ARM Profile Selection
You are tasked with designing the electronic control unit (ECU) for an autonomous passenger vehicle's emergency brake actuation system. The system must guarantee a hardware response time of under 500 nanoseconds, feature dual-core redundant hardware lockstep error checking, and recover deterministically from any single-event silicon radiation upsets. Which ARM processor profile is technically suited for this specific task?
( ) ARM Cortex-A
(*) ARM Cortex-R
( ) ARM Cortex-M
( ) ARM SecurCore
::: explanation
* **ARM Cortex-R (Real-Time)** is explicitly engineered for safety-critical, time-deterministic applications like automotive braking, avionics fly-by-wire, and hard drive servo heads. It supports dual-core lockstep hardware configurations (where two identical cores run the same instruction stream side-by-side to cross-check for silicon bit-flips) and guarantees deterministic interrupt response without non-deterministic cache stalls.
* **Cortex-A** lacks deterministic timing due to virtual memory MMU translations and out-of-order execution pipelines.
* **Cortex-M** is optimized for low-cost, low-power general microcontrollers and lacks native dual-core lockstep checking features.
:::

::: quiz Cortex-M23 vs Cortex-M33 Pipeline Architecture
How does the hardware pipeline structure of the Cortex-M23 differ from that of the Cortex-M33, and what is the engineering trade-off of this difference?
( ) Cortex-M23 has 3 stages for higher speed; Cortex-M33 has 2 stages for lower power.
(*) Cortex-M23 has a 2-stage pipeline to minimize silicon gate count and dynamic power; Cortex-M33 has a 3-stage pipeline to permit higher clock frequencies.
( ) Cortex-M23 uses an out-of-order 5-stage pipeline; Cortex-M33 uses a sequential 1-stage pipeline.
( ) Cortex-M23 has a 2-stage pipeline and includes a hardware Floating Point Unit; Cortex-M33 has a 3-stage pipeline without FPU support.
::: explanation
* The **Cortex-M23** implements a compact **2-stage pipeline** (Fetch $\to$ Decode/Execute). Combining decode and execute minimizes the number of pipeline registers in silicon, drastically lowering gate count and dynamic power draw at the cost of capping maximum clock speeds.
* The **Cortex-M33** implements a **3-stage pipeline** (Fetch $\to$ Decode $\to$ Execute). Isolating decode into its own clock cycle relaxes timing path constraints across the silicon die, allowing the Cortex-M33 to clock up to $250\text{ MHz}$ while supporting advanced features like hardware DSP instructions, single-cycle MAC, and a single-precision FPU.
:::

::: quiz Armv8-M Mainline Feature Set
Which set of architectural features accurately reflects the capabilities of an **Armv8-M Mainline** core (such as the ARM Cortex-M33 found in the **STM32U575**)?
(*) TrustZone security isolation, 3-stage pipeline, optional hardware single-precision FPU, DSP extensions, and hardware integer divide.
( ) 2-stage pipeline, 8-bit registers, MMU with virtual memory paging, and double-precision FPU.
( ) TrustZone security isolation, 2-stage pipeline, no hardware divide, and no DSP instruction support.
( ) Multi-core out-of-order execution, MMU page translation, and high-power branch prediction caches.
::: explanation
The **Armv8-M Mainline** (Cortex-M33) is the flagship 32-bit core designed for modern secure microcontrollers:
1. It features a **3-stage pipeline** (unlike the 2-stage baseline Cortex-M23).
2. It includes **ARM TrustZone** for hardware isolation between Secure and Non-Secure domains.
3. It features full **Thumb-2** ISA, **hardware integer division** (`SDIV`/`UDIV`), **DSP instructions** (SIMD operations), and an optional single-precision **Floating Point Unit (FPU)**.
:::
