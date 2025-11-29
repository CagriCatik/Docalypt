# 08 Importing Components  

## 1. Overview  

Transferring the schematic hierarchy onto the PCB canvas is a pivotal step in the design flow. The operation—commonly called **“Update PCB from Schematic”**—creates PCB‑level symbols (footprints) that correspond one‑to‑one with the schematic components, applies the net‑class definitions, and synchronises any changes made to the schematic after the initial layout. Performing this step correctly sets the foundation for a clean, DFM‑friendly placement and routing stage.  

---

## 2. Preparing the PCB Environment  

### 2.1 Layer Stack & Appearance Panel  

Before importing, verify that the PCB editor contains **only the layers required for the current design** (e.g., signal, power, ground, silkscreen). Unused layers add visual clutter and can hide placement errors.  

- **Appearance panel** – Use the right‑hand *Appearance* tab to toggle visibility of objects (tracks, pads, keep‑outs, etc.). Hiding non‑essential layers while importing helps you focus on component locations and net‑class assignments.  

### 2.2 Net‑Class Verification  

Net classes define default width, clearance, and routing rules for groups of nets (e.g., high‑current power, high‑speed differential pairs). Ensure that the net‑class table imported from the schematic reflects the intended design constraints **before** running the update. This guarantees that the PCB editor will automatically apply the correct design rules to each net as the components appear.  

---

## 3. Updating the PCB from the Schematic  

| Action | How to invoke | What happens |
|--------|---------------|--------------|
| **Update PCB** | Press **F8** or click the **“Update PCB with changes made to schematic”** button on the top‑right toolbar | A dialog summarises the pending changes (new components, deleted parts, moved symbols, net‑class updates). Confirming the dialog adds the missing footprints, removes obsolete ones, and synchronises net‑class data. |

> **Verified** – The shortcut *F8* and the toolbar button are the standard mechanisms for invoking the update operation.  

### 3.1 Dialog Interpretation  

The update dialog lists three categories:  

1. **Add** – New schematic symbols that lack a PCB counterpart.  
2. **Delete** – PCB objects whose schematic symbols have been removed.  
3. **Modify** – Changes to existing symbols (e.g., footprint swap, orientation).  

Accepting the dialog **adds all symbols** and **applies their associated footprints** to the PCB canvas. If the dialog reports **errors or warnings**, resolve them before proceeding (e.g., missing footprint libraries, mismatched pin counts).  

### 3.2 Post‑Import Interaction  

After the update, you can immediately interact with the newly placed components:  

- **Zoom** with the mouse wheel or middle‑button drag.  
- **Pan** by holding the middle mouse button.  
- **Place** components by left‑clicking; the first click drops the component, subsequent clicks continue placement of the next component in the queue.  

These navigation shortcuts are identical to the standard PCB editor controls and enable rapid initial placement.  

---

## 4. Initial Placement & Layout Strategy  

While the import operation positions components at their **default schematic coordinates** (often stacked at the origin), a deliberate placement plan should follow immediately:  

1. **Group by functional blocks** (e.g., power supply, MCU, I/O connectors).  
2. **Orient footprints** to minimise routing complexity and to respect mechanical constraints (board edges, mounting holes).  
3. **Reserve keep‑out zones** for high‑current traces, RF sections, or thermal pads before routing.  

> **Inference** – Early block‑level placement reduces later re‑work and improves signal‑integrity outcomes.  

---

## 5. Best Practices for Component Import  

| Practice | Rationale |
|----------|-----------|
| **Consistent library versions** – Use a single, vetted footprint library for the entire project. | Prevents mismatched pad stacks and ensures DFM compliance. |
| **Run ERC/DRC on the schematic first** – Resolve electrical rule check errors before import. | Guarantees that net‑class assignments are meaningful and that no illegal connections reach the PCB. |
| **Validate footprint‑to‑symbol mapping** – Confirm that each schematic symbol points to the intended footprint (e.g., 0603 resistor vs. 0805). | Avoids costly re‑footprinting after layout. |
| **Leverage net‑class defaults** – Assign high‑speed nets to a dedicated class with tighter clearance and width rules. | Automates impedance control and reduces manual rule overrides. |
| **Lock critical components** (e.g., crystal, high‑speed connectors) after placement. | Prevents accidental movement during bulk routing. |
| **Document any manual footprint swaps** in the design notes. | Provides traceability for future revisions and manufacturing hand‑off. |

---

## 6. Common Pitfalls & Troubleshooting  

| Symptom | Likely Cause | Remedy |
|---------|--------------|--------|
| **Update dialog shows warnings about missing footprints** | Footprint library not loaded or symbol‑footprint link broken. | Load the correct library, or edit the symbol’s footprint reference. |
| **Components appear at (0,0) overlapping** | Schematic symbols all share the same default coordinates. | After import, manually spread the components according to functional blocks. |
| **Net‑class rules not applied** | Net‑class table not linked to the PCB project or net names mismatched. | Re‑import net‑classes, verify net naming consistency. |
| **Unexpected component rotation** | Footprint orientation defined in the library differs from schematic orientation. | Adjust the footprint’s default rotation or rotate the component after placement. |

---

## 7. Design Flow Diagram  

The following flowchart visualises the import process and its integration with the broader design cycle:

```mermaid
flowchart TD
    A[Complete Schematic] --> B[Run ERC / DRC]
    B --> C[Verify Net‑Class Table]
    C --> D[Update PCB (F8 or Toolbar)]
    D --> E{Dialog Shows Errors?}
    E -- Yes --> F[Fix Library / Net Issues] --> D
    E -- No --> G[Components & Footprints Added]
    G --> H[Initial Placement & Block Grouping]
    H --> I[Run PCB DRC]
    I --> J[Proceed to Routing]
```

*The diagram emphasizes the iterative nature of error handling: any warnings in the update dialog must be resolved before proceeding to placement and routing.*  

---

## 8. Summary  

Importing components is more than a mechanical transfer; it is the moment where **schematic intent meets physical reality**. By preparing the PCB environment, confirming net‑class definitions, and following a disciplined update‑and‑place workflow, you lay a solid groundwork for efficient routing, reliable signal integrity, and manufacturable board layouts.  

---  

*End of Chapter 08 – Importing Components*