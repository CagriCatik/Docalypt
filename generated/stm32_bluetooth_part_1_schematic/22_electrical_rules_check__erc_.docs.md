# 22 – Electrical Rules Check (ERC)

## 1. Purpose of ERC  

The **Electrical Rules Check (ERC)** is the first automated verification step after schematic annotation. Its goal is to catch logical connectivity problems that would otherwise become costly re‑work in layout or hardware. Typical ERC checks include:

| Check | Typical error condition |
|-------|--------------------------|
| **Un‑connected pins** | A pin has no net assignment. |
| **Input not driven** | An input pin (e.g., a logic “IN” or power “VCC”) is not connected to any output pin that can source the required signal or voltage. |
| **Multiple drivers** | Two or more output pins are tied together without a proper bus‑or‑wire‑or‑tri‑state arrangement. |
| **Power‑ground mismatches** | Power input pins are not linked to a defined power net. |
| **Spice‑only tests** | Checks that rely on SPICE models (ignored when no models are attached). |

These checks are performed against the **ERC rule set** defined in **Edit → Schematic Setup → Electrical Rules Check**. The severity of each rule (Error, Warning, Info) can be tuned, but the default configuration is sufficient for most designs. [Verified]

---

## 2. Typical ERC Workflow  

```mermaid
flowchart TD
    A[Complete schematic annotation] --> B[Open Schematic Setup → ERC]
    B --> C[Run ERC]
    C --> D{Violations?}
    D -- Yes --> E[Inspect each violation]
    E --> F[Fix schematic (add nets, correct symbols, add power flags)]
    F --> C
    D -- No --> G[Proceed to footprint assignment]
```

*The loop continues until the ERC reports **no errors** (only warnings or ignored tests may remain). [Inference]*

---

## 3. Common ERC Findings and Their Remedies  

### 3.1 Un‑driven Power Pins  

**Symptom** – ERC reports *“Input Power Pin is not driven by any output power pins.”*  

**Root cause** – The schematic symbol does not correctly expose a power **output** pin, or the net is not linked to a **power flag** (a dedicated power symbol that defines a net as a source).  

**Remedy** –  

1. **Add a Power Flag**:  
   * Press **`P`** → *Add Power Symbol* → select **Power Flag** (e.g., `+5V`, `GND`).  
   * Wire the flag to the net that should supply the voltage.  

2. **Validate the Symbol**:  
   * If the library part (e.g., *VX_SMPS*) incorrectly defines a power output as an input, either edit the symbol or replace it with a correctly modeled part.  

After adding the flags, re‑run ERC. The power‑pin error should disappear. [Verified]

### 3.2 Ground Net Not Driven  

**Symptom** – Similar ERC message for the ground pin.  

**Remedy** – Add a **ground power flag** (`GND`) to the ground net and connect it with a wire. Re‑run ERC. [Verified]

### 3.3 Ignored SPICE Tests  

When no SPICE models are attached to components, ERC will list an *“Ignored test – SPICE model not found.”* This is harmless and can be dismissed. [Verified]

### 3.4 Library Symbol Quality  

A poorly defined symbol (e.g., a SMPS block that only shows a power **input** pin) can generate false ERC errors.  

**Best practice** –  
* Use vetted libraries from the vendor or a controlled internal library.  
* Review each symbol’s pin types (Input, Output, Power, Passive) before placing it.  
* If a symbol is ambiguous, edit the symbol to correctly label pins. [Inference]

---

## 4. Preparing for Footprint Assignment  

Once ERC reports **zero errors**, the schematic is considered electrically sound and ready for the next stage: **footprint assignment**.  

* The **Run Footprint Assignment** tool (top‑right toolbar) highlights components without an assigned footprint (yellow background).  
* Typical components awaiting footprints include passive parts (capacitors, resistors, inductors) and any custom devices.  

Assigning footprints **after** ERC ensures that any net‑level changes (e.g., adding power flags) are already reflected, preventing mismatches between schematic and layout. [Inference]

---

## 5. ERC Best‑Practice Checklist  

| Step | Reason | Recommendation |
|------|--------|----------------|
| **Run ERC early** | Catches schematic logic errors before layout. | After initial annotation, before any routing. |
| **Resolve all *Error* severity items** | Errors block layout generation. | Treat warnings as optional but review them. |
| **Use power flags for every supply rail** | Guarantees ERC sees a driver for power pins. | Add `+V`, `GND`, `VCC`, etc., as needed. |
| **Validate library symbols** | Prevents false positives/negatives. | Prefer manufacturer‑approved libraries; edit if necessary. |
| **Ignore SPICE‑only tests when no models** | Avoids cluttering the error list. | Keep SPICE models attached only when performing simulation. |
| **Re‑run ERC after each schematic edit** | Ensures new changes haven’t introduced fresh errors. | Automate with a shortcut or script if possible. |
| **Document any intentional violations** | Some designs deliberately leave pins floating (e.g., optional features). | Change severity to *Info* or add a comment in the schematic. |  

---

## 6. Trade‑offs and Design Decisions Reflected in ERC  

| Decision | Impact on Cost / Complexity | ERC Relevance |
|----------|-----------------------------|---------------|
| **Using generic power symbols vs. dedicated power‑flag nets** | Minimal cost impact; adds a tiny amount of schematic clutter. | Power‑flag nets eliminate ERC “un‑driven power pin” errors, reducing re‑work. |
| **Choosing a third‑party library vs. creating a custom symbol** | Custom symbols increase engineering time but improve accuracy. | Accurate pin types reduce false ERC violations and improve downstream DRC. |
| **Running SPICE simulation** | Requires licensed tools and model acquisition. | Enables additional ERC checks (e.g., voltage level validation) but adds complexity. |  

Understanding these trade‑offs helps the designer decide when to invest effort in library hygiene versus accepting a higher ERC warning count. [Inference]

---

## 7. Summary  

The ERC stage is a **gatekeeper** that validates the logical integrity of the schematic before any physical layout work begins. By:

* Adding **power flags** to define supply sources,
* Ensuring **library symbols** correctly label pin directionality,
* Ignoring irrelevant SPICE tests, and
* Resolving all **Error‑severity** violations,

the design proceeds to footprint assignment with confidence that the netlist is sound. This disciplined approach reduces costly iterations later in the PCB design flow and aligns the schematic with best‑practice DFM/DFA guidelines. [Verified]