# 03 – High‑Speed BGA Design and PCB Preparation  

## 3.1 Course Overview for Advanced BGA‑Based Systems  

A dedicated training program is available that teaches the complete workflow for designing with ball‑grid‑array (BGA) packages in high‑speed environments. The curriculum explicitly targets applications such as **GDDR3 memory modules**, **FPGA‑centric subsystems**, and **mission‑critical electronics used on ships**.  
> *“Design course where you can learn how to design with BGA packages high‑speed systems such as GDDR3 memory FPGA system on ships …”*  [Verified]  

The course typically covers:

* **Signal‑integrity (SI) fundamentals** for multi‑gigabit data paths.  
* **Controlled‑impedance stack‑up design** and the impact of dielectric material choices.  
* **Differential‑pair routing, length matching, and skew budgeting** for DDR and high‑speed serial links.  
* **Thermal management** for densely populated BGA footprints.  
* **Design‑for‑manufacturability (DFM)** and **design‑for‑assembly (DFA)** considerations specific to fine‑pitch BGAs.  

> *The inclusion of thermal and DFM topics is a logical extension of any high‑density BGA curriculum.*  [Inference]  

---

## 3.2 Managing Unused Pins and Symbol Hygiene  

When importing a component into a schematic editor such as **CubeIDE**, the tool can automatically hide pins that are not required by the current design. In the referenced design, pins **80** and **81** were marked as *hidden* because they are unused; consequently, they do not appear on the generated schematic symbol.  
> *“…this symbol hid from us if we go to CubeIDE these 80 81 pins and these are unused in our case so they also don't appear on the symbol here.”*  [Verified]  

### Why Hide Unused Pins?  

| Benefit | Explanation |
|---------|-------------|
| **Reduced visual clutter** | Designers see only the nets that matter, which speeds up schematic capture. |
| **Improved ERC/DRC results** | Unconnected pins cannot be mistakenly driven, preventing false‑positive errors. |
| **Cleaner netlist** | The downstream PCB layout receives a netlist without dangling, floating nets, simplifying rule checks. |

> *Omitting unused pins is a best‑practice that aligns with ERC/DRC hygiene.*  [Inference]  

### Recommended Workflow  

1. **Import the vendor library** and generate the full symbol.  
2. **Review the pin list** and mark any pins that are not required for the target configuration as *hidden* or *no‑connect*.  
3. **Run an Electrical Rule Check (ERC)** to verify that no required signals were inadvertently suppressed.  
4. **Synchronize the schematic to the PCB editor** so that the hidden‑pin state propagates to the layout.  

---

## 3.3 Transitioning from Schematic to PCB Layout  

With a clean schematic in hand, the next phase is the physical layout of the board. The following flowchart captures the typical high‑speed PCB development process, emphasizing the points where decisions about BGA packages and hidden pins have a direct impact.

```mermaid
flowchart TD
    A[Define System Requirements] --> B[Capture Schematic & Manage Symbols]
    B --> C[Run ERC / Verify Pin Usage]
    C --> D[Select Stack‑up & Impedance Targets]
    D --> E[Place Components (BGA First)]
    E --> F[Route High‑Speed Nets (Diff Pairs, Length Match)]
    F --> G[Perform DRC / SI Simulation]
    G --> H[Iterate Layout & Tuning]
    H --> I[Generate Fabrication Data]
    I --> J[Fabrication & Assembly]
    J --> K[Post‑Assembly Test & Validation]
```

*The flow emphasizes that **symbol hygiene** (step B‑C) precedes **stack‑up selection** (step D) because the presence of hidden pins can affect plane continuity and via placement strategies.*  [Inference]  

---

## 3.4 Key PCB Design Practices for High‑Speed BGA Designs  

### 3.4.1 Stack‑up and Reference Planes  

* **Dedicated ground and power planes** beneath the BGA reduce return‑path discontinuities and improve SI.  
* **Controlled‑impedance microstrip or stripline** layers should be defined early (step D in the flowchart) to meet the target differential impedance (e.g., 100 Ω for DDR).  

> *A multi‑layer stack‑up with at least four signal layers is common for GDDR3/FPGA designs.*  [Speculation]  

### 3.4.2 BGA Footprint and Via Strategy  

| Technique | When to Use | Trade‑off |
|-----------|-------------|-----------|
| **Via‑in‑pad (filled & capped)** | Very high pin density, critical for impedance continuity. | Increases cost and may require tighter DFM tolerances. |
| **Microvia (laser‑drilled)** | Fine‑pitch BGAs (< 0.5 mm pitch) where standard vias would violate clearance. | Requires advanced fab capabilities; may affect yield. |
| **Staggered via arrays** | To reduce via crowding and improve thermal conduction. | Slightly longer signal paths; careful length matching needed. |

> *Choosing the appropriate via type directly influences manufacturability and cost.*  [Inference]  

### 3.4.3 Controlled‑Impedance Routing  

* **Differential pairs** (e.g., DDR data lanes) must be routed with consistent spacing and width to maintain target impedance.  
* **Length matching** within a pair should be within a few mils (or a fraction of the signal’s rise time) to limit skew.  
* **Return‑path continuity** is essential; avoid routing high‑speed traces over split planes or large copper pours without stitching vias.  

### 3.4.4 Design‑for‑Manufacturability (DFM)  

* **Keep minimum clearance** between BGA pads and adjacent copper to satisfy fab house capabilities (typically ≥ 4 mil).  
* **Avoid 90° bends** on high‑speed traces; use 45° or curved transitions to reduce impedance discontinuities.  
* **Provide adequate via annular rings** around BGA pads to prevent drilling defects.  

> *These DFM rules are standard for fine‑pitch BGA assemblies and help maintain high yield.*  [Verified]  

### 3.4.5 Design‑for‑Assembly (DFA)  

* **Place the BGA footprint** near the board’s center of gravity when possible to aid thermal balance.  
* **Allocate sufficient solder mask clearance** to accommodate solder paste expansion and prevent bridging.  
* **Group related signals** (e.g., power, ground, control) to simplify pick‑and‑place programming and inspection.  

---

## 3.5 Verification and Validation  

1. **Electrical Rule Check (ERC)** – Run after schematic cleanup to catch any stray nets caused by hidden pins.  
2. **Design Rule Check (DRC)** – Enforce clearance, width, and via rules defined by the fab house.  
3. **Signal‑Integrity Simulation** – Use a 3‑D field solver or transmission‑line model to verify impedance, crosstalk, and eye‑diagram compliance for DDR/FPGA links.  
4. **Thermal Analysis** – Evaluate BGA hotspot temperatures under worst‑case power dissipation; adjust copper pours or add thermal vias as needed.  

> *A systematic verification sequence reduces the risk of costly re‑spins after fabrication.*  [Inference]  

---

## 3.6 Summary of Trade‑offs  

| Decision | Cost Impact | Performance Impact | Manufacturability |
|----------|-------------|--------------------|-------------------|
| **Higher layer count** | ↑ Cost (more material, fab time) | Enables dedicated planes → better SI/EMI | May increase fab complexity |
| **Microvias / via‑in‑pad** | ↑ Cost (laser drilling, fill) | Improves high‑frequency return paths | Requires advanced fab, tighter DFM |
| **Aggressive length matching** | ↑ Design effort | Reduces skew → higher data rates | May force non‑optimal component placement |
| **Conservative clearances** | ↓ Cost (standard fab) | May limit routing density | Improves yield, reduces defect risk |

> *Balancing these factors is central to a successful high‑speed BGA board.*  [Inference]  

---  

*End of Chapter 03 – Courses*