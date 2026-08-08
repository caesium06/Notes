

---

# CCNA Study Notes: Interfaces and Cables

## 1. Network Fundamentals & Units of Measurement

### Why Standards & Protocols Matter

* **Protocols/Standards:** Agreed-upon rules that allow devices from different manufacturers to communicate seamlessly, both physically (connectors, cabling) and logically (IP protocols).
* **Speed Measurement:** Network speeds are measured in **bits per second (bps)**, *not* bytes.
* **1 Byte = 8 Bits**
* Storage is measured in **Bytes** (e.g., Gigabytes); transmission speed is measured in **bits** (e.g., Gigabits).



### Units of Data Rate

| Unit | Equivalent Bits | Value |
| --- | --- | --- |
| **Kilobit (Kb)** | $10^3$ bits | 1,000 bits |
| **Megabit (Mb)** | $10^6$ bits | 1,000,000 bits |
| **Gigabit (Gb)** | $10^9$ bits | 1,000,000,000 bits |
| **Terabit (Tb)** | $10^{12}$ bits | 1,000,000,000,000 bits |

---

## 2. Copper Cabling (UTP & Ethernet Standards)

### Unshielded Twisted Pair (UTP)

* **Design:** Contains 8 individual copper wires twisted into **4 pairs**.
* **Interference Reduction:** Twisting the wire pairs protects against **Electromagnetic Interference (EMI)**.
* **Connector Type:** **RJ-45** (Registered Jack 45), which features 8 pins.
* **Maximum Distance:** **100 meters** (for all twisted-pair Ethernet standards).

### Copper Ethernet Standards (IEEE 802.3)

| Standard Name | Official Standard | Wires / Pairs Used | Max Distance | Speed |
| --- | --- | --- | --- | --- |
| **10BASE-T** | IEEE 802.3 | 4 wires (2 pairs) | 100 m | 10 Mbps |
| **100BASE-T** | IEEE 802.3u | 4 wires (2 pairs) | 100 m | 100 Mbps (Fast Ethernet) |
| **1000BASE-T** | IEEE 802.3ab | 8 wires (4 pairs) | 100 m | 1 Gbps (Gigabit Ethernet) |
| **10GBASE-T** | IEEE 802.3an | 8 wires (4 pairs) | 100 m | 10 Gbps |

---

## 3. Pinouts & Cable Types (10BASE-T / 100BASE-T)

### Pin Assignments

* **PCs, Routers, and Firewalls:**
* **Transmit (Tx):** Pins 1 & 2
* **Receive (Rx):** Pins 3 & 6


* **Switches:**
* **Receive (Rx):** Pins 1 & 2
* **Transmit (Tx):** Pins 3 & 6



### Straight-Through vs. Crossover Cables

* **Straight-Through Cable:**
* Pin mapping is identical on both ends (Pin 1 to Pin 1, Pin 2 to Pin 2, etc.).
* Used for connecting **unlike** device types:
* PC $\leftrightarrow$ Switch
* Router $\leftrightarrow$ Switch




* **Crossover Cable:**
* Pairs are crossed: Pin 1 $\leftrightarrow$ Pin 3, Pin 2 $\leftrightarrow$ Pin 6.
* Used for connecting **like** device types (or devices transmitting on the same pins):
* Switch $\leftrightarrow$ Switch
* Router $\leftrightarrow$ Router
* PC $\leftrightarrow$ PC
* PC $\leftrightarrow$ Router




* **Auto MDI-X:**
* Modern device feature that automatically detects the required pin assignments and adjusts Tx/Rx dynamically.
* Allows straight-through cables to be used between any devices.



### 1000BASE-T / 10GBASE-T Key Differences

* Uses all **4 pairs (8 wires)**.
* Each pair is **bidirectional** (transmits and receives simultaneously on the same pair).

---

## 4. Fiber-Optic Cabling

### Overview & Structure

* Transmits signals using **light impulses over glass fibers** (instead of electrical signals over copper).
* **Connectors:** Plug into **SFP (Small Form-factor Pluggable)** transceivers.
* **Duplex Design:** Uses two separate fibers—one dedicated to transmitting (Tx) and one to receiving (Rx).

### Cable Construction Layers (Inside to Outside)

1. **Core:** Fiberglass core carrying light.
2. **Cladding:** Reflective coating that keeps light contained within the core.
3. **Buffer:** Protective layer preventing glass breakage.
4. **Outer Jacket:** Outer cable casing.

### Multimode vs. Single-Mode Fiber

| Feature | Multimode Fiber (MMF) | Single-Mode Fiber (SMF) |
| --- | --- | --- |
| **Core Diameter** | Wider | Narrower |
| **Light Source** | LED (cheaper) | Laser (more expensive) |
| **Light Entry Angles** | Multiple modes/angles | Single mode/angle |
| **Distance Capability** | Shorter (up to ~550m - 2km) | Longer (up to 10km - 40km+) |
| **Cost** | Lower cost | Higher cost |

### Fiber Ethernet Standards

| Standard Name | Official Standard | Cable Type | Max Distance | Speed |
| --- | --- | --- | --- | --- |
| **1000BASE-LX** | IEEE 802.3z | MMF / SMF | 550m (MMF) / 5km (SMF) | 1 Gbps |
| **10GBASE-SR** | IEEE 802.3ae | MMF | 400 m | 10 Gbps |
| **10GBASE-LR** | IEEE 802.3ae | SMF | 10 km | 10 Gbps |
| **10GBASE-ER** | IEEE 802.3ae | SMF | 30 km | 10 Gbps |

---

## 5. Summary Comparison: UTP vs. Fiber-Optic

| Property | Copper (UTP) | Fiber-Optic |
| --- | --- | --- |
| **Cost** | Lower (Cables & RJ-45 ports) | Higher (Cables & SFP transceivers) |
| **Max Distance** | Short (100 meters max) | Very Long (Up to tens of kilometers) |
| **EMI Susceptibility** | Vulnerable (reduced by twisting pairs) | Immune to electrical interference |
| **Security** | Minor risk (faint signal leakage) | Highly secure (no light leakage) |
| **Primary Use** | End-host connection to switches | Switch-to-switch, backbones, inter-building |