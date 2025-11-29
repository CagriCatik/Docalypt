# 01 – Introduction  

This chapter outlines the overall intent, scope, and high‑level PCB engineering considerations for a Bluetooth‑enabled **STM32WB55** development board. The design is carried out in **KiCad 7** and proceeds from project creation through schematic capture, component placement, routing, and finally fabrication with **PCBWay**. The board mirrors a reference design that includes an STM32WB55 MCU, a USB‑Type‑C connector for power and data, a Tag‑Connect programming header, and a chip‑integrated antenna. In the present implementation a generic **UFL** antenna connector replaces the chip antenna, and only a subset of the MCU’s peripheral pins are routed to keep the project manageable within the available time.

> **Key takeaway:** The design demonstrates a pragmatic balance between feature completeness, manufacturability, and schedule constraints while exposing best‑practice PCB techniques that can be reused for other STM32‑based wireless projects.  

---

## 1. Design Scope and Constraints  

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Microcontroller** | STM32WB55 (Bluetooth‑capable) | Provides integrated BLE radio and sufficient processing resources for typical IoT applications. |
| **Antenna** | Generic UFL connector (instead of chip antenna) | Simplifies library handling and allows the use of an external antenna for testing; incurs a small RF‑performance trade‑off. |
| **USB Interface** | USB‑Type‑C receptacle (power + data) | Modern connector that supports reversible insertion and can deliver up to 5 V / 3 A; requires controlled‑impedance routing. |
| **Programming Header** | Tag‑Connect 6‑pin footprint | Enables solder‑less programming and debugging, reducing assembly steps. |
| **Layer Count** | Two‑layer board (assumed) | Keeps cost low and satisfies the modest signal‑integrity requirements of BLE and USB 2.0. |
| **Time Constraint** | Partial routing of MCU I/Os | Prioritises core functionality (power, USB, antenna, programming) while deferring less‑critical peripherals. |
| **Fabrication Partner** | PCBWay (sponsor) | Provides a reliable, low‑cost service with quick turn‑around for prototype volumes. |

All of the above decisions are **[Verified]** by the source material; the inferred motivations (e.g., cost vs. layer count) are **[Inference]** based on typical prototype design practice.

---

## 2. Core Sub‑systems and Their PCB Implications  

### 2.1 Power Delivery via USB‑Type‑C  

* **Voltage regulation** – The board must accept 5 V from the Type‑C VBUS and generate the MCU core voltage (typically 1.2 V or 1.8 V) using an LDO or buck regulator.  
* **Controlled‑impedance differential pair** – USB 2.0 high‑speed (480 Mbps) requires a 90 Ω differential pair with matched length and minimal skew. On a two‑layer board this is usually achieved by routing the pair on the outer layer with a solid ground plane on the opposite side.  
* **Decoupling strategy** – Place 0.1 µF ceramic capacitors within 5 mm of each power pin; larger bulk caps (e.g., 10 µF) near the regulator input.  

### 2.2 Bluetooth RF Front‑end  

* **Antenna interface** – The UFL connector provides a 50 Ω coaxial interface to an external antenna. A short, 50 Ω‑matched transmission line (microstrip) should be used from the MCU’s RF pin to the connector pad.  
* **Ground plane continuity** – A solid, uninterrupted ground plane beneath the RF trace reduces loss and improves radiation efficiency.  
* **Component placement** – Keep the RF front‑end (matching network, filter, connector) as close as possible to the MCU to minimise trace length and parasitic inductance.  

### 2.3 Tag‑Connect Programming Header  

* **Footprint orientation** – The Tag‑Connect pads are surface‑mount and must be placed on the component side with sufficient clearance for the probe’s spring pins.  
* **Signal integrity** – Since the programming interface operates at low speed, standard routing rules apply; however, keep the SWD lines short and away from high‑frequency traces to avoid crosstalk.  

### 2.4 MCU I/O Routing  

* **Partial routing** – Only essential signals (power, USB, RF, SWD) are routed in the initial prototype. Remaining peripheral pins can be added later as needed.  
* **Design rule checks (DRC/ERC)** – KiCad’s built‑in ERC will flag unconnected pins; these can be suppressed for intentionally unused pins.  

---

## 3. PCB Development Flow  

The following flowchart captures the end‑to‑end process used for this design, from concept to fabricated board.

```mermaid
flowchart TD
    A[Define Requirements] --> B[Create KiCad Project]
    B --> C[Schematic Capture]
    C --> D[Component Selection & Library Management]
    D --> E[Electrical Rule Check (ERC)]
    E --> F[PCB Layout & Placement]
    F --> G[Routing (Power, USB, RF, SWD)]
    G --> H[Design Rule Check (DRC) & Length Matching]
    H --> I[Generate Gerbers & Assembly Files]
    I --> J[Submit to PCBWay (Fabrication)]
    J --> K[Receive Boards & Perform Test]
    K --> L[Iterate as Needed]
```

*The flow reflects the **[Verified]** steps described in the source material and incorporates standard PCB engineering practice.*  

---

## 4. Design‑for‑Manufacturability (DFM) and Assembly (DFA) Highlights  

1. **Component Footprint Consistency** – Use KiCad’s official libraries or verified third‑party footprints to avoid mismatched pad sizes that could cause solder defects.  
2. **Clearance & Creepage** – Maintain at least the manufacturer‑specified minimum spacing (typically 0.2 mm for 1 oz copper on a 2‑layer board) between high‑speed traces and the antenna feed to prevent EMI coupling.  
3. **Via Selection** – For a two‑layer board, only through‑hole vias are available; keep via diameters small (≤0.3 mm) to reduce pad crowding but large enough for reliable plating.  
4. **Silkscreen Placement** – Avoid silkscreen over pads, especially on the UFL connector, to prevent solder mask bridging during assembly.  
5. **Panelization Considerations** – When ordering from PCBWay, request a standard panel layout with adequate spacing (e.g., 5 mm) to simplify depanelisation.  

These guidelines are **[Inference]** based on typical DFM/DFA practices for low‑cost prototype boards.

---

## 5. Trade‑offs and Lessons Learned  

| Trade‑off | Impact | Reasoning |
|-----------|--------|-----------|
| **UFL vs. chip antenna** | Slightly larger board outline, need for external antenna cable; easier to source and test. | Chip antennas are compact but require precise placement and matching; UFL offers flexibility during development. |
| **Two‑layer stackup** | Lower cost, easier fabrication; limited control over impedance for high‑speed signals. | BLE and USB 2.0 can be accommodated on a simple stackup with careful trace geometry. |
| **Partial peripheral routing** | Faster time‑to‑prototype; future revisions may need redesign of unused pins. | Prioritising core functionality meets schedule constraints while leaving room for expansion. |
| **Sponsor‑driven fab selection (PCBWay)** | Access to discounted prototype runs; must adhere to their design rules (e.g., minimum trace/space). | Aligning design constraints with fab capabilities avoids costly re‑spins. |

These observations are **[Inference]** drawn from the design choices described in the transcript.

---

## 6. Summary  

The introductory design establishes a solid foundation for a Bluetooth‑enabled STM32WB55 board by:

* Selecting a **generic UFL antenna** to simplify RF handling while acknowledging a modest performance trade‑off.  
* Implementing a **USB‑Type‑C power‑and‑data interface** with controlled‑impedance routing suitable for USB 2.0.  
* Using a **Tag‑Connect programming header** to streamline firmware updates and debugging.  
* Maintaining a **two‑layer, low‑cost stackup** that satisfies the signal‑integrity requirements of BLE and USB.  
* Following a disciplined **KiCad‑centric workflow** that integrates ERC/DRC checks, DFM best practices, and a clear hand‑off to the PCBWay fabrication service.  

The approach balances **feature completeness**, **manufacturability**, and **schedule constraints**, providing a repeatable template for future STM32‑based wireless hardware projects.