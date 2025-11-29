# 18 – Power Management – LDO Regulator  

## 1. Overview  

The board is powered from a USB‑C receptacle that supplies a **VBUS** voltage nominally at **5 V** (acceptable range 4.5 V – 5.5 V). The microcontroller (MCU) and its associated peripherals require a **3.3 V** rail. Because the current demand of the design is modest (tens of milliamps), a **low‑dropout linear regulator (LDO)** is the preferred solution over a switching buck converter.  

Key reasons for selecting an LDO in this application:  

| Consideration | LDO Advantage |
|---------------|----------------|
| **Current demand** | ≤ ~20 mA (MCU) + peripheral margin → well within typical LDO ratings. |
| **Voltage differential** | 5 V → 3.3 V (ΔV ≈ 1.7 V) results in low dissipation (≈ 2 W at worst‑case 1 A, but actual ≈ 30 mW). |
| **Noise sensitivity** | LDOs provide low output ripple, beneficial for analog sensors (though not critical here). |
| **Bill‑of‑materials (BOM) cost** | Simple SMD part, inexpensive, minimal external components. |
| **Design simplicity** | No inductor, fewer layout constraints, easier DFM. |

> The power loss estimate of ~2 W assumes a full‑amp load; with the actual ~20 mA load the loss is < 35 mW, which is negligible for a small board. [Verified]

## 2. Current Budget Estimation  

### 2.1 MCU Consumption  

Using the IDE’s power‑analysis tool (e.g., STM32CubeIDE), the MCU’s worst‑case current is **≈ 16 – 17 mA** when all enabled peripherals are active.  

### 2.2 Peripheral Margin  

Additional current from sensors, connectors, or relays must be added to the MCU budget. For a simple demonstration board that only adds a USB‑C connector and a few passive components, the total stays well below **150 mA**.  

> A design margin of ~2× the calculated peak current is recommended to accommodate future feature growth. [Inference]

## 3. LDO Selection Criteria  

When searching a distributor’s catalog, apply the following filters:

| Parameter | Desired Value / Reason |
|-----------|------------------------|
| **Package** | SMD, easy‑to‑solder (e.g., SOT‑23‑5) for hand assembly. |
| **Output Voltage** | Fixed 3.3 V (no external feedback network required). |
| **Maximum Output Current** | ≥ 150 mA (provides headroom). |
| **Input Voltage Range** | Must accept up to 5.5 V (USB‑C VBUS max). |
| **Quiescent Current** | Low µA range preferred to keep standby draw minimal. |
| **Stability Requirements** | Compatible with ≤ 1 µF ceramic output capacitor (simplifies BOM). |
| **Enable Pin** | Active‑high, tolerant to 0 V–Vin, must not be left floating. |

Applying these filters yields parts such as **Microchip MIC5365‑3.3Y** (SOT‑23‑5). This device meets all criteria, is in stock, and already has a KiCad symbol and footprint, reducing library‑creation effort.  

> The MIC5365’s datasheet confirms stability with a 1 µF ceramic output capacitor, eliminating the need for tantalum or electrolytic parts. [Verified]

## 4. External Component Requirements  

### 4.1 Input & Output Capacitors  

- **Input capacitor (Cin):** 4.7 µF ceramic (or similar) placed as close as possible to the LDO’s VIN pin.  
- **Output capacitor (Cout):** 4.7 µF ceramic (or ≥ 1 µF) placed adjacent to the VOUT pin.  

These capacitors satisfy the regulator’s stability criteria and also provide decoupling for downstream circuitry.  

### 4.2 Enable Pin Handling  

The MIC5365’s **EN** pin is active‑high; tying it directly to **VIN** (VBUS after ESD protection) forces the regulator on continuously. If future power‑sequencing is required, the EN pin can be driven by an MCU GPIO or a dedicated power‑management IC. The pin must never be left floating.  

> Connecting EN to VIN is the simplest approach for a board that is always powered when USB is attached. [Inference]

## 5. Schematic Integration  

A typical power‑rail schematic block is shown below.  

```mermaid
flowchart LR
    VBUS[VBUS (4.5‑5.5 V)] -->|ESD Protection| VIN[Vin of LDO]
    VIN -->|Cin| LDO[MIC5365 3.3 V LDO]
    LDO -->|Cout| V33[3.3 V Rail]
    V33 --> MCU[Microcontroller]
    V33 --> Periph[Peripherals]
    LDO --> EN[EN Pin]
    EN -->|Tie to VIN| VIN
```

*The diagram illustrates the power flow from the USB‑C VBUS through ESD protection, the LDO, and onto the 3.3 V rail used by the MCU and peripherals.*  

## 6. PCB Layout Considerations  

### 6.1 Placement  

- Position the LDO **close** to the USB‑C connector to minimize the length of the high‑current VBUS trace.  
- Keep Cin and Cout **adjacent** to the regulator pins to reduce loop inductance and ensure stability.  

### 6.2 Trace Width & Copper  

- For the **VBUS** trace feeding the LDO, a modest width (e.g., 0.25 mm) is sufficient given the low current (< 150 mA).  
- The **3.3 V** rail can be a thin trace or a small copper pour, provided it supplies the required current without excessive voltage drop.  

### 6.3 Ground Plane  

- Use a solid **ground plane** on the bottom layer (or internal layer for multi‑layer boards) to provide a low‑impedance return path for both input and output capacitors.  
- Ensure that the ground pins of the LDO and the capacitor grounds are connected directly to this plane to minimize parasitic inductance.  

### 6.4 Decoupling Strategy  

- Place **additional 0.1 µF** ceramic decoupling capacitors near the MCU VDD pins.  
- Group decoupling capacitors with the LDO output capacitor to form a low‑impedance supply network.  

### 6.5 DFM & Assembly  

- Choose an **SOT‑23‑5** package to avoid fine‑pitch soldering challenges.  
- Verify that the component footprint includes **solder‑mask clearance** and **courtyard** dimensions compliant with the chosen PCB fab house.  
- Run **ERC** (Electrical Rule Check) to ensure the EN pin is not left floating and that all power nets are correctly connected.  

## 7. Trade‑offs & Design Rationale  

| Decision | Benefit | Cost / Trade‑off |
|----------|---------|------------------|
| **LDO vs. Switching Buck** | Simpler schematic, fewer parts, lower EMI, cheaper | Higher (but negligible) power dissipation at low current |
| **Fixed‑output LDO** | No external resistor network, reduces BOM and layout complexity | Less flexibility if voltage needs change |
| **Ceramic capacitors only** | Small size, low ESR, easy to source | Must verify regulator stability with low‑ESR caps (confirmed in datasheet) |
| **EN tied to VIN** | Guarantees regulator is always on when USB is present | No software control over power‑down (acceptable for this design) |

> The chosen architecture balances cost, simplicity, and reliability for a low‑power USB‑C powered board. [Inference]

## 8. Verification & Testing  

1. **Power‑up test:** Measure VBUS (after ESD) and confirm the LDO output is 3.3 V ± 2 % under no‑load and full‑load conditions.  
2. **Load regulation:** Connect a variable load (e.g., a resistor bank) up to 150 mA and verify voltage droop remains within spec.  
3. **Thermal check:** With the worst‑case load, ensure the LDO does not exceed its thermal rating (unlikely given low dissipation).  
4. **ESD robustness:** Verify that the ESD protection device upstream of the LDO survives IEC 61000‑4‑2 test levels.  

## 9. Summary  

- The board’s power architecture uses a **USB‑C VBUS → ESD → MIC5365 LDO → 3.3 V rail**.  
- Current requirements are modest, making an LDO the most cost‑effective and straightforward solution.  
- Proper selection of input/output capacitors and correct handling of the enable pin guarantee stable operation.  
- Layout guidelines emphasize short, wide traces for VBUS, close placement of decoupling capacitors, and a solid ground plane to ensure low‑impedance power delivery.  

By adhering to these guidelines, designers can achieve a reliable, low‑noise 3.3 V supply with minimal BOM impact and straightforward manufacturability.