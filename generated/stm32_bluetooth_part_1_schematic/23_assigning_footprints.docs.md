# Assigning Footprints  

Assigning the correct PCB footprints is a critical bridge between the schematic and the physical board. The process must respect electrical requirements, manufacturing capabilities, cost targets, and component availability. The following section outlines the systematic approach used to select and assign footprints for the reference design, together with the engineering rationale behind each decision.

---

## 1. Component‑Selection Criteria  

### 1.1 Capacitors  

| Parameter | Design rule | Typical choice | Rationale |
|-----------|-------------|----------------|-----------|
| **Voltage rating** | ≥ 2 × maximum DC voltage the part will see | 10 V for 3.3 V‑rated nets; 25 V for 5 V‑exposed nets | Doubling the expected voltage provides a safety margin against transients and derating; higher voltage parts are slightly more expensive but improve reliability. [Verified] |
| **Capacitance tolerance** | ±20 % acceptable for decoupling caps (e.g., 100 nF) | 80 nF – 120 nF range | Decoupling does not require tight tolerance; tighter (1 %) parts increase cost dramatically. [Verified] |
| **Dielectric type** | X7R or X5R for temperature‑stable behavior | X7R preferred | X7R offers ±15 % capacitance variation over –55 °C → +125 °C, suitable for most MCU supply rails. [Verified] |
| **Package size** | Smallest practical that meets voltage & capacitance | 0402 for 100 nF, 0603 for 4.7 µF, 0805 for 10 µH inductors (EOL) | 0402 minimizes board area but raises assembly difficulty; 0603/0805 provide a better balance for larger values. [Inference] |
| **Cost vs. performance** | Sort by price after filtering for electrical specs | Choose the lowest‑priced in‑stock part (≈ $0.09 for 100 nF, 10 V, X7R) | Cost is the dominant driver when multiple parts meet the electrical envelope. [Verified] |

Very small capacitors (≤ 0.8 pF) are placed in 0402 footprints because the pad capacitance is comparable to the component value; any further size reduction would not improve net performance. [Inference]

### 1.2 Resistors  

| Parameter | Design rule | Typical choice |
|-----------|-------------|----------------|
| **Voltage rating** | Must exceed the highest node voltage (≥ 5 V) | 0402 1 % 0.5 W parts are sufficient for signal‑level resistors |
| **Power dissipation** | Low‑power signals → ≤ 0.125 W | 0402 1 % series resistors for USB‑C SE lines |
| **Tolerance** | 1 % for precision paths (e.g., USB‑C) | 1 % 0402 |
| **Package** | 0402 (imperial “402”) for uniformity across the board | Simplifies library management and assembly tooling |

All resistors were assigned the 0402 imperial footprint (designated “R402”) to keep the component library consistent and to reduce the number of unique footprints the assembler must handle. [Verified]

### 1.3 Inductors  

| Parameter | Design rule | Typical choice |
|-----------|-------------|----------------|
| **Value** | Follow MCU reference design (e.g., 10 µH for power‑rail filter) | 10 µH 0805 (EOL) – keep footprint, replace part if needed |
| **Package** | Match reference part; retain footprint for alternatives | 0402 for 2.7 nH RF filter, 0805 for 10 µH |
| **Availability** | Use distributor filters (in‑stock, price‑sorted) | Select cheapest in‑stock part that meets inductance and current rating |

When a part is marked “end‑of‑life,” the same footprint is retained, allowing a drop‑in replacement from another manufacturer without redesigning the layout. [Inference]

### 1.4 Crystals  

| Parameter | Design rule | Selected part |
|-----------|-------------|----------------|
| **Frequency** | 32 MHz for MCU core, 32.768 kHz for RTC | NX‑201016‑32M (2 × 1.6 mm) and NX‑20112 (2 × 1.2 mm) |
| **Load capacitance** | 10 pF (derived from reference design) | C15 & C16 set to 10 pF each |
| **Tolerance** | 10 ppm for frequency stability | As per datasheet |
| **Footprint** | SMD crystal 2 × 1.6 mm → “Crystal_SMD_2x1.6mm”; 2 × 1.2 mm → “Crystal_SMD_2x1.2mm” | Directly assigned in KiCad |

Using the exact package dimensions from the reference design guarantees mechanical fit and correct stray capacitance modeling. [Verified]

### 1.5 Connectors & Switches  

| Component | Selection rationale |
|-----------|---------------------|
| **USB‑C receptacle** | Choose a widely‑available GCT 4105 footprint; preview 3‑D model to verify mechanical clearance. |
| **Header (2.54 mm pitch)** | Any standard 2.54 mm header footprint; PicoBlade preferred for compactness. |
| **UFL (RF) connector** | Hyros UFL footprint selected for antenna interface. |
| **Push‑button** | Generic SMD tactile switch footprint; size chosen to match board‑level ergonomics. |

All connector footprints were taken from the KiCad library, filtered by pin count to ensure symbol‑footprint parity. [Verified]

---

## 2. Footprint‑Assignment Workflow  

The following flowchart captures the repeatable process used for each component class. It emphasizes the use of distributor data (e.g., Mouser) to filter by electrical parameters, availability, and price before committing a footprint.

```mermaid
flowchart TD
    A[Start – Open Schematic] --> B{Component Type?}
    B -->|Capacitor| C[Filter by Voltage, Dielectric, Size]
    B -->|Resistor| D[Filter by Voltage, Power, Tolerance]
    B -->|Inductor| E[Filter by Inductance, Current, Size]
    B -->|Crystal| F[Match Frequency & Load Cap]
    B -->|Connector| G[Match Pin Count & Package]
    C --> H[Select Cheapest In‑Stock Part]
    D --> H
    E --> H
    F --> I[Assign SMD Crystal Footprint]
    G --> J[Select Library Footprint & Preview 3D]
    H --> K[Assign Imperial/Metric Footprint (0402, 0603, 0805)]
    I --> K
    J --> K
    K --> L[Annotate Part Number & Distributor]
    L --> M[Run ERC / DRC Checks]
    M --> N[Finalize Schematic]
    N --> O[Proceed to PCB Layout]
```

*The diagram reflects the iterative nature of footprint assignment and highlights the verification step (ERC/DRC) before moving to layout.* [Verified]

---

## 3. Design‑for‑Manufacturability (DFM) & Cost Trade‑offs  

1. **Package density vs. assembly difficulty** – 0402 parts provide the smallest board area but demand precise placement and reflow profiles. For hand‑solderable prototypes, larger 0603 or 0805 packages are preferred.  
2. **Standardised footprints** – Using a single footprint family (e.g., all 0402 resistors and capacitors) reduces the number of unique tooling setups, lowering both NRE (non‑recurring engineering) costs and the risk of library mismatches.  
3. **Component cost hierarchy** – After electrical filtering, parts are sorted by price. Selecting the lowest‑priced in‑stock component yields a cost‑effective BOM while preserving performance margins.  
4. **End‑of‑life (EOL) parts** – Retaining the original footprint for an EOL component enables a straightforward part substitution without layout changes, preserving mechanical and electrical integrity.  
5. **Connector choice** – Selecting a connector footprint that matches a widely‑used part (e.g., GCT USB‑C) improves supply chain robustness and reduces the need for custom mechanical design.  

These considerations collectively ensure that the board can be fabricated at scale without sacrificing reliability or performance. [Inference]

---

## 4. Verification & Documentation  

- **Electrical Rule Check (ERC)** – Run after each batch of footprint assignments to catch mismatched voltage ratings, missing pins, or incorrect net connections.  
- **Design Rule Check (DRC)** – Validate clearance, copper‑to‑copper spacing, and pad‑to‑edge distances, especially for high‑voltage or RF sections.  
- **BOM enrichment** – Populate the BOM with manufacturer part numbers, distributor links, and the exact footprint name to streamline procurement and assembly.  
- **Schematic review** – Confirm that all pin‑outs, current consumptions, and power‑rail connections match the MCU datasheet and reference design before proceeding to layout.  

A disciplined verification routine prevents costly downstream revisions and ensures that the final PCB meets both electrical and manufacturability specifications. [Verified]

---

## 5. Summary of Best Practices  

- **Double‑margin voltage ratings** for capacitors and resistors to accommodate transients.  
- **Prefer X7R/X5R dielectrics** for temperature‑stable decoupling.  
- **Select the smallest practical package** that still allows reliable assembly; move to larger packages for hand‑soldered prototypes.  
- **Use distributor filters** (in‑stock, price‑sorted) to create a cost‑optimized BOM while meeting all electrical constraints.  
- **Maintain a uniform footprint library** (e.g., 0402, 0603, 0805) to simplify assembly and reduce library errors.  
- **Assign footprints before running ERC/DRC** to catch mismatches early.  
- **Document manufacturer part numbers and distributors** directly in the schematic to avoid ambiguity during procurement.  

By adhering to these guidelines, the transition from schematic to layout becomes predictable, cost‑effective, and manufacturable.