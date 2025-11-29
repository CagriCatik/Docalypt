# 33 Stitching  

## 1. Purpose of Via Stitching  

Via stitching (also called **ground stitching** or **plane stitching**) is the practice of placing a regular array of plated‑through vias (PTH) that connect one or more reference planes (typically ground) to each other and to copper pours (fills). The primary objectives are:

* **Suppress floating copper islands** – isolated copper pours can act as resonant patches at RF frequencies, creating unwanted emission and susceptibility. Stitching ties these islands to a solid reference, eliminating self‑resonance.  
* **Improve return‑path continuity** – a dense network of vias reduces the effective inductance of the ground return, which is critical for high‑frequency signals such as 2.4 GHz Bluetooth.  
* **Enhance plane‑to‑plane coupling** – tighter coupling between adjacent planes (e.g., ground‑plane to power‑plane) reduces loop area and improves overall impedance control.  
* **Assist DFM** – a regular via pattern simplifies fabrication (drilling, plating) and inspection, and it provides a reliable thermal path for heat dissipation.  

These benefits are especially important when the board contains **high‑speed or RF traces**, dense copper fills, or large ground/power planes.

---

## 2. Determining the Stitching Pitch  

### 2.1 Critical Length Concept  

The maximum spacing between stitching vias is governed by the **critical length** of the highest‑frequency signal on the board. A common rule‑of‑thumb is:

\[
\text{Critical Length} \approx \frac{\lambda}{20}
\]

where \(\lambda\) is the wavelength of the signal in the PCB dielectric.

* **Signal frequency** – for a Bluetooth Low Energy (BLE) link, the carrier is **2.4 GHz**.  
* **Propagation velocity** – \(v = \frac{c}{\sqrt{\varepsilon_r}}\) where \(c = 3\times10^8\ \text{m/s}\) and \(\varepsilon_r\) is the dielectric constant of the substrate. In the example, \(\varepsilon_r \approx 4.29\), giving \(v \approx 1.45\times10^8\ \text{m/s}\).  
* **Wavelength** – \(\lambda = \frac{v}{f} \approx \frac{1.45\times10^8}{2.4\times10^9} \approx 60\ \text{mm}\).  
* **Critical length** – \(\lambda/20 \approx 3\ \text{mm}\).  

Thus, **stitching vias should be placed no more than ~3 mm apart** to ensure that the return path does not become a resonant stub at the operating frequency. Using a tighter pitch (e.g., 2 mm) provides additional safety margin and does not penalize cost or manufacturability for typical board sizes.  

> **Verdict:** For a 2.4 GHz design, a stitching pitch ≤ 3 mm is recommended.  [Verified]

### 2.2 Via Size and Placement Options  

Two practical approaches are common:

| Approach | Via size (typical) | Placement strategy | Advantages |
|----------|-------------------|--------------------|------------|
| **Uniform grid** | 7 mil drill / 3 mil pad (or 9.4 mil drill for higher current) | Regular lattice (e.g., 1 mm or 2 mm spacing) across the entire board | Predictable DRC, easy to verify, uniform impedance improvement |
| **Scattered islands** | Same as above | Vias placed only around large copper pours or “islands” that would otherwise float | Reduces via count, saves drill time, still eliminates resonances where needed |

Both methods satisfy the ≤ 3 mm spacing rule when the grid is dense enough (e.g., 1 mm grid) or when scattered vias are placed at the edges of each copper island. The choice depends on **board size, via count budget, and DFM considerations**.  

> **Inference:** Larger 9.4 mil vias may be chosen when higher current return or mechanical robustness is required.  [Inference]

---

## 3. Practical Implementation  

1. **Identify copper pours** – Use the PCB editor’s “fill” or “polygon” inspection tools to locate isolated copper regions (ground, power, or signal fills).  
2. **Create a stitching net** – Define a dedicated net (e.g., `GND_STITCH`) that is electrically tied to the primary ground net.  
3. **Place vias**  
   * For a **uniform grid**, enable the “via array” or “grid placement” tool, set the desired pitch (≤ 3 mm), and populate the entire board.  
   * For **targeted stitching**, manually place vias around each island, ensuring the maximum distance between any two adjacent stitching vias does not exceed the critical length.  
4. **Verify spacing** – Use the measurement tool (often `Ctrl+Shift+M` in many ECAD suites) to confirm that the largest gap is within the calculated limit.  
5. **Run DRC/ERC** – Ensure that the stitching vias do not violate clearance rules, especially near high‑voltage nets or component pads.  
6. **Inspect in 3‑D view** – Visualize the via distribution (e.g., `Alt+3`) to confirm coverage and to spot any floating copper that may have been missed.  

---

## 4. Impact on Signal Integrity and EMI  

* **Reduced inductance** – A dense via network lowers the loop inductance of the ground return, which directly improves the **rise‑time performance** of high‑speed edges.  
* **Controlled impedance** – By tying adjacent planes together, the effective dielectric thickness between them is reduced, tightening the characteristic impedance of microstrip or stripline traces that reference those planes.  
* **Suppressed resonances** – Floating copper islands can act as half‑wave resonators at frequencies where their dimensions approach \(\lambda/2\). Stitching breaks up these resonant paths, reducing both conducted and radiated emissions.  
* **Improved EMC compliance** – A continuous ground plane with regular stitching provides a low‑impedance shield, helping the design meet regulatory limits for radiated emissions.  

> **Speculation:** In a multi‑layer stackup, stitching between non‑adjacent planes (e.g., top ground to inner power) can further improve decoupling, but may increase manufacturing cost due to additional blind/buried vias.  [Speculation]

---

## 5. Design Trade‑offs  

| Factor | Impact of More Stitching | Impact of Less Stitching |
|--------|--------------------------|--------------------------|
| **Cost** | Slight increase in drill time and copper usage; negligible for typical board volumes. | Lower drill count, marginal cost saving. |
| **Manufacturability** | Uniform grids simplify panelization and inspection; high via density may approach drill‑hole tolerance limits. | Fewer vias reduce risk of drill breakage, but irregular placement can complicate DRC. |
| **Performance** | Better return‑path continuity, lower EMI, improved impedance control. | Potential for resonant islands, higher loop inductance, degraded high‑frequency performance. |
| **Reliability** | More vias provide redundant ground paths, beneficial for thermal and mechanical stress. | Fewer redundant paths may increase susceptibility to open‑via failures. |

The optimal balance is usually **to adopt a uniform grid with a pitch at or below the critical length** (≈ 3 mm for 2.4 GHz). This approach delivers the performance benefits while keeping cost and DFM impact minimal.

---

## 6. Recommended Workflow  

```mermaid
flowchart TD
    A[Define highest‑frequency signal] --> B[Calculate wavelength λ]
    B --> C[Derive critical length = λ/20]
    C --> D[Set stitching pitch ≤ critical length]
    D --> E{Choose placement strategy}
    E -->|Uniform grid| F[Create via array (e.g., 1 mm spacing)]
    E -->|Targeted islands| G[Place vias around each copper pour]
    F --> H[Run DRC / ERC]
    G --> H
    H --> I[Verify spacing with measurement tool]
    I --> J[Inspect in 3‑D view]
    J --> K[Finalize layout and generate fabrication data]
```

*Step 1* – Identify the **fastest signal** (e.g., 2.4 GHz Bluetooth).  
*Step 2* – Compute the **critical length** and set a **stitching pitch** ≤ 3 mm.  
*Step 3* – Decide between a **uniform grid** or **targeted stitching** based on board size and via budget.  
*Step 4* – Populate the stitching vias, run **DRC/ERC**, and verify that **no gap exceeds the pitch**.  
*Step 5* – Perform a **3‑D visual inspection** to ensure all copper islands are tied down.  
*Step 6* – Proceed to **fabrication data generation** (Gerbers, drill files).  

Following this systematic approach guarantees that the board’s ground network remains robust across the entire operating frequency range, while keeping manufacturing complexity under control.   [Verified]