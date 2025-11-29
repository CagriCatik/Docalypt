# Initial Layout  

## 1. Defining the Board Outline  

Before any routing begins, the mechanical envelope of the board must be established. This includes:

* **Board outline** – the exact shape that will be cut from the panel.  
* **Mounting holes** – positioned according to the intended enclosure and any mechanical constraints.  
* **Keep‑out zones** – areas reserved for connectors, heatsinks, or other mechanical features.  

These steps are purely geometric; they do **not** affect net connectivity but they set the limits within which all components must be placed.  

> **Best practice:** Keep the outline simple (rectangular or gently rounded) unless the product form factor forces a more complex shape. Simpler outlines reduce panel‑utilization cost and simplify panelization.  

---

## 2. Establishing a Placement Origin  

Select a logical “origin” component—typically the central processor or a major connector. This component becomes the reference point for the entire layout and is often placed at a round‑number coordinate (e.g., (70 mm, 70 mm)).  

* **Why?**  
  * It provides a stable anchor for the rats‑nest (auto‑generated net‑connection preview).  
  * It simplifies coordinate‑based documentation and mechanical drawings.  

---

## 3. Grid Selection and Granularity  

| Grid type | Recommended unit | Typical coarse step | Minimum practical step |
|-----------|------------------|---------------------|------------------------|
| Metric    | millimetres (mm) | 1 mm – 0.5 mm       | 0.1 mm [Inference] |
| Imperial  | mils (thousandths of an inch) | 40 mil – 20 mil | 4 mil [Inference] |

* **Coarse grid (1 mm or 0.5 mm)** is used for the initial placement of large devices (MCU, connectors, regulators).  
* **Fine grid (0.1 mm)** is introduced later when positioning small passive components and routing tight traces.  

> **Tip:** Avoid using an excessively fine grid (e.g., 0.01 mm) during rough placement; it encourages unnecessary micro‑adjustments that hinder the iterative nature of layout.  

---

## 4. Iterative Placement Workflow  

1. **Place a high‑priority block** (e.g., MCU, RF front‑end, power regulator).  
2. **Run the rats‑nest** to visualise the shortest net connections.  
3. **Adjust neighboring components** to reduce crossing and length.  
4. **Repeat** until the board’s major functional zones are roughly defined.  

Because each move can create new constraints, the first solution is rarely optimal. The process is deliberately **iterative**; designers should expect to backtrack and reposition parts as the layout evolves.  

---

## 5. Cross‑Navigation Between Schematic and Layout  

Modern ECAD tools allow a click on any schematic symbol to highlight the corresponding footprint on the PCB, and vice‑versa. Keeping the schematic window open alongside the layout provides two major benefits:

* **Rapid verification** of net connectivity while moving components.  
* **Logical flow enforcement** – the physical placement can follow the schematic’s functional hierarchy (e.g., connector → ESD protection → MCU).  

> **Best practice:** Use a dual‑monitor setup (or a split‑screen) to keep both views visible at all times.  

---

## 6. Prioritising Critical Sub‑Systems  

Not all nets and blocks have equal sensitivity. Early identification of critical sections guides placement and routing decisions.

| Sub‑system | Criticality | Layout Guidance |
|------------|-------------|-----------------|
| **RF front‑end** (matching network, antenna) | High | Keep traces short, place as close to MCU RF pins as possible, use controlled‑impedance microstrip or stripline if required. |
| **Switch‑mode power supply (SMPS) nodes** (LX, HX) | High | Minimise loop area, place decoupling caps adjacent to power pins, keep high‑di/dt traces compact. |
| **Crystal oscillators (high‑speed & low‑speed)** | High | Short, symmetric traces, keep away from noisy digital lines. |
| **USB differential pair** (Full‑speed) | Medium‑High | Route as a differential pair with matched length and spacing; keep away from high‑current paths. |
| **Debug / UART** | Medium | Length matching less critical; route after high‑speed nets are placed. |
| **Boot‑select switch, reset line** | Low | Placement flexible; route after critical nets are satisfied. |

> **Inference:** The emphasis on short, compact routing for RF and SMPS sections reflects standard signal‑integrity and EMI best practices.  

---

## 7. Decoupling and Bypass Strategy  

Every active device requires local decoupling capacitors placed **as close as possible** to its power pins. The workflow is:

1. Identify the power pins of a component (e.g., MCU VDD, regulator output).  
2. Place the primary bulk capacitor (10 µF‑type) within a few millimetres of the pin.  
3. Add one or more high‑frequency bypass caps (0.1 µF, 0.01 µF) directly adjacent, preferably on opposite sides of the pin to minimise loop inductance.  

Grouping the regulator with its input and output caps (C1, C2) as a **single block** simplifies placement and ensures optimal power integrity.  

---

## 8. Component Grouping and Block Placement  

Instead of moving each part individually, treat logical groups as a unit:

* **LDO regulator + input/output caps** → place together.  
* **RF matching network + antenna connector** → keep as a compact block.  
* **Sensor interface (e.g., UART, I²C) + termination resistors** → cluster near the connector they serve.  

This block‑based approach reduces the number of placement iterations and preserves the intended electrical topology.  

---

## 9. Orientation and Rotation  

Rotating components can dramatically improve routing efficiency. For example, rotating the MCU so that its RF pins face the right side aligns them with the antenna connector and reduces the need for long bends.  

* Use the **R** hot‑key (or equivalent) to rotate a part in 90° increments.  
* Choose an orientation that aligns the majority of high‑speed or high‑frequency pins toward their destination blocks.  

> **Speculation:** The author’s preference for a right‑facing RF pin likely stems from a board‑level floorplan where the antenna is placed on the board’s right edge.  

---

## 10. High‑Level Initial‑Layout Flowchart  

```mermaid
flowchart TD
    A[Define Board Outline & Mounting Holes] --> B[Select Origin Component (e.g., MCU)]
    B --> C[Set Coarse Grid (1 mm)]
    C --> D[Place Critical Blocks (RF, Power, MCU)]
    D --> E[Run Rats‑Nest & Identify Net Lengths]
    E --> F[Iteratively Adjust Placement]
    F --> G[Group Related Components (Regulator+Caps, RF+Antenna)]
    G --> H[Rotate Components for Optimal Pin Access]
    H --> I[Verify with Schematic ↔ PCB Cross‑Navigation]
    I --> J[Proceed to Detailed Routing]
```

*The flowchart captures the recommended sequence for a first‑pass layout.*  

---

## 11. Summary of Key Takeaways  

| Action | Reason |
|--------|--------|
| Define mechanical outline first | Sets immutable constraints for all later steps. |
| Choose a logical origin component | Provides a stable reference for placement and documentation. |
| Use a coarse grid for rough placement | Encourages macro‑level thinking and reduces unnecessary micro‑adjustments. |
| Prioritise critical subsystems (RF, SMPS, crystals) | Short, low‑inductance paths improve performance and EMI compliance. |
| Keep decoupling caps adjacent to power pins | Minimises loop area and improves power integrity. |
| Group related parts as blocks | Reduces iteration count and preserves functional topology. |
| Rotate parts to align high‑speed pins with their destinations | Simplifies routing and reduces trace length. |
| Keep schematic and PCB windows linked | Enables rapid verification of net connections during placement. |
| Iterate repeatedly | The first placement is rarely optimal; refinement is essential. |

By following this structured approach, designers can achieve a clean, manufacturable layout that respects both electrical performance and mechanical constraints.