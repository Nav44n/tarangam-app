# ARM Core Registers, Memory, and Bus Architecture
**The Programmer's Model (R0–R15, xPSR, MSP/PSP, CONTROL), Operating Modes (Thread vs Handler), 4GB Memory Map, Bit-Banding Mathematics, and AHB/APB AMBA Bus Matrix.**

---

### Quick-Jump Navigation
* [1. The ARM Cortex-M Programmer's Model & Registers R0–R15](#the-intuition)
* [2. Operating Modes and The Dual Stack Pointer System (MSP vs PSP)](#the-dimensions)
* [3. The 4GB Linear Memory Map & Bit-Banding](#foundations)
* [4. The AMBA Bus Highway: AHB vs APB Matrix](#history)
* [5. Interactive Self-Check Quiz](#self-check)

---

<a id="the-intuition"></a>
## 1. The ARM Cortex-M Programmer's Model & Registers R0–R15

When writing embedded software, the Central Processing Unit (CPU) does not execute calculations directly inside RAM or Flash memory. Memory is physically distant from the ALU (Arithmetic Logic Unit). To add two numbers, compare two values, or check a hardware status bit, data must first be hauled inside the core into ultra-fast, microscopic storage cells known as **Registers**.

::: callout-intuition What is a Register? The Carpenter's Toolbelt
Imagine you are a master carpenter building a dining table inside a workshop:
* **Flash Memory (ROM)** is the printed blueprint on the wall. It holds the immutable instructions for how to cut and assemble the wood.
* **SRAM (RAM)** is the large lumber warehouse down the street. It can store stacks of wood and supplies, but driving a truck to the warehouse to pick up a single screw takes a long time ($2$ to $5$ clock cycles).
* **CPU Registers** are the **tools hanging directly on your leather work belt** (hammer, tape measure, chisel). You can draw, use, and return a chisel in a fraction of a second ($1$ single clock cycle) without moving your feet.

Because the toolbelt has limited physical space, a carpenter can only carry a few tools at a time. In the ARM Cortex-M architecture, the toolbelt holds exactly **16 primary 32-bit registers** (labeled `R0` through `R15`), plus a handful of specialized status and configuration dials.
:::

```
                 THE ARM CORTEX-M CORE REGISTER FILE (PROGRAMMER'S MODEL)
+-----------------------------------------------------------------------------+
| REG | NAME | ARCHITECTURAL FUNCTION & AAPCS USAGE                          |
+=============================================================================+
| R0  |      | General Purpose / Function Parameter 1 / Function Return Value| \
| R1  |      | General Purpose / Function Parameter 2 / Function Return Value|  |
| R2  | Low  | General Purpose / Function Parameter 3                        |  |-- Accessible
| R3  | Regs | General Purpose / Function Parameter 4                        |  |   by ALL 16-bit
| R4  |      | General Purpose (Callee-saved register)                       |  |   Thumb & 32-bit
| R5  |      | General Purpose (Callee-saved register)                       |  |   Thumb-2 instrs
| R6  |      | General Purpose (Callee-saved register)                       |  |
| R7  |      | General Purpose (Callee-saved register) / Syscall Frame Ptr   | /
+-----+------+---------------------------------------------------------------+
| R8  |      | General Purpose (Callee-saved register)                       | \
| R9  | High | General Purpose (Platform specific / Static Base pointer)     |  |-- Accessible
| R10 | Regs | General Purpose (Callee-saved register)                       |  |   by ALL 32-bit
| R11 |      | General Purpose (Callee-saved register) / Frame Pointer       |  |   Thumb-2 instrs
| R12 |      | Intra-Procedure Call Scratch Register (IP)                    | /
+-----+------+---------------------------------------------------------------+
| R13 | SP   | Stack Pointer (Banked physically into MSP and PSP)             |
+-----+------+---------------------------------------------------------------+
| R14 | LR   | Link Register (Stores Function Return Address & EXC_RETURN)   |
+-----+------+---------------------------------------------------------------+
| R15 | PC   | Program Counter (Points to current instruction address + 4)   |
+=============================================================================+
                                SPECIAL REGISTERS
+-----------------------------------------------------------------------------+
| xPSR       | Combined Program Status Register (APSR + IPSR + EPSR)         |
| PRIMASK    | Exception Mask: Disables all interrupts with configurable prio |
| FAULTMASK  | Fault Mask: Disables all exceptions except Non-Maskable Int   |
| BASEPRI    | Base Priority Mask: Disables interrupts below set priority     |
| CONTROL    | Mode Control: Selects Stack Pointer (MSP/PSP) & Privilege Level|
+-----------------------------------------------------------------------------+
```

---

### Deep Dive into Core Registers `R0` to `R15`

All sixteen core registers are **32 bits wide** ($4$ bytes), capable of holding unsigned integer values from $0$ to $4,294,967,295$ (`0x00000000` to `0xFFFFFFFF`) or signed two's-complement values from $-2,147,483,648$ to $+2,147,483,647$.

#### 1. Low Registers (`R0` – `R7`)
* Accessible by all legacy 16-bit Thumb instructions as well as modern 32-bit Thumb-2 instructions.
* **The AAPCS Standard:** Under the *ARM Architecture Procedure Call Standard* (AAPCS), when a C function calls another function:
  * Registers `R0`, `R1`, `R2`, and `R3` pass the first four arguments into the function.
  * Register `R0` (or `R0` + `R1` for 64-bit values) carries the return value back to the caller.
  * Registers `R4` through `R7` are *callee-saved*: if a helper function modifies them, it must first push their original contents onto the stack and pop them back before returning.

#### 2. High Registers (`R8` – `R12`)
* Fully accessible by all 32-bit Thumb-2 instructions; accessible by only a limited subset of 16-bit Thumb instructions (such as `MOV`, `CMP`, and `ADD`).
* Used as general scratchpad working variables during complex mathematical computations.

#### 3. Register `R13`: The Stack Pointer (`SP`)
The Stack Pointer holds the current memory address of the **Stack**—a Last-In, First-Out (LIFO) memory buffer in SRAM used to store local variables, function return frames, and saved register states.
* ARM Cortex-M uses a **Full-Descending Stack**: the stack grows downward from high memory addresses toward low memory addresses.
* When a 32-bit word is pushed onto the stack:
  $$\text{SP}_{\text{new}} = \text{SP}_{\text{old}} - 4$$
* `R13` is physically banked into **two distinct physical stack pointer registers**:
  1. **MSP (Main Stack Pointer):** Used by the Operating System Kernel, system boot routines, and all Exception/Interrupt Handlers.
  2. **PSP (Process Stack Pointer):** Used by unprivileged user application tasks in an RTOS environment.
* At any given clock cycle, the CPU only sees one `SP` mapped to `R13`, determined by the `CONTROL` register.

#### 4. Register `R14`: The Link Register (`LR`)
When your software executes a subroutine call (using the Branch with Link instruction `BL` or `BLX`), the processor automatically saves the return address of the *next* instruction into `R14` (`LR`).
* When the function finishes, it returns by branching to the address held in `LR`:
  ```assembly
  BX  LR   ; Branch to address in Link Register (returns to caller)
  ```
* **Exception Return Magic (`EXC_RETURN`):** When a hardware interrupt triggers, the CPU hardware overwrites `LR` with a special code pattern starting with `0xFFFFFFF` (such as `0xFFFFFFF9` or `0xFFFFFFFD`). This pattern is not a real memory address; it signals the core upon return which stack pointer to restore (`MSP` vs `PSP`) and whether floating-point hardware registers need unstacking!

#### 5. Register `R15`: The Program Counter (`PC`)
The Program Counter holds the memory address of the instruction currently being processed.
* Because the Cortex-M processor pipelines instructions (prefetching instructions ahead of time), reading `PC` returns the **current instruction address $+ 4$ bytes**.
* **The Thumb Bit Rule:** ARM Cortex-M cores execute instructions exclusively in the **Thumb/Thumb-2 state**. Therefore, **Bit 0 of the PC must always be set to `1`** when jumping to a function pointer or vector table address. If Bit 0 is ever cleared to `0`, the processor attempts to switch into legacy 32-bit ARM mode (which does not exist in Cortex-M silicon), instantly triggering an `INVSTATE` **UsageFault crash**!

---

### The Special Status Registers

```
                 THE COMBINED PROGRAM STATUS REGISTER (xPSR)
  31  30  29  28  27  26 25 24        16 15        9 8                     0
+---+---+---+---+---+------+--+---------+-----------+-----------------------+
| N | Z | C | V | Q |  ICI/IT | T (Thumb) |  Reserved |   IPSR (ISR Number)   |
+---+---+---+---+---+------+--+---------+-----------+-----------------------+
|<--- APSR -------->|<-------- EPSR -------------->|<------- IPSR --------->|
```

The processor core provides three distinct status registers mapped together into a unified 32-bit register called **`xPSR`**:

1. **Application Program Status Register (APSR) [Bits 31:27]:**
   Holds the arithmetic flags updated by ALU instructions:
   * **$N$ (Negative Flag, Bit 31):** Set to $1$ if the result of an operation is negative (MSB is $1$).
   * **$Z$ (Zero Flag, Bit 30):** Set to $1$ if the result of an operation is exactly zero.
   * **$C$ (Carry/Borrow Flag, Bit 29):** Set to $1$ if an addition generated an unsigned carry out, or an unsigned subtraction did not require a borrow.
   * **$V$ (oVerflow Flag, Bit 28):** Set to $1$ if a signed addition/subtraction yielded a mathematically incorrect result exceeding signed 32-bit boundaries.
   * **$Q$ (Sticky Saturation Flag, Bit 27):** Set to $1$ if a DSP saturation instruction saturated an output value.
2. **Interrupt Program Status Register (IPSR) [Bits 8:0]:**
   Contains the Exception Number currently being serviced by the core:
   * If value is $0$, the CPU is running normal user application code (Thread Mode).
   * If value is $15$, the CPU is servicing the **SysTick** timer exception.
   * If value is $\ge 16$, the CPU is servicing an external hardware interrupt ($\text{IRQ number} = \text{IPSR} - 16$).
3. **Execution Program Status Register (EPSR) [Bit 24 & Bits 15:10, 26:25]:**
   * **$T$ (Thumb Bit, Bit 24):** Must always be $1$. Indicates execution of Thumb instructions.
   * **ICI / IT Bits:** Holds execution state for multi-cycle load/store instructions or conditional `IT` (If-Then) blocks.

---

### Interrupt Masking and Control Registers

* **`PRIMASK` (1 bit):** The global interrupt mask. Writing a `1` to `PRIMASK` disables all interrupts that have configurable priority levels. Only Non-Maskable Interrupts (**NMI**) and **HardFault** exceptions can preempt execution.
  ```c
  __disable_irq(); // Assembly instruction: CPSID i (Sets PRIMASK = 1)
  __enable_irq();  // Assembly instruction: CPSIE i (Clears PRIMASK = 0)
  ```
* **`FAULTMASK` (1 bit):** Extreme fault mask. Writing a `1` raises the execution priority to $-1$, blocking all exceptions except NMI.
* **`BASEPRI` (8 bits):** Priority threshold filter. Writing a priority value (e.g., `0x40`) into `BASEPRI` disables all interrupts whose numerical priority is equal to or higher than `0x40`, while allowing higher-priority interrupts (e.g., `0x10`, `0x20`) to fire unimpeded.
* **`CONTROL` Register (3 bits):**
  * **Bit 0 (`nPRIV`):** Privilege level in Thread mode ($0 = \text{Privileged}$, $1 = \text{Unprivileged}$).
  * **Bit 1 (`SPSEL`):** Active Stack Pointer selection ($0 = \text{MSP}$, $1 = \text{PSP}$).
  * **Bit 2 (`FPCA`):** Floating-Point Context Active ($1 = \text{FPU registers active on stack}$).

---

<a id="the-dimensions"></a>
## 2. Operating Modes and The Dual Stack Pointer System (MSP vs PSP)

To guarantee that poorly written user tasks cannot crash safety-critical hardware drivers or corrupt operating system schedulers, the ARM Cortex-M architecture implements two **Operating Modes** paired with two **Privilege Levels**:

```
                       ARM CORTEX-M OPERATING STATE MATRIX
+-----------------------------------------------------------------------------+
| OPERATING MODE   | PRIVILEGE LEVEL         | STACK POINTER IN USE           |
+=============================================================================+
| Handler Mode     | Always PRIVILEGED       | Strictly MSP (Main Stack)      |
| (All ISRs/Faults)| (Full hardware access)  |                                |
+------------------+-------------------------+--------------------------------+
| Thread Mode      | PRIVILEGED (Default)    | MSP or PSP (Configurable via   |
| (Main App/Tasks) | or UNPRIVILEGED (User)  | CONTROL[1] bit)                |
+-----------------------------------------------------------------------------+
```

```
                 STATE TRANSITIONS BETWEEN MODES & STACKS
+-----------------------------------------------------------------------------+
|                                THREAD MODE                                  |
|                 (Runs User Applications & RTOS Tasks)                       |
|                                                                             |
|      Can run Privileged OR Unprivileged                                    |
|      Uses PSP (in RTOS tasks) or MSP (in bare-metal super-loops)            |
+-----------------------------------------------------------------------------+
               |                                             ^
               | Hardware Interrupt                          | Exception Return
               | (ADC Ready, UART IRQ, SysTick)             | (Loads EXC_RETURN
               |                                             |  into PC)
               v                                             |
+-----------------------------------------------------------------------------+
|                                HANDLER MODE                                 |
|                 (Runs Interrupt Service Routines - ISRs)                    |
|                                                                             |
|      ALWAYS Privileged                                                      |
|      ALWAYS uses MSP (Main Stack Pointer)                                   |
+-----------------------------------------------------------------------------+
```

---

::: callout-exam KTU High-Yield: Why ARM Has TWO Stack Pointers (MSP vs PSP) [KTU PBCST504 - 5 Marks]
**Model Exam Answer Breakdown:**

1. **Isolation of OS Kernel from Application Tasks:**
   In an embedded Real-Time Operating System (such as FreeRTOS), every user task has its own allocated stack buffer in SRAM. By setting the `CONTROL[1]` bit, all user tasks run in **Thread Mode using PSP (Process Stack Pointer)**. The OS kernel, scheduler, and all Interrupt Service Routines (ISRs) run using **MSP (Main Stack Pointer)**.
2. **Containment of Stack Overflows:**
   If an untrusted or buggy user task encounters an infinite recursion or declares a massive local array that overflows its stack, it corrupts only its local **PSP** memory space. Because interrupt handlers and system exceptions use the **MSP**, the CPU can still successfully take an interrupt, enter Handler Mode, and run the operating system's fault handler to terminate the rogue task safely without crashing the physical microcontroller!
3. **RAM Memory Conservation:**
   If the architecture only had one stack pointer, every single task in a multi-tasking system would have to reserve enough extra stack space to accommodate worst-case nested interrupt frames ($32$ to $64+$ bytes per nested interrupt). With dual stack pointers, interrupt nesting occurs exclusively on the **MSP**, allowing task stacks (on **PSP**) to remain compact, saving valuable SRAM.
:::

---

### Hardware Auto-Stacking During an Exception

When an interrupt fires, the Cortex-M core pauses the running code and executes a **hardware automatic stack push** before entering the ISR. It saves exactly **8 registers** (known as the *Basic Stack Frame*) onto the currently active stack:

```
          HARDWARE EXCEPTION STACK FRAME (Auto-Pushed by Core in 12 Cycles)
                    Low Address  +--------------------+
                                 |         R0         | <-- New SP value
                                 +--------------------+
                                 |         R1         |
                                 +--------------------+
                                 |         R2         |
                                 +--------------------+
                                 |         R3         |
                                 +--------------------+
                                 |        R12         |
                                 +--------------------+
                                 |  R14 (Return LR)   |
                                 +--------------------+
                                 |  R15 (Return PC)   |
                                 +--------------------+
                    High Address |        xPSR        |
                                 +--------------------+
```
Because the hardware silicon automatically stacks `R0`-`R3`, `R12`, `LR`, `PC`, and `xPSR` in parallel over the internal bus, standard C functions can serve directly as Interrupt Service Routines without requiring special compiler assembly wrappers!

---

<a id="foundations"></a>
## 3. The 4GB Linear Memory Map & Bit-Banding

The ARM Cortex-M architecture implements a single, contiguous **32-bit Linear Address Space**. A 32-bit address bus can uniquely address:
$$2^{32}\text{ bytes} = 4,294,967,296\text{ bytes} = 4\text{ Gigabytes}$$

ARM standardizes how this 4GB address space is carved up, ensuring software consistency across all semiconductor vendors:

```
                THE UNIFIED 4GB CORTEX-M MEMORY MAP ARCHITECTURE
+------------------------------------+ 0xFFFFFFFF
| Vendor-Specific Memory             | (512 MB)
+------------------------------------+ 0xE0100000
| Private Peripheral Bus (SCS/PPB)   | (1 MB) NVIC, SysTick, MPU, SCB
+------------------------------------+ 0xE0000000
| External Device Region             | (1.0 GB) Off-chip memory-mapped registers
+------------------------------------+ 0xA0000000
| External RAM Region                | (1.0 GB) Off-chip NOR/NAND Flash, SDRAM
+------------------------------------+ 0x60000000
| Peripheral Region (Internal APB/AHB| (512 MB) GPIO, Timers, USART, I2C, SPI
|  Includes Bit-Band Alias Region)   |           Base: 0x40000000
+------------------------------------+ 0x40000000
| SRAM Region (Internal Data Memory) | (512 MB) Stack, Heap, Static Variables
|  Includes Bit-Band Alias Region)   |           Base: 0x20000000
+------------------------------------+ 0x20000000
| Code Region (Internal Flash ROM)   | (512 MB) Vector Table, Machine Code
+------------------------------------+ 0x00000000
```

---

### The Bit-Banding Architecture

In bare-metal embedded systems, engineers constantly toggle individual peripheral control bits (e.g., turning an output pin ON or clearing an interrupt flag). 

#### The Traditional Race Condition (Read-Modify-Write)
In standard architectures, changing a single bit requires three distinct CPU assembly operations:
1. `LDR`: Read the 32-bit register from memory into a CPU register ($2$ clock cycles).
2. `ORR`: Modify the target bit inside the CPU register ($1$ clock cycle).
3. `STR`: Store the 32-bit register back out to peripheral memory ($2$ clock cycles).

```
THE DEADLY READ-MODIFY-WRITE (RMW) RACE CONDITION
================================================================================
 Clock 1: Main code executes LDR: Reads GPIO_ODR (Pins 0 to 7 are LOW: 0x00)
 Clock 2: Main code executes ORR: Intends to set Pin 0 HIGH (Val = 0x01)
          *** HARDWARE INTERRUPT (ISR) FIRES SUDDENLY! ***
          ISR executes: Sets Pin 1 HIGH and stores 0x02 directly to GPIO_ODR!
          ISR completes and returns control to Main code.
 Clock 3: Main code resumes: Executes STR with its stale cached value (0x01)!
 
 RESULT: Pin 0 turns ON, but Pin 1 is ACCIDENTALLY WIPED OUT (forced LOW)!
```

#### The Silicon Solution: Bit-Banding
To eliminate this race condition without disabling global interrupts, ARM introduced **Bit-Banding** (featured in Cortex-M3 and Cortex-M4 processors).

Bit-banding maps **every single individual bit** inside a $1\text{ MB}$ memory zone (the *Bit-Band Region*) to an entire unique **32-bit word** in a separate address space (the *Bit-Band Alias Region*).

```
BIT-BAND REGION (Base)                    BIT-BAND ALIAS REGION (Expanded)
+-------------------------------+         +-------------------------------+
| Address: 0x20000000           |         | Address: 0x22000000 (Word 0)  |---> Bit 0
| [ b7 | b6 | b5 | ... | b1 | b0]         +-------------------------------+
+-------------------------------+         | Address: 0x22000004 (Word 1)  |---> Bit 1
                                          +-------------------------------+
                                          | Address: 0x22000008 (Word 2)  |---> Bit 2
                                          +-------------------------------+
                                          | Address: 0x2200000C (Word 3)  |---> Bit 3
                                          +-------------------------------+
```

* Writing a `1` or `0` to the **Alias Address** causes the bus hardware to execute an **atomic, single-cycle, hardware-level bit set/clear** in the underlying physical register.
* No `ORR` or `AND` assembly step is required.
* Because the bus matrix hardware locks the transaction, interrupts cannot corrupt the bit.

::: callout-formula Bit-Band Alias Address Translation Formula
To calculate the 32-bit alias address corresponding to any target bit in the bit-band region:

$$\text{Alias Address} = \text{Alias Base} + (\text{Byte Offset} \times 32) + (\text{Bit Number} \times 4)$$

Where:
* **For SRAM Region:**
  * $\text{Base Address} = 0\text{x}20000000$
  * $\text{Alias Base} = 0\text{x}22000000$
* **For Peripheral Region:**
  * $\text{Base Address} = 0\text{x}40000000$
  * $\text{Alias Base} = 0\text{x}42000000$
* $\text{Byte Offset} = \text{Target Register Address} - \text{Base Address}$
* $\text{Bit Number} = \text{Target Bit Position } (0 \text{ through } 31)$
:::

---

### Step-by-Step Bit-Banding Numerical Problem

**Exam Problem Statement:**
Calculate the exact 32-bit Bit-Band Alias Address required to atomically set/clear **Bit 3** of the peripheral register located at physical address **`0x40000100`**.

#### Step 1: Identify the Regional Constants
* Target Address $= 0\text{x}40000100$ (Located in the Peripheral Region).
* Peripheral Base Address $= 0\text{x}40000000$.
* Peripheral Alias Base Address $= 0\text{x}42000000$.
* Target Bit Number $= 3$.

#### Step 2: Compute the Byte Offset
$$\text{Byte Offset} = \text{Target Address} - \text{Peripheral Base}$$
$$\text{Byte Offset} = 0\text{x}40000100 - 0\text{x}40000000 = 0\text{x}00000100 \ (\text{which equals } 256_{10}\text{ bytes})$$

#### Step 3: Multiply Byte Offset by 32 (Scale to Word Addresses)
Each byte in the base region contains 8 bits, and each bit maps to a 4-byte (32-bit) word in the alias region. Thus, each base byte spans $8 \times 4 = 32\text{ bytes}$ of alias space:
$$\text{Byte Offset} \times 32 = 0\text{x}100 \times 32_{10}$$
Convert $32_{10}$ to hexadecimal: $32_{10} = 0\text{x}20$.
$$\text{Offset Contribution} = 0\text{x}100 \times 0\text{x}20 = 0\text{x}2000$$
*(Verification in decimal: $256 \times 32 = 8,192 = 0\text{x}2000$)*

#### Step 4: Multiply Bit Number by 4 (Word Offset)
Each individual bit is represented by a 4-byte word:
$$\text{Bit Contribution} = \text{Bit Number} \times 4 = 3 \times 4 = 12_{10}$$
Convert $12_{10}$ to hexadecimal:
$$\text{Bit Contribution} = 0\text{x}000C$$

#### Step 5: Sum All Terms for the Final Alias Address
$$\text{Alias Address} = \text{Alias Base} + (\text{Byte Offset} \times 32) + (\text{Bit Number} \times 4)$$
$$\text{Alias Address} = 0\text{x}42000000 + 0\text{x}00002000 + 0\text{x}0000000C$$
$$\mathbf{\text{Alias Address} = 0\text{x}4200200C}$$

**Firmware Implementation:**
```c
// Setting Bit 3 atomically with a single instruction:
*(volatile uint32_t *)(0x4200200CUL) = 1; // Hardware sets Bit 3 of 0x40000100 to 1!

// Clearing Bit 3 atomically:
*(volatile uint32_t *)(0x4200200CUL) = 0; // Hardware clears Bit 3 of 0x40000100 to 0!
```

---

<a id="history"></a>
## 4. The AMBA Bus Highway: AHB vs APB Matrix

Inside an ARM microcontroller, data travels between the CPU core, memories, and peripherals across an advanced on-chip interconnection network standardized by ARM: the **AMBA (Advanced Microcontroller Bus Architecture)** specification.

```
                  THE AMBA ON-CHIP BUS TOPOLOGY MATRIX
+-----------------------------------------------------------------------------+
|                           ARM Cortex-M33 Core                               |
|        [ I-Code Bus ]       [ D-Code Bus ]       [ System Bus ]             |
+-----------------------------------------------------------------------------+
               |                    |                     |
               v                    v                     v
+=============================================================================+
|             ADVANCED HIGH-PERFORMANCE BUS (AHB) BUS MATRIX                  |
|       (Multi-Layer 32-bit / 64-bit Interconnect Running at Full Core Clock) |
+=============================================================================+
       |                  |                  |                  |
       v                  v                  v                  v
 [ Flash Memory ]   [ SRAM Memory ]    [ Direct Memory    [ High-Speed Crypto |
 [ (Accelerated) ]  [ (Zero Latency) ] [ Access (DMA) ]   [ & USB-OTG Core ]   |
                                             |
                                             v
                           +-----------------------------------+
                           |         AHB-to-APB BRIDGE         |
                           | (Buffers data & divides the clock)|
                           +-----------------------------------+
                                             |
                                             v
+=============================================================================+
|             ADVANCED PERIPHERAL BUS (APB) LOW-POWER HIGHWAY                 |
|               (Running at Divided Clock Frequency: 40 - 80 MHz)             |
+=============================================================================+
       |                  |                  |                  |
       v                  v                  v                  v
 [ GPIO Ports ]     [ UART / USART ]   [ I2C / SPI Busses][ General Timers ]  
```

::: callout-intuition The Freeway vs The Downtown City Street
Think of the on-chip bus network like urban transportation:
* **The AHB (Advanced High-Performance Bus)** is an **8-lane interstate highway**. Traffic moves at $160\text{ km/h}$ with non-stop flow, high throughput, and multi-lane overtaking (pipelined bursts). You place high-speed entities here: the CPU Core, Flash Memory, SRAM, and Direct Memory Access (DMA) engines.
* **The APB (Advanced Peripheral Bus)** is a **quiet residential side street** with speed bumps. Traffic moves at $30\text{ km/h}$. You do not need an 8-lane highway to connect a mailbox or a garbage can. Peripherals like a UART serial port (transmitting a few kilobits per second) or an I2C sensor bus live on the APB. This deliberate slowdown conserves massive amounts of dynamic silicon switching power ($P = C \cdot V^2 \cdot f$)!
* **The AHB-to-APB Bridge** acts as the highway off-ramp: it throttles the high-speed CPU transaction down to the relaxed timing required by peripheral registers.
:::

---

### Structural Comparison: AHB vs APB

<div class="table-wrap">

| Dimension | Advanced High-Performance Bus (AHB) | Advanced Peripheral Bus (APB) |
| :--- | :--- | :--- |
| **Bus Performance Tier** | First-tier, high-bandwidth system backbone | Secondary-tier, low-bandwidth peripheral bus |
| **Operating Clock Frequency** | Runs at full CPU system clock (e.g., $160\text{ MHz} - 250\text{ MHz}$) | Runs at divided peripheral clock (typically $\frac{1}{2}$ or $\frac{1}{4}$ system clock) |
| **Bus Width** | 32-bit, 64-bit, or 128-bit wide data buses | Typically strictly 32-bit wide data bus |
| **Pipelining Support** | **Fully Pipelined**: Overlaps address and data phases for continuous throughput | **Non-Pipelined**: Requires a basic 2-cycle transfer (Setup phase $\to$ Access phase) |
| **Burst Transfers** | Supported (multi-word bursts: incrementing or wrapping) | Not supported (single read/write transfers only) |
| **Bus Master Multiplicity** | **Multi-Master**: CPU core, DMA1, DMA2 can master the bus via priority arbitration | **Single-Master**: Only the AHB-to-APB Bridge can drive the APB bus |
| **Typical Connected Devices** | Internal Flash, SRAM, DMA Controllers, SDRAM Interface, USB-HS, Crypto | GPIO Ports, UART/USART, SPI, I2C, Watchdog Timers, DAC, Basic Timers |
| **Silicon Power Dissipation** | Higher dynamic power consumption due to continuous high-speed clocking | **Ultra-low power**: optimized to minimize switching currents when idle |

</div>

---

<a id="self-check"></a>
## 5. Interactive Self-Check Quiz

::: quiz Link Register and Return Behavior
During the execution of a normal C function call on an ARM Cortex-M processor, what does the Link Register (`R14` / `LR`) store, and what unique value does it hold when execution enters an Interrupt Service Routine (ISR)?
( ) It always holds the address of the Vector Table; during an ISR it holds zero.
( ) It stores the value of the Program Status Register; during an ISR it stores the task stack pointer.
(*) It stores the return address of the caller instruction; during an ISR it stores a special `EXC_RETURN` pattern indicating stack and execution state.
( ) It holds the current execution stack pointer; during an ISR it holds the address of the nested exception handler.
::: explanation
* In normal function calls (`BL`/`BLX`), `LR` stores the return address pointing to the instruction immediately following the call site.
* When an interrupt or exception triggers, the hardware automatically replaces `LR` with an **`EXC_RETURN` code** (e.g., `0xFFFFFFF9`, `0xFFFFFFFD`). When the ISR completes and branches to `LR` (`BX LR`), the processor detects this special signature, triggers hardware unstacking of `R0-R3, R12, LR, PC, xPSR`, and restores the previous processor operating mode and stack pointer.
:::

::: quiz Operating Modes and Stack Pointer Mapping
An embedded system running FreeRTOS encounters a software bug where a user application task executes an illegal instruction. Which operating mode and stack pointer are currently active while the user task is running, and which mode and stack pointer become active when the processor takes the resulting UsageFault exception?
( ) User task runs in Handler Mode using MSP; UsageFault executes in Thread Mode using PSP.
(*) User task runs in Thread Mode using PSP; UsageFault executes in Handler Mode using MSP.
( ) User task runs in Thread Mode using MSP; UsageFault executes in Handler Mode using PSP.
( ) User task runs in Handler Mode using PSP; UsageFault executes in Handler Mode using MSP.
::: explanation
* In an RTOS architecture, user application tasks execute in **Thread Mode** utilizing the **Process Stack Pointer (PSP)** (configured with unprivileged permissions).
* Whenever any exception or interrupt triggers (including a `UsageFault`), the hardware transitions immediately to **Handler Mode** and automatically forces the active stack pointer to the **Main Stack Pointer (MSP)**. Handler Mode is always privileged.
:::

::: quiz Bit-Band Alias Calculation
What is the exact 32-bit Bit-Band Alias Address to modify **Bit 5** of the SRAM memory byte located at address **`0x20000200`**?
( ) `0x22002005`
( ) `0x22004010`
(*) `0x22004014`
( ) `0x20004014`
::: explanation
Let us apply the bit-band translation formula:
$$\text{Alias Address} = \text{Alias Base} + (\text{Byte Offset} \times 32) + (\text{Bit Number} \times 4)$$
1. **Identify parameters:**
   * Region: SRAM (Base $= 0\text{x}20000000$, Alias Base $= 0\text{x}22000000$).
   * Target Address $= 0\text{x}20000200$.
   * Bit Number $= 5$.
2. **Byte Offset:**
   $$\text{Offset} = 0\text{x}20000200 - 0\text{x}20000000 = 0\text{x}00000200 \ (512_{10})$$
3. **Byte Offset $\times$ 32:**
   $$0\text{x}200 \times 0\text{x}20 = 0\text{x}4000 \ (512 \times 32 = 16,384_{10} = 0\text{x}4000)$$
4. **Bit Number $\times$ 4:**
   $$5 \times 4 = 20_{10} = 0\text{x}0014$$
5. **Sum terms:**
   $$\text{Alias Address} = 0\text{x}22000000 + 0\text{x}4000 + 0\text{x}0014 = \mathbf{0\text{x}22004014}$$
:::
