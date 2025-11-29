# Bill of Materials (BoM) & Pick‑and‑Place (CPL)

## 1. Overview  

A **Bill of Materials (BoM)** lists every component required to assemble a board, together with the exact part numbers, manufacturers, and sourcing links.  
A **Pick‑and‑Place (CPL) file** (also called a component‑placement file) provides the X‑Y coordinates, rotation, and layer for each part so that automated assembly equipment can locate and place the components accurately.  

Both files are essential deliverables for a PCB contract manufacturer (PCB fab) and a contract assembler (CFA). The BoM tells the assembler *what* to buy, while the CPL tells the assembly line *where* to put each part on the board.  

---

## 2. BoM Generation  

### 2.1 Adding Custom Fields to the Schematic  

| Field | Purpose |
|-------|---------|
| **Manufacturer** | Human‑readable name of the component maker. |
| **Manufacturer Part Number (MPN)** | Exact part identifier used by the supplier. |
| **Distributor Link** | URL to the component’s purchase page (e.g., Digi‑Key, Mouser). |

These fields are added via the **Bulk Edit → Fields** dialog in the schematic editor. After populating them, they become part of each component’s metadata and can be exported automatically.  

> **Why custom fields?**  
> The default KiCad BoM generators only output generic columns (designator, value, footprint). Adding manufacturer‑specific columns removes the need for manual post‑processing and reduces the risk of part‑mix‑ups during assembly. [Verified]

### 2.2 Exporting the BoM  

1. **Tools → Generate Bill of Materials**.  
2. Choose the **custom Python script** placed in the *plugins* folder. The script appends the three custom columns (Manufacturer, MPN, Distributor) to the header and pulls the per‑component values from the schematic. [Verified]  
3. Click **Generate**, then **Close**.  
4. The output file appears in the project directory as `<project_name>-bom.csv`.  

Typical CSV columns (example row):  

```
Designator,Footprint,Value,Manufacturer,MPN,Distributor
U1,QFP-64,STM32F407,STMicroelectronics,STM32F407VGT6,https://www.digikey.com/product-detail/...
C3,0603,0.1µF,TDK,CGJ3E2X7R1H104K,https://www.mouser.com/ProductDetail/...
```

> **Excluding non‑assembly items** – Fiducials, mounting holes, and mechanical test points are deliberately omitted from the BoM because they are not purchased components. [Verified]

### 2.3 BoM Best Practices  

| Recommendation | Rationale |
|----------------|-----------|
| **Keep the MPN exact** – Do not truncate or re‑format part numbers. | Guarantees that the assembler orders the correct device. [Verified] |
| **Provide a single distributor link** – Prefer a global distributor that ships to the assembly location. | Simplifies procurement and reduces lead‑time. [Inference] |
| **Group by placement side** (top vs. bottom) if the board is double‑sided. | Helps the assembler stage parts for separate pick‑and‑place heads. [Speculation] |
| **Version‑control the BoM** – Store the CSV alongside the project files in Git or another VCS. | Enables traceability of component changes across revisions. [Inference] |
| **Validate the BoM against the schematic** using KiCad’s **ERC** and **DRC** checks before export. | Catches missing fields or mismatched footprints early. [Verified] |

---

## 3. Component Placement (Pick‑and‑Place) File  

### 3.1 Defining the Placement Origin  

The **origin (datum)** for all placement coordinates should be set to the **bottom‑left corner of the board outline**.  

* In the PCB editor, set **Grid Origin → Bottom‑Left**.  
* Also set **Place File Origin → Bottom‑Left** so that the exported coordinates match the datum used by the assembly line. [Verified]  

Choosing the board’s lower‑left corner as the datum is a de‑facto industry standard because most pick‑and‑place machines expect a consistent reference point for X‑Y positioning. [Inference]

### 3.2 Exporting the CPL  

1. **File → Fabrication Outputs → Component Placement (CPL)**.  
2. Choose an output directory (e.g., `manufacturing/` or a dedicated `assembly/` folder).  
3. Select the **format** – either **ASCII (TXT)** or **CSV**. The tutorial uses **ASCII** for readability. [Verified]  
4. Set **Units** to **millimeters** (most assembly houses require metric).  
5. If the board is single‑sided, leave the **Top‑Side Only** radio button selected; otherwise, generate separate files for each side. [Verified]  
6. Click **Generate**.  

The resulting file (e.g., `project‑cpl.txt`) contains one line per component:

```
Designator   Value   Package   X(mm)   Y(mm)   Rotation   Layer
U1           STM32F4 QFP-64    45.12   30.45   0          Top
C3           0.1uF   0603      12.34   78.90   90         Top
```

* **X/Y** – Center of the component pad(s) relative to the datum.  
* **Rotation** – Angle (in degrees) of the component’s reference orientation.  
* **Layer** – `Top` or `Bottom`.  

> **Why include rotation?**  
> The pick‑and‑place head must know the exact orientation to place the component correctly, especially for polarized parts (diodes, electrolytic caps, ICs with a defined pin‑1). [Verified]

### 3.3 Interpreting the CPL  

* **Designator** links the placement entry back to the BoM row.  
* **Package** must match the footprint used in the layout; any mismatch will cause a placement error.  
* **Layer** informs the machine whether to use the top‑side or bottom‑side head (or a flip‑over operation).  

A mismatch between BoM and CPL (e.g., a missing designator) will be flagged by the assembler’s **CPL‑BoM cross‑check** and must be resolved before production. [Inference]

---

## 4. Integrating BoM, CPL, and Fabrication Data  

A typical hand‑off package for a contract manufacturer looks like this:

```
manufacturing/
├─ gerbers/          ← Layer data (copper, soldermask, silkscreen, paste)
├─ drill/            ← NC drill files
├─ project-bom.csv   ← Complete Bill of Materials
├─ project-cpl.txt   ← Component placement (pick‑and‑place) file
└─ readme.txt        ← Assembly instructions, notes on special handling
```

* **Gerbers** provide the physical board definition.  
* **Drill files** define via and mounting‑hole locations.  
* **BoM** tells the assembler which parts to procure.  
* **CPL** tells the assembler where to place each part.  

All files should be **zipped** and sent together to avoid version mismatches. [Verified]

---

## 5. Common Pitfalls & Recommendations  

| Issue | Symptom | Remedy |
|-------|---------|--------|
| **Origin mismatch** | Components appear shifted on the assembly line. | Verify that both *Grid Origin* and *Place File Origin* are set to **Bottom‑Left** before export. [Verified] |
| **Missing custom fields** | BoM lacks manufacturer or distributor data. | Ensure the custom Python script is selected in the BoM generator and that each schematic symbol has the fields filled. [Verified] |
| **Incorrect rotation** | Parts placed upside‑down or with pins mis‑aligned. | Double‑check the rotation column in the CPL; re‑export after correcting any manual edits in the PCB editor. [Inference] |
| **Fiducials omitted from CPL** (but needed for alignment) | Assembly machine cannot locate reference points. | Export a separate **fiducial placement file** if the assembler requires it, or include fiducials in the CPL with a distinct layer label. [Speculation] |
| **Unit inconsistency** | X/Y values interpreted as inches instead of mm. | Confirm that the CPL export unit is set to **millimeters** and that the assembler’s import settings match. [Verified] |
| **Package mismatch** | Pick‑and‑place head reports “footprint not found”. | Ensure the **Package** column matches the exact footprint name used in the PCB layout (case‑sensitive). [Verified] |

---

## 6. Process Flow (Mermaid Diagram)

```mermaid
flowchart TD
    A[Schematic Design] --> B[Add Custom Fields (Mfg, MPN, Distributor)]
    B --> C[Generate BoM CSV (custom script)]
    A --> D[PCB Layout]
    D --> E[Set Origin (Bottom‑Left)]
    E --> F[Export CPL (ASCII/CSV, mm)]
    D --> G[Export Gerbers & Drill Files]
    C --> H[Package for Manufacturer]
    F --> H
    G --> H
    H --> I[Contract PCB Fab & Assembly]
```

*The diagram illustrates the sequential generation of the BoM, CPL, and fabrication data, and how they converge into a single manufacturing package.* [Inference]

---

## 7. Summary  

* Populate **Manufacturer**, **MPN**, and **Distributor** fields directly in the schematic to automate a complete BoM.  
* Use a **custom BoM script** to include those fields in the exported CSV.  
* Set the **placement datum** to the board’s bottom‑left corner before exporting the CPL.  
* Export the CPL in **ASCII or CSV**, with units in **millimeters**, and verify that rotation and layer information are correct.  
* Assemble a **single zip** containing Gerbers, drill files, BoM, and CPL, and provide clear read‑me instructions to the contract manufacturer.  

Following these practices ensures a smooth transition from design to production, minimizes manual data entry errors, and reduces the risk of costly re‑work during assembly. [Verified]