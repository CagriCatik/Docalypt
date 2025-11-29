# SMPS Routing Guidelines {#smps-routing}

This section documents proven PCB‑layout techniques for low‑power switch‑mode power supplies (SMPS). The focus is on trace‑width selection, routing topology, copper‑pour usage, and ground‑pad handling. All recommendations are compatible with typical 2‑layer or 4‑layer boards fabricated with standard FR‑4 processes.

---

## 1. Trace‑Width Selection for Low‑Current SMPS {#trace-width}

- **Baseline width** – Use the pad width of the SMPS input/output pins as the initial trace width. In the reference design the pad is **25 mil** wide, which provides a convenient starting point.  
  *[Verified]*

- **Why it matters** – At the modest currents of a low‑power regulator, the trace width has little impact on temperature rise; even a 2 mm (≈80 mil) trace could carry the required current without issue. The primary benefit of a wider trace in this context is **reduced parasitic inductance**, which improves transient response.  
  *[Verified]*

- **Practical workflow (KiCad shortcuts)**  

  | Shortcut | Action |
  |----------|--------|
  | **X** | Start routing from a pad |
  | **W** | Increase trace width (repeat to step up) |
  | **Ctrl + W** | Decrease trace width |
  | **N** | Cycle grid size (use a finer grid when widening) |

  Begin routing with the pad‑width trace, then, as soon as clearance permits, press **W** to broaden the trace to the desired width (e.g., 0.5 mm). This “grow‑as‑you‑go” method keeps the initial segment short while quickly reducing inductance.  
  *[Verified]*

---

## 2. Switch‑Node Routing {#switch-node}

- **Keep it short** – The high‑frequency switching node should be routed with the minimum possible length to minimise loop area and ringing.  
  *[Verified]*

- **Width on demand** – Use only as much copper as required for the instantaneous current of the switch. For low‑current parts a modest width (the same as the pad or slightly larger) is sufficient.  
  *[Inference]*

- **Routing style** – After the initial short segment, widen the trace (using **W**) as soon as the surrounding clearance allows. This mirrors the strategy used for the input/output traces and yields a low‑inductance path without sacrificing board space.  
  *[Verified]*

---

## 3. Feedback & Output Node Implementation {#feedback-output}

### 3.1 When to Use a Copper Pour (Polygon)

The feedback pin and the output voltage node often do not carry significant steady‑state current. Instead of a single trace, a **filled copper zone** (polygon) can be employed:

- **Advantages**  
  - Provides a low‑impedance return path.  
  - Saves routing space for other signals.  
  - Improves thermal spreading for any occasional surge currents.  

- **Design steps (KiCad)**  

  1. **Add Filled Zone** – Select *Add Filled Zone* and place it above the pad.  
  2. **Assign Net** – The zone automatically inherits the net (e.g., `SMPS_FB`).  
  3. **Set Clearance** – Typical clearance is 2 mm (adjustable per design rules).  
  4. **Pad Connection** – Choose **Solid** (no thermal relief) for reflow‑compatible soldering.  
  5. **Corner Style** – Use 45° corners to simplify DRC and keep the zone tidy.  
  6. **Repour** – Press **B** to regenerate the copper pour after any geometry change.  

  The resulting polygon directly ties the feedback pin to the output pad, eliminating a separate trace.  
  *[Verified]*

### 3.2 Adjusting Clearance & Repouring

If a tighter clearance is required (e.g., to meet creepage rules or to accommodate a nearby high‑voltage trace), double‑click the zone, modify the clearance value (e.g., to **2.25 mm**), and repour. The zone will automatically re‑anchor to the pad while respecting the new spacing.  
*[Verified]*

---

## 4. Ground‑Pad Connection Strategies {#ground-pad}

The SMPS ground pin (often pin 32) may be positioned between the power input pad and the feedback zone. Two common approaches exist:

1. **Direct Pad‑to‑Pad Routing**  
   - Route a trace of the same width as the ground pad directly from the SMPS ground pad to the exposed ground pad on the board.  
   - This eliminates the need for a via, reduces inductance, and mirrors commercial reference designs.  
   - **Trade‑off**: Requires sufficient clearance from adjacent nets; may force a slight component spread.  
   *[Verified]*

2. **Via‑Based Connection**  
   - Place a via near the ground pad, route around the intervening pins, and connect to the ground plane.  
   - Useful when component density is high or when the ground pad is otherwise blocked.  
   - **Trade‑off**: Adds a small amount of inductance and a manufacturing step (via drilling).  
   *[Inference]*

Select the method that best satisfies the board’s **creepage/clearance** constraints and **component placement** goals.

---

## 5. General Layout Best Practices for Low‑Power SMPS {#general-practices}

| Practice | Rationale |
|----------|-----------|
| **Start with pad‑width traces** | Guarantees manufacturability and provides a clean anchor point. |
| **Widen as soon as clearance permits** | Reduces parasitic inductance without sacrificing routing flexibility. |
| **Use 45° corners for polygons** | Simplifies DRC and avoids acute‑angle copper islands. |
| **Prefer solid pad connections for low‑current nets** | Improves solderability during reflow. |
| **Maintain consistent clearance** (e.g., ≥2 mm for low‑voltage nets) | Ensures compliance with standard IPC‑2221 creepage rules. |
| **Keep high‑frequency loops minimal** | Limits EMI and improves transient response. |
| **Validate with DRC/ERC** after each major change (trace widening, zone repour). | Prevents inadvertent rule violations. |

---

## 6. Routing Flow Overview {#routing-flow-diagram}

The following Mermaid flowchart summarises the recommended routing sequence for a low‑power SMPS:

```mermaid
flowchart TD
    A[Start: Identify SMPS pads] --> B[Set initial trace width = pad width]
    B --> C[Route short segment from pad]
    C --> D{Clearance available?}
    D -- Yes --> E[Press W to widen trace]
    D -- No --> C
    E --> F[Route switch node (short, wide as needed)]
    F --> G[Create copper pour for feedback/output]
    G --> H[Set zone clearance & solid pad connection]
    H --> I[Repour (B) and verify]
    I --> J{Ground pad placement}
    J -- Direct pad‑to‑pad --> K[Route ground trace same width]
    J -- Via needed --> L[Place via, route around]
    K --> M[Final DRC/ERC check]
    L --> M
    M --> N[Design complete]
```

*The flowchart reflects the step‑by‑step methodology described above and is applicable to most low‑power SMPS layouts.*  
*[Inference]*

---

### End of Section

This documentation provides a concise yet comprehensive guide for routing low‑power SMPS circuits with an emphasis on manufacturability, electrical performance, and design robustness.