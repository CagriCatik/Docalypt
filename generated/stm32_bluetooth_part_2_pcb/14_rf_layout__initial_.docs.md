# 14 – RF Layout (Initial)

## 1. Overview  

The first stage of an RF‑centric PCB layout is to establish a **physical envelope** that guarantees the required electrical performance while respecting manufacturability constraints.  In this design the most critical RF elements are:

| Symbol | Description | Placement constraint |
|--------|-------------|----------------------|
| **U2** | RF front‑end IC (source/receiver) | Fixed pin‑out that defines the RF I/O location |
| **J4** | UFL (Ultra‑Small Form‑Factor) connector – external antenna interface | Must be reachable from the RF pin of U2 |
| **Pi‑matching network** | Lumped L‑C network that matches the RF port to 50 Ω | Must fit **between** U2 and J4 |
| **Filter** | Band‑pass or low‑pass element that cleans the RF spectrum | Should be placed as close as possible to the matching network to minimise inter‑stage parasitics |
| **X2** | 4‑pin crystal oscillator for the high‑speed external clock | Needs a short, low‑inductance path to the RF core and to the MCU clock input |

The initial layout exercise therefore revolves around **allocating space** for the matching network and filter, while simultaneously **optimising trace lengths** for the crystal and the RF feed‑line.

---

## 2. Critical RF Component Placement  

### 2.1 Pi‑Matching Network  

The Pi‑network is a **lumped‑element** topology that must be positioned **directly between** the RF pin of U2 and the UFL connector (J4).  This requirement dictates a **clear corridor** on the board where no other components or routing may intrude.  The corridor width is driven by the physical size of the inductors and capacitors, as well as the required clearance for solder mask and assembly tolerances.

> *“The Pi matching network needs to fit in between U2 and J4.”* **[Verified]**

### 2.2 Filter Placement  

A practical workflow is to **place the filter first** (using the move shortcut *M*), roughly where the Pi‑network will sit, and then insert the matching network adjacent to it.  This approach ensures that the **inter‑stage distance** is minimised, reducing stray inductance and capacitance that would otherwise degrade the filter’s response.

> *“I could place the filter very roughly where it needs to be and then I could take my matching network and place it next to it.”* **[Verified]**  
> *“Placing the filter first then the matching network is a valid workflow.”* **[Inference]**

### 2.3 Crystal Oscillator (X2)  

X2 is a **four‑pin crystal** that provides the high‑speed external clock.  Because the crystal’s **equivalent series resistance (ESR)** and **load capacitance** are highly sensitive to trace length and via inductance, the layout must keep the **X2‑to‑core** and **X2‑to‑MCU** paths as short and direct as possible.  The rats‑nest view in the CAD tool highlights the long connections, prompting the designer to relocate X2 to a region “up over here” where the paths become shorter.

> *“X2 is our crystal oscillator for the high‑speed external clock.”* **[Verified]**  
> *“Rats‑nest lines are long, indicating trace length should be minimized.”* **[Verified]**  
> *“Using the rats‑nest tool helps to quickly identify optimal component locations for shortest RF paths.”* **[Inference]**

---

## 3. Using the Rats‑Nest for Length Optimisation  

The **rats‑nest** (net‑highlight) feature automatically draws straight‑line “ghost” connections between pins that are not yet routed.  In RF designs these lines are a **visual cue** for:

* **Identifying long, high‑inductance paths** that must be shortened.  
* **Guiding component relocation** before any copper is placed.  
* **Validating that the Pi‑network corridor remains clear** of competing nets.

By iteratively moving components and observing the rats‑nest, the designer can converge on a placement that satisfies both **electrical length** and **mechanical clearance** constraints without committing to a final routing scheme.

---

## 4. Defining the Board Outline  

Once the critical RF blocks are positioned, the **board outline** can be refined.  Two complementary strategies are common:

1. **Component‑first approach** – Place all high‑frequency parts, then draw the board edge to enclose them with adequate clearance for edge‑coupled effects and mechanical handling.  
2. **Outline‑first approach** – Define a mechanical envelope based on enclosure constraints, then fit the RF components inside, adjusting as needed.

Both methods benefit from the **early rats‑nest analysis**, because the outline can be shaped to avoid forcing long RF traces around board edges.

> *“Another way is maybe first of all focusing on all other parts making sure everything fits around and then we can define maybe a board outline.”* **[Verified]**

---

## 5. Trade‑offs and Best‑Practice Checklist  

| Concern | Decision | Rationale |
|---------|----------|-----------|
| **Component density vs. RF performance** | Keep the Pi‑network and filter as a **compact block** with minimal separation. | Reduces parasitic inductance and improves filter Q. |
| **Trace length vs. routing flexibility** | Prioritise **short, straight RF traces**; use the rats‑nest to relocate components rather than adding bends. | Shorter traces lower insertion loss and phase error. |
| **Manufacturability vs. fine‑pitch placement** | Ensure **minimum clearance** around the Pi‑network for solder mask and stencil; avoid sub‑0.2 mm spacing unless the fab can guarantee it. | Prevents solder bridges and improves yield. |
| **Controlled impedance** | For the RF feed‑line (U2 ↔ J4) use a **microstrip** or **stripline** with calculated width/spacing to achieve 50 Ω. | Guarantees impedance matching and reduces reflections. *[Speculation]* |
| **Via selection** | Use **short, low‑inductance vias** (e.g., blind or micro‑vias) for the crystal and filter connections when possible. | Minimises via‑induced phase shift in high‑speed paths. *[Speculation]* |

---

## 6. Initial Layout Flow (Mermaid Diagram)

The diagram below summarises the **iterative workflow** used during the first RF layout pass.

```mermaid
flowchart TD
    A[Identify critical RF blocks] --> B[Place Pi‑matching network corridor]
    B --> C[Insert filter near corridor]
    C --> D[Place crystal (X2) using rats‑nest guidance]
    D --> E[Evaluate rats‑nest lengths]
    E -->|Long traces| F[Relocate components]
    E -->|Acceptable| G[Define board outline]
    F --> B
    G --> H[Apply controlled‑impedance rules]
    H --> I[Pre‑DRC/ERC check]
    I --> J[Iterate until layout meets RF & DFM goals]
```

*The flow emphasises the **feedback loop** between component placement, rats‑nest analysis, and board‑outline definition.*  

---

## 7. Summary  

The initial RF layout stage is driven by **geometric constraints** (the Pi‑network corridor) and **electrical optimisation** (short crystal and RF feed‑line paths).  Leveraging the CAD tool’s rats‑nest feature enables rapid visual assessment of trace lengths, guiding component relocation before any copper is routed.  By establishing a clear placement hierarchy—**filter → matching network → crystal → board outline**—the designer can balance **performance**, **manufacturability**, and **mechanical fit** early in the design cycle, setting a solid foundation for subsequent detailed routing, impedance control, and DRC/ERC verification.