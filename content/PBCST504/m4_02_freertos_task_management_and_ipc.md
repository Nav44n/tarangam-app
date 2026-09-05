# Real-Time Operating Systems (RTOS) and FreeRTOS on STM32

**RTOS Foundations, Task Control Blocks, Priority Preemptive Scheduling, Software Timers, Queues, Semaphores, and Mutex Priority Inheritance.**

<a id="the-intuition"></a>
## 1. General-Purpose OS vs Real-Time Operating System

::: callout-intuition Determinism vs Raw Throughput
<!-- Conceptual intuition syntax block: Hard real-time vs Soft real-time deadlines -->
:::

* **Hard Real-Time vs Soft Real-Time**:
  <!-- Guaranteed timing deadlines vs statistical average completion time -->
* **The FreeRTOS Microkernel**:
  <!-- Small memory footprint (< 10 KB), written in portable C, preemptive tick timer -->

---

<a id="the-dimensions"></a>
## 2. FreeRTOS Task Lifecycle & Priority Scheduling

<div class="table-wrap">

| Task State | Description | Transition Trigger |
| :--- | :--- | :--- |
| **Running** | Currently utilizing the CPU core | Scheduled by RTOS scheduler |
| **Ready** | Ready to run but waiting for higher-priority task | Unblocked or preempted |
| **Blocked** | Waiting for a temporal delay or IPC event (Queue/Semaphore) | Calling `vTaskDelay` or waiting on IPC |
| **Suspended** | Explicitly removed from scheduler consideration | `vTaskSuspend` / `vTaskResume` |

</div>

```c
// [FreeRTOS Task Creation & Delay Syntax Template]
void Task_BlinkLED(void *pvParameters) {
    for (;;) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        vTaskDelay(pdMS_TO_TICKS(500)); // Non-blocking context-switching delay
    }
}

void app_main(void) {
    xTaskCreate(Task_BlinkLED, "LED_Task", 128, NULL, 2, NULL);
    vTaskStartScheduler();
}
```

---

<a id="foundations"></a>
## 3. Inter-Process Communication (IPC): Queues & Semaphores

* **FreeRTOS Message Queues**:
  <!-- Thread-safe FIFO byte copying, blocking reads/writes with timeout ticks -->
* **Binary Semaphores vs Counting Semaphores**:
  <!-- Task-to-ISR synchronization vs resource pool tracking -->

```c
// [FreeRTOS Message Queue Syntax Template]
QueueHandle_t sensorQueue;

void SensorProducerTask(void *pvParameters) {
    uint32_t sensorData;
    for (;;) {
        sensorData = read_hardware_sensor();
        xQueueSend(sensorQueue, &sensorData, portMAX_DELAY);
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
```

---

<a id="history"></a>
## 4. Mutexes & The Priority Inversion Dilemma

::: callout-exam KTU High-Yield Focus: Priority Inheritance
<!-- KTU Exam Focus syntax block: Unbounded priority inversion, Mars Pathfinder rover bug, and automatic priority inheritance in FreeRTOS mutexes -->
:::

* **Binary Semaphore vs Mutex**:
  <!-- Mutex includes ownership and priority inheritance; binary semaphore is for synchronization -->
* **Priority Inheritance Protocol**:
  <!-- Temporarily elevating low-priority holder's priority to match highest blocked waiting task -->

---

<a id="self-check"></a>
## 5. Self-Check Interactive Quiz

::: quiz FreeRTOS Non-Blocking Delays
Why is `vTaskDelay()` strictly preferred over busy-wait loops like `HAL_Delay()` inside a FreeRTOS task?
(*) `vTaskDelay()` moves the task into the Blocked state, yielding CPU execution to lower or equal priority ready tasks.
( ) `vTaskDelay()` increases the CPU clock frequency to finish the delay faster.
( ) `HAL_Delay()` causes an immediate memory segmentation fault inside an RTOS.
( ) `vTaskDelay()` terminates the task and frees its stack memory completely.
::: explanation
`vTaskDelay()` places the calling task into the **Blocked state**, allowing the FreeRTOS scheduler to execute other tasks during the delay, eliminating wasteful CPU cycles.
:::
