# Power & Ground Routing  

*This section documents the key PCB‑level decisions, constraints, and best‑practice techniques for routing power and ground nets on a typical four‑layer board that includes a USB‑C connector, an LDO regulator, an MCU (QFN), and RF‑critical traces.*

---

## 1. Solid Connections to Mounting‑Hole Pads  

When a mounting‑hole pad must be tied to the ground plane, the **Footprint → Options → Clearance Overrides → Connection to Copper Zones** setting should be changed to **“Solid”**.  
- This forces the pad to be *electrically* (not just thermally) connected to the copper pour, guaranteeing a low‑impedance path to ground.  
- The change is applied per‑footprint (press **B** to confirm) and repeated for every mounting‑hole pad.  

> **Why?** A solid connection eliminates the high‑frequency resistance that a thermal‑only relief would introduce, which is critical for EMI shielding and mechanical robustness.  [Verified]

---

## 2. Trace Width vs. Inductance  

| Net type | Recommended trace width | Rationale |
|----------|------------------------|-----------|
| High‑current / power (5 V, 3.3 V) | **As wide as the pad** (e.g., 0.6 mm on a 0.6 mm pad) | Wide traces lower DC resistance **and** reduce loop inductance; inductance scales roughly with the inverse of trace width. [Verified] |
| Low‑current signal (e.g., LDO enable) | Narrower trace (≈0.19 mm) | The net carries only a few milliamps, so a slimmer trace saves space without harming performance. [Verified] |
| RF / high‑speed differential pairs | Controlled‑impedance micro‑strips (≈50 Ω) | Requires precise width/spacing based on stack‑up; not covered in detail here but the four‑layer board enables the needed thin traces. [Inference] |

> **Design tip:** Start a trace at the pad width, then **widen** it as soon as clearance permits. This “flare” reduces the effective inductance of the short segment that connects the component to the power plane. [Inference]

---

## 3. Power Distribution Strategies  

### 3.1 Wide Traces vs. Polygon Pours (Power Puddles)  

Both approaches are acceptable; the choice depends on board density and the need for **plane capacitance**.  

* **Wide Traces** – Simple, explicit routing; ideal when the net has few branches or when you need to keep the layout readable.  
* **Polygon Pours (Power Puddles)** – Fill the copper around the net, automatically stitching to all pads of that net. This creates a **distributed capacitance** between the power plane and the adjacent ground plane, lowering the net’s effective inductance.  

> In the example design, the 3.3 V net is poured on the **bottom layer** while the inner layers host solid ground planes, yielding a low‑inductance power delivery network. [Verified]

### 3.2 Example Flow (5 V → LDO → 3.3 V)  

```mermaid
flowchart LR
    USB5V[USB‑C 5 V Pad] -->|T‑junction| LDO_IN[LD0 Vin]
    LDO_IN --> LDO[Low‑Dropout Regulator]
    LDO --> LDO_OUT[LD0 Vout (3.3 V)]
    LDO_OUT -->|Polygon Pour| PWR_PLANE[Bottom‑layer 3.3 V Plane]
    PWR_PLANE --> MCU_3V3[MCU 3.3 V Pins]
    PWR_PLANE --> CAP[Decoupling Capacitors]
```

*The flow shows the high‑level net topology; each arrow represents either a wide trace or a polygon pour.* [Inference]

---

## 4. Layer Utilization & Plane Strategy  

| Layer | Primary purpose | Typical copper usage |
|-------|----------------|----------------------|
| **Top (L1)** | Component placement, RF & USB differential pairs | Mostly signal; optional ground pour for copper balance |
| **Inner 1 (L2)** | Solid ground plane (GND) | 100 % copper (no cutouts) |
| **Inner 2 (L3)** | Solid ground plane (GND) | 100 % copper (mirrors L2) |
| **Bottom (L4)** | 3.3 V power plane (polygon pour) | Continuous 3.3 V copper, stitched to GND via vias |

*Benefits of this stack‑up*  

- **Low‑inductance power delivery**: The close spacing (≈0.11 mm dielectric) between the bottom 3.3 V plane and the inner ground planes creates a **parallel‑plate capacitance** that damps voltage transients. [Verified]  
- **RF performance**: With dedicated inner ground planes, the top‑layer RF traces see a stable reference, simplifying controlled‑impedance routing. [Inference]  

---

## 5. Copper Balance & Fill Management  

### 5.1 Why Copper Balance Matters  

Uneven copper distribution can cause **warpage**, **thermal gradients**, and **unequal etching** during fabrication. In a four‑layer board where the inner layers are solid ground and the bottom layer is a full power plane, the top layer may become **copper‑starved** if left empty.

### 5.2 Implementing a Top‑Layer Ground Pour  

1. Change the **Top‑layer copper** to a **ground polygon** (press **B** to repour).  
2. Enable **thermal reliefs** on pads to aid solderability.  
3. Verify that the pour does **not** encroach on high‑speed RF traces; maintain a clearance of at least **3 × dielectric height** (≈3 × 0.11 mm ≈ 0.33 mm). The design uses a **0.35 mm** clearance, which is acceptable for most manufacturers. [Verified]  

### 5.3 Keep‑Out Areas  

If a full top‑layer pour is undesirable, draw a **keep‑out polygon** around the RF and USB differential sections (shortcut: **Ctrl + Shift + K**). This prevents copper from being placed too close to the high‑speed traces, preserving their impedance. [Inference]

---

## 6. Stitching Vias (Ground Vias)  

To ensure that all ground planes behave as a single low‑impedance node, place **ground stitching vias** at regular intervals (e.g., every 5–10 mm) across the board.  

- **Function**: They provide a low‑inductance path between the top ground pour, inner ground planes, and any copper‑filled bottom layers.  
- **Placement**: Avoid placing them directly under high‑speed signal pads unless a via‑in‑pad is required for thermal reasons.  

> Stitching is especially important when multiple ground pours exist (top, inner, bottom) to prevent **plane splitting** and to maintain a uniform return path for RF currents. [Verified]

---

## 7. Summary of Best Practices  

| Practice | Reason |
|----------|--------|
| Set mounting‑hole pads to **Solid** connection to copper zones | Guarantees low‑impedance ground reference. |
| Use **wide traces** (pad‑width or greater) for power nets | Reduces both DC resistance and loop inductance. |
| Prefer **polygon pours** for dense power nets when space permits | Adds distributed capacitance and simplifies routing. |
| Keep **inner layers solid ground** and locate **power planes** on outer layers | Provides low‑inductance supply rails and a stable reference for high‑speed signals. |
| Maintain **copper balance** by pouring the top layer or adding copper fills | Prevents warpage and improves thermal uniformity. |
| Apply **clearance rules** (≥ 3 × dielectric height) around RF traces when adding copper pours | Preserves controlled‑impedance characteristics. |
| Use **keep‑out zones** for RF sections if a full pour would violate clearance. |
| Distribute **ground stitching vias** uniformly across the board | Couples all ground planes into a single low‑impedance node. |
| Adjust **thermal‑relief parameters** (spoke width, gap) to balance solderability and copper continuity. |  

By following these guidelines, a designer can achieve a robust power distribution network, reliable ground connectivity, and predictable high‑speed signal behavior on a compact four‑layer PCB.