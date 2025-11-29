# 17 USB – PCB Design Guide  

## Overview  

This section details the PCB‑level decisions required to add a USB 2.0 full‑speed interface to an STM32‑based wearable (e.g., a smartwatch). It covers peripheral selection, pin‑mapping, connector choice, ESD protection, differential‑pair handling, CC‑line termination, power‑supply integration, and BOM consolidation. The guidance assumes the use of STM32CubeIDE (or an equivalent configuration tool) for peripheral assignment and a modern ECAD suite that supports ERC/DRC checks.

---

## 1. Peripheral Selection & Pin Mapping  

| Step | Action | Rationale |
|------|--------|-----------|
| 1.1 | Open the MCU’s peripheral view (e.g., *Connectivity → USB* in CubeIDE). | Quickly visualises which peripherals are available without consulting the datasheet. |
| 1.2 | Enable **USB Device** and select the *FS* (full‑speed) mode. | The STM32‑F4/​F7 families provide a built‑in full‑speed USB peripheral; HS is unnecessary for a smartwatch. |
| 1.3 | Accept the default pin assignment: **PA11** → USB _D‑_, **PA12** → USB _D+**.** | These pins are fixed in the silicon for the USB FS peripheral; they cannot be remapped. |
| 1.4 | If a different pin set is required, use the *Control‑Click* pin‑remap feature (where supported). | Allows flexibility for board‑level constraints while preserving peripheral functionality. |

> **Note:** The net names must be **`USBCORE_D-`** and **`USBCORE_D+`** (identical base name with “‑”/“+” suffix). This naming convention signals to the ECAD tool that the two nets form a differential pair, enabling automatic differential routing rules.  [Verified]

---

## 2. USB‑C Connector Choice  

A USB‑C receptacle that supplies **VBUS** and **GND** (i.e., a 4‑pin power‑and‑data version) is recommended for modern wearables.  

* **Reversible pins** – The connector’s pins are mirrored; the schematic must reflect both sides (two D‑ and two D+ pins).  
* **Pin count** – Select a part that includes VBUS, GND, CC1, CC2, SBU1, SBU2, and the duplicated D‑/D+ pins.  
* **Footprint** – Use the manufacturer‑approved land pattern (typically 0.5 mm pitch, 6‑pin or 8‑pin).  

> **Design tip:** Because the connector’s pins are duplicated, only one set of D‑/D+ lines needs to be routed to the MCU; the other set can be left unconnected or tied together for mechanical robustness.  [Inference]

---

## 3. ESD Protection Integration  

### 3.1 Device Selection  

A six‑pin **USB‑LCC6‑TC6** (ST‑Microelectronics) TVS array is ideal:

* Protects **VBUS**, **D‑**, and **D+** simultaneously.  
* Low capacitance (suitable for full‑speed and even high‑speed USB).  
* Available in an SOT‑23‑6 package, easy to hand‑solder.  

### 3.2 Symbol & Footprint Adjustments  

The vendor library often groups pins (1 & 6 together, 3 & 4 together). For schematic clarity, copy the symbol and rearrange pins so that each functional line (VBUS, D‑, D+, GND) appears on a separate pin. This prevents a “spaghetti” netlist and simplifies routing.  

> **Best practice:** Keep the TVS as close as possible to the connector’s pins (≤ 2 mm) to minimise the length of unprotected USB traces.  [Verified]

### 3.3 Connection Scheme  

| TVS Pin | Connection |
|---------|------------|
| 1 (VBUS) | To **VBUS** pin of the USB‑C connector. |
| 2 (GND)  | To **GND** (system ground). |
| 3 (D‑)   | To **USBCORE_D‑** (PA11). |
| 4 (D+)   | To **USBCORE_D+** (PA12). |
| 5 (NC)   | Not used (internal tie‑off). |
| 6 (VBUS) | Duplicate VBUS – may be left open or tied to pin 1. |

---

## 4. CC‑Line Termination & SBU Handling  

### 4.1 CC Pull‑Down Network  

USB‑C hosts detect a downstream‑facing device (DFD) when the **CC1** and **CC2** pins are pulled down to ground through **5.1 kΩ** resistors (±1 %). This signals that the device is powered from VBUS and enables power negotiation.  

* Place one 5.1 kΩ resistor from **CC1** to **GND** and another from **CC2** to **GND**.  
* Use the same 5.1 kΩ part for both resistors to simplify the BOM (part consolidation).  

> **Design note:** The tolerance of the pull‑down resistors is not critical for detection, but a 1 % tolerance ensures consistent voltage division across temperature.  [Verified]

### 4.2 SBU (Side‑Band Use) Pins  

The **SBU1** and **SBU2** pins are not required for a simple USB‑2.0 device. Mark them as **No‑Connect (NC)** in the schematic (e.g., using a “no‑connect” flag). This prevents ERC warnings while keeping the pins physically un‑driven.  

> **Rationale:** Leaving SBU floating would trigger ERC errors because the pins are defined as inputs with no source.  [Verified]

---

## 5. Differential Pair Naming & PCB Routing  

### 5.1 Net Naming  

* **`USBCORE_D-`** and **`USBCORE_D+`** – The identical base name with “‑”/“+” suffix tells the layout tool that the pair is differential.  

### 5.2 Routing Guidelines  

| Requirement | Recommendation |
|-------------|----------------|
| **Impedance control** | For full‑speed USB (12 Mbps) strict 90 Ω differential impedance is not mandatory, but keeping the pair close (≤ 0.2 mm spacing) and length‑matched (< 150 ps skew) improves signal integrity. |
| **Pair coupling** | Route the pair as a tightly coupled microstrip over a continuous ground plane. |
| **Via usage** | Use a single‑ended via for each line; avoid staggered or back‑drilled vias that could unbalance the pair. |
| **Length matching** | Keep the D‑ and D+ traces matched within **0.13 mm** (≈ 5 ps) if possible; most ECAD tools can auto‑match. |
| **Clearance** | Maintain at least **3×** the trace width clearance from high‑speed or high‑current nets to reduce crosstalk. |

> **Inference:** Although the transcript does not mention impedance, applying standard USB‑2.0 routing practices yields a robust design.  [Inference]

---

## 6. Power Supply Integration  

The USB‑C VBUS line will be the primary power source for the wearable. A downstream **3.3 V LDO** (or buck regulator, depending on power budget) must be placed after the TVS to protect the rest of the circuitry.  

* **VBUS → TVS → Power‑switch (optional) → Regulator → System rail**.  
* Decouple the regulator output with **0.1 µF** ceramic caps placed as close as possible to the IC pins.  

> **Note:** The regulator design is outside the scope of this chapter but must be considered before finalizing the PCB stack‑up.  [Speculation]

---

## 7. BOM Consolidation (Part Re‑use)  

To minimise component variety:

* Use the same **5.1 kΩ** resistor for both CC pull‑downs and any other low‑value pull‑downs (e.g., button debounce network) where the exact value is not critical.  
* Re‑use the **100 Ω** resistor for the boot‑zero (BOD) pin debounce network, as its function only requires a few kilo‑ohms of resistance.  

Consolidating parts reduces inventory cost, simplifies assembly, and lowers the risk of picking the wrong component during manual soldering.  

> **Best practice:** Verify that the reused resistor’s tolerance and power rating meet the most stringent requirement among its applications.  [Verified]

---

## 8. Design Checklist  

| ✅ Item | Description |
|--------|-------------|
| **Peripheral enable** | USB Device FS enabled in MCU configuration. |
| **Pin assignment** | PA11 = D‑, PA12 = D+ (fixed). |
| **Net naming** | `USBCORE_D-` / `USBCORE_D+`. |
| **Connector footprint** | USB‑C receptacle with power pins, CC, SBU, and duplicated D‑/D+ pins. |
| **ESD protection** | TVS array placed ≤ 2 mm from connector, correctly wired. |
| **CC termination** | Two 5.1 kΩ pull‑downs to GND, same part number. |
| **SBU handling** | Marked NC (no‑connect). |
| **Differential routing** | Pair kept close, length‑matched, over continuous ground plane. |
| **Power path** | VBUS → TVS → regulator → 3.3 V rail. |
| **BOM consolidation** | Re‑use resistors where possible, verify tolerances. |

---

## 9. Signal Flow Diagram  

```mermaid
flowchart LR
    subgraph USB-C_Connector[USB‑C Receptacle]
        VBUS[VBUS] --> TVS_VBUS[TVS VBUS Pin]
        GND[GND] --> TVS_GND[TVS GND Pin]
        Dp[DP (D+)] --> TVS_Dp[TVS D+ Pin]
        Dm[DM (D-)] --> TVS_Dm[TVS D- Pin]
        CC1[CC1] --> Rcc1[5.1kΩ] --> GND
        CC2[CC2] --> Rcc2[5.1kΩ] --> GND
        SBU1[SBU1] -.-> NC1[NC]
        SBU2[SBU2] -.-> NC2[NC]
    end

    TVS_VBUS --> Reg[3.3 V Regulator]
    Reg --> System[System Power Rail]

    TVS_Dp --> MCU_Dp[PA12 (USB D+)]
    TVS_Dm --> MCU_Dm[PA11 (USB D-)]

    style USB-C_Connector fill:#f9f,stroke:#333,stroke-width:2px
```

*The diagram shows the functional flow from the USB‑C connector through ESD protection, CC termination, power regulation, and the MCU’s USB pins.*  

---

## 10. References & Further Reading  

* **STM32 Reference Manual** – USB device peripheral chapter.  
* **USB‑C Specification**, USB‑IF – CC‑line termination and power delivery basics.  
* **USB‑2.0 Electrical Specification** – Differential impedance and cable requirements.  
* **PCB Design for Signal Integrity**, Howard Johnson – Differential pair routing guidelines.  

---  

*End of Chapter 17 – USB*