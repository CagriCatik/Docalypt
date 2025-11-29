# 38 – Gerber Generation & Verification  

*This section documents the complete workflow for exporting, validating, and packaging Gerber and drill data ready for PCB fabrication. It captures the key decisions, constraints, and best‑practice recommendations that ensure a smooth hand‑off to the manufacturer.*

---  

## 1. Overview  

The Gerber export stage translates the PCB layout into the industry‑standard vector files that describe every physical layer of the board (copper, mask, paste, silkscreen, and outline). A complementary Excellon drill file set describes all plated‑through holes (PTH) and non‑plated‑through holes (NPTH). After export, each file must be inspected with a Gerber viewer to catch hidden errors before the data are zipped and sent to the fab house.

---  

## 2. Gerber Export Settings  

| Setting | Recommended Value | Rationale |
|---------|-------------------|-----------|
| **Output directory** | `manufacturing/` (or a similarly named folder) | Keeps fabrication data separate from design sources, reducing the risk of accidental modification. |
| **Units** | Millimetres (mm) | Most manufacturers accept mm; it matches the typical mechanical drawing convention. |
| **File format** | RS‑274X (extended Gerber) | Embeds aperture definitions, eliminating the need for separate aperture files. |
| **Layer selection** | • All copper layers (top, inner, bottom)  <br>• Top solder‑mask (bottom mask optional)  <br>• Top paste (bottom paste omitted)  <br>• Front silkscreen (bottom silkscreen omitted)  <br>• Edge‑cut (board outline) | The board in this example has no components on the bottom side, so bottom paste and silkscreen are unnecessary, reducing file count and avoiding confusion for the fab. |
| **Plot options** | *Do not* plot footprint values or reference designators | Keeps the Gerbers clean; the fab does not need textual data that belong in the assembly files. |
| **Origin** | Use the *drill place file origin* (same origin for Gerbers and drills) | Guarantees that the drill data line up perfectly with the copper layers. |
| **Drill file options** | • Separate files for PTH and NPTH  <br>• Units = mm  <br>• Default drill tolerance (leave at standard) | Splitting PTH/NPTH simplifies fab quoting and lets the fab apply different plating processes. |

> **Note:** All of the above settings are widely supported by major PCB houses and are considered *best practice* for most low‑ to medium‑complexity designs.  [Verified]

---  

## 3. Layer‑Selection Rationale  

1. **Copper layers** – Every conductive plane must be exported; missing an inner layer will cause an open circuit.  
2. **Solder mask** – Only the top mask is required because the bottom side contains no surface‑mount parts; omitting the bottom mask reduces the chance of mask‑related defects (e.g., mask slivers covering pads that never exist).  
3. **Paste layer** – Paste is needed only where stencil apertures will be generated. Since the board has no bottom‑side SMD parts, the bottom paste layer is unnecessary.  
4. **Silkscreen** – Front silkscreen is retained for component reference on the populated side; a bottom silkscreen would be invisible after assembly and could cause confusion.  
5. **Edge‑cut** – The outline defines the board shape and must be present; it is often called the *mechanical layer* in the CAD tool.  

These choices reflect a **cost‑vs‑complexity trade‑off**: fewer layers mean fewer files to manage and a lower chance of mismatched data, while still providing all information the fab needs.  [Inference]

---  

## 4. Drill File Generation  

The Excellon drill files are generated after the Gerbers:

* **Plated‑through holes (PTH)** – Used for signal and power interconnects; the fab will plate the copper walls.  
* **Non‑plated‑through holes (NPTH)** – Typically for mounting hardware, clearance holes, or slots; no plating is applied.  

Key parameters:

* **Units** – Millimetres (consistent with Gerbers).  
* **Zero suppression** – Use *leading* zero suppression (default) unless the fab specifies otherwise.  
* **Tool table** – Let the CAD tool auto‑generate; verify that each drill size matches the component library (e.g., 0.3 mm for standard vias, 0.8 mm for mounting holes).  

> **Tip:** Keep the drill file names explicit, e.g., `board_pth.drl` and `board_npth.drl`, to avoid ambiguity during fab quotation.  [Verified]

---  

## 5. Gerber Verification Workflow  

Even a perfectly configured export can hide subtle errors (e.g., missing pads, incorrect mask clearance). A systematic visual check with a Gerber viewer is essential.

```mermaid
flowchart TD
    A[Export Gerbers & Drill Files] --> B[Create ZIP archive]
    B --> C[Open Gerber Viewer]
    C --> D[Hide all layers]
    D --> E[Iteratively enable each layer]
    E --> F[Inspect copper, mask, paste, silk, outline]
    F --> G[Cross‑check drill holes (PTH/NPTH) against copper]
    G --> H[Confirm alignment with origin]
    H --> I[Fix any issues in CAD]
    I --> J[Re‑export & repeat verification]
    J --> K[Finalize archive for fab]
```

**Step‑by‑step checklist**

1. **Hide all layers** – Provides a clean slate.  
2. **Enable one layer at a time** – Start with the top copper, then inner layers, bottom copper, mask layers, paste, silkscreen, and finally the edge‑cut.  
3. **Zoom to critical features** – Verify that via pads, component footprints, and clearance holes appear correctly.  
4. **Inspect drill overlays** – Turn on the drill layer to ensure that all holes land on copper where required (e.g., PTH on signal nets) and that NPTH holes avoid copper.  
5. **Look for “orphan” geometry** – Small stray polygons often indicate a misplaced pad or an incomplete zone fill.  
6. **Check board outline** – Confirm that the edge‑cut matches the intended mechanical dimensions and that there are no stray lines outside the outline.  

> **Why this matters:** The Gerber viewer renders the data in a different visual context than the layout editor, often exposing errors that are invisible in the CAD environment.  [Verified]

---  

## 6. Packaging for Manufacture  

1. **Collect files** – Place the following items into a single folder (commonly named `manufacturing/`):  
   * All Gerber files (`*.gbr` or `*.gtl`, `*.gbl`, `*.gts`, `*.gbs`, `*.gto`, `*.gbo`, `*.gm1`, etc.)  
   * Drill files (`*.drl` for PTH, `*.txt` or `*.drl` for NPTH)  
   * Pick‑and‑place file (usually CSV or IPC‑2581)  
   * Bill of Materials (BOM) – optional but highly recommended for assembly quotes  
2. **Compress** – Create a ZIP archive (or the format required by the fab). The archive name should include the project identifier and revision, e.g., `projX_rev2.zip`.  
3. **Verify archive contents** – Open the ZIP and confirm that no extra files (e.g., intermediate PDFs, simulation results) are present; only the fabrication‑essential files should be shipped.  

> **Best practice:** Keep a copy of the exact ZIP that was sent to the fab in your version‑control system. This provides an immutable record for future reference or re‑order.  [Verified]

---  

## 7. Common Pitfalls & DFM Tips  

| Pitfall | Impact | Mitigation |
|---------|--------|------------|
| **Missing bottom paste/silkscreen** when a component later migrates to the bottom side | Unmanufacturable board (no stencil, no reference) | Review component placement before final export; keep optional layers in the CAD file even if they are disabled for the current build. |
| **Incorrect drill origin** (e.g., using layout origin instead of drill origin) | Misaligned holes, potential short circuits | Always select “drill place file origin” for both Gerbers and drills. |
| **Zero‑suppression mismatch** between CAD export and fab requirement | Drill file mis‑interpreted, leading to wrong hole sizes | Confirm the fab’s preferred zero‑suppression mode (leading vs. trailing) and set it explicitly. |
| **Mask clearance too tight** for fine‑pitch components | Mask slivers causing solder defects | Apply a minimum mask clearance (typically 0.1 mm) in the design rules; verify with the Gerber viewer’s mask overlay. |
| **Unfilled copper zones** (e.g., missing thermal reliefs) | Poor heat dissipation, possible copper delamination | Run a *zone fill* check in the CAD tool before export; enable “fill all zones” option. |
| **Incorrect file naming** (e.g., swapping top/bottom copper) | Fab confusion, increased lead time | Follow the manufacturer’s naming convention (e.g., `*_top.gtl`, `*_bottom.gbl`). |

> **Design‑for‑Manufacturability (DFM) Insight:** Reducing the number of unique aperture shapes (e.g., standardizing pad sizes) simplifies the photoplotting process and can lower fab cost.  [Inference]

---  

## 8. Summary  

Exporting Gerbers and drill files is a deterministic process, but it requires disciplined configuration, thorough visual verification, and careful packaging. By:

* Selecting only the necessary layers (top paste, front silkscreen, top/bottom mask, all copper, edge‑cut)  
* Using a consistent origin and metric units  
* Generating separate PTH/NPTH drill files  
* Inspecting each layer in a Gerber viewer  
* Archiving the exact set of fabrication files  

you minimize the risk of costly re‑spins and ensure a smooth transition from design to production.  

Adhering to the outlined DFM recommendations further improves yield and reduces overall board cost.  

---