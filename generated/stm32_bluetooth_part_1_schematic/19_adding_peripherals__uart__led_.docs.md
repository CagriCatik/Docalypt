# 19 – Adding Peripherals (UART & LED)

## 1. Overview  

This section documents the recommended approach for exposing **UART** and **status‑LED** peripherals on an S32WB55‑based board. It covers schematic‑level decisions (pin selection, net naming, protection components) and the rationale behind each choice, providing a solid foundation for subsequent PCB layout and firmware development.

---

## 2. Power‑Rail Annotation (VBUS Flag)

* **Why it matters** – Adding a **+5 V flag** on the USB VBUS net makes the nominal voltage explicit, helping ERC/DRC tools and downstream designers quickly identify the rail’s purpose.  
* **Implementation** – Place a *Power Flag* symbol (e.g., “+5 V”) directly on the VBUS line at the USB connector. This practice is **verified** in most design libraries and improves schematic readability.  

> **Best practice:** Keep the flag close to the source of the rail (the USB connector) and label any downstream rails (e.g., “+3.3 V”) with similar flags.

---

## 3. UART Peripheral Selection & Pin Assignment  

### 3.1 Choosing the UART Instance  

The S32WB55 offers several UART modules (U1, U2, …). For a simple debug or console interface, **UART 1 (U1)** is a convenient choice because its pins are located on the **PA2 (TX)** and **PA3 (RX)** pins, which are not heavily used by other functions in a typical low‑pin‑count design.  

### 3.2 Pin Placement Considerations  

| Criterion | Reasoning |
|-----------|-----------|
| **Avoid crowded regions** | Selecting PA2/PA3 keeps the UART away from pins already dedicated to other high‑speed interfaces (e.g., PV4/PV5). |
| **Routing simplicity** | These pins lie on the same side of the MCU, reducing the number of vias and trace length for the UART connector. |
| **Future expandability** | Leaving other PA/PB pins free enables later addition of I²C, SPI, or additional UARTs without a major redesign. |

> **Inference:** Choosing pins with minimal neighboring connections reduces routing congestion and improves signal integrity.

### 3.3 Net Naming  

* **TXC** – UART‑1 transmit line (MCU → external device)  
* **RXC** – UART‑1 receive line (external device → MCU)  

Consistent, descriptive net names simplify schematic navigation and later netlist verification.

---

## 4. Connector Design for UART  

### 4.1 Generic 1×4 Header  

A **1 × 4 pin header** is used as a placeholder for the UART connector. The exact part (e.g., 2.54 mm pitch, right‑angle or straight) can be selected during the layout phase when the mechanical envelope is known.  

### 4.2 Protection & Current Limiting  

| Component | Purpose | Typical Value |
|-----------|---------|---------------|
| **Series resistor** (each line) | Limits in‑rush current, provides basic ESD protection, and helps match impedance for low‑speed UART signals. | 100 Ω (adjusted to 220 Ω after LED‑resistor sizing, see §5) |
| **ESD diode (optional)** | Clamps high‑voltage transients that could damage the MCU I/O. | TVS diode rated for 5 V rail |
| **Decoupling capacitor** (optional) | Stabilises the 3.3 V rail at the connector, reducing noise injection into the UART lines. | 0.1 µF close to the connector pins |

> **Speculation:** Adding a TVS diode is recommended for environments with frequent plug‑in/out events, though it was omitted in the demonstration for brevity.

### 4.3 Wiring Example  

```
U1_TX (PA2) ──[220 Ω]───> UART_TX (pin 1 of header)
U1_RX (PA3) ──[220 Ω]───> UART_RX (pin 2 of header)
3.3 V       ─────────────> VCC (pin 3)
GND         ─────────────> GND (pin 4)
```

All nets should be **labelled** (TXC, RXC, VCC, GND) to propagate through the design hierarchy.

---

## 5. LED Integration Using a Timer PWM Channel  

### 5.1 Selecting a PWM‑Capable Pin  

The S32WB55 provides multiple timer channels. **PA7** is mapped to **Timer 17 Channel 1**, which supports PWM output. Verifying PWM capability at the schematic stage prevents later firmware‑layout mismatches.  

### 5.2 LED Drive Considerations  

| Parameter | Typical Range | Design Implication |
|-----------|---------------|--------------------|
| **Forward voltage (Vf)** | 1.8 V – 3.3 V (depends on colour) | Determines series‑resistor value. |
| **Desired current (If)** | 1 mA – 10 mA (1 mA–2 mA for low‑brightness) | Sets resistor to limit current appropriately. |
| **MCU I/O drive capability** | ≤ 4 mA per pin (check datasheet) | Ensure LED current does not exceed pin rating. |

### 5.3 Calculating the Series Resistor  

Assuming **full‑duty PWM (100 %)**, a 3.3 V supply, and an LED forward voltage of 2.0 V with a target current of 2 mA:

\[
R = \frac{V_{CC} - V_f}{I_f} = \frac{3.3\text{ V} - 2.0\text{ V}}{2\text{ mA}} \approx 650\ \Omega
\]

In the demonstration, the existing **100 Ω** resistors were bulk‑edited to **220 Ω** to provide a compromise between brightness and MCU current limits. This value is **acceptable** for a modestly bright LED while staying safely under the pin’s current rating.  

> **Inference:** Using the same resistor value for both UART lines and the LED simplifies BOM management, though the LED resistor may be oversized for optimal brightness.

### 5.4 Schematic Connection  

```
PA7 (Timer17_CH1) ──[220 Ω]───> LED Anode (LED_A)
LED Cathode (LED_K) ────────> GND
```

Label the nets as **LED_A** and **LED_K** (or **LED_R**, **LED_G**, etc., depending on colour).

---

## 6. Design‑Level Checks & Best Practices  

1. **ERC/DRC Validation** – Run Electrical Rule Check after adding power flags, series resistors, and net labels to catch unconnected pins or mismatched net names.  
2. **Pin‑Current Verification** – Cross‑reference each I/O pin’s absolute maximum source/sink current in the MCU datasheet; ensure the LED resistor limits current accordingly.  
3. **ESD Protection** – For production boards, add TVS diodes on all external I/O (UART, LED, etc.) to improve robustness.  
4. **Decoupling Strategy** – Place a 0.1 µF capacitor as close as possible to each connector’s VCC pin; this mitigates voltage droop when the UART transmits bursts of data.  
5. **Naming Consistency** – Adopt a clear convention (e.g., `*_TX`, `*_RX`, `*_A`, `*_K`) and apply it uniformly across schematic sheets and PCB layout.  
6. **Future Expandability** – Keep alternate PA/PB pins free in the schematic to allow later addition of I²C, SPI, or extra UART channels without redesigning the board outline.  

---

## 7. High‑Level Peripheral Assignment Flow  

```mermaid
flowchart TD
    A[Define Required Peripherals] --> B[Select MCU Pins]
    B --> C{Check Pin Capabilities}
    C -->|PWM Available| D[Assign LED to Timer PWM Pin]
    C -->|UART Available| E[Assign UART TX/RX Pins]
    D --> F[Add Current‑Limiting Resistor]
    E --> G[Add Series Resistor & Optional TVS]
    F --> H[Label Nets (LED_A, LED_K)]
    G --> H
    H --> I[Add Power Flag & Decoupling]
    I --> J[Run ERC/DRC & Verify]
```

*The flowchart illustrates the decision sequence from functional requirements to final schematic validation.*

---

## 8. Summary  

By explicitly flagging power rails, carefully selecting UART and PWM‑capable pins, and protecting external interfaces with series resistors (and optionally TVS diodes), the design achieves:

* **Clear documentation** for downstream engineers and manufacturers.  
* **Robustness** against ESD and over‑current conditions.  
* **Flexibility** for future peripheral expansion.  

Following the guidelines above will streamline both schematic capture and PCB layout, reducing the risk of re‑work and improving overall product reliability.