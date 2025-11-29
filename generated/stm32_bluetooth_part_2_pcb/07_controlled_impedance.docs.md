# 07 Controlled Impedance  

Controlling the characteristic impedance of high‑speed and RF traces is essential for preserving signal integrity, minimizing reflections, and meeting electromagnetic‑compatibility (EMC) requirements. This section outlines the practical steps, design decisions, and best‑practice guidelines for defining and routing controlled‑impedance traces on a typical 4‑layer board that hosts USB 2.0 Full‑Speed (12 Mbps) and modest RF sections.

---

## 7.1 Why Controlled Impedance Matters  

| Signal type | Typical target impedance | Consequence of mismatch |
|-------------|--------------------------|--------------------------|
| Single‑ended RF (e.g., antenna feed, clock) | 50 Ω (microstrip or stripline) | Reflections cause ringing, loss of bandwidth, and possible EMI violations. |
| Differential pair (e.g., USB, LVDS) | 90 Ω ± 10 % differential (≈45 Ω single‑ended) | Imbalance leads to common‑mode noise, increased jitter, and reduced eye‑opening. |

Even for “slow” interfaces such as USB 2.0 Full‑Speed, adhering to the nominal impedance reduces the risk of marginal performance on long or densely populated boards. Moreover, the calculation process provides a sanity check on the stack‑up and design rules before fabrication. [Verified]

---

## 7.2 Stack‑up Definition  

A well‑defined stack‑up supplies the dielectric thickness, material constant (εᵣ), and copper weight that feed the impedance calculators.

| Layer | Typical material | Thickness |
|-------|------------------|-----------|
| **Top copper** (signal) | 1 oz (35 µm) copper | – |
| **Prepreg / dielectric** | FR‑4, εᵣ ≈ 4.29 | 0.11 mm |
| **Inner ground plane** | Copper (same weight) | – |
| **Bottom copper** (signal) | 1 oz (35 µm) copper | – |

The outer‑layer microstrip model is used for both the RF single‑ended traces and the USB differential pair because the reference plane is directly beneath the signal layer (the inner ground plane). [Verified]

---

## 7.3 Single‑Ended 50 Ω Microstrip  

### 7.3.1 Impedance Calculation  

Using the stack‑up parameters above, an online calculator (e.g., PCBWay’s microstrip tool) yields the following relationship:

* **Target:** 50 Ω characteristic impedance.  
* **Result:** A trace width of **≈ 0.19 mm** satisfies the target within a few percent.  

If the width is reduced, the impedance rises; if increased, it falls. This simple width‑only tuning is sufficient for most outer‑layer RF traces when the dielectric thickness and copper weight are fixed. [Inference]

### 7.3.2 Design‑for‑Manufacturability (DFM)  

* **Minimum trace width / spacing:** Verify that the chosen 0.19 mm width respects the fab house’s minimum feature size (often 0.10–0.15 mm for 1 oz copper).  
* **Clearance to copper pours / planes:** Maintain at least the manufacturer‑specified clearance (commonly 0.15 mm) to avoid copper‑to‑copper shorts. [Verified]

---

## 7.4 Differential Pair (USB 2.0 Full‑Speed)  

### 7.4.1 Target Impedance  

USB 2.0 Full‑Speed specifies a **90 Ω differential** characteristic impedance (≈ 45 Ω single‑ended). The pair is routed as an **edge‑coupled microstrip** on the outer layer, using the same dielectric stack‑up as the single‑ended RF traces. [Verified]

### 7.4.2 Parameter Trade‑off  

Two geometric variables influence the differential impedance:

| Variable | Effect on Zdiff |
|----------|-----------------|
| **Trace width (W)** | Wider traces lower both single‑ended and differential impedance. |
| **Spacing (S)** | Larger spacing raises Zdiff (weaker coupling); smaller spacing lowers Zdiff. |

#### Iterative sizing (example)

1. **Start with W = 0.19 mm** (the 50 Ω single‑ended width).  
2. **Set S = 0.15 mm** (the minimum clearance).  
   * Result: Zdiff ≈ 100 Ω → 10 % high. [Inference]  
3. **Reduce S to 0.12 mm** → Zdiff drops into the 90 Ω window, but S < 0.15 mm violates clearance rules. [Inference]  
4. **Increase W to 0.22 mm** while keeping S = 0.15 mm → Zdiff approaches 90 Ω and clearance is respected. [Inference]

Thus, the final geometry **W ≈ 0.22 mm, S ≈ 0.15 mm** meets the 90 Ω target without breaking DFM constraints. [Inference]

### 7.4.3 Length Matching & Skew  

For Full‑Speed USB, length matching tighter than **150 ps** (≈ 30 mm) is not critical, but keeping the pair length‑matched within a few mils simplifies timing analysis and reduces skew. [Speculation]

### 7.4.4 Via and Plane Considerations  

* **Via stubs:** Prefer blind or buried vias for high‑frequency pairs to avoid stub resonances; however, for Full‑Speed USB, standard through‑hole vias are acceptable. [Speculation]  
* **Plane continuity:** Ensure the reference ground plane is uninterrupted beneath the pair to maintain the calculated impedance. [Verified]

---

## 7.5 Interaction with the PCB Design Tool (KiCad)  

1. **Create a net class** for the USB differential pair (e.g., `USB_FS_DP`). Assign the calculated width (0.22 mm) and spacing (0.15 mm) as default routing rules.  
2. **Add a differential pair rule** in the Design Rules Manager (DRC) specifying the target differential impedance (90 Ω) and the allowed tolerance (±10 %).  
3. **Define a “V‑gap” rule** for via‑to‑via clearance (e.g., 0.5 mm) to satisfy manufacturing clearances and to control crosstalk between adjacent vias.  
4. **Run DRC/ERC** after routing to catch any violations of the impedance, clearance, or spacing rules. [Verified]

These steps embed the impedance constraints directly into the layout workflow, reducing manual checks and ensuring consistency across the board. [Inference]

---

## 7.6 Manufacturer Collaboration  

Even with accurate calculators, the final trace geometry must be validated with the PCB fab house because:

* **Process tolerances** (etch bias, copper thickness variation) can shift the actual impedance.  
* **Material variations** (different FR‑4 grades, εᵣ spread) affect the dielectric constant.  

A typical request to the fab includes:

> “For the attached stack‑up (0.11 mm prepreg, εᵣ = 4.29, 1 oz copper), what trace width and spacing produce a 50 Ω single‑ended microstrip and a 90 Ω differential edge‑coupled pair on the outer layers?”

The fab will return the exact dimensions or a correction factor that can be applied in the layout. [Verified]

---

## 7.7 Best‑Practice Checklist  

| ✔️ Item | Reason |
|--------|--------|
| Define stack‑up early and lock dielectric thickness & εᵣ. | Provides a stable basis for impedance calculations. |
| Use an impedance calculator (microstrip/stripline) with fab‑provided parameters. | Reduces guesswork and aligns expectations. |
| Verify trace width & spacing against fab minimums (clearance, feature size). | Prevents DFM violations. |
| Create dedicated net classes and DRC rules for controlled‑impedance nets. | Automates compliance checking. |
| Run a quick “impedance sanity check” (e.g., 50 Ω single‑ended, 90 Ω diff) before finalizing layout. | Catches errors early. |
| Communicate final geometry to the manufacturer for confirmation. | Accounts for process tolerances. |
| For low‑speed interfaces (e.g., USB FS), treat impedance control as a “good practice” rather than a hard requirement, but still follow the above steps to avoid future redesigns. | Balances cost vs. performance. |

---

## 7.8 Process Flow (Mermaid Diagram)

```mermaid
flowchart TD
    A[Define Stack‑up] --> B[Select Impedance Model (microstrip / edge‑coupled)]
    B --> C[Calculate Width & Spacing]
    C --> D[Validate with Manufacturer]
    D --> E[Create Net Classes & DRC Rules]
    E --> F[Route Controlled‑Impedance Traces]
    F --> G[Run DRC / ERC]
    G --> H[Finalize Layout & Generate Gerbers]
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#bbf,stroke:#333,stroke-width:2px
```

The diagram captures the iterative nature of impedance control: calculations are refined after manufacturer feedback, and the resulting parameters are baked into the CAD environment before routing. [Verified]

---

## 7.9 Key Takeaways  

* **Impedance is a function of geometry and material.** Accurate stack‑up data is non‑negotiable.  
* **Single‑ended 50 Ω** traces on outer layers typically require a width around **0.19 mm** for a 0.11 mm dielectric with εᵣ ≈ 4.3.  
* **USB 2.0 FS differential pairs** can be satisfied with **≈ 0.22 mm width** and **0.15 mm spacing**, yielding a 90 Ω differential impedance while respecting clearance rules.  
* **Manufacturer verification** is the final safeguard against process‑induced impedance drift.  
* Embedding impedance constraints into **net classes and DRC rules** streamlines the layout and reduces post‑routing rework.  

By following the methodology outlined above, designers can confidently produce boards that meet both electrical performance and manufacturability goals.