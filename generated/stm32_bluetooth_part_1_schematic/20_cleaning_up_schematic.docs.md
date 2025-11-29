# Cleaning Up the Schematic – Best‑Practice Guidelines  

A well‑organized schematic is the foundation of a reliable PCB design.  
Beyond merely connecting symbols, the schematic should convey intent, aid
verification, and streamline the transition to layout. The following
guidelines capture proven techniques for polishing a schematic before
footprint assignment and board‑level work.

---

## 1. Explicitly Mark Unused Pins  

- **No‑Connect (NC) flags** – Place an NC symbol on every pin that is not
  electrically connected. This forces the Electrical Rule Check (ERC) to
  flag any accidental net that lands on a supposedly unused pin.  
  *Benefit:* Guarantees that every pin has been deliberately considered.  
  **[Verified]**

- **Workflow tip:** In most ECAD tools the shortcut `Q` (or the equivalent
  “Place NC” command) inserts the flag quickly. After adding NC flags,
  run ERC to confirm that no stray connections remain.

---

## 2. Visual Grouping with Bounding Boxes  

When a schematic spans several pages or contains many functional blocks,
draw rectangular frames around related groups (e.g., power‑regulation,
sensor interface, debug header).  

- Use the **“Add Connected Graphic Lines”** tool (often bound to `I`) to
  create the box, then label it with a concise title (e.g., *5 V → 3.3 V
  LDO*).  
- Bounding boxes act as visual cues during design reviews and make it
  easier to locate a subsystem when discussing the schematic with
  colleagues.  

**[Verified]**

---

## 3. Annotate Design Intent with Text Fields  

### 3.1. Component Calculations  

For critical passive values, add a short note that shows the underlying
calculation. Example for an LED‑current‑limiting resistor:

```
R = (VCC – VF) / IF = (3.3 V – 1.8 V) / 7 mA ≈ 220 Ω
```

Embedding the math in the schematic eliminates the need to revisit the
datasheet later and documents the design rationale for future revisions.  

**[Verified]**

### 3.2. Section Descriptions  

Place a brief description at the top of each page (or within each bounding
box) summarising its purpose, such as *“Boot‑Zero switch and associated
debug header”*. This aids rapid navigation and clarifies intent for reviewers
who may not be familiar with the project.  

**[Verified]**

---

## 4. Title Block and Revision Management  

Every schematic should contain a populated title block that includes:

| Field | Recommended Content |
|-------|----------------------|
| **Document Title** | Short, descriptive name (e.g., *Main Board Schematic*) |
| **Revision** | Incremental identifier (A, B, … or 1.0, 1.1) |
| **Date** | ISO‑8601 format (YYYY‑MM‑DD) |
| **Author / Owner** | Name(s) of the designer(s) |
| **Project / Part Number** | Reference to the overall product |

Most ECAD packages allow double‑clicking the title block to edit these
fields directly. Maintaining accurate revision data prevents confusion
when multiple engineers are working on the same design.  

**[Verified]**

---

## 5. Component Annotation and Part Numbering  

### 5.1. Consistent Prefixes  

Adopt a clear naming convention for reference designators:

| Prefix | Typical Use |
|--------|--------------|
| **U** | Integrated circuits (MCU, regulators, etc.) |
| **R** | Resistors |
| **C** | Capacitors |
| **J** | Connectors (e.g., J1, J2, J3) |
| **L** | Inductors |
| **D** | Diodes / LEDs |

The ECAD tool usually auto‑assigns numbers as components are placed.
After the schematic is complete, run an **annotation** pass to ensure
sequential ordering (e.g., R1, R2, …) and to resolve any gaps caused by
deleted parts.  

**[Verified]**

### 5.2. Linking to Real Parts  

For passive components the schematic symbol only carries a value.
Before moving to layout, each symbol must be linked to a **real component
definition** that includes:

- Manufacturer part number (or generic description)
- Package type (e.g., 0805, 1206, 0603)
- Electrical ratings (voltage, tolerance, temperature range)
- Material class (MLCC, X7R, C0G, etc.)

This linkage enables the ECAD tool to automatically assign the correct
footprint during the **Footprint Assignment** stage.  

**[Verified]**

---

## 6. Preparing for Footprint Assignment  

### 6.1. Verify Component Types  

Passive values (e.g., “100 nF”) are ambiguous without a package spec.
Decide early whether the capacitor will be an **MLCC 0805**, a **tantalum
1206**, or another type. The choice impacts:

- **Board space** – Smaller packages increase density but may be harder
  to hand‑solder.  
- **Electrical performance** – MLCCs have lower ESR, which matters for
  high‑frequency decoupling.  
- **Cost** – Larger packages are typically cheaper in high volumes.  

**[Inference]**

### 6.2. Capture Additional Attributes  

For each component, record:

- **Voltage rating** (must exceed the highest node voltage it will see).  
- **Temperature rating** (especially for automotive or industrial
  environments).  
- **ESD protection class** for connectors and I/O pins.  

These attributes become part of the **BOM** and guide the manufacturer’s
selection of parts that meet reliability requirements.  

**[Verified]**

---

## 7. From Schematic to PCB – The Hand‑off  

The PCB fabricator receives only the **netlist**, **footprint data**, and
the **assembly drawing**. A clean schematic ensures that:

1. **All nets are intentional** – No stray connections survive ERC.  
2. **Component footprints match the intended packages** – Prevents
   mismatches that would cause assembly re‑work.  
3. **Design intent is documented** – Text notes and bounding boxes help
   the layout engineer understand power‑domain separation, critical
   signal paths, and any special handling (e.g., keep‑out zones).  

**[Verified]**

---

## 8. Summary Flowchart  

The diagram below visualises the recommended cleanup sequence before
footprint assignment.

```mermaid
flowchart TD
    A[Complete initial schematic] --> B[Add No‑Connect flags]
    B --> C[Run ERC & resolve warnings]
    C --> D[Draw bounding boxes for functional blocks]
    D --> E[Insert explanatory text (calculations, section titles)]
    E --> F[Populate title block (date, revision, author)]
    F --> G[Run annotation to enforce reference‑designator scheme]
    G --> H[Define real component attributes (package, rating, manufacturer)]
    H --> I[Link symbols to footprints]
    I --> J[Ready for PCB layout]
```

---

## 9. Practical Tips & Common Pitfalls  

| Pitfall | Mitigation |
|---------|------------|
| **Floating pins left unmarked** | Use NC flags on every unused pin; run ERC after each addition. |
| **Inconsistent naming (e.g., R01 vs R1)** | Enforce a naming policy via the ECAD tool’s annotation settings. |
| **Missing package information for passives** | Create a component library entry that includes both value and package before schematic entry. |
| **Out‑of‑date title block** | Update the title block immediately after any major change; treat it as part of the design checklist. |
| **Over‑crowded schematic pages** | Split large designs into logical pages and use cross‑references (e.g., “See Page 3 – Power Section”). |

---

## 10. References & Further Reading  

- **Capacitor Selection Basics** – Video #114 (covers dielectric types,
  DC‑bias derating, temperature effects).  
- **PCB Design for Manufacturability (DFM)** – Recommended reading for
  understanding how schematic decisions influence fabrication yield.  

*End of “Cleaning Up the Schematic” documentation.*