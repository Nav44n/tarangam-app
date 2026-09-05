# ARM TrustZone Security Architecture and Code Optimization

**ARM TrustZone for Armv8-M, Secure vs Non-Secure Execution Worlds, SAU/IDAU Partitioning, Non-Intrusive Hardware Debugging, and Code/Memory Optimization.**

<a id="the-intuition"></a>
## 1. ARM TrustZone for Armv8-M Microcontrollers

::: callout-intuition Hardware-Enforced Security Domain Partitioning
<!-- Conceptual intuition syntax block: System-on-Chip divided into Secure World and Non-Secure World at hardware level -->
:::

* **TrustZone Threat Model**:
  <!-- Protecting cryptographic keys, secure boot, and firmware integrity from vulnerable third-party application code -->
* **Secure World vs Non-Secure World**:
  <!-- Orthogonal to privileged/unprivileged execution; 4 distinct execution states -->

---

<a id="the-dimensions"></a>
## 2. Security Attribution: SAU, IDAU, and Secure Gateways

<div class="table-wrap">

| Component | Full Name | Security Enforcement Function |
| :--- | :--- | :--- |
| **SAU** | Security Attribution Unit | <!-- Programmable internal register bank defining memory security state --> |
| **IDAU** | Implementation Defined Attribution Unit | <!-- Fixed SoC hardware memory security mapping --> |
| **NSC** | Non-Secure Callable Region | <!-- Memory region holding SG (Secure Gateway) landing-pad instructions --> |

</div>

::: callout-exam KTU High-Yield Focus: Secure Gateway (SG) Instruction
<!-- KTU Exam Focus syntax block: How Non-Secure code transitions into Secure functions safely via NSC and SG veneer branches -->
:::

```c
// [ARM TrustZone Non-Secure Callable (NSC) Veneer Syntax Template]
/* In Secure World firmware: */
__attribute__((cmse_nonsecure_entry))
uint32_t Secure_CalculateHash(const uint8_t *data, uint32_t len) {
    // Cryptographic hashing execution inside Secure World
    return 0;
}
```

---

<a id="foundations"></a>
## 3. Embedded Software Optimization Techniques

* **Compiler Optimization Flags**:
  <!-- -O0 (Debug), -O2 (Speed), -Os / -Oz (Code Size) -->
* **Memory Footprint Reduction**:
  <!-- Aligning data structures to avoid padding, placing constant lookup tables in Flash (`const`) -->
* **Loop Unrolling & Register Allocation**:
  <!-- Eliminating branch overhead and taking advantage of 32-bit barrel shifter -->

---

<a id="history"></a>
## 4. Hardware Debugging & Trace Interfaces

* **JTAG vs Serial Wire Debug (SWD)**:
  <!-- 4-5 pin JTAG vs 2-pin SWD (SWDIO, SWCLK) pin efficiency -->
* **CoreSight Debug Peripherals**:
  <!-- Instrumentation Trace Macrocell (ITM), Embedded Trace Macrocell (ETM), Serial Wire Output (SWO) -->

---

<a id="self-check"></a>
## 5. Self-Check Interactive Quiz

::: quiz TrustZone Secure Gateway Instruction
What is the purpose of the **Secure Gateway (`SG`)** instruction located in the Non-Secure Callable (NSC) memory region in Armv8-M architecture?
(*) It validates that branches from the Non-Secure world enter only through authorized entry points, preventing arbitrary jumps into secure memory.
( ) It decrypts Flash memory on-the-fly during boot.
( ) It increases the clock frequency when entering secure functions.
( ) It resets the processor if a stack overflow occurs.
::: explanation
The `SG` instruction serves as an **authorized entry gate**: the hardware CPU core permits entry into Secure state from Non-Secure memory only if the branch lands directly on an `SG` instruction within an NSC region.
:::
