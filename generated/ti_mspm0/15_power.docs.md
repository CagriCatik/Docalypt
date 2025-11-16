# 15 – Power Supply Design  

## 1. Overview  

A robust power‑distribution network is essential for reliable operation of a mixed‑signal board that is powered from a USB‑Type‑C VBUS line (nominal 5 V, allowable range 4.5 V – 5.5 V). The schematic is organized as a simple cascade:

```
VBUS → Pi‑filter → Low‑Drop‑Out (LDO) regulator → 3.3 V rail → MCU
```

The design deliberately includes a **placeholder Pi‑filter** and a **fixed‑output LDO** (SPX3819) to provide noise attenuation and voltage regulation while keeping the bill of materials (BOM) minimal.  

---

## 2. Power‑Net Naming Conventions  

- **Net flags** are used to label power domains directly on the schematic (e.g., `VBUS`, `+3V3`).  
- A leading “+” is prefixed to all **positive‑voltage nets** (`+5V`, `+3V3`). This groups them together when the net list is sorted, simplifying verification and documentation. `[Verified]`  
- Global ports are avoided unless the net must cross many hierarchical sheets; instead, **net labels** are placed on wires to keep the schematic tidy and to reduce zig‑zag routing. `[Verified]`  

---

## 3. Pi‑Filter Implementation  

### 3.1 Topology  

A classic Pi‑filter consists of **C‑R‑C** (capacitor – resistor – capacitor). In the schematic the series element is a **zero‑ohm resistor** (placeholder) that can later be replaced with a precise value if required.  

### 3.2 Bidirectional Filtering  

The filter attenuates high‑frequency noise **both** from the external VBUS source **and** from internal board noise that may be injected back onto the VBUS line. The low‑pass corner frequency is given by  

\[
f_c = \frac{1}{2\pi R C}
\]

where `R` is the series resistance and `C` the filter capacitance. Using a placeholder resistor (0 Ω) yields a very high corner frequency, effectively acting as a **decoupling capacitor** until a real value is chosen. `[Inference]`  

### 3.3 Design Rationale  

- **Early inclusion** of the Pi‑filter prevents a later board spin or the need for “flying wires” on a revision‑A prototype.  
- Placeholder components keep the BOM unchanged while allowing rapid iteration.  
- The filter can be removed or the resistor value adjusted without affecting the rest of the schematic.  

---

## 4. Linear Regulator Selection  

### 4.1 LDO vs. Switching Regulator  

| Criterion                | Linear LDO (e.g., SPX3819) | Switching Regulator |
|--------------------------|----------------------------|---------------------|
| **Efficiency**           | Moderate (≈ 70 % at 5 V→3.3 V) | High (≥ 90 %) |
| **Component count**      | Low (input cap, LDO, output cap) | Higher (inductor, diode, feedback network) |
| **Design complexity**    | Simple, easy to verify | Requires careful layout for EMI |
| **Cost**                 | Low | Higher |
| **Noise performance**    | Low‑frequency noise can be reduced with bypass cap | Switching noise must be filtered |

Given the modest current demand (≤ 500 mA) and a primarily digital load, the **LDO** was chosen for its simplicity and low part count. `[Verified]`  

### 4.2 SPX3819 Features  

- Fixed 3.3 V output, 500 mA capability.  
- Input voltage range up to 16 V (far above the 5.5 V VBUS max).  
- Bypass pin (pin 4) for optional external noise‑reduction capacitor.  
- Low output noise, suitable for analog supplies when needed.  

---

## 5. Decoupling and Bypass Strategy  

### 5.1 Input/Output Capacitors  

- **Minimum**: 2 µF electrolytic (or 1 µF tantalum) per the datasheet.  
- **Implementation**: Existing 10 µF multilayer ceramic capacitors are reused for both input and output, avoiding extra BOM entries.  

> **Note:** Ceramic capacitors are acceptable for the SPX3819 provided their **equivalent series resistance (ESR)** is low, which is typical for modern MLCCs. `[Verified]`  

### 5.2 Bypass Pin Capacitor  

- A **470 nF** capacitor is connected to the bypass pin to further suppress output voltage ripple.  
- For a purely digital design, this is optional; however, adding it incurs negligible cost and improves margin.  

---

## 6. Schematic Cleanliness & DFM Considerations  

- **Net flags** are placed directly on power rails; floating net labels are minimized.  
- Wires are routed to avoid excessive crossing; when unavoidable, **global ports** are used sparingly.  
- All placeholder components (zero‑ohm resistor, generic caps) are clearly labeled, making later part substitution straightforward.  
- The schematic hierarchy is kept shallow to simplify **ERC/DRC** checks and to reduce the risk of orphan nets. `[Verified]`  

---

## 7. USB‑C Ground and Shield Handling  

- The **shield** of the USB‑C connector is tied to the board ground, as recommended by the USB‑C specification.  
- In some designs a **high‑voltage capacitor** may be inserted between shield and ground to improve EMI performance; this is noted as a possible enhancement. `[Speculation]`  

---

## 8. Power‑Path Summary  

```mermaid
flowchart LR
    VBUS[VBUS (4.5‑5.5 V)] -->|Pi‑filter| PI[Pi‑filter (C‑R‑C)]
    PI -->|Filtered| LDO[SPX3819 LDO (3.3 V)]
    LDO -->|3.3 V rail| V33[+3V3 Net]
    V33 --> MCU[Microcontroller]
    USBShield[USB‑C Shield] -->|Tie to| GND[Ground]
    style VBUS fill:#f9f,stroke:#333,stroke-width:2px
    style LDO fill:#bbf,stroke:#333,stroke-width:2px
    style V33 fill:#bfb,stroke:#333,stroke-width:2px
```

The diagram illustrates the sequential power conversion from the USB‑C VBUS line through the Pi‑filter, the LDO regulator, and finally to the 3.3 V rail that powers the MCU. The shield‑to‑ground connection is also shown.  

---

## 9. Key Takeaways  

1. **Early inclusion of a Pi‑filter** provides flexibility for noise mitigation without incurring redesign costs.  
2. **Consistent net naming** (leading “+” for positive rails) simplifies net‑list management and verification.  
3. **Choosing an LDO** for modest current, digital‑only loads balances efficiency, cost, and layout simplicity.  
4. **Reusing existing decoupling capacitors** reduces BOM size while meeting regulator stability requirements.  
5. **Clean schematic practices** (minimal floating labels, judicious use of global ports) improve DFM and reduce ERC/DRC errors.  
6. **Shield‑to‑ground routing** follows USB‑C spec recommendations and can be enhanced with a high‑voltage capacitor if EMI is a concern.  

By adhering to these guidelines, the power distribution network remains **robust, manufacturable, and easy to modify** throughout the product development cycle.