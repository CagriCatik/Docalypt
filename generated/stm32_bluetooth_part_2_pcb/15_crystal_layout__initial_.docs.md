# 15 – Crystal Layout (Initial)

## 1. Overview  

The crystal subsystem is one of the most layout‑sensitive blocks in a mixed‑speed MCU board.  Both the **high‑speed external crystal** (used for the MCU core clock) and the **low‑speed external crystal** (used for watchdog/RTC) must be placed as close as possible to their respective MCU pins, with minimal trace length and a clear, symmetric routing to the load capacitors.  Early‑stage “rat’s‑nest” visualisation in the CAD tool is essential for identifying the optimal placement, required component orientation, and the routing clearance needed for the surrounding high‑current switch node.

---

## 2. High‑Speed vs. Low‑Speed Crystal Placement  

| Item | Recommended Placement | Rationale |
|------|----------------------|-----------|
| **High‑speed crystal (X1)** | Adjacent to MCU pins **24** and **25** (the core‑clock pins). | Keeping the crystal within a few millimetres of the pins minimises trace inductance and capacitance, which directly improves frequency stability and phase noise. `[Verified]` |
| **Low‑speed crystal** | Near the dedicated low‑speed pins (exact numbers not shown in the excerpt). | The same principle applies, but the timing budget is far more forgiving, allowing a slightly larger placement envelope. `[Verified]` |
| **Load capacitors (C8, C17)** | Directly beside the crystal, on the same side of the board, with short, wide traces to the crystal pins. | Short connections reduce series resistance and maintain the intended load capacitance value. `[Verified]` |

> **Design Insight** – The proximity of the crystal to its pins also reduces the exposure of the high‑frequency signal to board‑level EMI sources. In a multi‑layer stack‑up, placing the crystal over a solid ground plane further improves shielding and provides a low‑impedance return path. `[Inference]`

---

## 3. Rat’s‑Nest Analysis & Component Orientation  

The CAD tool’s *rat’s‑nest* view instantly highlights the net‑length hierarchy:

1. **Initial placement** – When the crystal is far from the MCU, the rat’s‑nest lines span the entire board, indicating excessive trace length.  
2. **Moving the crystal** – Dragging the part (shortcut **M**) toward the MCU pins collapses the rat’s‑nest, showing a tighter net.  
3. **Rotating the crystal** – Pressing **R** twice (180° rotation) aligns the crystal pins with the MCU pin pair, preserving symmetry about the centre line formed by pins 2 and 3. This symmetry simplifies routing and balances the electrical environment on both sides of the crystal. `[Verified]`

> **Best‑Practice Note** – Maintaining symmetry around the centre line of the crystal pins reduces differential skew and eases the placement of the load capacitors on either side, which is especially valuable when later fine‑tuning the layout for tighter tolerances. `[Inference]`

### 3.1. Clearance for Adjacent Pins  

Even after achieving a compact placement, sufficient clearance must be left for **pin 1** and **pin 4** of the crystal package. If the crystal is positioned too close, routing these pins becomes impossible without violating design‑rule checks (DRC) or creating acute angles that are difficult to manufacture. `[Verified]`

---

## 4. Switch Node Integration (L1, L2, LX Pin)  

The crystal layout is not isolated; it shares board real‑estate with the **high‑current switch node** formed by inductors **L1** and **L2** and the MCU’s **LX** pin (pin 33).  

* The **LX pin** is a **high‑current switching node** that drives the external power‑switch MOSFETs. Its location on the MCU (pin 33) is adjacent to the crystal pins, so the routing of the crystal must not obstruct the relatively wide, low‑impedance traces required for the switch node. `[Verified]`  
* When moving the crystal, the rat’s‑nest shows a competing demand: the crystal wants to connect to **U2** (the MCU) while the inductors need to reach the same region. The layout must therefore allocate a **dedicated routing corridor** for the switch node, typically a short, thick trace on the top layer with a solid ground plane underneath to minimise voltage spikes and EMI. `[Inference]`

> **Thermal Consideration** – The switch node can generate significant heat; keeping it physically separated from the crystal helps avoid temperature‑induced frequency drift. `[Speculation]`

---

## 5. Recommended Layout Workflow  

```mermaid
flowchart TD
    A[Place MCU footprint] --> B[Identify crystal pins (high‑speed & low‑speed)]
    B --> C[Place load capacitors near pins]
    C --> D[Drag crystal (M) toward MCU pins]
    D --> E[Rotate crystal (R,R) for symmetry]
    E --> F[Check rat’s‑nest for net length]
    F --> G[Verify clearance for pins 1 & 4]
    G --> H[Allocate routing corridor for LX switch node]
    H --> I[Run DRC / ERC checks]
    I --> J[Iterate until all constraints satisfied]
```

*The flowchart summarises the iterative placement‑and‑verification process used during the initial crystal layout.* `[Verified]`

---

## 6. Consolidated Best‑Practice Checklist  

| Aspect | Guideline | Reason |
|--------|-----------|--------|
| **Proximity** | Keep crystal within a few mm of its MCU pins. | Minimises trace inductance and improves frequency stability. `[Verified]` |
| **Symmetry** | Align crystal so that pins 2 and 3 are centred on a vertical axis. | Simplifies routing and balances parasitics. `[Inference]` |
| **Load Capacitors** | Place C8 & C17 directly beside the crystal, with short, wide traces. | Preserves intended load capacitance and reduces series resistance. `[Verified]` |
| **Clearance** | Reserve at least one trace width around pins 1 and 4. | Prevents routing dead‑ends and DRC violations. `[Verified]` |
| **Switch Node Separation** | Route LX, L1, L2 on a dedicated corridor, away from the crystal’s high‑frequency traces. | Reduces EMI coupling and thermal interaction. `[Inference]` |
| **Ground Plane** | Locate the crystal over a solid ground plane (or copper pour) on the layer beneath. | Provides a low‑impedance return path and shields against EMI. `[Speculation]` |
| **Design Rule Checks** | Run ERC/DRC after each major move; pay special attention to clearance, trace width, and via placement for the high‑current node. | Early detection of violations saves redesign time. `[Verified]` |

---

## 7. Summary  

The initial crystal layout hinges on **proximity**, **symmetry**, and **clearance**. By leveraging the CAD tool’s rat’s‑nest visualisation, rotating the crystal for optimal alignment, and deliberately reserving routing space for the high‑current LX switch node, a robust foundation is established for subsequent fine‑tuning and high‑speed signal integrity optimisation. Following the workflow and checklist above will help ensure that the crystal subsystem meets both electrical performance and manufacturability requirements from the earliest stages of the design.