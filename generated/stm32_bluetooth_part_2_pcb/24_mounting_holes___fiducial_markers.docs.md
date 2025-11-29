# Mounting Holes & Fiducial Markers  

Mounting holes and fiducial markers are the two most common **non‑electrical** features on a PCB.  Although they do not carry signal, they have a decisive impact on mechanical integration, manufacturability, and automated assembly.  This section describes a robust workflow for adding them in KiCad (or any comparable ECAD tool), the key design decisions that must be made, and best‑practice placement guidelines.

---

## 1. Adding Mounting Holes in the Schematic  

| Step | Action | Rationale |
|------|--------|-----------|
| 1️⃣ | Insert a **Mounting‑Hole** component from the library. | Mounting holes are treated like any other component, which guarantees that they are propagated to the layout and can be tied to a net. |
| 2️⃣ | Choose **“with connection”** (e.g., tied to **GND**) **or** “without connection”. | A grounded hole can provide a low‑impedance path for EMI shielding when the hole passes through a ground plane. A floating hole is used when no electrical function is required. |
| 3️⃣ | Hide the value field and set **`Exclude from BOM`** (and optionally **`Exclude from POS`**) in the component properties. | Prevents the hole from appearing on the parts list or pick‑and‑place files – it is a mechanical feature only. |
| 4️⃣ | Replicate the hole as needed (copy‑paste or use the *repeat* tool) and connect each instance to the same net (usually **GND**). | Guarantees consistent net‑tie and simplifies later DRC checks. |

> **Note:** In KiCad the component is automatically linked to a footprint once the schematic is updated, so the hole will appear on the PCB as a through‑hole pad.  This workflow also works in other ECAD suites that support schematic‑driven placement.  [Verified]

---

## 2. Selecting the Correct Footprint & Size  

Mounting‑hole footprints are defined by the **screw size** (M2, M3, etc.) and the **standard** (ISO, DIN, etc.).  

* **M2 vs. M3** – Choose the smallest size that satisfies the mechanical load and tolerance of the enclosure.  Smaller holes free up board area but may require tighter drilling tolerances from the fab house.  [Speculation]  
* **Pad Diameter** – Must be large enough to accommodate the plated‑through hole plus a sufficient annular ring (typically ≥ 0.2 mm).  KiCad libraries already encode the correct pad size for each standard.  
* **Attributes** – Set **`Exclude from BOM`** and **`Exclude from DRC`** (if the tool permits) to avoid false violations.  

If a hole appears oversized in the layout, edit the schematic component’s **Footprint** field (bulk edit) and select the appropriate smaller variant, then re‑synchronize the PCB.  This avoids manual footprint swaps that could break net ties.  [Verified]

---

## 3. Electrical Considerations for Ground‑Tied Holes  

* Ground‑tied holes provide a **via** that connects the top and bottom copper layers through the board’s ground plane.  This can improve **EMI shielding** and **mechanical rigidity**.  
* For high‑frequency designs, keep the hole’s **plating thickness** within the fab’s tolerance to avoid unintended inductance.  
* When the board contains **internal power or ground planes**, place the hole **through the plane** so that the via acts as a low‑impedance short.  This is especially useful for mounting a metal enclosure that will be grounded.  [Inference]

---

## 4. Adding Fiducial Markers  

Fiducials are high‑contrast reference features used by pick‑and‑place machines and optical inspection systems.  They consist of an **exposed copper pad** surrounded by a **clearance ring** (no copper) and are **not electrically connected** to any net.

### 4.1. Library Insertion  

1. Insert a **Fiducial** component (search “fiducial” in the library).  
2. Hide the value field and set **`Exclude from BOM`**.  
3. Assign a **fiducial footprint** – most libraries provide a 1 mm × 1 mm pad with a 1 mm opening.  Smaller variants exist for tight‑space boards.  

> The typical 1 mm pad / 1 mm opening size offers a good balance between camera resolution and board real‑estate.  [Verified]

### 4.2. Global vs. Local Fiducials  

* **Global fiducials** – At least three, placed near the board corners, provide a reference frame for the entire board or panel.  
* **Local fiducials** – Additional markers placed close to high‑density component groups improve alignment for those specific regions.  

For a **single‑sided assembly** only the side that receives components needs fiducials; for **double‑sided** boards, place a matching set on each side.  [Verified]

---

## 5. Placement Guidelines  

### 5.1. Mounting Holes  

* **Clearance** – Keep a minimum distance (e.g., 0.5 mm) from the board outline and from any copper features to satisfy the fab’s **creepage/clearance** rules.  
* **Alignment** – Align holes in a grid or along the mechanical axes of the enclosure (e.g., 50 mm or 75 mm spacing) to simplify CNC drilling and enclosure design.  
* **Symmetry** – When possible, place holes symmetrically to balance mechanical stress.  

### 5.2. Fiducials  

* **Separation** – Space the three global fiducials as far apart as possible, ideally near three corners of the board.  This maximizes the lever arm for camera alignment and reduces error propagation.  
* **Avoid Obstruction** – Do not place fiducials under large copper pours, components, or near high‑frequency traces where they could be masked by solder mask or copper.  
* **Silkscreen** – Turn off silkscreen for fiducials (uncheck **Visible** in the layer properties) to keep the marker pure white on the board.  

### 5.3. General DFM Tips  

* **Through‑hole consumption** – Remember that each mounting hole and fiducial consumes a drilled hole; factor this into the panelization density.  
* **Panelization** – When designing a panel, replicate the fiducial set for each sub‑board or use a **panel‑wide** fiducial pattern if the assembly equipment supports it.  
* **DRC Checks** – Run a **Design Rule Check** after placement to verify clearance to copper, other holes, and the board edge.  [Verified]

---

## 6. Updating the PCB and Verifying the Layout  

1. **Synchronize** – After editing the schematic (adding holes/fiducials, changing footprints), press **F8** (or “Update PCB from Schematic”) to propagate changes.  
2. **Inspect** – Verify that the pads appear as **plated‑through** (through‑hole) in the layout view.  
3. **Run DRC** – Ensure no clearance violations, especially between mounting holes and copper pours.  
4. **Export** – When generating Gerbers, confirm that the **drill file** includes the mounting‑hole and fiducial locations, and that the **assembly drawing** shows the fiducials (if required).  

> Keeping the schematic as the single source of truth for mechanical features prevents mismatches between the netlist and the physical board.  [Inference]

---

## 7. Summary Flowchart  

```mermaid
flowchart TD
    A[Add Mounting‑Hole Component] --> B{Choose Connection}
    B -->|Ground| C[Tie to GND Net]
    B -->|Floating| D[No Net Tie]
    C --> E[Set Exclude‑from‑BOM & Hide Value]
    D --> E
    E --> F[Add Fiducial Component]
    F --> G[Select Fiducial Footprint (1 mm pad/1 mm opening)]
    G --> H[Set Exclude‑from‑BOM & Hide Value]
    H --> I[Update PCB (F8)]
    I --> J[Place Holes & Fiducials on Layout]
    J --> K[Run DRC / Verify Clearances]
    K --> L[Generate Gerbers & Drill Files]
```

*The flowchart captures the end‑to‑end process from schematic entry to final fabrication files.*  

---

## 8. Best‑Practice Checklist (for quick reference)

| ✅ Item | Reason |
|--------|--------|
| Add mounting holes as schematic components (ground‑tied if shielding is needed). | Guarantees net tie and BOM exclusion. |
| Choose the smallest mechanically‑acceptable hole size (M2, M3, …). | Saves board area and reduces cost. |
| Hide value fields and set **Exclude from BOM** for all mechanical parts. | Keeps parts list clean. |
| Use a 1 mm × 1 mm fiducial pad with a 1 mm clearance ring (or smaller if required). | Provides reliable optical reference. |
| Place at least three global fiducials near board corners, far apart. | Maximizes alignment accuracy. |
| Turn off silkscreen for fiducials. | Prevents visual clutter and mask interference. |
| Maintain clearance from board outline and other copper features. | Satisfies fab DFM rules. |
| Run DRC after placement and before export. | Catches clearance violations early. |
| Verify drill files contain all through‑hole pads (mounting holes & fiducials). | Ensures manufacturability. |

---  

By following the workflow and placement guidelines above, designers can ensure that mounting holes and fiducial markers are **mechanically robust**, **assembly‑friendly**, and **manufacturing‑ready**, while keeping the schematic and layout in perfect sync.  This foundation simplifies downstream processes such as panelization, automated pick‑and‑place, and final quality inspection.