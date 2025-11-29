# 16 – SMPS Layout (Initial)

## 1. Overview  

The initial placement of a switching‑mode power‑supply (SMPS) on a PCB must balance **electrical performance**, **mechanical clearance**, and **manufacturability**.  
Fast switching edges generate large di/dt currents that demand a compact, low‑inductance current loop around the **switch node** (the node that sees the MOSFET drain, the inductor(s), and the output capacitor). The following sections describe the key decisions made during the first‑pass layout, the rationale behind them, and the best‑practice guidelines that should be applied in subsequent refinements.

---

## 2. High‑Speed Node Considerations  

- **Loop Length** – The high‑frequency switching node should be kept as short as possible to minimise parasitic inductance and ringing. A short loop also reduces electromagnetic interference (EMI) and improves transient response.  
- **Edge Rate Sensitivity** – Fast edge rates amplify the effect of any stray inductance; therefore, the physical distance between the MOSFET, the series inductors, and the output capacitor must be minimised.  
- **Current Density** – Wide, low‑impedance traces (or copper pours) are preferred for the high‑current path to keep temperature rise within acceptable limits.  

> **Best practice:** Route the switch node on the same layer, using a solid copper pour or a thick‑trace bus, and keep the total loop length well below a few millimetres. [Verified]

---

## 3. Switch‑Node Filter Placement  

The filter that defines the switch node consists of **L1**, **L2**, and **C14**. Their relative placement determines both electrical performance and mechanical feasibility.

### 3.1. Inductor Pair (L1 & L2)  

- **Series Combination** – L1 and L2 are effectively a single inductance when placed in series. Their combined magnetic fields can interact, so a modest spacing that avoids magnetic coupling but does not increase loop length is ideal.  
- **Orientation** – Rotating the inductors (e.g., using the “R” shortcut) can free up adjacent pins (such as pins 34, 35, and ground pads) and provide a more ergonomic layout for routing.  

> **Inference:** Rotating the inductors was chosen to clear space for nearby high‑density pins while preserving a short loop. [Inference]

### 3.2. Output Capacitor (C14)  

- **Proximity** – C14 should be placed as close as possible to the series inductors to complete the LC filter with minimal trace length.  
- **Thermal Considerations** – The capacitor may dissipate heat; providing a modest clearance from heat‑sensitive components (e.g., the LDO) helps maintain reliability.  

### 3.3. Overall Geometry  

A simplified block diagram of the switch‑node filter is shown below.

```mermaid
flowchart LR
    MOSFET[Switch Node (MOSFET Drain)] --> L1[L1]
    L1 --> L2[L2]
    L2 --> C14[C14 (Output Capacitor)]
    C14 --> Load[Load / Output Rail]
    style MOSFET fill:#f9f,stroke:#333,stroke-width:2px
    style L1 fill:#bbf,stroke:#333,stroke-width:2px
    style L2 fill:#bbf,stroke:#333,stroke-width:2px
    style C14 fill:#bfb,stroke:#333,stroke-width:2px
```

> **Speculation:** The diagram assumes a conventional series‑inductor, shunt‑capacitor topology; the actual schematic may differ. [Speculation]

---

## 4. Component Orientation & Clearance  

- **Rotation for Clearance** – Using the rotate command (`R`) to re‑orient components can free up routing channels and avoid pin‑crowding, especially around dense connector pins (e.g., UART header pins 34/35).  
- **Minimum Spacing** – While it is tempting to place components as tightly as possible to shorten loops, **design‑for‑assembly (DFA)** and **design‑for‑manufacturability (DFM)** dictate a reasonable amount of clearance. Too‑tight placement can hinder solder paste deposition, inspection, and rework.  
- **Assembly & Test Access** – Components that will be probed or replaced during testing (e.g., the inductors) should be positioned where a test probe can reach without disturbing neighbouring parts.  

> **Inference:** The layout deliberately leaves extra space around L1/L2 to accommodate assembly and testing operations. [Inference]

---

## 5. Routing Strategy – Following the “Rat’s Nests”  

During the initial placement phase, the **rat’s‑nest** view (the auto‑generated net‑connection preview) is used to guide component movement:

1. **Identify Critical Nets** – Highlight the high‑speed switch node and any sensitive analog or digital signals.  
2. **Iteratively Move Parts** – Drag components (e.g., the UART header) until the rat’s‑nest lines become short, straight, and orthogonal.  
3. **Validate with DRC/ERC** – Run design‑rule checks (DRC) and electrical rule checks (ERC) after each major move to catch clearance violations early.  

> **Best practice:** Use the rat’s‑nest as a first‑order metric for placement quality, but follow up with detailed impedance and length‑matching analysis for high‑speed nets. [Verified]

---

## 6. Handling Non‑Critical Blocks  

Components such as the **LDO** regulator and the **UART header** are less sensitive to loop length and can be placed after the critical switch node is secured. Their placement should still respect:

- **Thermal Separation** – Keep heat‑generating parts away from temperature‑sensitive devices.  
- **Signal Integrity** – Route high‑speed UART traces with controlled impedance if the data rate warrants it; otherwise, standard routing is sufficient.  
- **Mechanical Constraints** – Ensure that connectors and headers have adequate clearance for mating cables and mechanical stress.  

> **Inference:** The designer deferred placement of the LDO and UART header until after the switch node was roughly defined. [Inference]

---

## 7. Design Trade‑offs Observed  

| Trade‑off | Decision Made | Rationale |
|-----------|---------------|-----------|
| **Component Density vs. Assembly Ease** | Moderate spacing around inductors and connectors | Prevents solder paste bridging and facilitates probe access. |
| **Loop Length vs. Routing Complexity** | Prioritised a short switch‑node loop, even if it required rotating parts | Minimises parasitic inductance and EMI. |
| **Cost vs. Advanced Stack‑up** | Initial layout uses a simple two‑layer approach (implied) | Keeps prototype cost low; controlled‑impedance may be added later if needed. |
| **Thermal Management vs. Board Real Estate** | Provided clearance between C14 and the LDO | Reduces thermal coupling that could degrade regulator performance. |

> **Inference:** The layout reflects a typical early‑prototype mindset where performance is balanced against cost and manufacturability. [Inference]

---

## 8. Summary & Next Steps  

The initial SMPS layout establishes a **compact, low‑inductance switch node** by:

- Placing L1, L2, and C14 in close proximity with careful orientation.  
- Maintaining reasonable clearances for assembly, testing, and thermal management.  
- Using the rat’s‑nest view to iteratively improve net lengths before detailed routing.

Future refinement should focus on:

1. **Precise Trace Width & Impedance Control** for the high‑speed loop.  
2. **Via Optimization** (e.g., using low‑inductance vias for the switch node).  
3. **EMI Shielding & Ground Plane Stitching** to further suppress radiated emissions.  
4. **Formal DFM Review** to verify that the chosen clearances meet the selected manufacturer’s capabilities.

By adhering to these guidelines, the SMPS layout will evolve from a functional prototype to a robust, production‑ready design.