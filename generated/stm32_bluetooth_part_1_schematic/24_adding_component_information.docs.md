# Adding Component Information  

*Providing complete, accurate part data is a cornerstone of a reliable design‑to‑manufacture (DTM) flow. The following guidelines describe how to enrich schematic symbols with manufacturer‑specific metadata, manage non‑component items, and generate a production‑ready Bill of Materials (BOM).*

---

## 1. Why Enrich Symbol Fields?  

- **Assembly & Procurement:**  Manufacturer name, part number, and distributor URL allow the assembly house to source exact components without manual lookup.  
- **Design‑for‑Manufacturability (DFM):**  Explicit part numbers make it easy to verify that the selected footprints match the physical package and that the parts meet cost, availability, and reliability targets.  
- **Traceability:**  In regulated or safety‑critical projects, a complete parts traceability matrix is often required for certification.  

> The practice of storing this data directly on the schematic symbol is **verified** in modern PCB design tools and aligns with industry‑standard DFM workflows.  

---

## 2. Bulk Editing Symbol Fields  

Most schematic editors (e.g., KiCad) provide a *Bulk Edit* dialog that presents all symbols in a tabular view:

| Ref‑Des | Value | Footprint | Qty | **Manufacturer** | **Mfg‑Part‑No** | **Distributor Link** |
|--------|-------|-----------|-----|------------------|----------------|----------------------|

1. **Open the bulk‑edit window** from the schematic editor toolbar.  
2. **Add custom columns** for the three fields above (or any additional data such as RoHS status, temperature rating, etc.).  
3. **Save the table** – the editor writes the values back to each symbol’s property list.

> This bulk‑edit approach eliminates the tedious per‑symbol editing and guarantees that every part in the design carries the same set of metadata. `[Verified]`

---

## 3. Populating Manufacturer Data  

### 3.1 Source of Information  

- **Distributor Catalogues** (Mouser, Digi‑Key, Arrow, etc.) provide the most up‑to‑date manufacturer part numbers and a permanent URL to the product page.  
- **Manufacturer Datasheets** contain the definitive part number and often a “preferred distributor” link.  

### 3.2 Workflow  

```mermaid
flowchart TD
    A[Open Distributor Site] --> B[Search by Value/Footprint]
    B --> C[Copy Manufacturer Part Number]
    C --> D[Copy Distributor URL]
    D --> E[Paste into Symbol Fields]
    E --> F[Repeat for All Parts]
    F --> G[Export BOM (CSV)]
```

1. Locate the component on the chosen distributor site.  
2. Copy the **Manufacturer** name, **Manufacturer Part Number**, and the **Distributor URL**.  
3. Paste these values into the corresponding columns of the bulk‑edit table.  

> Using a single, preferred distributor simplifies cost comparison and reduces the risk of “out‑of‑stock” surprises during production. `[Inference]`

### 3.3 Preferred‑Brand Strategy  

When a design team has a **preferred brand** (e.g., a specific resistor series), pre‑populate the table with those part numbers. This ensures component consistency across multiple projects and can leverage volume pricing agreements.  

---

## 4. Library Considerations  

Ideally, the **manufacturer data should live in the component library** so that every instance of the part automatically inherits the correct fields.  

- **Current KiCad behavior:**  Some libraries omit these fields, requiring manual entry per design.  
- **Best practice:**  Create or edit library symbols to include the three custom fields as default values. This makes the data **portable** across projects and reduces the chance of missing entries.  

> Adding these fields to the library is a **recommended improvement** to the standard KiCad workflow, even though the tool does not enforce it by default. `[Inference]`

---

## 5. Excluding Non‑Component Items from the BOM  

Certain footprints, such as **tag‑connect headers** or test points, are **mechanical aids** rather than parts that need to be purchased.  

- In the symbol properties, enable the **“Exclude from BOM”** flag.  
- The footprint will still appear on the PCB layout (providing the necessary pads or holes) but will be omitted from the exported BOM.  

> This prevents the assembly house from ordering unnecessary hardware and keeps the BOM clean. `[Verified]`

---

## 6. Exporting the BOM  

After all fields are populated:

1. Use the schematic editor’s **BOM export** function.  
2. Choose **CSV** (or the format required by the assembly house).  
3. Verify that the exported columns include: Ref‑Des, Quantity, Manufacturer, Part Number, Distributor Link, and any custom fields needed for cost or compliance analysis.  

The resulting CSV can be directly uploaded to most **PCB assembly portals**, where it drives the **pick‑and‑place** and **procurement** processes.

---

## 7. Practical Tips & Trade‑offs  

| Consideration | Impact | Recommendation |
|---------------|--------|----------------|
| **Component Availability** | Low‑stock parts cause delays. | Prefer parts with long lead‑times and multiple distributors. |
| **Cost vs. Preferred Brand** | Premium brands increase BOM cost. | Use preferred brand for critical functions; select cost‑effective equivalents for non‑critical parts. |
| **Library Maintenance Effort** | Adding fields to every library symbol is time‑consuming. | Create a **master parts database** (e.g., Excel or a PLM system) and sync it with the schematic via bulk‑edit. |
| **Data Consistency** | Manual entry can introduce typos. | Use copy‑paste from distributor pages or automate with a small script that queries the distributor API. |
| **Regulatory Traceability** | Required for medical, aerospace, etc. | Keep a separate column for **RoHS**, **REACH**, or **MIL‑SPEC** compliance flags. |

> Balancing **design flexibility** with **manufacturing predictability** is a core DFM decision. Maintaining accurate part metadata early in the design cycle pays off by reducing change‑order cycles and assembly errors. `[Inference]`

---

## 8. Summary Checklist  

| ✅ | Action |
|---|--------|
| Bulk‑edit schematic symbols to add **Manufacturer**, **Mfg‑Part‑No**, **Distributor Link** fields. |
| Populate each field from a trusted distributor catalogue. |
| Mark mechanical-only footprints (e.g., tag‑connect headers) as **Exclude from BOM**. |
| Export a **CSV BOM** that includes all enriched fields. |
| (Optional) Extend component libraries to store these fields by default for future projects. |

By following this workflow, the design team ensures a **complete, accurate, and assembly‑ready BOM**, streamlines procurement, and minimizes the risk of costly production surprises.