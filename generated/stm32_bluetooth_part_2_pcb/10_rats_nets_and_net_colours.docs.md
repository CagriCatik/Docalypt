# Rats Nets and Net Colours  

Understanding and visualising the connectivity of a board before any copper is laid down is a cornerstone of efficient PCB layout.  The *rat’s‑nest* (the “air‑wire” preview of un‑routed nets) together with colour‑coded **net classes** give the designer an at‑a‑glance map of where components should be placed and how critical signals must be treated.  

---  

## 1. What the Rat’s‑Nest Represents  

When a schematic is transferred to the PCB editor, every net that has not yet been routed appears as a thin, often‑crossing line called a *rat’s‑nest* or *air‑wire*.  

* Each line connects the pads that belong to the same net.  
* The direction and length of the air‑wire hint at the most logical placement of the associated components.  
* For high‑speed or RF nets, the rat’s‑nest also reveals potential length‑matching or shielding concerns before any copper is drawn.  

> **Why it matters** – By inspecting the rat’s‑nest you can avoid costly re‑placements later (e.g., moving a USB‑C connector far from its ESD protection network).  This early visual cue is the first step toward a clean, manufacturable layout.  [Verified]  

---  

## 2. Net Classes – Logical Grouping of Nets  

A **net class** is a user‑defined collection of nets that share a common purpose (e.g., all USB‑debug signals, all RF traces, all power rails).  Net classes serve two primary functions:  

| Function | Benefit |
|----------|---------|
| **Design‑rule grouping** – you can assign specific clearance, width, and via rules per class. | Guarantees that critical nets (high‑speed, high‑current) obey tighter constraints. |
| **Visual grouping** – each class can be given a distinct colour that propagates to the rat’s‑nest, schematic, and PCB view. | Enables instant visual identification of where a particular family of signals lives on the board. |

> **Best practice** – Define net classes **before** starting placement; this forces you to think about signal hierarchy early on. [Inference]  

---  

## 3. Colour‑Coding Strategy  

Colour is the fastest way for the human brain to separate information.  The following palette has proven effective in many designs, but the exact hues are a matter of personal preference – the key is consistency.  

| Net Class | Suggested Colour | Rationale |
|-----------|------------------|-----------|
| **Power rails** (5 V, 3.3 V, 1.8 V…) | Red (or orange) | Red draws attention; power nets often require wider traces and careful thermal management. |
| **Ground** | Gray or muted green | Ground is ubiquitous; a neutral colour prevents it from overwhelming the view. |
| **High‑speed / RF** | Bright yellow or cyan | High‑visibility colours flag nets that need controlled impedance, length matching, and extra clearance. |
| **USB / Debug** | Blue | Distinguishes communication links from power and RF. |
| **Switch‑mode power supply (SMPS)** | Pink or magenta | Differentiates the switching network (inductors, diodes, output caps) from static power rails. |
| **Miscellaneous signals** | Light pastel shades | Keeps the canvas readable without competing with critical colours. |

> **Tip** – Use the *Net Display Options* to switch from “Rat’s‑Nest only” to “All colours” so that both the air‑wires **and** the copper traces inherit the same hue, reinforcing the visual link. [Verified]  

---  

## 4. Using the Rat’s‑Nest as a Placement Guide  

1. **Identify critical clusters** – Look for dense bundles of coloured air‑wires (e.g., a blue USB‑debug cluster).  
2. **Align components** – Position the associated parts (connector, ESD protection, MCU pins) so that the air‑wires become short, straight, and orthogonal where possible.  
3. **Respect hierarchy** – Keep high‑speed clusters (yellow RF) away from noisy digital or power sections (red).  
4. **Iterate** – After a first placement pass, re‑run the rat’s‑nest view; any long, crossing air‑wires indicate a need for component relocation.  

> **Why this works** – Shorter, more direct routes reduce parasitic inductance and capacitance, improve signal integrity, and simplify DRC compliance. [Inference]  

---  

## 5. Workflow for Adding or Modifying Net Classes  

The following flowchart summarises the typical loop when a new net class is required after the schematic has already been created.  

```mermaid
flowchart TD
    A[Open Schematic] --> B[Edit → Schematic Setup]
    B --> C[Add Net Class (e.g., SNPS)]
    C --> D[Assign Nets to Class (wild‑card pattern)]
    D --> E[Save Schematic & Update PCB]
    E --> F[Open PCB Editor – Net Classes Panel]
    F --> G[Assign Colour to New Class]
    G --> H[Enable “All Colours” in Net Display Options]
    H --> I[Verify Rat’s‑Nest Colours Match Expected Nets]
    I --> J[Proceed with Placement & Routing]
```

> **Key point** – The net‑class definition lives in the schematic; once the PCB is refreshed, the new class appears automatically, ready for colour assignment. [Verified]  

---  

## 6. Best‑Practice Checklist  

| Practice | Reason |
|----------|--------|
| **Define net classes early** | Guarantees consistent rule sets and visual cues from the start. |
| **Use high‑visibility colours for critical nets** | Prevents accidental routing violations (e.g., insufficient spacing for RF). |
| **Keep the rat’s‑nest visible for all classes** | Hides nothing; you can always toggle visibility per class if the canvas becomes cluttered. |
| **Group related components based on coloured air‑wires** | Minimises trace length and reduces EMI coupling. |
| **Retrofit net classes via schematic when needed** | Changes propagate cleanly to the PCB, avoiding manual net‑list edits. |
| **Document colour conventions in the design handbook** | Ensures team members share the same visual language. |
| **Run DRC/ERC after each major placement step** | Early detection of clearance or connectivity errors saves re‑work. |
| **Consider DFM implications of colour‑driven placement** – e.g., keep dense clusters away from panel edges to avoid panel‑level routing complications. | Balances visual optimisation with manufacturability. [Inference]  

---  

## 7. Example Subsystem Relationship Diagram  

A high‑level view of how the coloured net classes interconnect the major board blocks.  

```mermaid
graph LR
    MCU[Microcontroller] -->|USB‑Debug (Blue)| USB[USB‑C Connector]
    MCU -->|RF (Yellow)| RF[RF Front‑End]
    MCU -->|Power (Red)| VCC[Power Rail]
    VCC -->|SMPS (Pink)| SMPS[Switch‑Mode Regulator]
    SMPS -->|Ground (Gray)| GND[Ground Plane]
    USB -->|ESD (Blue)| ESD[ESD Protection]
    RF -->|Antenna (Yellow)| ANT[External Antenna]
```

> **Interpretation** – The colour of each edge matches the net‑class colour, reinforcing the visual mapping between schematic blocks and PCB layout. [Verified]  

---  

## 8. Summary  

- **Rat’s‑nest** provides an immediate, geometry‑based map of un‑routed connections.  
- **Net classes** let you group, rule‑check, and colour‑code those connections for rapid visual analysis.  
- **Colour conventions** (red = power, gray = ground, bright = high‑speed) turn a cluttered air‑wire view into an intuitive placement guide.  
- **Workflow**: create/modify net classes in the schematic → update PCB → assign colours → use coloured rat’s‑nest to drive component placement → route with confidence.  

By integrating these practices into every new design, you reduce routing errors, improve signal integrity, and accelerate the overall layout process.   [Verified]