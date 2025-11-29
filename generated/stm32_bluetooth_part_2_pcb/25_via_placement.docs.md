# Via Placement  

Designing a robust via strategy is essential for low‑impedance power/ground distribution, thermal management, and reliable assembly. The following guidelines capture the proven workflow and best‑practice decisions for placing vias in a multilayer board that uses internal ground (and optionally power) planes.

---

## 1. Design Intent  

All surface‑mount ground pads (e.g., decoupling capacitors, MCU exposed‑copper pads) must be tied to the internal ground planes **as directly as possible**. A short, wide copper trace from the pad to a via that penetrates the ground planes provides the lowest possible inductance and ensures a solid thermal path. The same principle applies to power nets (e.g., 3.3 V) when an internal power plane is present.

> **Why?**  
> * Low‑impedance connections reduce voltage droop and improve signal‑integrity for high‑speed or RF sections.  
> * Wide traces lower inductance ( L ∝ length/width ).  
> * Vias that land on internal planes act as thermal conduits, spreading heat into the larger copper area of the plane.  [Verified]

---

## 2. Via Size Selection  

| Parameter | Typical Value | Rationale |
|-----------|---------------|-----------|
| **Finished drill** | 0.30 mm (≈ 12 mil) – 0.25 mm preferred | Small enough to limit solder‑paste wicking while staying within standard cost brackets.  [Verified] |
| **Pad (annular ring) diameter** | 0.70 mm (≈ 28 mil) – 0.75 mm | Provides adequate copper for plating and mechanical strength; matches the “7 mm × 3 mm” naming convention used in the example layout.  [Verified] |

> **Cost note:** 7 mm × 3 mm (pad × drill) is a “cheap” via size that works for most designs; only move to smaller dimensions when density forces it.  [Inference]

---

## 3. Placement Guidelines  

1. **Location relative to the pad**  
   * Place the via **outside** the solder‑mask opening, not directly under the pad.  
   * Keep a **medium offset** (≈ 0.5 – 1 × pad diameter) so that the copper trace can be short and wide without the via encroaching on the solder‑paste area.  
   * Avoid placing the via too close to the pad edge; otherwise, capillary action can draw paste into the via barrel, leading to insufficient paste on the pad.  [Verified]

2. **One‑via‑per‑pad rule**  
   * Minimum: **one grounded via** for every ground pad.  
   * Exceptions: large capacitors, high‑current power pads, or thermal‑critical devices may require **multiple parallel vias**.  [Verified]

3. **Routing to the via**  
   * Use a **short, wide trace** (≥ 5 mm width in the example) from the pad to the via.  
   * The trace should be as direct as possible to keep inductance low.  [Verified]

4. **Avoiding routing conflicts**  
   * When a via placement would intersect a critical signal (e.g., RF trace, differential pair), rotate or shift the via to a clear area while preserving the short‑wide connection.  
   * Pre‑plan via locations before routing high‑speed nets to prevent later blockages.  [Inference]

---

## 4. Replicating Via Structures  

For boards with many identical pads (e.g., a series of 0.4 µF decoupling caps), create a **via‑plus‑trace template**:

1. Place the via and route the short wide trace for the first pad.  
2. Select the entire structure (pad + trace + via).  
3. Copy (`Ctrl C`) and paste (`Ctrl V`) onto each subsequent pad, rotating (`R`) as needed.  

This method guarantees consistent impedance and thermal performance across all pads.  [Verified]

---

## 5. Multiple Vias for High‑Current / Thermal Management  

### 5.1 Parallel Ground Vias  
* Larger capacitors or power‑stage components benefit from **two or more ground vias** placed around the pad perimeter.  
* Parallel vias lower the overall inductance (L_total ≈ L_single / N) and provide redundancy.  

### 5.2 Thermal Vias in Exposed Pads (QFN, BGA)  
* Exposed copper pads on MCUs or power ICs serve both **electrical grounding** and **heat sinking**.  
* **Staggered peripheral vias** (e.g., 4‑6 vias equally spaced around the pad edge) give solder paste a solid “island” in the centre, reducing paste wicking while still providing an efficient thermal path.  
* Keep the **finished drill ≤ 0.30 mm**; 0.25 mm is ideal for balancing manufacturability and thermal performance.  [Verified]  

> **Design tip:** Do **not** place a via directly in the centre of the pad unless the component’s datasheet explicitly permits it. Peripheral placement preserves a robust solder joint.  [Inference]

---

## 6. Power‑Plane Vias (e.g., 3.3 V)  

Even when a dedicated internal power plane is not used, pre‑placing **power vias** on the top layer simplifies later routing:

* Duplicate the ground‑via template, change the net assignment to **3.3 V**, and connect it to the appropriate internal plane (or to a copper‑fill polygon on the bottom layer).  
* This practice reserves clear zones for the power‑via traces, preventing later congestion with high‑speed signals such as USB or differential pairs.  [Verified]

---

## 7. Pre‑Planning and Iterative Refinement  

A robust via strategy follows an **iterative workflow**:

```mermaid
flowchart TD
    A[Define internal planes (GND, 3.3 V)] --> B[Select via size (pad & drill)]
    B --> C[Place via near each ground/power pad]
    C --> D[Route short wide trace to via]
    D --> E[Duplicate structure for similar pads]
    E --> F[Add parallel vias where needed]
    F --> G[Run DRC / ERC checks]
    G --> H{Issues?}
    H -->|Yes| C
    H -->|No| I[Proceed to signal routing]
```

* **DRC/ERC** checks after each batch of via placements catch clearance violations, missing connections, or unintended net assignments before signal routing begins.  [Verified]

---

## 8. Trade‑offs & DFM Considerations  

| Aspect | Decision | Impact |
|--------|----------|--------|
| **Via size** | Standard 0.30 mm finished hole | Low cost, acceptable for most currents; smaller holes increase cost and risk of plating defects. |
| **Number of vias per pad** | Minimum 1, add more for high‑current or thermal pads | Improves impedance & thermal spread but adds drill time and may increase solder‑paste wicking risk. |
| **Via placement offset** | Medium offset (≈ 0.5 × pad diameter) | Balances solder‑paste retention with short trace length. |
| **Parallel vs. polygon connection** | Use parallel vias for high‑current; otherwise rely on copper‑fill polygons | Parallel vias give deterministic low inductance; polygons are cheaper but may have higher effective inductance. |
| **Thermal via pattern** | Peripheral staggered array | Preserves central solder‑paste area, improves heat extraction, modest increase in drill count. |

> **Manufacturability tip:** Keep all via drill sizes within the **standard drill set** of the chosen fab house to avoid extra tooling charges.  [Speculation]

---

## 9. Summary of Best Practices  

1. **Define internal reference planes** early (ground, optional power).  
2. **Select a cost‑effective via size** (≈ 0.30 mm finished hole, 0.70 mm pad).  
3. **Place one via per pad** outside the solder‑mask opening, with a medium offset.  
4. **Route a short, wide trace** from pad to via to minimize inductance.  
5. **Copy the via‑plus‑trace template** to all identical pads for consistency.  
6. **Add parallel vias** for large capacitors, high‑current pads, or thermal pads; stagger them around the pad perimeter.  
7. **Pre‑place power vias** even without an internal power plane to reserve routing space.  
8. **Run DRC/ERC** after each placement batch; iterate if violations appear.  
9. **Consider DFM**: stay within standard drill sizes, avoid excessive via density, and preserve solder‑paste islands.  

Following this systematic approach yields a board with low‑impedance power/ground distribution, reliable thermal paths, and a layout that is friendly to both high‑speed routing and manufacturability.