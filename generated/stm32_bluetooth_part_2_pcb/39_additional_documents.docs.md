# 39 Additional Documents for PCB Fabrication & Assembly  

*This section describes the supplemental documentation that should accompany a PCB design when it is handed off to a fabricator/assembler. The goal is to convey all mechanical, electrical, and manufacturability requirements that cannot be inferred from the Gerber files alone.*  

---  

## Overview  

When a board is ready for production the design data set normally consists of:

| Item | Typical File Type | Primary Purpose |
|------|-------------------|-----------------|
| **Gerbers** | `.gbr` | Layer images (copper, soldermask, silkscreen, drill, edge‑cuts) |
| **Drill & Via Data** | `.drl` | Hole locations and sizes |
| **Bill of Materials (BOM)** | `.csv` / `.xls` | Parts list, part numbers, footprints |
| **Pick‑and‑Place (Centroid) File** | `.pos` | Automated assembly coordinates |
| **Assembly Drawing** | `.pdf` | Human‑readable component locations, orientations, notes |
| **Manufacturing Information Document** | `.txt` / `.pdf` | Board dimensions, stack‑up, surface finish, impedance specs, IPC references |

The Gerbers convey the *what* (the physical patterns), while the assembly drawing and manufacturing information document convey the *how* and *why* – e.g., which side is “top”, how to orient polarized components, and which traces must meet controlled‑impedance targets. Supplying these documents reduces the need for back‑and‑forth clarification and helps the fab/assembler meet performance and reliability goals on the first try.  

---  

## Assembly Drawing  

### What it Contains  

- **Top‑ and bottom‑view renderings** of the finished board.  
- **Component designators** (e.g., `U1`, `R12`) placed at the exact footprint location.  
- **Pin‑1 / polarity markers** for ICs, connectors, diodes, and polarized passives.  
- **Orientation arrows** (e.g., “⟳” for clockwise rotation) when the board is viewed from the component side.  
- **Critical assembly notes** (e.g., “handle with care – exposed pad”, “solder paste only on pads 1‑4”).  
- **Edge‑cut outline** to verify board size and keep‑out zones.  

> **How to generate (KiCad example)** – Open the **Plot** dialog, enable the *Fabrication* layer (`F.Fab`/`B.Fab`) and the *Edge‑Cuts* layer, then plot to PDF. The resulting file is a minimal assembly drawing that already includes designators and pin‑1 markers extracted from the footprints.  

### Best‑Practice Tips  

- **Include both sides** even if components are only on one side; this helps the assembler verify “no‑pop” solder‑mask clearance.  
- **Add manual notes** directly in the PDF (e.g., using a PDF editor) for parts that require special handling such as heat‑sensitive devices or high‑current MOSFETs.  
- **Keep the drawing legible**: use a line weight that prints clearly at 1:1 scale; avoid overly dense silkscreen that can obscure designators.  

[Verified]  

---  

## Manufacturing Information Document  

### Core Content  

| Section | Typical Content |
|---------|-----------------|
| **General Board Data** | Overall dimensions, thickness, number of layers, material (e.g., FR‑4, Rogers), surface finish (HASL, ENIG, OSP). |
| **Stack‑up Description** | Layer order, dielectric thicknesses, copper weight per layer, reference planes. |
| **Impedance Control Requirements** | Target impedance (e.g., 50 Ω single‑ended, 90 Ω differential), tolerance (commonly ±10 %), trace geometry (microstrip / stripline), reference layer, assumed trace width/spacing. |
| **Special Fabrication Notes** | IPC standard(s) to follow (e.g., IPC‑2221, IPC‑6012), required copper‑weight tolerances, minimum annular ring, via fill requirements, solder‑mask clearance rules. |
| **Assembly Constraints** | Preferred component placement orientation, keep‑out zones for heat‑sensitive parts, required solder‑paste thickness, optional conformal‑coat instructions. |
| **Verification Requests** | “Please confirm that the 50 Ω microstrip on layer 1 (reference layer 2) will be achieved with the supplied stack‑up” – a request for the fab to validate the impedance calculation. |

> The document can be a simple plain‑text file (`manufacturing.txt`) placed alongside the Gerber zip. Most fab portals accept arbitrary supporting files and will forward them to the production engineer.  

### Controlled‑Impedance Example (Illustrative)  

```
IMPEDANCE CONTROL
-----------------
1. Single‑ended 50 Ω microstrip
   • Layer: 1 (top copper)
   • Reference: Layer 2 (ground plane)
   • Target width: 0.19 mm  (calculated for 1.6 mm FR‑4, 35 µm copper)
   • Tolerance: ±10 %
   • Ground fill: 0.5 mm clearance from trace edges

2. Differential 90 Ω microstrip pair
   • Layer: 1
   • Reference: Layer 2
   • Target width: 0.19 mm, spacing: 0.15 mm
   • Tolerance: ±10 %
   • Single‑ended 50 Ω requirement also applies to each line.
```

> The numbers above are taken from the example in the source material; they illustrate how to convey the designer’s expectations without prescribing the exact stack‑up.  

[Verified]  

---  

## Integrating the Documents into the Production Package  

1. **Create a dedicated folder** (e.g., `production_package`).  
2. **Copy all Gerber files**, drill file, and the **pick‑and‑place** file into the folder.  
3. **Add the assembly drawing PDF** (`assembly_drawing.pdf`).  
4. **Add the manufacturing information document** (`manufacturing.txt` or `manufacturing.pdf`).  
5. **Compress the folder** into a zip archive (`myboard_v1.zip`).  
6. **Upload** the zip to the fab’s portal, ensuring the upload UI shows the auxiliary files (some portals have a “Supporting Documents” field).  

> Even for quick‑turn services that claim “Gerbers are enough”, providing the assembly drawing and a short manufacturing note is considered good practice and often prevents costly re‑spins.  

[Inference]  

---  

## Best‑Practice Checklist  

| ✔️ Item | Reason |
|--------|--------|
| **Assembly drawing** (top & bottom) | Enables manual verification, reduces placement errors. |
| **Manufacturing information file** | Communicates stack‑up, impedance, and IPC standards. |
| **Explicit layer naming** (e.g., `F.Cu`, `B.Cu`, `F.Fab`) | Prevents misinterpretation by the fab’s CAM software. |
| **Clear tolerance statements** for impedance | Gives the fab a quantitative target to meet. |
| **Reference to IPC standards** (e.g., IPC‑2221) | Aligns expectations on drill tolerances, copper‑weight, etc. |
| **Ground‑fill / copper‑pour specifications** for high‑speed zones | Improves return‑path integrity and reduces EMI. |
| **Verification request** (e.g., “confirm 50 Ω microstrip”) | Encourages the fab to run a signal‑integrity check before production. |
| **Version control** (file naming with revision) | Avoids mix‑ups between design iterations. |

---  

## Common Pitfalls & Mitigations  

| Pitfall | Symptom | Mitigation |
|---------|---------|------------|
| **Missing pin‑1 markers** | Assembler rotates ICs incorrectly, leading to functional failure. | Include pin‑1 arrows in the assembly drawing and verify footprint libraries contain the marker. |
| **Impedance spec only in the BOM** | Fab assumes default FR‑4 stack‑up and produces mismatched trace widths. | Add a dedicated “Impedance Control” section in the manufacturing document. |
| **Edge‑cut not exported** | Board is cut to the wrong size, causing component overhang. | Ensure the *Edge‑Cuts* layer is plotted and included in the zip. |
| **Ambiguous layer count** | Fab produces a 2‑layer board when 4 layers were intended. | State the exact layer count and provide a stack‑up diagram. |
| **No IPC reference** | Fab applies generic tolerances that may be too loose for high‑frequency designs. | Cite the relevant IPC standard (e.g., IPC‑2221 for generic PCB, IPC‑6012 for high‑reliability). |

---  

## Example Flowchart  

The following diagram shows the typical hand‑off flow, highlighting where the additional documents are introduced.  

```mermaid
flowchart TD
    A[Design Completion] --> B[Generate Gerbers & Drill]
    B --> C[Create Pick‑and‑Place File]
    C --> D[Produce Assembly Drawing]
    D --> E[Write Manufacturing Info Document]
    E --> F[Package All Files (ZIP)]
    F --> G[Upload to Fabricator]
    G --> H[Fabrication & Assembly]
    H --> I[First‑Article Inspection]
    I --> J[Release for Production]
```

---  

## References & Further Reading  

- **IPC‑2221** – Generic Standard on Printed Board Design.  
- **IPC‑6012** – Qualification and Performance Specification for Rigid PCBs.  
- **High‑Speed Digital Design: A Handbook of Black Magic** (Howard Johnson) – Chapter on controlled‑impedance routing.  
- **KiCad Documentation – Plotting & Export** – Guidance on generating fabrication layers and PDFs.  

---  

*End of Chapter 39 – Additional Documents*