# 21 – Component Annotation & Reference‑Designator Management  

*How to obtain a logical, assembly‑friendly numbering scheme for every part in a KiCad (or similar) schematic.*

---  

## 1. Why Annotation Matters  

A well‑ordered set of reference designators is more than a cosmetic convenience:

| Benefit | Explanation |
|---|---|
| **Assembly clarity** | Pick‑and‑place machines and human assemblers read the BOM in the same order the schematic presents the parts. |
| **Debug efficiency** | Engineers can locate a component on the board by following the logical sequence (e.g., J1 → J2 → U1 → C1). |
| **DFM/DFA compliance** | Consistent numbering reduces the chance of mismatched footprints, missing parts, or incorrect polarity during fabrication. |
| **Documentation consistency** | Test reports, schematics, and layout files all reference the same identifiers, avoiding confusion. |

> **Key principle** – *Reference designators should follow the physical flow of the board (left‑to‑right, top‑to‑bottom) and group related functional blocks together.*  `[Inference]`

---  

## 2. Recommended Annotation Strategy  

1. **Define a naming convention before the first annotation**  
   - Connectors: `J1, J2, …`  
   - Integrated circuits: `U1, U2, …`  
   - Power regulators: `U3, U4, …` (or a dedicated `VR` prefix)  
   - Capacitors: `C1, C2, …`  
   - Resistors: `R1, R2, …`  

2. **Reserve ranges for each functional block**  
   - Example: `J1‑J4` for external I/O (USB‑C, header, antenna, UFL).  
   - Example: `C1‑C20` for the power‑rail decoupling network.  

3. **Annotate in two passes**  
   - **Pass 1 – Automatic XY sort** – Clears all designators and lets KiCad assign numbers based on component centroids.  
   - **Pass 2 – Manual correction** – Adjust any out‑of‑order items (e.g., a regulator that received `C6` instead of `C1`).  

4. **Lock the final designators** (e.g., by disabling “auto‑renumber on move”) to prevent later edits from overwriting the manual ordering.  

---  

## 3. Practical Workflow in KiCad (or equivalent ECAD)  

```text
1. Open the schematic editor.
2. **Tools → Annotate schematic…**
   • Choose **“Clear existing annotations”**.
   • Set **“Annotation mode” → “By position (X/Y)”**.
   • Click **Annotate** → **Close**.
3. Review the generated list:
   • Connectors should appear as J1, J2, J3, J4 in the desired physical order.
   • Verify that high‑priority parts (e.g., LDO regulator) have the first capacitor numbers (C1, C2…).
4. For any mismatches:
   • Double‑click the component.
   • Edit the **Reference** field manually (e.g., change `C6` → `C1`).
   • Press **Enter** to commit.
5. (Optional) Re‑run **Annotate** with **“Do not renumber existing designators”** to fill any gaps left by manual edits.
6. Save the schematic and generate an updated BOM.
```

> The above steps reproduce the exact sequence described in the source material and are **verified** as a common KiCad workflow. `[Verified]`

---  

## 4. When Manual Intervention Is Required  

KiCad offers only two automatic sorting options:

| Mode | Typical outcome |
|---|---|
| **Sheet order** | Numbers follow the order of schematic pages, not physical layout. |
| **XY position** | Numbers follow the geometric centre of each symbol; components placed higher on the page receive lower numbers. |

Because the XY algorithm bases its order on *centroid* positions, a connector placed slightly above another may be numbered first even if the designer intends the opposite logical flow. This leads to situations such as:

- `J1` (USB‑C) correctly placed at the top, but `J3` (antenna header) receiving a higher number because its centre is lower.  
- A low‑dropout regulator receiving `C6` while the first decoupling capacitor is already labelled `C1`.  

Consequently, **manual re‑annotation** is the reliable way to enforce a logical sequence. `[Inference]`

---  

## 5. Best‑Practice Guidelines  

| Guideline | Rationale |
|---|---|
| **Group by function** – Keep all I/O connectors together, then power circuitry, then digital logic. | Simplifies BOM generation and assembly line setup. |
| **Increment within a block** – After assigning `J1‑J4`, start the next block at `U1`. | Prevents accidental cross‑block numbering (e.g., a resistor being labelled `J5`). |
| **Avoid gaps** – If a component is removed, renumber or reserve the missing identifier for future revisions. | Keeps the BOM tidy and avoids “missing part” warnings in ERC/DRC. |
| **Document exceptions** – If a part must break the sequence (e.g., a test point that shares a footprint with a resistor), note the deviation in the design notes. | Guarantees traceability for later revisions. |
| **Lock after finalization** – Disable automatic renumbering before releasing the design to fabrication. | Guarantees that the approved BOM matches the fabricated board. |

---  

## 6. Impact on DFM / DFA  

- **Pick‑and‑place programming** reads the BOM in order; a sequential, gap‑free list reduces the chance of mis‑feeds.  
- **Automated ERC/DRC** tools often flag duplicate or missing designators; a clean annotation eliminates false positives.  
- **Silkscreen labeling** (e.g., “J1 USB‑C”) aligns directly with the reference designator, aiding field service and troubleshooting.  

---  

## 7. Example Annotation Flow (Mermaid)  

```mermaid
flowchart TD
    A[Start – Open schematic] --> B[Clear existing designators]
    B --> C[Annotate by XY position]
    C --> D[Review auto‑assigned numbers]
    D -->|All good| E[Lock designators & generate BOM]
    D -->|Mismatches| F[Manually edit designators]
    F --> G[Re‑run annotate (no renumber)]
    G --> D
```

*The loop continues until the designer is satisfied that the reference designators follow the intended logical order.* `[Inference]`

---  

## 8. Common Pitfalls & Mitigations  

| Pitfall | Mitigation |
|---|---|
| **Connector gets a higher number than intended** because it sits lower on the sheet. | Move the symbol slightly upward *or* manually rename after the automatic pass. |
| **Capacitor series receives non‑sequential numbers (C1, C6, C7…)** after XY sort. | Manually renumber the series before final lock‑in. |
| **Later schematic edits cause auto‑renumbering to overwrite manual changes**. | Use the “Do not renumber existing designators” option or lock the schematic file. |
| **Missing designators in the BOM** due to gaps left by deleted parts. | Run a quick “Find unused designators” script or manually fill the gaps. |
| **Inconsistent prefixes across sheets** (e.g., `J` on one sheet, `CON` on another). | Enforce a global naming convention via a design‑rules file or project‑wide template. |

---  

## 9. Summary  

A disciplined annotation process—starting with a clear naming convention, using KiCad’s XY‑based automatic pass, and finishing with targeted manual adjustments—produces a logical, assembly‑ready reference designator scheme. This practice directly improves **manufacturability**, **serviceability**, and **documentation integrity**, and it mitigates many of the common errors that arise during later stages of PCB production.  

Adopt the workflow and guidelines outlined above for every new schematic to ensure that the design’s logical structure is faithfully reflected in its physical realization.