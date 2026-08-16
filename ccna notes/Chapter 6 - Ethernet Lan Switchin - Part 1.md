Here are structured study notes based on the CCNA video transcript covering Ethernet LAN Switching.

---

# CCNA Study Notes: Ethernet LAN Switching (Part 1)

## 1. OSI Model & Encapsulation Review

* **Layer 1 (Physical):** Defines physical medium characteristics (voltage, connectors, cable specs, transmission limits).
* *Example:* Ethernet UTP cables (max 100m).


* **Layer 2 (Data Link):** Provides node-to-node connectivity and data formatting. Detects physical layer errors.
* *Devices:* Switches.
* *Addressing:* MAC Addresses (Layer 2), distinct from IP Addresses (Layer 3).


* **Encapsulation Recap (PDUs):**
* Data $\rightarrow$ **Segment** (L4 Header added) $\rightarrow$ **Packet** (L3 Header added) $\rightarrow$ **Frame** (L2 Header/Trailer added).



## 2. Ethernet Frame Structure

Ethernet is the L2 protocol for virtually all LANs. An Ethernet frame consists of a **Header** and a **Trailer**.

| Field | Size (Bytes) | Description |
| --- | --- | --- |
| **Preamble** | 7 | Alternating 1s and 0s (10101010) for clock synchronization. |
| **SFD** | 1 | Start Frame Delimiter (10101011) to signal the start of the frame. |
| **Destination MAC** | 6 | Layer 2 address of the receiving device. |
| **Source MAC** | 6 | Layer 2 address of the sending device. |
| **Type/Length** | 2 | Indicates the L3 protocol (Type) or frame size (Length). |
| **FCS** | 4 | Frame Check Sequence (Trailer) for error detection. |

* **Total Header/Trailer size:** 26 bytes.
* **FCS (Frame Check Sequence):** Uses a **CRC (Cyclic Redundancy Check)** algorithm to detect data corruption during transmission.

### Type vs. Length Field Logic

* **Value $\le$ 1500:** Indicates the **Length** of the encapsulated packet in bytes.
* **Value $\ge$ 1536:** Indicates the **Type** of the encapsulated protocol.
* `0x0800` = IPv4
* `0x86DD` = IPv6



---

## 3. MAC Addresses (Media Access Control)

* **Definition:** A 48-bit (6-byte) physical address assigned to a device NIC (Network Interface Card) at the time of manufacturing. Also called a **Burned-In Address (BIA)**.
* **Structure:**
* **OUI (Organizationally Unique Identifier):** The first 24 bits (3 bytes); assigned to the manufacturer (e.g., Cisco).
* **Device ID:** The second 24 bits (3 bytes); unique to the specific device.


* **Format:** Written as 12 hexadecimal characters (e.g., `AA.AA.AA.00.00.01`).

### Hexadecimal Basics

* Base-16 system (0–9 and A–F).
* A=10, B=11, C=12, D=13, E=14, F=15.
* Used for representing MAC addresses and later IPv6 addresses.

---

## 4. Ethernet Switch Operations

Switches use a **MAC Address Table** to determine where to forward frames.

### Learning & Forwarding Logic

1. **MAC Learning (Dynamic):**
* The switch inspects the **Source MAC Address** of every incoming frame.
* It associates that MAC address with the interface on which the frame arrived.
* Entries are dynamic (they age out and are removed after **5 minutes** of inactivity).


2. **Forwarding Logic:**
* **Known Unicast:** If the destination MAC is in the table, forward the frame only out the specific associated port.
* **Unknown Unicast:** If the destination MAC is **not** in the table, **FLOOD** the frame out of all ports *except* the ingress (receiving) port.
* **Broadcast/Multicast:** Frames sent to a destination MAC of all Fs (`FFFF.FFFF.FFFF`) are flooded out all ports (except the source port).



### Key Terms

* **Unicast:** Frame destined for a single specific host.
* **Flood:** Sending a frame out of all active ports (used when the destination location is unknown).
* **Unknown Unicast:** A unicast frame where the destination MAC is not yet in the switch table.

---

## 5. Quiz Review

* **Receiver Clock Sync:** Performed by the **Preamble**.
* **MAC Address Length:** **48 bits** (6 bytes).
* **OUI:** The **first half** (24 bits) of a MAC address.
* **MAC Learning:** Switches use the **Source MAC Address** field to populate the MAC address table.
* **Flooding:** Switches flood **Unknown Unicast** frames.
