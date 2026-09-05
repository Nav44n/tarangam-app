# Analog Peripherals: SAR ADC, Sensor Interfacing, and DAC Waveform Synthesis
**Successive Approximation Register (SAR) ADC, Quantization Math, Sensor Signal Conditioning (LM35, LDR, Microphone), R-2R Ladder DAC, and Sine Wave Synthesis.**

---

### Quick Navigation
* [1. The Continuous World vs Discrete Silicon (ADC Foundations)](#the-intuition)
* [2. How Successive Approximation Register (SAR) ADC Works](#the-dimensions)
* [3. Sensor Signal Conditioning & Real-World Interfacing](#foundations)
* [4. Digital-to-Analog Conversion (DAC) & Waveform Synthesis](#history)
* [5. Interactive Self-Check Quiz](#self-check)

---

<a id="the-intuition"></a>
## 1. The Continuous World vs Discrete Silicon (ADC Foundations)

Physical reality is inherently analog and continuous. The heat radiating from an engine, the acoustic sound pressure of a human voice, the fluid pressure in a medical ventilator, and the ambient light of a sunset do not change in stepped integer jumps; they vary smoothly across an infinite spectrum of values.

In contrast, an ARM microcontroller is a discrete digital machine. Its internal registers, buses, and arithmetic units operate exclusively on binary digits ($0$ and $1$). It cannot natively comprehend an analog voltage of $1.734891\text{ V}$.

An **Analog-to-Digital Converter (ADC)** bridges this physical-digital divide by transforming a continuous analog voltage into a proportional discrete binary word.

```
                  THE ANALOG-TO-DIGITAL CONVERSION BRIDGE
====================================================================================================
 PHYSICAL PHENOMENON             ANALOG SENSOR                   STM32 ADC PERIPHERAL
 [ Continuous World ]            [ Transducer ]                  [ Discrete Silicon ]
 
   Heat, Pressure,       ---->   Continuous Analog    ---->      Quantized Binary Integer
   Light, Sound Waves            Voltage (0V - 3.3V)             (e.g., 12-bit word: 0x8A4)
====================================================================================================
```

---

### The 3 Pillars of Analog-to-Digital Conversion

Converting an analog signal to a digital number requires three sequential operations:

```
              THE THREE STAGES OF ANALOG-TO-DIGITAL CONVERSION
  Continuous
  Signal V(t)       1. SAMPLING             2. QUANTIZATION          3. ENCODING
     ^              (Discretize Time)       (Discretize Amplitude)   (Assign Binary Word)
     |                     |                        |                        |
 3.3V|     _--_            |   *     *              |   +--+ [Level 7]       |   111
     |   /      \    ===>  |  * *   * *       ===>  |   |  | [Level 6] ===>  |   110
     |  /        \         | *   * *   *            |   +--+ [Level 5]       |   101
   0V+------------>        +-------------->         +-------------->         +--------->
       Time (t)                Time (t_s)               Discrete Bins            Data Bus
```

1. **Sampling (Discretization in Time):**
   * An analog voltage varies continuously at every infinitesimal fraction of a second. The ADC samples the voltage at fixed periodic intervals of time ($T_s = \frac{1}{f_s}$, where $f_s$ is the sampling frequency).
   * **The Nyquist-Shannon Sampling Theorem:** To faithfully capture and reconstruct an analog signal without destructive distortion (**aliasing**), the sampling frequency $f_s$ must be at least twice the maximum frequency component ($f_{\max}$) present in the input signal:
     $$f_s \ge 2 \cdot f_{\max}$$
     *(Example: Human speech reaches up to $4\text{ kHz}$. A voice ADC must sample at a rate no lower than $8\text{ kHz}$.)*
2. **Quantization (Discretization in Amplitude):**
   * While the input voltage can take on an infinite number of continuous values between $0\text{ V}$ and $V_{\text{REF}}$, the digital system can only represent a finite number of discrete levels.
   * An $N$-bit ADC partitions the continuous voltage range between $0\text{ V}$ and the reference voltage ($V_{\text{REF}}$) into exactly $2^N$ discrete voltage "bins" or steps.
3. **Encoding (Binary Assignment):**
   * The converter assigns a unique $N$-bit binary integer to the quantized voltage level and deposits it into the microcontroller's peripheral data register.

---

### Core Mathematical Formulas

#### 1. ADC Resolution (1 LSB Voltage Step Size)
The resolution represents the smallest change in analog voltage that the ADC can physically detect. It corresponds to the voltage weight of the Least Significant Bit (LSB):

$$\text{Resolution (1 LSB)} = \frac{V_{\text{REF}}}{2^N}$$

Where:
* $V_{\text{REF}}$ is the analog reference voltage (typically $+3.3\text{ V}$ on STM32 boards).
* $N$ is the bit-width of the ADC converter (e.g., $12\text{ bits}$).

#### 2. Analog Voltage to Digital Code Translation
When the ADC samples an unknown input voltage $V_{\text{analog}}$, the resulting raw digital integer $D_{\text{raw}}$ is:

$$D_{\text{raw}} = \text{round}\left( \frac{V_{\text{analog}}}{V_{\text{REF}}} \times (2^N - 1) \right)$$

Conversely, firmware calculates the physical voltage from the raw integer reading using:

$$V_{\text{analog}} = \frac{D_{\text{raw}}}{2^N - 1} \times V_{\text{REF}} \quad \approx \quad D_{\text{raw}} \times \left(\frac{V_{\text{REF}}}{2^N}\right)$$

#### 3. Quantization Error ($Q$)
Because continuous analog voltages are rounded into discrete bins, an inherent uncertainty exists between the true physical voltage and its digital representation. This error is strictly bounded by half of one LSB:

$$\text{Quantization Error } (Q) = \pm \frac{1}{2}\text{LSB} = \pm \frac{V_{\text{REF}}}{2^{N+1}}$$

::: callout-formula Signal-to-Quantization-Noise Ratio (SQNR)
Every additional bit of ADC resolution cuts the quantization noise voltage in half, improving the theoretical dynamic range and signal clarity by approximately $6.02\text{ dB}$:

$$\text{SQNR} = 6.02 \cdot N + 1.76\text{ dB}$$

* For an 8-bit ADC: $\text{SQNR} \approx 49.9\text{ dB}$
* For a 12-bit ADC (STM32 default): $\text{SQNR} \approx \mathbf{74.0\text{ dB}}$
* For a 16-bit high-precision ADC: $\text{SQNR} \approx 98.1\text{ dB}$
:::

---

### Numerical Worked Example (Step-by-Step)

**Problem Statement:**
An engineer interfaces an analog pressure sensor to an STM32 12-bit ADC ($N = 12$). The microcontroller is powered from a stable analog reference rail $V_{\text{REF}} = 3.30\text{ V}$.
1. Calculate the voltage step size represented by $1\text{ LSB}$.
2. Calculate the theoretical maximum Quantization Error.
3. If the ADC Data Register reads a raw value of **$2450$**, compute the exact physical analog voltage present on the pin.

#### Step 1: Calculate 1 LSB Resolution
$$2^N = 2^{12} = 4096 \text{ discrete levels}$$
$$\text{Resolution (1 LSB)} = \frac{V_{\text{REF}}}{2^N} = \frac{3.30\text{ V}}{4096} = 0.00080566\text{ V} = \mathbf{805.66\ \mu\text{V} \ (0.806\text{ mV})}$$

#### Step 2: Calculate Maximum Quantization Error
$$\text{Quantization Error } (Q) = \pm \frac{1}{2} \text{LSB} = \pm \frac{805.66\ \mu\text{V}}{2} = \mathbf{\pm 402.83\ \mu\text{V}}$$

#### Step 3: Calculate the Physical Input Voltage
Using the full-scale span ($2^{12} - 1 = 4095$):
$$V_{\text{analog}} = \frac{D_{\text{raw}}}{4095} \times V_{\text{REF}}$$
$$V_{\text{analog}} = \frac{2450}{4095} \times 3.30\text{ V} = 0.5982906 \times 3.30\text{ V} = \mathbf{1.97436\text{ V}}$$

*(Verification using LSB step sizing: $2450 \times 805.664\ \mu\text{V} \approx 1.97388\text{ V}$. Both methods match to within the quantization margin of $\pm 0.4\text{ mV}$.)*

---

<a id="the-dimensions"></a>
## 2. How Successive Approximation Register (SAR) ADC Works

The vast majority of modern general-purpose microcontrollers, including the STM32 family, employ a **Successive Approximation Register (SAR)** ADC architecture. 

SAR converters are the industry standard for embedded systems because they strike an optimal balance between **high resolution ($10 - 16\text{ bits}$)**, **fast conversion speeds ($1 - 5\text{ MSPS}$)**, **low power consumption**, and **compact silicon footprint**.

::: callout-intuition The Pan Balance with Binary Weights Analogy
Imagine you are an old-world merchant with a two-pan balance scale. You are handed an unknown bag of gold dust (the unknown input voltage $V_{\text{in}}$) and a set of precision metric weights that follow a binary progression: **$8\text{g}$**, **$4\text{g}$**, **$2\text{g}$**, and **$1\text{g}$**.

How do you find the unknown weight in the fewest possible steps? You do not start by guessing random numbers; you perform a **Binary Search**:

1. **Test the heaviest weight (8g) - The MSB:** Place 8g on the right pan. 
   * *Did the scale tip right?* If yes, the bag is lighter than 8g $\to$ Remove the 8g weight (Bit = 0).
   * *If no*, the bag is heavier than 8g $\to$ Keep the 8g weight on the pan (Bit = 1).
2. **Test the next weight (4g):** Add 4g to the pan.
   * Compare total pan weight against the gold. Keep it if the scale doesn't tip; discard it if it does.
3. **Repeat sequentially** for 2g, and finally 1g (the LSB).

In exactly **4 balance tests**, you have resolved an unknown weight between $0\text{g}$ and $15\text{g}$ down to $1\text{g}$ accuracy! A SAR ADC operates on this exact binary search principle using voltages inside silicon.
:::

---

### Silicon Architecture of a SAR ADC

```
                       INTERNAL ARCHITECTURE OF A SAR ADC
====================================================================================================
                        SAMPLE & HOLD (S/H) CIRCUIT
                      
                      Sampling Switch (S1)
  ANALOG INPUT PIN -------o/ o------------+
  (e.g., PA0)                             |
                                         === Hold Capacitor (C_hold)
                                         === (~5 pF - 10 pF)
                                          |
                                         GND
                                          |
                                          v  V_sample (Stable held voltage)
                                       +-----+
                                       |  +  |
                                       |     |--------+
                                  +--->|  -  |        |
                                  |    +-----+        |
                                  |   High-Speed      v
                                  |   Comparator    +--------------------------------+
                                  |                 | SAR CONTROL LOGIC              |
                                  |                 | - Clock Sequencer              |
                                  |                 | - Shift Registers              |
                                  |                 +--------------------------------+
                                  |                                 |
                                  | (V_DAC feedback)                v
                        +-------------------+         +------------------------------+
  V_REF (3.3V) -------->| INTERNAL R-2R /   |<--------| SAR OUTPUT REGISTER          |
                        | CAPACITIVE DAC    |         | (Holds current binary guess) |
                        +-------------------+         +------------------------------+
                                                                    |
                                                                    v
                                                      +------------------------------+
                                                      | ADC DATA REGISTER (ADC_DR)   |---> CPU AHB Bus
                                                      +------------------------------+
====================================================================================================
```

#### The 4 Critical Silicon Blocks:
1. **Sample and Hold (S/H) Unit:**
   An analog input signal must not fluctuate while the binary search is underway. The S/H circuit closes an analog switch for a programmed duration (the *Sampling Time*), charging a small internal capacitor ($C_{\text{hold}} \approx 5\text{ pF} - 10\text{ pF}$). The switch opens, locking the sampled voltage on the capacitor for the rest of the conversion.
2. **High-Speed Analog Comparator:**
   A high-gain differential amplifier. It compares the sampled voltage on the capacitor ($V_{\text{sample}}$) against the feedback voltage produced by the internal DAC ($V_{\text{DAC}}$).
   * If $V_{\text{sample}} > V_{\text{DAC}}$, the comparator outputs a digital `1`.
   * If $V_{\text{sample}} < V_{\text{DAC}}$, the comparator outputs a digital `0`.
3. **Successive Approximation Register (SAR Logic):**
   A digital state machine clocked by the peripheral bus clock ($ADCCLK$). It controls the binary search sequence, setting and clearing individual bits in sequence from Most Significant Bit (MSB) to Least Significant Bit (LSB).
4. **Internal Precision Digital-to-Analog Converter (Internal DAC):**
   Generates precision reference test voltages ($V_{\text{REF}}/2, V_{\text{REF}}/4, \dots$) inside the silicon die for the comparator to check against.

---

### Step-by-Step 4-Bit SAR Conversion Walkthrough

Let $V_{\text{REF}} = 3.2\text{ V}$. An unknown input voltage $V_{\text{in}} = 2.15\text{ V}$ is held on the sampling capacitor.

```
                  SAR BINARY SEARCH CONVERSION PROGRESSION
====================================================================================================
 Clock Cycle | Bit Tested | Binary Guess | DAC Voltage Produced | Comparator Decision | Action Taken
 ------------+------------+--------------+----------------------+---------------------+-------------
  Clock 1    | Bit 3 (MSB)| `0b1000`     | 1.60 V (V_REF / 2)   | 2.15V > 1.60V (HIGH)| KEEP bit 3 = 1
  Clock 2    | Bit 2      | `0b1100`     | 2.40 V (1.6V + 0.8V) | 2.15V < 2.40V (LOW) | CLEAR bit 2 = 0
  Clock 3    | Bit 1      | `0b1010`     | 2.00 V (1.6V + 0.4V) | 2.15V > 2.00V (HIGH)| KEEP bit 1 = 1
  Clock 4    | Bit 0 (LSB)| `0b1011`     | 2.20 V (2.0V + 0.2V) | 2.15V < 2.20V (LOW) | CLEAR bit 0 = 0
====================================================================================================
 FINAL RESULT: `0b1010` (Decimal 10). Reconstructed Voltage = 10 * 0.2V = 2.00V (Within 1 LSB).
 Total Conversion Time = Exactly 4 Clock Cycles!
```

* **Deterministic Timing:** An $N$-bit SAR ADC **always requires exactly $N$ clock cycles** for the approximation phase, regardless of whether the input voltage is $0.01\text{ V}$ or $3.29\text{ V}$. 
* Total ADC time is given by:
  $$T_{\text{conv}} = T_{\text{sample}} + N \cdot T_{\text{ADCCLK}}$$

---

### Comparative Evaluation: SAR vs Flash vs Delta-Sigma ADC

<div class="table-wrap">

| Characteristic | Successive Approximation (SAR) | Flash (Parallel Direct) | Sigma-Delta ($\Sigma\Delta$ Over-sampling) |
| :--- | :--- | :--- | :--- |
| **Conversion Principle** | Iterative binary search using internal DAC | Massive parallel bank of $2^N - 1$ comparators | High-frequency 1-bit modulation + digital filter |
| **Conversion Speed** | Moderate to Fast ($1\text{ MSPS} - 10\text{ MSPS}$) | **Ultra-Fast** ($1\text{ GSPS} - 10\text{ GSPS}$) | Slow to Moderate ($10\text{ kSPS} - 500\text{ kSPS}$) |
| **Resolution** | Medium to High ($10 - 16\text{ bits}$) | Low ($6 - 8\text{ bits}$, rarely 10) | **Ultra-High** ($16 - 24\text{ bits}$) |
| **Silicon Complexity** | Low ($1$ comparator, $1$ DAC, control logic) | **Extreme** ($4095$ comparators for 12 bits!)| Moderate (Analog integrator + DSP decimation filter) |
| **Power Consumption** | Very Low (microwatts to low milliwatts) | Very High (watts of thermal dissipation) | Low to Medium |
| **Cost** | Low (inexpensive on-chip integration) | Prohibitive for general MCU integration | Moderate |
| **Typical Target Use** | **General MCU sensors, motor control, audio** | Oscilloscopes, radar, software-defined radio | Weigh scales, seismic sensors, medical ECG |

</div>

::: callout-exam KTU Question: Working Principle of SAR ADC [KTU PBCST504 - 5 Marks]
**Model Exam Answer Breakdown:**
1. **Block Diagram:** Draw the Sample & Hold stage, Analog Comparator, SAR Logic, Internal DAC, and Data Register.
2. **Operational Principle:** State that SAR executes a **Binary Search algorithm**. In the first clock cycle, the MSB is set to `1` (producing $V_{\text{REF}}/2$). The comparator compares this against the held analog voltage. If $V_{\text{in}} > V_{\text{DAC}}$, the MSB remains `1`; otherwise, it is reset to `0`. This process repeats sequentially down to the LSB.
3. **Conversion Speed:** An $N$-bit conversion requires exactly $N$ conversion clock cycles.
:::

---

<a id="foundations"></a>
## 3. Sensor Signal Conditioning & Real-World Interfacing

Microcontroller ADC pins cannot be directly wired to raw physical sensors without analyzing the electrical characteristics of the interface. Input voltages must be scaled, buffered, and impedance-matched.

```
                   4 ESSENTIAL ANALOG SENSOR INTERFACES
====================================================================================================
 1. POTENTIOMETER (Ratiometric)                2. LM35 PRECISION TEMPERATURE SENSOR
 
        +3.3V                                            +5V / +3.3V
          |                                                |
        +---+                                         +----------+
        |   | 10 kOhm                                 |   LM35   |
        |   |<----+---------> [ PA0 (ADC) ]           |  Linear  |---------> [ PA0 (ADC) ]
        |   |     |                                   |  Sensor  |            (10 mV / deg C)
        +---+     |                                   +----------+
          |      === C_decouple                            |
         GND     === (100 nF)                             GND
                  |
                 GND
----------------------------------------------------------------------------------------------------
 3. LIGHT DEPENDENT RESISTOR (LDR)             4. ELECTRET MICROPHONE WITH OP-AMP
 
        +3.3V                                            +3.3V
          |                                                |
         [R] LDR (Photoresistor)                          [R1] 2.2k (DC Bias)
         [ ] (1k Light - 1M Dark)                          |
          |                                                +----||----+ (C1 = 100nF AC Coupling)
          +-----------------> [ PA0 (ADC) ]                |          |
          |                                              [MIC]        |      +3.3V
         [R] Fixed Resistor                              Capsule      |        |
         [ ] (10 kOhm)                                     |          v      +---+
          |                                               GND        [R3] 10k|   | [R4] 100k
         GND                                                          |      +---+ (Gain = 10)
                                                        V_REF/2 ------+----+   |   |
                                                        (1.65V)       |    |   v   |
                                                                     [R2]  +-|\  |
                                                                     10k   |  \--+--> [PA0]
                                                                           |+ /
                                                                       +---|/
                                                                       |
                                                                      GND
====================================================================================================
```

### 1. The Potentiometer (Ratiometric Voltage Divider)
* A three-terminal mechanical resistor acts as an adjustable voltage divider:
  $$V_{\text{ADC}} = V_{\text{DD}} \times \left(\frac{R_{\text{bottom}}}{R_{\text{total}}}\right)$$
* **Why Ratiometric Interfaces Are Immune to Power Supply Fluctuations:**
  Because the potentiometer and the ADC's internal reference use the same voltage rail ($V_{\text{DD}} = V_{\text{REF}}$), any drift in the supply voltage cancels out mathematically in the ADC conversion:
  $$D_{\text{raw}} = \frac{V_{\text{ADC}}}{V_{\text{REF}}} \times 4095 = \frac{V_{\text{DD}} \cdot \frac{R_2}{R_{\text{total}}}}{V_{\text{DD}}} \times 4095 = \left(\frac{R_2}{R_{\text{total}}}\right) \times 4095$$
  The digital reading is proportional purely to mechanical shaft position, independent of power supply stability!

### 2. LM35 / TMP36 Linear Temperature Sensors
* The **LM35** outputs an analog voltage directly proportional to Celsius temperature with a precision scale factor of **$10.0\text{ mV} / ^\circ\text{C}$**:
  $$V_{\text{out}} = 10\text{ mV} \times T \quad \implies \quad T(^\circ\text{C}) = \frac{V_{\text{out}}}{0.010\text{ V}} = V_{\text{out}} \times 100$$
* If an STM32 12-bit ADC reads $V_{\text{out}} = 0.250\text{ V}$ ($250\text{ mV}$), the temperature is:
  $$T = 0.250\text{ V} \times 100 = 25.0^\circ\text{C}$$
* *(Note: The TMP36 introduces an intentional $+500\text{ mV}$ offset to measure negative temperatures down to $-40^\circ\text{C}$: $T = (V_{\text{out}} - 0.50\text{ V}) \times 100$.)*

### 3. Light Dependent Resistor (LDR) in a Divider Network
* An LDR (Cadmium-Sulfide photoresistor) exhibits variable bulk resistance:
  * In pitch darkness: $R_{\text{LDR}} \approx 1\text{ M}\Omega$ ($1,000,000\ \Omega$).
  * Under bright sunlight: $R_{\text{LDR}} \approx 1\text{ k}\Omega$ ($1,000\ \Omega$).
* Placing the LDR on the high side with a fixed $10\text{ k}\Omega$ reference resistor pulls $V_{\text{ADC}}$ close to $0\text{ V}$ in total darkness, and sweeps toward $+3.3\text{ V}$ under bright illumination:
  $$V_{\text{ADC}} = 3.3\text{ V} \times \left(\frac{10\text{ k}\Omega}{R_{\text{LDR}} + 10\text{ k}\Omega}\right)$$

### 4. Electret Microphone (AC-Coupled Audio Interfacing)
An electret microphone capsule produces tiny AC electrical signals of only **$2\text{ mV}$ to $20\text{ mV}$ peak-to-peak**, centered around $0\text{ V}$. Connecting this directly to an STM32 ADC creates two major problems:
1. **The Substrate Diode Destruction Hazard:** Microcontroller pins cannot measure negative voltages. Negative AC excursions drop below $V_{\text{SS}} - 0.3\text{ V}$, forward-biasing the ESD clamping diodes and corrupting conversion results.
2. **Inadequate Signal Amplitude:** A $10\text{ mV}$ signal spans only $\approx 12$ counts out of 4096 on a 12-bit ADC, resulting in poor signal-to-noise ratio.
* **The Solution:** 
  1. Use a **$2.2\text{ k}\Omega$ pull-up resistor** to provide internal FET bias current.
  2. Use a **$100\text{ nF}$ DC-blocking capacitor** to strip away the microphone's DC bias.
  3. Use an active operational amplifier (Op-Amp) configured for non-inverting gain ($A_v = 1 + \frac{R_f}{R_{\text{in}}} \approx 10 - 50$).
  4. Bias the non-inverting terminal to **mid-rail reference ($\frac{V_{\text{DD}}}{2} \approx 1.65\text{ V}$)** using a dual-resistor voltage divider. Audio waveforms now oscillate symmetrically between $0.65\text{ V}$ and $2.65\text{ V}$, centered cleanly at $1.65\text{ V}$!

::: callout-pitfall The High Source Impedance Trap ($R_{\text{SRC}} > 10\text{ k}\Omega$)
The internal sample-and-hold capacitor ($C_{\text{hold}} \approx 8\text{ pF}$) inside the STM32 ADC must charge through the output impedance of your external sensor ($R_{\text{sensor}}$).

If you connect a high-impedance source (e.g., a $100\text{ k}\Omega$ thermistor divider) without an op-amp buffer, the capacitor will not fully charge to the true signal voltage during the brief sampling window ($T_{\text{sample}} \approx 1\ \mu\text{s}$), causing the ADC reading to read systematically lower than the actual voltage. 

**Rule of thumb:** If the source impedance exceeds $10\text{ k}\Omega$, you must increase the ADC sampling clock cycles (e.g., set sampling time to `ADC_SAMPLETIME_640CYCLES_5`) or insert a unity-gain Op-Amp buffer follower!
:::

---

### Production-Ready STM32 HAL C Implementation

```c
#include "main.h"

ADC_HandleTypeDef hadc1;

// 1. POLLING MODE (Simple, Blocking Execution)
uint32_t Read_ADC_Polling(void) {
    uint32_t raw_value = 0;

    // Start ADC conversion on the configured channel
    HAL_ADC_Start(&hadc1);

    // Wait until conversion completes (timeout after 10 ms)
    if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {
        // Read raw 12-bit integer (0 to 4095) from Data Register
        raw_value = HAL_ADC_GetValue(&hadc1);
    }

    HAL_ADC_Stop(&hadc1);
    return raw_value;
}

// 2. INTERRUPT-DRIVEN MODE (Non-Blocking)
void Start_ADC_Interrupt_Read(void) {
    // Non-blocking trigger: processor executes other code while SAR runs!
    HAL_ADC_Start_IT(&hadc1);
}

// Hardware calls this callback automatically when conversion completes
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc) {
    if (hadc->Instance == ADC1) {
        uint32_t raw = HAL_ADC_GetValue(hadc);
        
        // Convert to voltage (using millivolts to avoid floating point overhead)
        uint32_t voltage_mv = (raw * 3300) / 4095;
        
        // Calculate LM35 temperature: 10 mV per degree Celsius
        uint32_t temp_celsius = voltage_mv / 10;
        (void)temp_celsius;
    }
}
```

---

<a id="history"></a>
## 4. Digital-to-Analog Conversion (DAC) & Waveform Synthesis

A **Digital-to-Analog Converter (DAC)** performs the exact reverse of an ADC: it accepts a discrete $N$-bit binary value from the processor and generates a proportional, continuous output voltage.

```
+-----------------------------------------------------------------------------+
| APPLICATIONS OF EMBEDDED DAC PERIPHERALS:                                   |
|  - Synthetic Audio Synthesis (WAV sound effects, speech prompts)            |
|  - Precision Analog Voltage Control (programmable DC power supply outputs)  |
|  - Function Generators (Sine, Triangle, Sawtooth test signals)              |
|  - Proportional Valve & Variable Frequency Drive (VFD) speed referencing    |
+-----------------------------------------------------------------------------+
```

---

### DAC Architectures: Binary Weighted vs R-2R Ladder

#### The Failure of the Binary-Weighted Resistor DAC on Silicon
A basic DAC sums currents through resistors scaled in binary powers ($R, 2R, 4R, 8R, 16R, \dots, 2^{N-1}R$).

```
                BINARY WEIGHTED RESISTOR DAC (Flawed for Silicon)
====================================================================================================
  Bit 3 (MSB) ---[  R  ]---+
  Bit 2       ---[ 2R  ]---|
  Bit 1       ---[ 4R  ]---+--------(-) \  Op-Amp
  Bit 0 (LSB) ---[ 8R  ]---+            |------> V_OUT
                           |        (+)-/
                          GND        |
                                    GND
====================================================================================================
```
* **Why this fails in integrated circuits:** For a 12-bit DAC, the ratio between the smallest and largest resistor is:
  $$\frac{R_{\text{LSB}}}{R_{\text{MSB}}} = 2^{12-1} = 2^{11} = 2048$$
  Fabricating resistors spanning three orders of magnitude ($1\text{ k}\Omega$ to $2.048\text{ M}\Omega$) on silicon with matched temperature coefficients is practically impossible. Thermal drift and manufacturing variations ruin the linearity of the converter.

---

### The R-2R Resistor Ladder Architecture

The **R-2R Ladder** circumvents this manufacturing bottleneck by utilizing **only two resistor values**: $R$ and $2R$ (typically $10\text{ k}\Omega$ and $20\text{ k}\Omega$).

```
                         4-BIT R-2R RESISTOR LADDER DAC SCHEMATIC
====================================================================================================
                          R             R             R
                 +------[###]----+----[###]----+----[###]----+
                 |               |             |             |
                [ ] 2R          [ ] 2R        [ ] 2R        [ ] 2R          +3.3V
                [#]             [#]           [#]           [#]               |
                 |               |             |             |            +-------+
                 |               |             |             +------------|- \    |
                [ ] 2R           |             |                          |   |---+---> V_ANALOG
                [#] (Term)       |             |                    +-----|+ /|   |  OUT
                 |               |             |                    |     +---+   |
                GND              |             |                    |         |
                                 |             |                   GND       GND
                 |               |             |             |
                 o/              o/            o/            o/  (CMOS Digital Switches)
                /               /             /             /
               GND             GND           GND           GND
               (or VREF)       (or VREF)     (or VREF)     (or VREF)
              
              BIT 0 (LSB)     BIT 1         BIT 2         BIT 3 (MSB)
====================================================================================================
```

* **How it Works (Thévenin Equivalence):** 
  Looking left from any node in the ladder, the equivalent resistance to ground is always exactly $R$. 
  At each node, incoming current splits evenly in half: $50\%$ flows left down the ladder, and $50\%$ flows toward the summing node. 
  This yields true binary current scaling ($I, \frac{I}{2}, \frac{I}{4}, \frac{I}{8}, \dots$) using only two precisely matchable resistor geometries on the silicon die!

---

### Generating a Stepped Sine Wave via Lookup Table

To synthesize an analog sine wave without consuming continuous CPU math cycles calculating floating-point trigonometry, we pre-compute a **Sine Lookup Table** stored in Flash ROM.

```
                  SINE WAVE LOOKUP TABLE DISCRETIZATION (M = 32 SAMPLES)
====================================================================================================
 Voltage
   ^
3.3V +                     *   *   *
     |                 *               *
     |              *                     *           STAIR-STEPPED DAC OUTPUT
1.65V+ - - - - - * - - - - - - - - - - - - - * - - -  (Discrete samples updated at interval t_s)
     |          *                             *
     |        *                                 *
 0V  +---+--*-------------------------------------*-------------------------------------------->
     |   |<-- t_s -->|                                |                                   Time (t)
     |   |           |                                |
     0   1   2   3 ...                               31  (Array Indices 0 to M-1)
====================================================================================================
```

#### The Mathematical Generation Formula
For a table of $M$ samples scaled to a 12-bit DAC ($0$ to $4095$ range) with reference $V_{\text{REF}}$:

$$D[n] = \text{round}\left( \frac{4095}{2} \cdot \left[ 1 + \sin\left(\frac{2\pi \cdot n}{M}\right) \right] \right) \quad \text{for } n = 0, 1, 2, \dots, M-1$$

* At $n = 0$: $\sin(0) = 0 \implies D[0] = 2047$ (Mid-scale: $1.65\text{ V}$).
* At $n = \frac{M}{4}$ ($90^\circ$): $\sin(\pi/2) = 1 \implies D[8] = 4095$ (Peak positive: $3.3\text{ V}$).
* At $n = \frac{3M}{4}$ ($270^\circ$): $\sin(3\pi/2) = -1 \implies D[24] = 0$ (Trough: $0.0\text{ V}$).

```c
// 32-point pre-computed 12-bit Sine Wave Lookup Table (Stored in Flash ROM)
const uint16_t Sine12Bit_LUT[32] = {
    2048, 2447, 2831, 3185, 3495, 3750, 3939, 4056,
    4095, 4056, 3939, 3750, 3495, 3185, 2831, 2447,
    2048, 1648, 1264,  910,  600,  345,  156,   39,
       0,   39,  156,  345,  600,  910, 1264, 1648
};
```

---

### Waveform Reconstruction: Smoothing the Staircase

The raw output of the DAC is a sequence of discrete voltage steps. This staircase contains the desired fundamental sine frequency ($f_0$) plus unwanted high-frequency switching harmonics centered around the update rate ($f_{\text{update}} = M \cdot f_0$).

```
                 ANALOG RECONSTRUCTION LOW-PASS FILTER (RC)
====================================================================================================
                Resistor (R)
  DAC OUT -------[######]--------+----------> CLEAN SMOOTH SINE WAVE
  (PA4)                          |
                                === Capacitor (C)
                                ===
                                 |
                                GND
====================================================================================================
```
* By inserting an analog **RC Low-Pass Filter** whose cutoff frequency $f_c = \frac{1}{2\pi RC}$ is placed just above the target fundamental frequency $f_0$, all high-frequency steps are smoothed out, leaving a pure analog sine wave!

---

### STM32 HAL C Implementation: DAC Sine Wave Synthesis

```c
#include "main.h"

DAC_HandleTypeDef hdac1;

void Synthesize_Sine_Wave(void) {
    // Start DAC Channel 1 (Pin PA4 on STM32)
    HAL_DAC_Start(&hdac1, DAC_CHANNEL_1);

    while (1) {
        // Sequentially stream the 32 samples out to the DAC
        for (uint8_t i = 0; i < 32; i++) {
            // Write 12-bit right-aligned value to DAC Channel 1
            HAL_DAC_SetValue(&hdac1, DAC_CHANNEL_1, DAC_ALIGN_12B_R, Sine12Bit_LUT[i]);
            
            // Delay controls the frequency of the generated wave:
            // T_period = 32 * 10 us = 320 us -> Frequency = 1 / 320 us ~ 3.125 kHz
            DWT_Delay_us(10); 
        }
    }
}
```

---

<a id="self-check"></a>
## 5. Interactive Self-Check Quiz

::: quiz 12-bit ADC Voltage Resolution
An STM32 microcontroller utilizes an internal 12-bit SAR ADC referenced to $V_{\text{REF}} = 3.30\text{ V}$. What is the smallest change in input voltage that this converter can distinguish (1 LSB), and what raw digital integer will be read if the pin voltage is precisely $1.65\text{ V}$?
( ) $0.403\text{ mV}$ and raw code $1024$
(*) $0.806\text{ mV}$ and raw code $2047$ (or $2048$)
( ) $3.220\text{ mV}$ and raw code $4095$
( ) $0.050\text{ mV}$ and raw code $512$
::: explanation
1. **Resolution:**
   $$\text{Resolution (1 LSB)} = \frac{V_{\text{REF}}}{2^N} = \frac{3.30\text{ V}}{4096} = 0.00080566\text{ V} \approx \mathbf{0.806\text{ mV}}$$
2. **Digital Code at $1.65\text{ V}$:**
   $$D_{\text{raw}} = \frac{V_{\text{in}}}{V_{\text{REF}}} \times (2^N - 1) = \frac{1.65\text{ V}}{3.30\text{ V}} \times 4095 = 0.5 \times 4095 \approx \mathbf{2047.5 \implies 2047 \text{ or } 2048}$$
   $1.65\text{ V}$ is exactly half-scale, mapping directly to mid-scale code $2047/2048$.
:::

::: quiz Successive Approximation Register Logic
During an analog-to-digital conversion cycle on an 8-bit SAR ADC with $V_{\text{REF}} = 2.56\text{ V}$, the unknown input voltage is $V_{\text{in}} = 1.50\text{ V}$. On the very first clock cycle, the SAR tests the MSB ($B_7$). What voltage does the internal DAC generate, what does the comparator output, and does the SAR keep or clear the MSB?
( ) DAC outputs $2.56\text{ V}$; Comparator outputs LOW; SAR clears $B_7$ to $0$.
(*) DAC outputs $1.28\text{ V}$; Comparator outputs HIGH; SAR keeps $B_7$ as $1$.
( ) DAC outputs $1.50\text{ V}$; Comparator outputs LOW; SAR clears $B_7$ to $0$.
( ) DAC outputs $0.64\text{ V}$; Comparator outputs HIGH; SAR keeps $B_7$ as $1$.
::: explanation
1. In the first clock cycle of a SAR conversion, the register sets the MSB ($B_7 = 1$) while keeping all lower bits zero (`0b10000000`).
2. The internal DAC generates half of full scale:
   $$V_{\text{DAC}} = \frac{V_{\text{REF}}}{2} = \frac{2.56\text{ V}}{2} = 1.28\text{ V}$$
3. The comparator checks if $V_{\text{in}} > V_{\text{DAC}}$. Here, $1.50\text{ V} > 1.28\text{ V}$, so the comparator outputs a **HIGH (Logic 1)**.
4. Because the comparator output is HIGH, the SAR logic **keeps $B_7$ as $1$** and proceeds to test bit $B_6$ on the next clock cycle.
:::

::: quiz Microphone Interfacing Hazards
Why is it unacceptable to connect an electret microphone capsule directly to an STM32 ADC input pin without an operational amplifier and a DC bias circuit?
( ) The electret microphone produces a $100\text{ V}$ inductive back-EMF spike that vaporizes the microcontroller.
( ) Microphones output digital I2S serial data that cannot be decoded by an analog pin.
(*) The microphone outputs an unamplified AC waveform that swings below $0\text{ V}$, which will forward-bias the microcontroller's internal ESD protection diodes and clip the negative cycle.
( ) Microphones require a $12\text{ V}$ differential RS-485 bus receiver to interface with microcontrollers.
::: explanation
A raw microphone produces small AC voltage fluctuations ($\pm 10\text{ mV}$) centered around $0\text{ V}$. Because microcontrollers operate strictly on unipolar positive supplies ($0\text{ V}$ to $3.3\text{ V}$), any voltage that swings below ground ($< -0.3\text{ V}$) forward-biases the internal silicon substrate ESD clamping diodes, causing severe signal distortion and potential latch-up damage. A DC bias network shifts the signal midpoint up to $V_{\text{REF}}/2$ ($1.65\text{ V}$), and an Op-Amp amplifies the millivolt-level signal to utilize the full dynamic range of the ADC.
:::
