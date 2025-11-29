# JLCPCB – Design, Layout, and Production Services  

*This section documents the workflow, design considerations, and best‑practice recommendations when using JLCPCB (including their optional layout service) for the MSPM0 family of boards. All statements are annotated with certainty labels.*

---

## 1. Overview of JLCPCB Capabilities  

JLCPCB provides a full‑stack PCB solution: schematic capture, layout, fabrication, and turnkey assembly. The company is widely used for **low‑cost, fast‑turn** production of both simple hobby boards and **high‑speed, high‑density** designs.  

- The author’s experience with the MSPM0 boards resulted in **“fantastic”** quality assemblies, confirming the reliability of JLCPCB’s standard process. `[Verified]`  
- JLCPCB also offers a **professional layout service** that can take a netlist or schematic and deliver a production‑ready PCB. This service is staffed by engineers experienced in **high‑speed, high‑density, and multi‑layer** designs. `[Verified]`  

### When to Use the Layout Service  

| Situation | Benefit | Typical Trade‑off |
|-----------|---------|-------------------|
| **No in‑house layout expertise** – you have a schematic but lack time or skill to create a robust stack‑up. | Faster time‑to‑market; reduced risk of DFM violations. | Slightly higher cost than a DIY layout. |
| **Complex high‑speed signals** (e.g., USB, Ethernet, high‑frequency clocks). | Access to controlled‑impedance routing, length‑matched differential pairs, and proper reference planes. | Requires close communication of signal‑integrity requirements. |
| **Large production runs** where design errors become costly. | Professional verification (ERC/DRC, SI checks) before tape‑out. | May involve additional review cycles. |

> **Inference:** Leveraging JLCPCB’s layout team can shorten development cycles for teams focused on firmware or system integration rather than PCB geometry. `[Inference]`

---

## 2. End‑to‑End Development Flow  

The following flowchart captures the typical sequence from concept to a shipped assembled board when using JLCPCB (including the optional layout service).

```mermaid
flowchart TD
    A[Requirements & Specification] --> B[Schematic Capture (KiCad 9)]
    B --> C{Layout Path}
    C -->|DIY Layout| D[PCB Layout (KiCad) → DRC/ERC → Gerber Export]
    C -->|JLCPCB Layout Service| E[Submit Netlist → JLCPCB Engineer → Layout Package]
    D --> F[Design Review (DFM/DFA) → Quote Request]
    E --> F
    F --> G[Manufacturing Quote & Lead‑time]
    G --> H[Place Order → Fabrication]
    H --> I[Assembly (SMT placement, reflow, inspection)]
    I --> J[Final Test & Shipping]
```

*The diagram reflects the standard process; the “DIY Layout” branch assumes the designer performs all DFM/DFA checks before upload.* `[Verified]`

---

## 3. Preparing a KiCad Project for JLCPCB  

### 3.1 Schematic Checklist  

1. **Complete Symbol Libraries** – Ensure all parts have a corresponding footprint.  
2. **Electrical Rule Check (ERC)** – Resolve all “unconnected pin” or “multiple drivers” warnings.  
3. **Bill of Materials (BOM) Export** – Include part numbers, values, and preferred manufacturers (JLCPCB’s component library is searchable via their “Component Library” tool).  

### 3.2 Layout Checklist  

| Item | Why It Matters | Recommended Action |
|------|----------------|--------------------|
| **Design Rule Check (DRC)** | Prevents manufacturability issues (minimum clearance, drill sizes). | Run DRC with JLCPCB’s default rule set (e.g., 0.15 mm clearance, 0.2 mm trace width) and adjust if needed. |
| **Layer Stack‑up Definition** | Controls impedance, EMI, and thermal performance. | For high‑speed signals, use a 4‑layer stack‑up with solid ground and power planes adjacent to signal layers. |
| **Controlled‑Impedance Traces** | Required for USB, high‑frequency clocks, etc. | Define trace width/spacing based on the chosen stack‑up; JLCPCB can fabricate 50 Ω single‑ended and 90 Ω differential pairs. |
| **Via Types** | Determines cost and reliability. | Use standard through‑hole vias for most connections; reserve micro‑vias for dense high‑speed sections (note that micro‑vias increase cost). |
| **Component Placement for Assembly** | Affects pick‑and‑place efficiency and reflow quality. | Group components by type (passives, ICs) and keep tall parts away from the board edges. |
| **Silkscreen and Courtyard Clearance** | Prevents solder mask bridging and component clash. | Keep silkscreen at least 0.2 mm away from copper; ensure component courtyards respect JLCPCB’s clearance rules. |

> **Speculation:** JLCPCB’s standard DFM guidelines recommend a minimum 0.15 mm clearance for 1 oz copper; designers should verify the latest rule set on the JLCPCB website. `[Speculation]`

### 3.3 Gerber & Drill Export  

- Export **Gerber files** for each layer (copper, solder mask, silkscreen) using the **RS‑274X** format.  
- Include a **drill file** (NC drill) and an **assembly drawing** (optional but helpful for manual inspection).  
- Verify the stack‑up order in the Gerber viewer; mismatched layer ordering is a common source of fabrication errors.  

---

## 4. Manufacturing & Assembly Considerations  

### 4.1 Fabrication Options  

| Parameter | Typical Choices | Impact |
|-----------|----------------|--------|
| **Board Thickness** | 1.2 mm (standard) vs. 0.8 mm (thin) | Thin boards reduce material cost but increase handling difficulty. |
| **Copper Weight** | 1 oz vs. 2 oz | Higher copper improves current handling and thermal performance but raises cost. |
| **Surface Finish** | HASL, ENIG, OSP | ENIG offers better solderability for fine‑pitch components; OSP is cheaper but less robust for multiple re‑flows. |
| **Solder Mask Color** | Green (default) vs. white/black | Cosmetic choice; no electrical impact. |

> **Inference:** Selecting ENIG is advisable for high‑density, fine‑pitch parts (e.g., QFN, BGA) to ensure reliable solder joints. `[Inference]`

### 4.2 Assembly Service  

JLCPCB’s assembly line supports **SMT placement**, **reflow soldering**, and **automated optical inspection (AOI)**.  

- **Component Library Integration** – When ordering assembly, you can map your BOM to JLCPCB’s stocked parts, reducing lead time and cost.  
- **Turn‑around Time** – Typical “standard” assembly is 3–5 business days after fabrication; “express” options are available for an additional fee.  
- **Quality Assurance** – Boards are inspected for solder bridges, missing components, and mis‑alignments.  

> **Speculation:** For the MSPM0 boards, the author likely used JLCPCB’s standard SMT assembly with a green solder mask and HASL finish, balancing cost and performance. `[Speculation]`

### 4.3 Cost‑Saving Tips  

- **Coupons & Promotions** – JLCPCB frequently publishes discount codes (e.g., 10 % off PCB fab, 5 % off assembly). The author notes that such coupons are linked in the video description. `[Verified]`  
- **Batch Ordering** – Ordering multiple identical boards in a single panel reduces per‑board cost due to shared panelization.  
- **Standard Stack‑up** – Sticking to JLCPCB’s default 2‑layer or 4‑layer stack‑ups avoids extra charges for custom stack‑ups.  

---

## 5. Design‑for‑Manufacturability (DFM) & Design‑for‑Assembly (DFA) Checklist  

| DFM Aspect | Recommended Practice |
|------------|----------------------|
| **Clearance & Creepage** | Maintain at least the manufacturer‑specified minimum (typically 0.15 mm for 1 oz copper). |
| **Via Size** | Use ≥0.3 mm drill for reliable plating; avoid vias under fine‑pitch pads unless necessary. |
| **Pad Design** | Follow IPC‑7351 “B” (minimum) or “C” (maximum) land patterns; ensure solder mask clearance is adequate. |
| **Silkscreen** | Avoid placing silkscreen over pads; keep text away from high‑frequency traces. |
| **Thermal Relief** | Provide adequate thermal spokes for large copper pours to aid solder reflow. |
| **Component Orientation** | Standardize polarity markings to simplify pick‑and‑place programming. |

| DFA Aspect | Recommended Practice |
|------------|----------------------|
| **Component Spacing** | Keep a minimum of 0.5 mm between adjacent components to allow placement head clearance. |
| **Tall Parts** | Place connectors, headers, and tall passive components near board edges to avoid placement collisions. |
| **Test Points** | Include accessible test pads for post‑assembly verification. |
| **Panelization** | Use a “break‑away” or “V‑cut” panel style to simplify depaneling. |

> **Inference:** Following these DFM/DFA guidelines will reduce the likelihood of “rework” charges from JLCPCB and improve overall yield. `[Inference]`

---

## 6. Summary  

JLCPCB offers a **complete, low‑cost ecosystem** for turning a KiCad schematic into a fully assembled board. Their **layout service** is a practical option for teams lacking PCB expertise or dealing with high‑speed, high‑density requirements. By adhering to standard **ERC/DRC checks**, defining an appropriate **stack‑up**, and observing **DFM/DFA best practices**, designers can reliably obtain high‑quality assemblies with short lead times. Leveraging **coupons** and **batch ordering** further optimizes cost, making JLCPCB a compelling partner for both prototyping and low‑volume production.  

---