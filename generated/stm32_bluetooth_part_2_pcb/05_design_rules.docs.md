# 05 – Design Rules  

## 1. Why Design‑for‑Manufacturability (DFM) Matters  

A PCB layout that ignores the capabilities of the chosen fabricator will either be rejected during the **Design Rule Check (DRC)** or will incur hidden cost penalties.  
Typical DFM constraints include:

* Minimum trace width and spacing (to allow reliable etching).  
* Minimum drill size and annular‑ring width (to guarantee plated‑through reliability).  
* Minimum copper‑to‑hole and copper‑to‑edge clearances (to avoid shorting and to meet safety creepage requirements).  
* Surface‑finish, solder‑mask colour, and silk‑screen options (each adds a price multiplier).  

Collecting the fabricator’s capability table and translating it into the ECAD tool is the first step toward a manufacturable design. [Verified]

---

## 2. Extracting Manufacturer Capabilities  

Most PCB houses publish a **Capabilities** page that lists the absolute minima they can produce. For example, a typical low‑cost prototype shop may specify:

| Parameter | Minimum Capability |
|-----------|-------------------|
| Drill size | 0.20 mm – 6.30 mm |
| Trace width | 0.15 mm (≈ 6 mil) |
| Trace spacing | 0.15 mm (≈ 6 mil) |
| Annular ring | 0.15 mm |
| Via diameter (finished) | 0.25 mm |
| Copper‑to‑hole clearance | 0.25 mm |
| Copper‑to‑edge clearance | 3 mm |

These values are **hard minima**; designing exactly at the limit is risky because tolerances, panelization, and process variations can push the part out of spec. [Inference]

**Best practice:** add a safety margin (typically 20‑30 %) to each minimum before entering the values into the design rule set.

---

## 3. Cost Sensitivity of Design Choices  

Even when a dimension stays above the manufacturer’s minimum, the **price** can change dramatically:

| Design Variable | Effect on Cost (example) |
|-----------------|--------------------------|
| Trace/spacing ≤ 4 mil (0.10 mm) | Cost increase (requires tighter etch) |
| Hole diameter ≤ 2 mm | Cost jump (requires finer drilling) |
| Solder‑mask colour (green → matte black) | Higher material & processing cost |
| Silk‑screen colour (white, yellow, etc.) | Additional charge |
| Surface finish (ENIG, HASL, OSP, etc.) | Varies from low to premium |

In a quick quote for a 100 × 100 mm, 4‑layer board (10 pcs), the base price was ≈ US $51 when using the default 6 mil trace/spacing and a 0.25 mm via. Reducing the spacing to 4 mil raised the price, while moving to 5 mil kept the cost unchanged. Hole diameters below 2 mm caused a “dramatic” price increase. [Verified]

**Takeaway:** stay comfortably above the minimums unless the application truly demands finer features; the cost penalty is rarely justified for prototypes. [Inference]

---

## 4. Recommended Rule Set for a Typical 4‑Layer Prototype  

| Rule | Recommended Value | Rationale |
|------|-------------------|-----------|
| **Clearance (trace‑to‑trace, trace‑to‑pad, pad‑to‑pad)** | 0.15 mm (6 mil) – preferably 0.38 mm (15 mil) | 15 mil provides a comfortable margin and does **not** increase cost. |
| **Trace width** | 0.15 mm (6 mil) | Minimum feature size for a 4‑layer board; yields reliable etch without extra charge. |
| **Minimum connection width (polygon fill, copper pours)** | 0.15 mm | Same as trace width; ensures proper plating and isolation. |
| **Annular ring** | ≥ 0.15 mm | Guarantees sufficient copper around plated‑through holes. |
| **Via (finished) diameter** | 0.25 mm (10 mil) | Below this the price jumps; 0.25 mm is a safe, cost‑neutral choice. |
| **Copper‑to‑hole clearance** | ≥ 0.25 mm (use 0.26 mm) | Prevents copper encroachment on the plated hole. |
| **Copper‑to‑edge clearance** | 3 mm | Provides mechanical robustness and satisfies creepage for most low‑voltage designs. |
| **Differential‑pair trace width / spacing** | Define after impedance calculation; typical start point 0.15 mm / 0.15 mm for 90 Ω microstrip on FR‑4. | Needed for high‑speed signals; adjust per stack‑up. |

All of the above values lie **above** the manufacturer’s minima and avoid any cost adders in the quoted price. [Inference]

---

## 5. Annular‑Ring Calculation – A Quick Reference  

When a via is drilled, the **drill size** (raw hole) is larger than the **finished hole** after plating. The annular ring is the copper that remains around the hole:

\[
\text{Annular Ring} = \frac{\text{Pad Diameter} - \text{Finished Hole Diameter}}{2}
\]

*Typical practice:* the finished hole is ~0.1 mm smaller than the drill size (the plating adds ~0.05 mm on each side).  

**Example**  
* Desired finished hole: 0.30 mm  
* Drill size used: 0.40 mm (0.10 mm larger)  
* Pad diameter: 0.70 mm  

\[
\text{Annular Ring} = \frac{0.70 - 0.30}{2} = 0.20\text{ mm}
\]

A 0.20 mm annular ring comfortably exceeds the 0.15 mm minimum and does **not** trigger a cost increase. [Verified]

---

## 6. Implementing the Rules in KiCad (or similar ECAD)  

1. **Open the Board Setup → Design Rules** dialog.  
2. Set **Clearance** to the chosen value (e.g., 0.38 mm).  
3. Define **Track Width** and **Via Size** under the *Net Classes* or *Design Rules* tab.  
4. Add a **Net Class** for differential pairs and specify the pair width/spacing.  
5. Enable **DRC** and run a full check; resolve any violations before proceeding to the **Fabrication Output**.  

KiCad’s *Pre‑defined Sizes* panel lets you store these values as defaults for future projects, ensuring consistency across designs. [Inference]

---

## 7. Trade‑offs Summary  

| Decision | Impact on Cost | Impact on Performance / Reliability |
|----------|----------------|--------------------------------------|
| **Tighter trace/spacing (< 5 mil)** | Higher fab cost, possible extra lead time | Allows higher component density, but may increase crosstalk. |
| **Smaller vias (< 0.25 mm)** | Cost jump, tighter tolerances | Useful for high‑density interconnect (HDI) but reduces mechanical strength. |
| **Non‑standard solder‑mask colour** | Premium surcharge | No electrical benefit; purely aesthetic. |
| **Premium surface finish (ENIG)** | Higher unit price | Improves solderability and flatness; beneficial for fine‑pitch components. |
| **Increasing copper‑to‑edge clearance** | No cost impact (within standard limits) | Improves mechanical robustness and creepage for higher‑voltage designs. |

Designers should balance **budget constraints** against **electrical performance** and **reliability** requirements, selecting the most economical rule set that still meets the functional spec. [Inference]

---

## 8. Design‑Rule‑Setup Flow (Mermaid)

```mermaid
flowchart TD
    A[Gather Manufacturer Capability Table] --> B[Define Minimum Design Rules]
    B --> C[Add Safety Margins (20‑30%)]
    C --> D[Enter Rules into ECAD (Clearance, Width, Via, etc.)]
    D --> E[Run DRC / ERC]
    E -->|No violations| F[Generate Fabrication Outputs]
    E -->|Violations| G[Iterate Layout Adjustments]
    F --> H[Obtain Quote & Verify Cost Impact]
    H --> I[Finalize Design for Production]
```

The diagram illustrates the iterative nature of DFM: **capability extraction → rule definition → ECAD implementation → verification → cost check → finalization**. [Inference]

---

### Bottom Line  

By respecting the manufacturer’s minima, adding a modest safety margin, and consciously selecting rule values that avoid cost adders, a designer can produce a reliable, low‑cost prototype without sacrificing manufacturability. Consistently applying these rules in the ECAD environment and validating with DRC ensures a smooth hand‑off to the fab. [Verified]