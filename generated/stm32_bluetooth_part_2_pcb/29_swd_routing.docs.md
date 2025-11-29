# 29 SWD Routing  

## Overview  

Serial Wire Debug (SWD) provides a two‑wire debug interface (SWDIO and SWCLK) that must be routed with controlled impedance and strict clearance rules to preserve signal integrity and to avoid coupling with nearby high‑speed nets such as the USB differential pair (DP/DM). This section documents the recommended workflow, the key PCB‑level constraints, and best‑practice techniques for routing SWD on a typical 2‑layer or 4‑layer board.

---

## 1. Net‑Class Configuration  

| Parameter | Recommended Setting | Rationale |
|-----------|---------------------|-----------|
| **Net class name** | `SWD` | Groups all debug nets for a single set of rules. |
| **Trace width** | *≈ 0.19 mm* (or the width that yields the target impedance in the chosen stack‑up) | Provides the required controlled‑impedance for the ~100 MHz SWD clock. `[Verified]` |
| **Clearance** | Minimum clearance to other signal traces, pads, and copper pours as defined by the DRC rule set (typically ≥ 3× trace width for high‑speed nets) | Reduces capacitive coupling and cross‑talk, especially near the USB DP/DM pair. `[Verified]` |
| **Via style** | Through‑hole or micro‑via with a pad‑to‑pad clearance that respects the same rule set | Guarantees consistent impedance across layer transitions. `[Inference]` |

*Implementation tip*: In most ECAD tools the net class can be edited via **Edit → Predefined Sizes → Net Classes**, then select `SWD` and set the trace width to **0.19 mm**. Press **OK** to apply the change globally.

---

## 2. Routing Strategy  

### 2.1. General Path Planning  

1. **Start from the MCU pins** (SWDIO and SWCLK) and route outward toward the connector.  
2. **Avoid large through‑hole pads** early in the route; if a via must be used, keep a generous clearance (≥ 2× trace width) from the pad edge.  
3. **Maintain a “break‑away” zone** around passive components (e.g., decoupling capacitors) to prevent the trace from hugging the component body. This reduces parasitic capacitance and cross‑talk. `[Verified]`  
4. **Use the grid‑snap function** (`N` key in many tools) to align the trace to the design grid, which simplifies DRC compliance and eases later length‑matching adjustments.  

### 2.2. Specific Considerations for SWDIO  

* **Cross‑talk with USB DP/DM** – The SWDIO line often runs close to the USB differential pair. To mitigate coupling:  
  * Keep a **minimum orthogonal separation** (≥ 3× trace width) between SWDIO and either USB trace.  
  * If space is limited, **re‑position the USB connector** or **move the nearby decoupling capacitor** leftward to create a larger routing corridor. `[Inference]`  

* **Asymmetric Differential Pair Routing** – When the board geometry forces the D+ and D‑ traces to follow different paths (e.g., due to a component blockage), route them **as symmetrically as possible** and later apply length‑matching (tuning with serpentine meanders) to meet the skew budget (typically < 100 ps). `[Speculation]`

### 2.3. Specific Considerations for SWCLK  

* The SWCLK line is a single‑ended clock that can tolerate slightly tighter spacing than the differential pair, but **still requires a clear path** away from high‑frequency edges.  
* Route SWCLK **first**, then use the freed space to guide SWDIO, ensuring that the clock does not cross under any large copper pours that could introduce unwanted capacitance.  

---

## 3. Design‑Rule Checks (DRC) & Electrical‑Rule Checks (ERC)  

| Check | Typical Threshold | Action if Violated |
|-------|-------------------|--------------------|
| **Minimum clearance** | ≥ 3× trace width (or manufacturer‑specified) | Move trace or adjust component placement. |
| **Maximum trace length mismatch (SWDIO pair)** | ≤ 5 mm (≈ 30 ps) | Add serpentine meanders to the shorter trace. |
| **Via‑to‑via clearance** | ≥ 2× via drill diameter | Shift via locations or use staggered via patterns. |
| **Impedance deviation** | ± 10 % of target (e.g., 45 Ω ± 10 %) | Refine trace width or adjust stack‑up parameters. |

Run DRC **after each major routing pass**. ERC will flag any unconnected SWD nets or accidental short‑circuits to power/ground planes.

---

## 4. Layout Adjustments & Trade‑offs  

When the initial routing attempt fails due to insufficient clearance (as often observed near a large capacitor), designers have two primary options:

1. **Component relocation** – Shift the offending capacitor leftward (or to another quadrant) to enlarge the routing channel. This may increase board area but improves signal integrity and reduces the need for complex routing gymnastics. `[Inference]`  

2. **Asymmetric pair routing** – Accept a non‑mirrored path for D+ and D‑, then compensate with length‑matching. This keeps the component layout unchanged but adds extra routing effort and may slightly increase EMI due to the non‑balanced geometry. `[Inference]`  

The choice hinges on **cost vs. performance**: moving components may increase BOM and assembly time, while asymmetric routing may raise the risk of EMI problems in high‑speed designs.

---

## 5. Recommended Routing Flow  

```mermaid
flowchart TD
    A[Define SWD Net Class] --> B[Set Controlled‑Impedance Width]
    B --> C[Place MCU & Connector Pads]
    C --> D[Pre‑route Critical Clearance Zones]
    D --> E[Route SWCLK (single‑ended)]
    E --> F[Route SWDIO (differential pair)]
    F --> G[Check DRC / ERC]
    G -->|Pass| H[Length‑match & Tune Impedance]
    G -->|Fail| I[Adjust Component Placement / Grid]
    I --> D
    H --> J[Finalize Layout & Generate Gerbers]
```

*The flowchart captures the iterative nature of SWD routing, emphasizing early clearance planning and the feedback loop between DRC failures and component placement adjustments.* `[Verified]`

---

## 6. Summary of Best Practices  

| Practice | Why It Matters |
|----------|----------------|
| **Use a dedicated net class** for SWD nets | Guarantees consistent trace width and clearance across the board. |
| **Maintain generous spacing from large pads and capacitors** | Reduces parasitic coupling and eases DRC compliance. |
| **Route the clock first** | Provides a clean reference for the data line and avoids later cross‑overs. |
| **Avoid “hugging” other high‑speed traces** | Minimizes cross‑talk, especially with the USB DP/DM pair. |
| **Leverage the grid and snap tools** | Improves manufacturability and simplifies later length‑matching. |
| **Iteratively run DRC/ERC** | Early detection of clearance violations prevents costly redesigns. |
| **Consider component relocation before complex asymmetric routing** | Often the simplest way to meet spacing rules without sacrificing signal integrity. |

By following these guidelines, the SWD interface will meet its electrical performance targets while remaining manufacturable and reliable.