# Ground Planes  

Ground planes are the backbone of a robust PCB stack‑up.  They provide a low‑impedance return path, improve signal integrity, reduce electromagnetic interference (EMI), and aid thermal management.  This section details the practical workflow for creating copper‑filled ground zones, the key electrical properties that must be defined, and the best‑practice considerations for multi‑layer boards.

---

## 1. Creating a Ground‑Plane Zone  

1. **Activate the “Add Filled Zone” tool** – typically invoked with **Shift + Z**.  
2. **Select the target copper layer** (e.g., *Layer 1 – Front Copper*).  
3. **Assign the net** that will be the ground reference (commonly named **GND**).  
4. **Configure the zone’s electrical properties** (see §2).  
5. **Draw the polygon outline** by clicking to place vertices; the shape does **not** need to follow the exact board contour—rough geometry is sufficient because the zone will be repoured later.  
6. **Repour the zone** (shortcut **B**) to fill the defined area with copper.

> The workflow above mirrors the standard zone‑creation process in most ECAD tools and ensures that the ground plane respects the design‑rule constraints set in step 4. [Verified]

---

## 2. Defining Electrical Properties  

| Property | Typical Setting (from example) | Rationale |
|----------|--------------------------------|-----------|
| **Clearance to other features** | **3 mm** | Provides ample creepage for high‑current or high‑voltage sections, reducing the risk of arcing. [Verified] |
| **Minimum width** | **0.15 mm** | Guarantees manufacturability on standard 1 oz copper processes. [Verified] |
| **Thermal‑relief spoke width** | **0.25 mm** | Balances solderability (enough heat can flow) with the need to keep the pad’s resistance low. [Verified] |
| **Thermal‑relief gap** | **0.4 mm** | Prevents the thermal relief from acting as a solid connection, which would increase soldering effort. [Verified] |
| **Fill type** | **Solid** | A solid fill maximises the plane’s conductivity and shielding effectiveness. [Verified] |

> **Inference:**  Using a solid fill for ground planes is generally preferred because it yields the lowest possible DC resistance and provides a continuous reference for high‑speed signals. [Inference]

---

## 3. Thermal Reliefs for Pads  

When a pad (through‑hole, SMD, or via) connects to a ground plane, a **thermal‑relief** pattern is automatically generated based on the spoke width and gap settings.  

* **Benefits**  
  * Reduces the heat‑sink effect during soldering, improving solder joint quality.  
  * Limits the current that can flow directly from the pad into the massive plane, which can be advantageous for protecting delicate components.  

* **Design tip** – For high‑current power pads (e.g., power‑IN, large MOSFET drains) consider **removing** the thermal relief (i.e., using a solid connection) to lower the resistance path.  This decision should be weighed against solder‑ability concerns. [Inference]

---

## 4. Polygon Drawing and Repouring  

The zone polygon can be drawn freely:

* **Vertex placement** – Click to add points; the tool does not require right‑angle corners.  
* **Mid‑mouse drag** – Holding the middle mouse button while dragging pans the view, allowing precise placement of vertices without losing context.  
* **Closing the polygon** – Return to the first vertex to complete the shape.  

After the outline is defined, press **B** (or use *Edit → Fill All Zones*) to **repour**. The ECAD engine automatically:

* Generates the copper fill respecting the clearance and minimum‑width rules.  
* Cuts out any copper where the zone intersects drill holes, plated‑through holes, or other copper features, preserving required clearances.  

> The repour operation also respects the **Edge‑Cuts** layer, automatically maintaining a **0.3 mm** clearance from the board outline. [Verified]

---

## 5. Multi‑Layer Ground Planes  

For boards with internal layers:

1. **Enable the zone on each inner copper layer** (e.g., *Inner 1* and *Inner 2*).  
2. **Assign the same ground net** to both zones.  
3. **Repour** each layer individually or use a batch fill command.  

Resulting stack‑up example:

```
Top Layer (Front Copper)   → Ground plane (solid)
Inner Layer 1               → Ground plane (solid)
Inner Layer 2               → Ground plane (solid)
Bottom Layer (Back Copper) → Ground plane (solid)
```

> **Speculation:**  Deploying two internal ground planes can dramatically lower the overall impedance of the power distribution network and improve EMI shielding, at the cost of increased fabrication complexity and board thickness. [Speculation]

---

## 6. Interaction with Edge‑Cuts (Board Outline)  

The **Edge‑Cuts** layer defines the mechanical outline of the PCB. When a ground zone is repoured:

* The tool automatically enforces the **clearance rule** (e.g., 0.3 mm) between the copper fill and the board edge.  
* Designers can draw a **rough outline**; the repour algorithm will trim the copper to respect the clearance, eliminating the need for pixel‑perfect polygon tracing.  

This feature accelerates layout and reduces the likelihood of accidental copper‑to‑edge shorts.

---

## 7. Visibility Management  

During layout, it is common to **hide** internal copper layers that are already verified to keep the viewport uncluttered:

* Right‑click a layer → *Hide All Layers but Active*  
* Toggle visibility via the layer manager  

This practice helps focus on the active design area (e.g., front and back copper plus outline) without sacrificing the ability to re‑enable hidden layers for inspection later.

---

## 8. Adding Mounting Holes and Fiducial Markers  

After the ground planes are in place, the next typical steps are:

* **Mounting holes** – Define mechanical fastener locations; they are usually non‑plated through holes (NPTH) that cut through all copper layers, creating intentional gaps in the ground planes.  
* **Fiducial markers** – Small copper pads (often on the ground net) placed at known positions to aid automated optical inspection and pick‑and‑place alignment.  

Both features should be placed **before** the final repour of the zones to ensure the copper is correctly cleared around them.

---

## 9. Best‑Practice Checklist for Ground Planes  

| ✅ Item | Reason |
|--------|--------|
| **Assign a dedicated net** (e.g., GND) to each ground zone. | Guarantees consistent connectivity across the board. |
| **Set realistic clearance and minimum‑width values** based on the PCB manufacturer’s capabilities. | Prevents DRC violations and reduces yield loss. |
| **Use thermal reliefs on all pads except high‑current power pads**. | Balances solderability with low‑resistance connections. |
| **Prefer solid fill for ground planes** unless specific thermal‑relief requirements dictate otherwise. | Maximises shielding and reduces plane resistance. |
| **Repour after any geometry change** (e.g., added holes, new components). | Keeps the copper fill up‑to‑date with the latest layout. |
| **Verify that the Edge‑Cuts clearance is respected**. | Avoids copper‑to‑edge shorts that can cause board failure. |
| **Document the layer stack‑up** (which layers carry ground, power, signal). | Essential for signal‑integrity analysis and manufacturing hand‑off. |
| **Hide non‑essential layers during detailed routing**. | Improves visual clarity and reduces accidental edits. |
| **Place mounting holes and fiducials before final repour**. | Guarantees proper copper clearance around these features. |

---

## 10. Common Pitfalls & Mitigations  

| Pitfall | Symptom | Mitigation |
|---------|---------|------------|
| **Insufficient clearance to the board edge** | DRC errors, potential short to the board chassis. | Set the Edge‑Cuts clearance rule (e.g., 0.3 mm) and verify after each repour. |
| **Thermal reliefs too narrow** | Difficulty soldering, cold joints. | Increase spoke width (≥ 0.25 mm) and gap (≥ 0.4 mm). |
| **Over‑constraining minimum width** | Unfilled zones, missing copper in tight spaces. | Align minimum‑width rule with the manufacturer’s capabilities (commonly 0.15 mm for 1 oz copper). |
| **Neglecting to enable ground zones on all intended layers** | Unintended floating ground sections, increased EMI. | Double‑check layer visibility and zone assignment before final repour. |
| **Drawing overly complex polygon outlines** | Longer repour times, higher chance of DRC violations. | Use simple, rough outlines; let the tool trim to the exact shape. |

---

## 11. Process Flow Diagram  

```mermaid
flowchart TD
    A[Start Layout] --> B[Select Add Filled Zone]
    B --> C[Choose Copper Layer(s)]
    C --> D[Assign Ground Net (GND)]
    D --> E[Set Clearance & Minimum Width]
    E --> F[Configure Thermal Reliefs]
    F --> G[Draw Rough Polygon Outline]
    G --> H[Repour Zone (B)]
    H --> I[Verify Clearance to Edge Cuts]
    I --> J[Add Mounting Holes & Fiducials]
    J --> K[Final Repour All Zones]
    K --> L[Run DRC / ERC Checks]
    L --> M[Proceed to Routing / Fabrication]
```

*The flowchart captures the sequential actions required to create reliable ground planes and integrate them into the overall PCB design.*  

---

### Closing Remarks  

Ground planes are more than just a copper sheet; they are a critical design element that influences electrical performance, manufacturability, and mechanical robustness. By adhering to the outlined workflow, respecting clearance and thermal‑relief rules, and leveraging multi‑layer planes where appropriate, designers can achieve low‑impedance, well‑shielded boards that meet both functional and production requirements.