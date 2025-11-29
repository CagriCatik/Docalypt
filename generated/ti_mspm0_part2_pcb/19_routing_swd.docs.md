# Routing SWD, UART, and Associated Signals  

*This section documents the recommended methodology for routing Serial Wire Debug (SWD), UART, reset, and ancillary I²C connections on a typical 2‑layer board. The practices described balance signal‑integrity, manufacturability, and layout efficiency.*



## 1. Design‑Rule Preparation  

Before any trace is placed, the **Design Rule Check (DRC)** must be fully configured:

| Rule | Typical Setting | Rationale |
|------|----------------|-----------|
| Minimum trace width | 0.3 mm (as used for SWD/UART) | Guarantees copper thickness for current handling and satisfies most fab houses for 1 oz copper. |
| Minimum clearance | per fab specification (often 0.15 mm) | Prevents shorts and ensures reliable etching. |
| Minimum via annular ring | per fab specification | Avoids drilling failures. |
| Keep‑out zones for high‑speed or sensitive nets | optional | Reduces crosstalk. |

*Why?* A fully defined rule set prevents the creation of “unmanufacturable” geometry (e.g., a trace that is too narrow to clear a neighboring pad) and allows the DRC engine to catch violations automatically. **[Verified]**


## 2. Trace‑Width Strategy (Neck‑Down / Neck‑Up)  

1. **Start with the nominal width** (0.3 mm) when leaving a pad.  
2. **Neck down** only in the narrowest sections where clearance forces a smaller geometry. In KiCad this is done with **Shift + W** (or the equivalent “narrow” command).  
3. **Neck back up** to the nominal width as soon as the congestion is cleared (shortcut **W**).  

> **Benefit:** Wider traces reduce resistance, improve thermal performance, and are easier for the fab to reproduce. Narrow sections are kept to the absolute minimum required for clearance, preserving manufacturability while still fitting the layout. **[Inference]**


## 3. Routing Order & Topology  

A disciplined routing sequence minimizes back‑tracking and keeps the board tidy:

1. **SWCLK (Serial Wire Clock)** – route first, heading right‑hand side of the board.  
2. **SWDIO (Serial Wire Data I/O)** – follow the same path, keeping a modest separation from SWCLK.  
3. **RESET** – typically runs underneath the MCU; if space permits, a peripheral‑side detour is preferred to keep the trace short.  
4. **I²C (SCL/SDA)** – placed after the debug lines, moving leftward.  
5. **UART (TX/RX)** – routed after I²C, using the same “right‑to‑left” progression.  
6. **Power & Ground** – deferred until the signal nets are placed; they will often be routed underneath the previously placed traces.  

```mermaid
flowchart LR
    A[SWCLK] --> B[SWDIO]
    B --> C[RESET]
    C --> D[I²C]
    D --> E[UART]
    E --> F[Power & Ground]
    style A fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style F fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
```

*The diagram reflects the logical progression of routing from the right side of the board toward the left, ending with power distribution.* **[Inference]**


## 4. Handling Congested Areas  

### 4.1 90° Bends vs. Angled Traces  

- Use **45° or 90° bends** sparingly; a gentle arc reduces impedance discontinuities and eases fabrication.  
- When a tight clearance forces a 90° turn, keep the bend radius as large as the available space permits.  

### 4.2 Drag‑Mode Refinement  

- After the initial placement, employ KiCad’s **drag mode** (left‑mouse‑button drag) to fine‑tune trace positions and smooth out jagged sections.  
- This manual adjustment is especially useful for aesthetic improvement and for meeting specific clearance requirements without re‑routing from scratch.  

### 4.3 Under‑Component Routing  

- Routing a signal **under the MCU** (or any large component) is acceptable when no other nets compete for that space and the trace does not cross high‑frequency lines.  
- The trade‑off is a slightly longer path length versus a cleaner surface layout. In most low‑speed debug and UART nets, the added length is negligible. **[Inference]**  


## 5. Specific Net Examples  

### 5.1 SWCLK  

- **Start:** Pad → 0.3 mm width.  
- **Avoid:** Direct rightward movement that would intersect the SWDIO corridor.  
- **Solution:** Immediately divert upward, pass over the top of the board, then re‑enter the desired column after clearing the SWDIO lane.  

### 5.2 SWDIO  

- **Start:** Pad → 0.3 mm width.  
- **Goal:** Reach pad 2 of the Tag‑Connect header.  
- **Technique:** Slightly offset below the SWCLK trace, neck down only where the header’s pitch forces a tighter clearance, then restore the nominal width.  

### 5.3 RESET  

- **Path:** Between two MCU pads, passing under the microcontroller.  
- **Routing Detail:** Use a short 90° segment to enter the under‑component region, then exit toward the external reset header.  
- **Alternative:** A peripheral detour is possible but would increase trace length and may interfere with later power routing.  

### 5.4 I²C & UART  

- **Approach:** Follow the same “right‑to‑left” methodology, applying neck‑down only in the dense header area.  
- **Note:** Keep I²C lines close together to preserve the pair’s common‑mode noise rejection, but do not treat them as a differential pair requiring controlled impedance (standard for low‑speed I²C). **[Inference]**


## 6. Power Routing (Deferred)  

After all signal nets are placed, **power and ground planes** are added. Because many of the debug and UART traces occupy the upper layers, the power distribution will often be routed **underneath** these signals, using wider traces (or a solid plane) to meet current‑carrying requirements.  

- **Design tip:** Reserve a clear corridor for the main power rail before finalizing signal routing to avoid later re‑work.  
- **Manufacturability:** Wider power traces reduce the risk of copper thinning and improve thermal dissipation. **[Inference]**


## 7. Summary of Best Practices  

| Practice | Reason |
|----------|--------|
| Define full DRC rules before routing | Prevents illegal geometry early. |
| Use a standard trace width (0.3 mm) and only narrow where forced | Improves yield and reliability. |
| Route high‑priority nets (SWD, UART) first, moving from right to left | Reduces congestion and back‑tracking. |
| Apply “neck‑down” only in tight spots, then restore width | Balances clearance with manufacturability. |
| Employ drag‑mode for post‑routing cleanup | Achieves a tidy, production‑ready layout. |
| Allow under‑component routing for low‑speed signals when necessary | Saves surface area without compromising performance. |
| Defer power routing until signal nets are placed | Guarantees clear space for high‑current paths. |

By adhering to these guidelines, the board layout will be **DRC‑clean**, **manufacturable**, and **electrically robust**, while keeping the debug and communication interfaces easily accessible for testing and firmware development. **[Verified]**