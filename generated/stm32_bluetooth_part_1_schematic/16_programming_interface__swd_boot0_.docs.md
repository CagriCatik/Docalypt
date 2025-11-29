# Programming Interface (SWD / BOOT0)

## 1. Overview  

Modern STM32‑based designs are typically programmed and debugged through **Serial Wire Debug (SWD)**.  
The same MCU family also provides a **bootloader** that can be activated via the **BOOT0** pin, allowing firmware updates over USB, UART, I²C or SPI.  
Choosing the right combination of pins, connectors, and supporting circuitry is essential for a reliable development platform and for production‑grade units that may need field upgrades.

---

## 2. Required MCU Pins  

| Function | MCU Pin | Typical Role | Remarks |
|----------|---------|--------------|---------|
| **SWDIO** | PA13 | Serial‑wire data line | Minimum‑size differential pair not required; keep trace short and away from noisy nets. |
| **SWCLK** | PA14 | Serial‑wire clock line | Same routing considerations as SWDIO. |
| **nRESET** | NRST (active‑low) | Global reset input | Internally pulled‑up (~40 kΩ) but an external RC network is recommended for deterministic reset behavior. |
| **SWO (Trace)** | PB3 | Optional asynchronous trace output | Useful for real‑time variable monitoring; add only if board space permits. |
| **BOOT0** | PH3 | Boot‑mode selector | Must be **pull‑down** for normal run mode; a **push‑button** or switch can pull it high to invoke the system bootloader. |

> The MCU also allows BOOT0 to be repurposed after reset (e.g., as a GPIO or analog input). This flexibility can be leveraged for user‑interface functions once the bootloader has finished sampling the pin. [Verified]

---

## 3. Connector Strategy  

### 3.1 Tag‑Connect TC2030  

* **Advantages**  
  * No through‑hole header required – only two plated‑through holes for the pogo‑pin pads.  
  * Low cost and minimal board real‑estate.  
  * Compatible with ST‑Link, J‑Link, and other SWD probes via a simple adapter.  

* **Implementation**  
  * Place the TC2030 footprint on the outer layer.  
  * Route PA13, PA14, PB3 (if used), and NRST to the corresponding pads.  
  * Add VCC (3.3 V) and GND pads for reference and optional ESD protection.  

> The TC2030 is a through‑hole component that does **not** appear on the BOM because it consists only of copper pads; the mechanical retainer is supplied with the connector kit. [Inference]

### 3.2 Alternative Header Solutions  

* 2×5 or 2×3 0.1 in pitch headers are common for low‑cost prototypes.  
* Trade‑off: extra board area, higher assembly cost, and potential for mis‑alignment during debugging.  

---

## 4. Schematic Implementation  

### 4.1 nRESET Network  

* **Internal pull‑up** (~40 kΩ) eliminates the need for an external resistor.  
* Recommended external **100 nF** decoupling capacitor from NRST to GND to filter bounce and provide a clean reset edge.  
* No external pull‑up is required; the capacitor alone is sufficient for most designs.  

> This follows the MCU datasheet recommendation (section 6.3.8) and is a proven practice for STM32 devices. [Verified]

### 4.2 BOOT0 Pull‑Down and User Button  

1. **Pull‑down resistor** (R₁) – 10 kΩ to 100 kΩ is typical; a 10 kΩ value provides a solid low level without excessive current when the button is pressed.  
2. **Push‑button** (SW₁) – connects PH3 to 3.3 V when pressed, overriding the pull‑down.  
3. **Debounce RC** – a 100 nF capacitor (C₁) in parallel with R₁ forms a simple low‑pass filter, reducing spurious transitions during manual actuation.  

```
PH3 ----+---- R₁ (10 kΩ) ---- GND
        |
        +---- SW₁ ---- 3.3 V
        |
        +---- C₁ (100 nF) ---- GND
```

> The RC values are not critical; any combination that yields a time constant of a few milliseconds works for a human‑operated button. [Inference]

### 4.3 Power & Ground Routing  

* Connect VCC (3.3 V) and GND pins of the TC2030 directly to the board’s power rails with **wide copper pours** to minimise voltage drop.  
* Place a **0.1 µF** decoupling capacitor close to each MCU VDD pin (including the VDDIO pins used by SWD) to satisfy high‑frequency current demand.  

### 4.4 ESD Protection  

* For development boards, the native robustness of the STM32 SWD pins often suffices.  
* For production units, consider **TVS diodes** or **ESD protection arrays** on the SWDIO, SWCLK, and nRESET lines, especially if the connector is exposed to user handling.  

> Adding protection is a best‑practice for commercial products but may be omitted on simple test rigs to save cost and board space. [Inference]

---

## 5. PCB Layout Recommendations  

| Aspect | Recommendation |
|--------|----------------|
| **Trace Length** | Keep SWDIO and SWCLK traces **≤ 30 mm** and avoid 90° bends; use 45° or curved routing to reduce impedance discontinuities. |
| **Impedance Control** | Not required for SWD (≤ 10 MHz), but maintain a consistent trace width (e.g., 0.25 mm) and keep them on the same layer to avoid unnecessary vias. |
| **SWO (PB3)** | If used, route as a **single‑ended** line with a controlled impedance of 50 Ω if the external debugger expects it; otherwise treat as a regular GPIO. |
| **Via Placement** | Use **through‑hole vias** for the TC2030 pads; keep the via pad annular ring ≥ 0.2 mm to ensure reliable pogo‑pin contact. |
| **Ground Plane** | Provide a solid ground plane under the SWD traces to reduce EMI and improve signal integrity. |
| **Clearance** | Maintain at least **0.5 mm** clearance between the SWD pads and high‑current traces to avoid cross‑talk. |
| **Silkscreen** | Clearly label the SWD pins and the BOOT0 button on the silkscreen to aid assembly and debugging. |

> These guidelines balance manufacturability, cost, and signal integrity for typical 2‑layer hobbyist or low‑volume boards. [Inference]

---

## 6. Manufacturing & Assembly Considerations  

* **Component Placement** – Position the TC2030 pads near the board edge to simplify probe access; keep the BOOT0 button away from high‑temperature components to avoid solder‑mask delamination.  
* **DFM** – Verify that the through‑hole pads for the pogo‑pin connector meet the PCB fab house’s minimum drill size and annular ring specifications.  
* **Testing** – Include a **test point** on NRST and SWDIO for in‑circuit testing (ICT) if the production flow requires it.  

---

## 7. Decision Flow for Programming Interface  

```mermaid
flowchart TD
    A[Start: Define Programming Needs] --> B{Require High‑Speed Trace?}
    B -- Yes --> C[Add SWO (PB3) & Route Trace]
    B -- No --> D[Omit SWO]
    C --> E[Select Tag‑Connect TC2030]
    D --> E
    E --> F{Need External Bootloader?}
    F -- Yes --> G[Add BOOT0 Pull‑Down + Push‑Button]
    F -- No --> H[Pull‑Down BOOT0 only]
    G --> I[Add Debounce RC]
    H --> I
    I --> J[Add nRESET RC Network]
    J --> K[Finalize Layout & DFM Review]
    K --> L[Proceed to Fabrication]
```

*The flowchart captures the typical decision points when configuring a board for SWD debugging and optional bootloader access.*  

---

## 8. Summary of Best Practices  

1. **Expose SWD pins** (PA13, PA14) on every prototype; they are the most reliable programming method.  
2. **Prefer Tag‑Connect** for low‑cost, space‑efficient debugging; ensure proper pad geometry.  
3. **Implement a robust nRESET network** with a decoupling capacitor; rely on the internal pull‑up.  
4. **Provide a configurable BOOT0** (pull‑down + push‑button) to enable the internal bootloader when needed.  
5. **Add simple RC debounce** to the BOOT0 button to avoid accidental mode changes.  
6. **Consider optional SWO** only if trace data is required; otherwise omit to save pins and routing effort.  
7. **Apply ESD protection** on exposed debug pins for production units.  
8. **Maintain clear silkscreen labeling** and adequate clearances for reliable assembly and service.

By following these guidelines, designers can create a PCB that is easy to program, debug, and update throughout both development and production lifecycles.