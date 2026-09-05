# Interrupt Architecture (NVIC/EXTI), Hardware Timers, PWM, and Real-Time Clock
**Nested Vectored Interrupt Controller, Tail-Chaining, Priority Grouping, EXTI Lines, Hardware Timer Prescalers & ARR, PWM Duty Cycle Math, and RTC 32.768 kHz Subsystem.**

---

### Quick Navigation
* [1. Polling vs Interrupts & The ARM Cortex-M NVIC](#the-intuition)
* [2. Interrupt Priorities & The External Interrupt (EXTI) Controller](#the-dimensions)
* [3. Hardware Timers & Frequency/Overflow Math](#foundations)
* [4. Pulse Width Modulation (PWM) & Real-Time Clock (RTC) Subsystem](#history)
* [5. Interactive Self-Check Quiz](#self-check)

---

<a id="the-intuition"></a>
## 1. Polling vs Interrupts & The ARM Cortex-M NVIC

When writing embedded software, a microcontroller core must constantly react to outside events: a human pressing a push-button, an analog sensor crossing an emergency threshold, an incoming serial packet, or a periodic timer tick.

There are two fundamental design paradigms for detecting these real-world events: **Polling** and **Interrupts**.

::: callout-intuition Polling vs The Doorbell
Imagine you are sitting in your living room expecting an urgent courier delivery:
* **Polling Approach:** Every $10$ seconds, you stop what you are doing, walk to the front door, open it, check if a package is sitting on the porch, close the door, and walk back to your chair.
  * You waste $100\%$ of your mental energy pacing back and forth.
  * If the delivery driver drops the package and rings the bell while you are walking back, you won't notice until your next scheduled check.
  * If a fire starts in the kitchen while you are staring at the door, the house burns down.
* **Interrupt Approach:** You install an electric **Doorbell**. You sit comfortably at your desk writing code or taking a nap. 
  * When the courier arrives, they press the doorbell button.
  * The chime rings through the house, **instantly pausing** your work.
  * You walk to the door, sign for the package, and immediately return to your desk, resuming your work at the exact syllable you left off.
  * While waiting, your CPU consumes near-zero power and wastes zero clock cycles!
:::

```
                        POLLING vs INTERRUPT TIMING
====================================================================================================
 POLLING (Wastes CPU cycles in infinite status checks):
  CPU Core: [ Check Flag ] -> [ Check Flag ] -> [ Check Flag ] -> [ Event Detected! ] -> [ Service ]
  Time:     |------------- 100% CPU Bandwidth Consumed --------------------------------->|
 
 INTERRUPT-DRIVEN (Asynchronous, Zero-Waste, Instantaneous Response):
  CPU Core: [ Useful App Math / Low-Power Sleep ] ----+                +--> [ Resume App Math ]
                                                      |                |
  Hardware Event (EXTI / Timer):                      v (12 Cycles)    | (Restore State)
                                                [ Auto-Stack ]         |
                                                [ Execute ISR Handler ]+
====================================================================================================
```

---

### What Makes ARM NVIC "Vectored" and "Nested"?

Every modern ARM Cortex-M processor integrates a dedicated hardware peripheral called the **NVIC (Nested Vectored Interrupt Controller)** directly inside the silicon die alongside the CPU core.

```
                  THE ARM CORTEX-M NVIC SILICON ARCHITECTURE
====================================================================================================
  HARDWARE INTERRUPT SOURCES
  - EXTI (Pushbuttons / Pins) ----+
  - TIM2 / TIM3 (Hardware Timers)-|
  - USART1 (Serial RX Ready) -----|      +-----------------------------------------+
  - ADC1 (Conversion Complete) ---+====> | NESTED VECTORED INTERRUPT CONTROLLER    |
  - I2C / SPI Transfer Done ------|      | (NVIC)                                  |
                                         | - 16 System Exceptions (SysTick, Faults)|
                                         | - Up to 240 Hardware IRQ Lines          |
                                         | - Hardware Priority Arbitration         |
                                         +-----------------------------------------+
                                                              |
                                        Vector Address Jump   | Core Preempt Signal
                                                              v
                                         +-----------------------------------------+
                                         | ARM Cortex-M CPU Core (ALU & Pipeline)  |
                                         +-----------------------------------------+
====================================================================================================
```

The name **Nested Vectored Interrupt Controller** defines its two core architectural pillars:

1. **Vectored (Direct Hardware Branching):**
   * In legacy 8-bit microcontrollers (like standard 8051 or PICs), whenever any interrupt triggered, the CPU jumped to a single shared address. The firmware had to run multiple `if/else` checks polling status bits to figure out which peripheral fired.
   * In ARM Cortex-M, each interrupt source has a dedicated, predefined slot in Flash memory known as the **Vector Table**. When Timer 2 overflows, the NVIC hardware reads the address stored at slot 28 and **branches directly to that specific C function** (`TIM2_IRQHandler`) in hardware!
2. **Nested (Dynamic Execution Preemption):**
   * If the microcontroller is currently executing a low-priority interrupt routine (e.g., updating an LCD screen) and an urgent high-priority emergency arrives (e.g., a motor overcurrent sensor trips), the NVIC **immediately preempts (pauses)** the running ISR, executes the emergency ISR, and then returns to finish the low-priority display routine.

::: callout-intuition The Executive Secretary Metaphor
Think of the **NVIC** as a ruthlessly efficient Executive Assistant sitting outside the CEO's (the CPU's) office:
* If the intern walks in with routine paperwork (low priority), the assistant lets them speak only if the CEO is idle.
* If a VP walks in with a quarterly report (medium priority), the assistant pauses the intern and sends in the VP.
* If the Fire Chief kicks the door open screaming that the building is on fire (highest priority / Non-Maskable Interrupt), the assistant instantly pauses the VP, routes the Fire Chief straight to the CEO's desk, and evacuates the building!
:::

---

### Low-Latency Silicon Optimizations

The ARM Cortex-M NVIC achieves hard real-time determinism through three specialized silicon acceleration features:

```
          HARDWARE EXCEPTION STACK FRAME (Auto-Pushed by Silicon in 12 Cycles)
                    Low Address  +--------------------+
                                 |         R0         | <-- New Stack Pointer (SP)
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

1. **Automatic Hardware Register Stacking (12 Clock Cycles):**
   When an interrupt occurs, the hardware automatically pushes eight CPU registers (`R0-R3`, `R12`, `LR`, `PC`, `xPSR`) onto the active stack in parallel over the internal bus. Because this is hardwired in silicon, **standard C functions can serve directly as Interrupt Service Routines (ISRs)** without needing custom assembly prologue/epilogue code!
2. **Tail-Chaining (6-Cycle Seamless Handoff):**
   If a second interrupt arrives while an ISR is already executing, the processor does not waste $12$ cycles popping the registers off the stack just to waste another $12$ cycles pushing them right back. Instead, it skips unstacking entirely, saving $\approx 18\text{ clock cycles}$ and transitioning directly into the pending ISR in only **$6$ cycles**!
3. **Late-Arrival Optimization:**
   If a high-priority interrupt fires while the core is in the middle of stacking registers for a low-priority interrupt, the NVIC does not abort or restart. It finishes the 12-cycle stacking sequence and immediately vectors to the *high-priority* handler first.

---

<a id="the-dimensions"></a>
## 2. Interrupt Priorities & The External Interrupt (EXTI) Controller

### Priority Grouping: Preemption Priority vs Sub-Priority

ARM Cortex-M divides its interrupt priority register into two functional tiers using a concept called **Priority Grouping**:

```
                       8-BIT / 4-BIT PRIORITY FIELD SPLIT
====================================================================================================
   [ BIT 7 ]   [ BIT 6 ]   [ BIT 5 ]   [ BIT 4 ]   |   [ BIT 3 ]   [ BIT 2 ]   [ BIT 1 ]   [ BIT 0 ]
  +--------------------------------------------+---+--------------------------------------------+
  |            PREEMPTION PRIORITY             |                  SUB-PRIORITY                  |
  |  (Determines who can interrupt a running   |       (Tie-breaker when two interrupts        |
  |   ISR to execute immediately)              |        arrive at the EXACT same cycle)         |
  +--------------------------------------------+------------------------------------------------+
====================================================================================================
```

* **Preemption Priority:** If Interrupt $A$ has higher preemption priority than running Interrupt $B$, the NVIC pauses Interrupt $B$ and runs Interrupt $A$ immediately.
* **Sub-Priority:** If two interrupts with the *same* preemption priority arrive at the *exact same clock cycle*, the one with the higher sub-priority executes first. **Sub-priority can NEVER preempt an already running ISR!**

::: callout-pitfall The Inverted Priority Rule
In ARM Cortex-M silicon: **A lower numerical value indicates a HIGHER physical priority!**
* **Priority 0:** The absolute highest, most urgent software priority.
* **Priority 15:** The lowest, least urgent priority.
If you configure your emergency brake button to Priority 15 and your blinky LED timer to Priority 1, the LED will preempt and block your emergency brake!
:::

---

### The External Interrupt / Event Controller (EXTI)

Microcontrollers do not have hundreds of separate physical interrupt pins. Instead, the STM32 routes physical GPIO pins into the NVIC using an intermediate **EXTI (External Interrupt) Multiplexer**.

```
                   STM32 EXTI LINE MULTIPLEXING ARCHITECTURE
====================================================================================================
  PORT A         PORT B         PORT C
  [ PA0 ]        [ PB0 ]        [ PC0 ]
     |              |              |
     +-------+      |      +-------+
             |      |      |
             v      v      v
          +-------------------+
          |  SYSCFG / EXTI0   |--------> [ EXTI Line 0 ] -------> NVIC IRQ 6 (EXTI0_IRQn)
          |    Multiplexer    |
          +-------------------+
             ^      ^      ^
             |      |      |
  [ PA1 ]----+      |      +----[ PC1 ]
                    v
                 [ PB1 ]
          +-------------------+
          |  SYSCFG / EXTI1   |--------> [ EXTI Line 1 ] -------> NVIC IRQ 7 (EXTI1_IRQn)
          |    Multiplexer    |
          +-------------------+
====================================================================================================
```

#### The Fundamental EXTI Multiplexing Limitation:
* An STM32 has 16 independent EXTI lines for GPIO pins: `EXTI0` through `EXTI15`.
* Pin index $n$ from every port (`PA[n]`, `PB[n]`, `PC[n]`, `PD[n]`) feeds into a multiplexer for `EXTI[n]`.
* **Rule:** **You CANNOT use `PA0` and `PB0` as simultaneous external interrupts!** You can only select one pin per numerical index at any given time.

#### Edge Triggering Modes:
Each EXTI line contains hardware edge-detection latches configured via software:
1. **Rising Edge Trigger:** Fires when pin voltage transitions from $0\text{ V} \to 3.3\text{ V}$.
2. **Falling Edge Trigger:** Fires when pin voltage transitions from $3.3\text{ V} \to 0\text{ V}$ (ideal for active-low pushbuttons with pull-up resistors).
3. **Rising & Falling (Both Edges):** Fires on every state transition (ideal for rotary encoders).

---

### Annotated STM32 HAL C Implementation

```c
#include "main.h"

// 1. HARDWARE INITIALIZATION (Configures PA0 as an Interrupt Source)
void MX_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // Enable clock access for GPIO Port A
    __HAL_RCC_GPIOA_CLK_ENABLE();

    // Configure PA0 as an Input with Falling Edge Triggering
    GPIO_InitStruct.Pin  = GPIO_PIN_0;
    GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;   // Trigger when button pulled to GND
    GPIO_InitStruct.Pull = GPIO_PULLUP;            // Internal pull-up to 3.3V
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    // Set Priority in NVIC: Preemption Priority = 2, Sub-Priority = 0
    HAL_NVIC_SetPriority(EXTI0_IRQn, 2, 0);

    // Enable the Interrupt Line inside the NVIC
    HAL_NVIC_EnableIRQ(EXTI0_IRQn);
}

// 2. LOW-LEVEL VECTOR HANDLER (Located in stm32u5xx_it.c)
// The hardware jumps directly to this exact function when PA0 triggers
void EXTI0_IRQHandler(void) {
    // Clear pending flag in EXTI hardware register and call user callback
    HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0);
}

// 3. HIGH-LEVEL USER CALLBACK (Override inside main.c)
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if (GPIO_Pin == GPIO_PIN_0) {
        // Safe, non-blocking response: Toggle status LED
        HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_7);
    }
}
```

::: callout-pitfall The Fatal ISR Delay Trap: Never Call `HAL_Delay()` Inside an ISR
One of the most common beginner bugs is writing `HAL_Delay(500);` or heavy `printf()` statements inside an interrupt callback:

```c
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    HAL_Delay(1000); // SYSTEM LOCKUP DISASTER!
}
```

**Why this locks up the microcontroller:**
`HAL_Delay()` relies on the **SysTick** timer interrupt ticking every $1\text{ ms}$ to increment an internal counter. By default, the SysTick interrupt has a preemption priority level of $15$ (or $0$ depending on setup). If your EXTI interrupt executes at the same or higher priority than SysTick, **SysTick cannot preempt your ISR**. The millisecond counter freezes, `HAL_Delay()` waits forever, and the system crashes into a permanent deadlock!

**The Golden Rule:** Keep ISRs extremely short (a few microseconds). Clear hardware flags, store data in a buffer, set a `volatile uint8_t flag = 1;`, and let the main `while(1)` loop handle slow processing!
:::

---

<a id="foundations"></a>
## 3. Hardware Timers & Frequency/Overflow Math

### Why Software Delay Loops Fail

In introductory desktop programming, developers use simple delay loops:
```c
for (volatile int i = 0; i < 500000; i++); // Burn clock cycles
```
In embedded systems, software delay loops are unacceptable:
1. **$100\%$ CPU Starvation:** The processor cannot execute communications, compute sensor filters, or service display buffers while stuck spinning in a loop.
2. **Timing Drift:** If an interrupt occurs during the loop, the delay stretches unpredictably.
3. **Compiler Fragility:** Turning on compiler optimizations (`-O2` or `-O3`) often eliminates the loop entirely!

The solution is an autonomous **Hardware Timer**.

---

### Anatomical Silicon Blocks of a General-Purpose Timer

A hardware timer is a dedicated silicon digital counter operating entirely in parallel with the CPU. It runs from an independent peripheral clock bus ($f_{\text{TIM\_CLK}}$).

```
                 HARDWARE GENERAL-PURPOSE TIMER DATA-PATH
====================================================================================================
 TIM_CLK (e.g., 16 MHz)
       |
       v
 +-----------------------------+
 | PRESCALER REGISTER (PSC)    |  Divides clock frequency down by (PSC + 1):
 | (16-bit: 0 to 65,535)       |  f_counter = f_TIM_CLK / (PSC + 1)
 +-----------------------------+
       |
       v  Count Pulses (Tick Rate)
 +-----------------------------+
 | COUNTER REGISTER (CNT)      | <---+  Increments on every prescaled clock pulse.
 | (16-bit or 32-bit)          |     |
 +-----------------------------+     |
       |                             |
       | Compares equality           | Reset CNT to 0 on match!
       v                             |
 +-----------------------------+     |
 | AUTO-RELOAD REGISTER (ARR)  |-----+
 | (16-bit or 32-bit)          |
 +-----------------------------+
       |
       v  Comparator Match Event (CNT == ARR)
 +--------------------------------------------------------------------------------------------------+
 | HARDWARE UPDATE EVENT (UEV) -> Sets UIF Flag -> Triggers TIMx_IRQHandler in NVIC (Interrupt!)   |
 +--------------------------------------------------------------------------------------------------+
====================================================================================================
```

#### The 3 Core Registers:
1. **Prescaler Register (`PSC` - 16 bits):**
   A digital divider that scales down the incoming high-speed bus clock. It divides the frequency by an integer factor of $(\text{PSC} + 1)$.
2. **Counter Register (`CNT` - 16 or 32 bits):**
   The active storage register that increments (or decrements) by $1$ on every prescaled pulse.
3. **Auto-Reload Register (`ARR` - 16 or 32 bits):**
   The ceiling threshold value. When `CNT` counts up and matches `ARR`, the timer triggers an **Update Event (UEV)**, resets `CNT` to zero, and continues counting.

---

### The Golden Timer Equations (Derived from First Principles)

#### 1. Counter Tick Frequency ($f_{\text{CNT}}$)
The rate at which the `CNT` register increments each second:
$$f_{\text{CNT}} = \frac{f_{\text{TIM\_CLK}}}{\text{PSC} + 1}$$

#### 2. Total Ticks Required for One Overflow Period
To count from $0$ up to $\text{ARR}$ takes exactly $(\text{ARR} + 1)$ individual counter ticks:
$$\text{Ticks per Period} = \text{ARR} + 1$$

#### 3. Timer Overflow Period ($T_{\text{overflow}}$) & Update Frequency ($f_{\text{overflow}}$)
Multiplying the tick period by the number of ticks yields the total overflow duration:

$$T_{\text{overflow}} = \frac{(\text{PSC} + 1) \times (\text{ARR} + 1)}{f_{\text{TIM\_CLK}}}$$

$$f_{\text{overflow}} = \frac{1}{T_{\text{overflow}}} = \frac{f_{\text{TIM\_CLK}}}{(\text{PSC} + 1) \times (\text{ARR} + 1)}$$

::: callout-formula Why We Always Add 1 to PSC and ARR
Microcontroller registers are zero-indexed:
* If you write $\text{PSC} = 0$, the clock is divided by $(0 + 1) = 1$ (no division).
* If you write $\text{ARR} = 0$, the counter steps through $1$ state ($0 \to \text{overflow}$), taking $(0 + 1) = 1$ tick.
* Therefore, the physical divisor is always $(\text{PSC} + 1)$ and $(\text{ARR} + 1)$.
:::

---

### Worked Step-by-Step Engineering Example

**Problem Statement:**
An engineer uses an STM32 timer clocked from an internal bus at $f_{\text{TIM\_CLK}} = 16\text{ MHz}$ ($16,000,000\text{ Hz}$). 
Calculate the exact 16-bit register values for **`PSC`** and **`ARR`** required to trigger a periodic timer interrupt at a rate of precisely **$1.000\text{ Hz}$ ($T_{\text{overflow}} = 1.000\text{ second}$)** to toggle a heartbeat LED.

#### Step 1: Establish the 16-Bit Register Constraints
Both `PSC` and `ARR` on standard timers (like TIM3) are **16-bit registers**:
$$\text{Max Value} = 2^{16} - 1 = \mathbf{65,535}$$

#### Step 2: Test Direct Division Without Prescaler
If we set $\text{PSC} = 0$:
$$(\text{PSC} + 1) \times (\text{ARR} + 1) = f_{\text{TIM\_CLK}} \times T_{\text{overflow}} = 16,000,000 \times 1.0\text{ s} = 16,000,000$$
$$\text{ARR} + 1 = 16,000,000 \implies \text{ARR} = 15,999,999$$
Because $15,999,999 > 65,535$, **this value overflows a 16-bit register!** We must use the prescaler to reduce the counter frequency.

#### Step 3: Select a Prescaler to Scale the Clock
Let us divide the $16\text{ MHz}$ clock down to a clean, human-scale frequency—such as **$10\text{ kHz}$ ($10,000\text{ Hz}$)**:
$$f_{\text{CNT}} = \frac{f_{\text{TIM\_CLK}}}{\text{PSC} + 1} = 10,000\text{ Hz}$$
$$\text{PSC} + 1 = \frac{16,000,000\text{ Hz}}{10,000\text{ Hz}} = 1600$$
$$\mathbf{\text{PSC} = 1600 - 1 = 1599}$$
*(Validation: $1599 \le 65535$. This fits safely inside a 16-bit register!)*

#### Step 4: Calculate ARR for a 1.000 Second Period
Now, determine how many $10\text{ kHz}$ ticks are needed to reach $1.000\text{ second}$:
$$T_{\text{overflow}} = \frac{\text{ARR} + 1}{f_{\text{CNT}}} \implies 1.000\text{ s} = \frac{\text{ARR} + 1}{10,000\text{ Hz}}$$
$$\text{ARR} + 1 = 1.000 \times 10,000 = 10,000$$
$$\mathbf{\text{ARR} = 10,000 - 1 = 9999}$$
*(Validation: $9999 \le 65535$. This also fits inside a 16-bit register!)*

#### Step 5: Final Mathematical Verification
$$T_{\text{overflow}} = \frac{(1599 + 1) \times (9999 + 1)}{16,000,000} = \frac{1600 \times 10,000}{16,000,000} = \frac{16,000,000}{16,000,000} = \mathbf{1.00000\text{ Seconds!}}$$
* **Configuration:** Write `PSC = 1599` and `ARR = 9999`. The hardware timer will generate an interrupt at an exact $1.000\text{ Hz}$ rate without consuming any CPU execution cycles!

---

<a id="history"></a>
## 4. Pulse Width Modulation (PWM) & Real-Time Clock (RTC) Subsystem

### Pulse Width Modulation (PWM)

Pulse Width Modulation is a technique for controlling the average electrical power delivered to an analog load using a purely digital output pin.

::: callout-intuition Throttling Power Without Heat
Suppose you want to dim a $12\text{ V}$ incandescent light bulb to $50\%$ brightness:
* **The Inefficient Analog Method:** Insert a large variable resistor (rheostat) in series. The resistor drops $6\text{ V}$ and converts that electrical power directly into waste heat ($P = I^2 R$). The resistor gets hot, and energy is lost.
* **The Efficient PWM Method:** Connect an electronic switch (MOSFET) that flips between fully ON ($12\text{ V}$) and fully OFF ($0\text{ V}$) hundreds of times per second. 
  * If it stays ON for $50\%$ of the time and OFF for $50\%$ of the time, the bulb receives an average of $6\text{ V}$.
  * Because the transistor is either fully ON (near zero resistance) or fully OFF (zero current), **virtually zero energy is lost as waste heat**!
:::

---

### PWM Generation Mechanics & The Compare Register (`CCR`)

To generate PWM in hardware, the timer introduces a fourth register: the **Capture/Compare Register (`CCR`)**.

```
                   PWM GENERATION WAVEFORM (PWM Mode 1: Active High)
====================================================================================================
 Counter (CNT)
   ^
ARR+                                         /|          /|          /|
   |                                        / |         / |         / |
CCR+ - - - - - - - - - - - - - - - - - - - / -|- - - - / -|- - - - / -|- - - - - -
   |                                      /   |       /   |       /   |
   |                                     /    |      /    |      /    |
 0 +------------------------------------+-----+-----+-----+-----+-----+------------------------->
   |<----------- Period (T) ----------->|     |     |     |     |     |                      Time
                                        |     |     |     |     |     |
 PWM Pin (25% Duty Cycle)               |     |     |     |     |     |
3.3V+----+                              +-----+     +-----+     +-----+
   | ON |                              | ON  |     | ON  |     | ON  |
 0V+----+-------------------------------+-----+-----+-----+-----+-----+------------------------->
   |<-D->|<--------- OFF -------------->|
====================================================================================================
```

* In standard **PWM Mode 1 (Upcounting)**:
  * While $\text{CNT} < \text{CCR}$, the physical output pin is driven **HIGH** ($3.3\text{ V}$).
  * The moment $\text{CNT} \ge \text{CCR}$, the output pin drops **LOW** ($0\text{ V}$).
  * When $\text{CNT}$ reaches $\text{ARR}$, it resets to $0$, driving the output HIGH again.

#### Duty Cycle Formula:
$$\text{Duty Cycle (\%)} = \frac{\text{CCR}}{\text{ARR} + 1} \times 100\%$$

```
                         PWM DUTY CYCLE COMPARISONS
====================================================================================================
 25% Duty Cycle:   +--+        +--+        +--+
 (Dim LED / Slow)  |  |________|  |________|  |________ (High for 25% of period)
 
 50% Duty Cycle:   +----+      +----+      +----+
 (Half Speed)      |    |______|    |______|    |______ (High for 50% of period)
 
 75% Duty Cycle:   +------+    +------+    +------+
 (Bright / Fast)   |      |____|      |____|      |____ (High for 75% of period)
====================================================================================================
```

---

### The Real-Time Clock (RTC) Subsystem

While general-purpose timers are well-suited for measuring microsecond delays or generating PWM, **they cannot keep real-world wall-clock time**:
1. When the microcontroller enters deep sleep (Stop or Standby mode) or main power is disconnected, high-speed clocks are turned off.
2. Standard high-speed crystal oscillators consume too much power to run continuously from a small battery.

The **RTC (Real-Time Clock)** is an autonomous, ultra-low-power peripheral designed to maintain seconds, minutes, hours, days, months, and leap years across decades.

```
                     THE STM32 RTC SUBSYSTEM ARCHITECTURE
====================================================================================================
  VBAT PIN (Backup Coin-Cell 3V)
       |
       +------------------------------------+
                                            |
  LSE OSCILLATOR PIN                        v
  [ 32.768 kHz Quartz ] ---> +-------------------------------+
  External Crystal           | 15-STAGE ASYNCHRONOUS         |   Divides 32,768 Hz by 2^15
                             | BINARY PRESCALER (DIVIDER)    |   down to PRECISELY 1.000 Hz!
                             +-------------------------------+
                                            |
                                            v  1 Hz Clock Pulse (Exact 1-Second Tick)
                             +-------------------------------+
                             | SHADOW CALENDAR REGISTERS     |
                             | (Encoded in Binary-Coded      |
                             |  Decimal - BCD Format)        |
                             | - Seconds (00 - 59)           |
                             | - Minutes (00 - 59)           |
                             | - Hours   (00 - 23)           |
                             | - Date, Month, Year, Leap Year|
                             +-------------------------------+
====================================================================================================
```

#### The Mathematics of $32.768\text{ kHz}$: Why This Specific Frequency?
Engineers chose $32.768\text{ kHz}$ for real-time clocks because it is an exact mathematical power of two:

$$32,768 = 2^{15}$$

* By feeding a $32.768\text{ kHz}$ quartz crystal into a simple **15-stage binary flip-flop ripple counter**, the frequency splits in half 15 times:
  $$\frac{32,768}{2 \times 2 \times 2 \times \dots \text{ (15 times)}} = \frac{32,768}{32,768} = \mathbf{1.00000\text{ Hz}}$$
* This yields a **$1\text{ second}$ tick** using minimal silicon logic, drawing less than **$300\text{ nA}$** of current!

#### The Backup Battery Domain ($V_{\text{BAT}}$):
* The RTC block lives in a physically segregated silicon power island powered by the **$V_{\text{BAT}}$** pin.
* When the main $+3.3\text{ V}$ power supply is unplugged, an internal power switch switches the RTC supply rail over to a $3\text{ V}$ coin-cell battery (CR2032). The microcontroller's CPU can remain unpowered on a shelf for 10 years; when plugged back in, it still knows the correct calendar date and time.

---

<a id="self-check"></a>
## 5. Interactive Self-Check Quiz

::: quiz Preemption Priority vs Sub-Priority
In an STM32 NVIC configuration, Interrupt Line $A$ has Preemption Priority $1$ and Sub-Priority $2$. Interrupt Line $B$ has Preemption Priority $2$ and Sub-Priority $0$. If Interrupt Line $B$ is currently running inside its ISR handler, and Interrupt Line $A$ triggers, what happens?
( ) Interrupt $A$ waits in a queue until Interrupt $B$ finishes, because $B$ has a higher sub-priority ($0$ vs $2$).
(*) The NVIC immediately preempts (pauses) Interrupt $B$ and executes Interrupt $A$, because $A$ has a higher preemption priority ($1$ vs $2$).
( ) The processor encounters a HardFault exception due to priority conflict.
( ) The NVIC merges both interrupts and executes them in lockstep.
::: explanation
Preemption priority determines whether one interrupt can interrupt another running interrupt. In ARM Cortex-M, **lower numerical values represent higher urgency**. Interrupt $A$ has Preemption Priority $1$, which is numerically lower (and therefore physically higher in priority) than Interrupt $B$'s Preemption Priority of $2$. Therefore, NVIC preempts Interrupt $B$ immediately. Sub-priority is evaluated only as a tie-breaker when two interrupts with the *same* preemption priority arrive simultaneously; it can never prevent preemption.
:::

::: quiz Hardware Timer Prescaler Calculations
A general-purpose hardware timer is clocked from an internal bus running at $f_{\text{TIM\_CLK}} = 84\text{ MHz}$. You need to generate an interrupt with an overflow period of precisely $T_{\text{overflow}} = 10\text{ milliseconds}$ ($0.010\text{ s}$). If the Prescaler (`PSC`) is set to $839$, what value must be written to the Auto-Reload Register (`ARR`)?
( ) `999`
(*) `999`
( ) `1000`
( ) `99`
::: explanation
Let us calculate step-by-step:
1. **Counter frequency:**
   $$f_{\text{CNT}} = \frac{f_{\text{TIM\_CLK}}}{\text{PSC} + 1} = \frac{84,000,000}{839 + 1} = \frac{84,000,000}{840} = 100,000\text{ Hz} \ (100\text{ kHz})$$
2. **Each counter tick takes:**
   $$T_{\text{tick}} = \frac{1}{100,000\text{ Hz}} = 10\ \mu\text{s} = 0.00001\text{ s}$$
3. **Target period:**
   $$T_{\text{overflow}} = (\text{ARR} + 1) \times T_{\text{tick}} \implies 0.010\text{ s} = (\text{ARR} + 1) \times 0.00001\text{ s}$$
   $$\text{ARR} + 1 = \frac{0.010}{0.00001} = 1000$$
   $$\mathbf{\text{ARR} = 1000 - 1 = 999}$$
*(Writing $\text{ARR} = 999$ yields exactly $10\text{ ms}$).*
:::

::: quiz EXTI Multiplexer Constraints
An engineer is laying out a printed circuit board for an STM32 project. They connect an emergency stop button to pin `PA0` and a door-interlock safety limit switch to pin `PB0`. Both switches are configured to trigger an external interrupt in software. What issue will occur when running the firmware?
( ) The microcontroller will physically burn out due to cross-conduction.
( ) The pins will work correctly because Port A and Port B have independent NVIC vector addresses.
(*) Only one switch can be active at any given time; `PA0` and `PB0` share the single multiplexed line `EXTI0`, making simultaneous external interrupts impossible.
( ) EXTI lines only work on Port C and Port D, not Port A or B.
::: explanation
In the STM32 EXTI architecture, all pins with the same numerical index (`PA0`, `PB0`, `PC0`, `PD0`, etc.) are routed through a multiplexer into a single shared interrupt line: **`EXTI0`**. The SYSCFG multiplexer can only select one port source for line 0 at a time. Therefore, `PA0` and `PB0` cannot function as independent external interrupts concurrently. To resolve this, one of the switches must be moved to a pin with a different number (such as `PB1` on `EXTI1`).
:::
