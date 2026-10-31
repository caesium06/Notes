# CCNA Notes --- Ethernet LAN Switching, ARP & MAC Tables

## 1. Ethernet Frame

The Ethernet frame contains:

-   Preamble
-   SFD
-   Destination MAC
-   Source MAC
-   Type
-   Payload
-   FCS

The Preamble and SFD are sent with every Ethernet frame, but they are
usually not considered part of the Ethernet header.

The Ethernet header consists of:

-   Destination MAC
-   Source MAC
-   Type

The Ethernet header plus trailer is 18 bytes, excluding the Preamble and
SFD.

### Minimum Ethernet Frame Size

-   Minimum Ethernet frame size: **64 bytes**
-   Ethernet header + trailer: **18 bytes**
-   Minimum payload: **46 bytes**

``` text
64 - 18 = 46 bytes
```

If the payload is less than 46 bytes, padding bytes are added.

Example:

``` text
Payload = 34 bytes
Required payload = 46 bytes
Padding = 12 bytes
```

The padding bytes are zeros.

> The 64-byte minimum frame size does not include the Preamble and SFD.

------------------------------------------------------------------------

## 2. MAC Addresses

A MAC address is a **Layer 2 address**.

Example:

``` text
0C2F.B011.9D00
```

The first half is the **OUI (Organizationally Unique Identifier)**,
which identifies the manufacturer.

The second half is unique to the device.

Devices made by the same manufacturer can therefore share the same OUI
while having different complete MAC addresses.

------------------------------------------------------------------------

## 3. IP Addresses and MAC Addresses

Example network:

``` text
Network: 192.168.1.0/24

PC1: 192.168.1.1
PC2: 192.168.1.2
PC3: 192.168.1.3
PC4: 192.168.1.4
```

If PC1 wants to send data to PC3:

### IP Packet

``` text
Source IP      = 192.168.1.1
Destination IP = 192.168.1.3
```

### Ethernet Frame

``` text
Source MAC      = PC1 MAC
Destination MAC = PC3 MAC
```

PC1 knows PC3's IP address, but it initially does not know PC3's MAC
address.

PC1 uses **ARP** to discover it.

------------------------------------------------------------------------

## 4. ARP --- Address Resolution Protocol

**ARP (Address Resolution Protocol)** is used to discover the Layer 2
MAC address of a device when its Layer 3 IP address is already known.

``` text
Known IP address
       |
       v
      ARP
       |
       v
   MAC address
```

Example:

``` text
192.168.1.3 -> PC3's MAC address
```

ARP uses two messages:

  Message       Type        Purpose
  ------------- ----------- --------------------------
  ARP Request   Broadcast   Discover the MAC address
  ARP Reply     Unicast     Provide the MAC address

------------------------------------------------------------------------

## 5. ARP Request

The ARP request is sent as a **broadcast Ethernet frame**.

Broadcast MAC address:

``` text
FFFF.FFFF.FFFF
```

The request asks:

``` text
Who has 192.168.1.3?
Tell 192.168.1.1
```

Because PC1 does not know PC3's MAC address, it broadcasts the request
to the local network.

------------------------------------------------------------------------

## 6. ARP Reply

PC3 receives the ARP request and sees that the destination IP is its
own:

``` text
Destination IP = 192.168.1.3
```

PC3 sends an **ARP Reply** to PC1.

The ARP Reply is **unicast** because PC3 knows PC1's MAC address from
the ARP Request.

PC1 then stores the IP-to-MAC mapping in its ARP table.

------------------------------------------------------------------------

## 7. Complete ARP Process

Suppose PC1 wants to communicate with PC3.

Initially:

``` text
PC1 knows:
PC3 IP = 192.168.1.3

PC1 does not know:
PC3 MAC
```

### Step 1 --- ARP Request

PC1 broadcasts:

``` text
Destination MAC = FFFF.FFFF.FFFF
```

The request asks:

``` text
Who has 192.168.1.3?
```

### Step 2 --- Switch receives the frame

The switch:

1.  Learns PC1's source MAC address.
2.  Adds it to the MAC address table as a dynamic MAC address.
3.  Sees that the destination is broadcast.
4.  Floods the frame out all interfaces except the interface on which it
    was received.

### Step 3 --- Other PCs receive the request

PC2 checks the destination IP. It is not PC2's IP, so PC2 ignores the
request.

PC4 does the same.

PC3 sees that the destination IP is its own IP and responds.

### Step 4 --- ARP Reply

PC3 sends a unicast ARP Reply to PC1.

### Step 5 --- Switches learn PC3's MAC

The switches learn PC3's source MAC address and add it to their MAC
address tables.

### Step 6 --- PC1 updates its ARP table

PC1 now knows:

``` text
192.168.1.3 -> PC3 MAC
```

PC1 can now send the actual traffic to PC3.

------------------------------------------------------------------------

## 8. ARP Table

An ARP table stores:

``` text
IP address <-> MAC address
```

On Windows, macOS, and Linux:

``` bash
arp -a
```

Typical fields include:

  Field              Meaning
  ------------------ -------------------
  Internet Address   IP address
  Physical Address   MAC address
  Type               Static or Dynamic

### Static

A static/default entry that was not learned through an ARP request.

### Dynamic

An entry learned through an ARP Request and ARP Reply.

------------------------------------------------------------------------

## 9. Ping

**Ping** is a network utility used to test reachability between devices.

It measures **round-trip time**, for example:

``` text
PC1 -> PC3 -> PC1
```

Ping uses **ICMP**.

The two ICMP messages are:

1.  ICMP Echo Request
2.  ICMP Echo Reply

An ICMP Echo Request is sent to a specific host. It is not broadcast.

------------------------------------------------------------------------

## 10. ARP and Ping Together

Suppose PC1 runs:

``` text
ping 192.168.1.3
```

If PC1 does not already know PC3's MAC address:

``` text
PC1
 |
 | ARP Request
 | Broadcast
 v
PC3
 |
 | ARP Reply
 | Unicast
 v
PC1
 |
 | ICMP Echo Request
 | Unicast
 v
PC3
 |
 | ICMP Echo Reply
 | Unicast
 v
PC1
```

### Why can the first ping fail?

PC1 first has to use ARP to learn the destination MAC address.

The first ping can fail while the ARP process is taking place.

After PC1 learns PC3's MAC address, subsequent pings can succeed.

------------------------------------------------------------------------

## 11. Cisco IOS Ping

By default, a Cisco IOS ping sends:

-   5 ICMP Echo Requests
-   Each ping is 100 bytes

Cisco IOS ping output uses:

-   `!` for a successful ping
-   `.` for a failed ping

Example:

``` text
!!!!.
```

This means:

-   4 successful
-   1 failed
-   Success rate = 80%

Cisco IOS also displays the minimum, average, and maximum round-trip
times for successful pings.

------------------------------------------------------------------------

## 12. Cisco ARP Table

On Cisco IOS, use:

``` text
show arp
```

This displays the ARP table.

------------------------------------------------------------------------

## 13. Wireshark

Wireshark allows you to perform **packet captures** and analyze network
traffic.

You can inspect:

-   Source MAC
-   Destination MAC
-   Source IP
-   Destination IP
-   ARP packets
-   ICMP packets
-   Ethernet Type
-   Padding

For a ping where the destination MAC is not already known, a packet
capture can show:

``` text
ARP Request
ARP Reply
ICMP Echo Request
ICMP Echo Reply
```

------------------------------------------------------------------------

## 14. MAC Address Table

A Cisco switch maintains a **MAC address table**.

It maps:

``` text
MAC address -> Switch interface
```

Command:

``` text
show mac address-table
```

The MAC address table contains:

1.  VLAN
2.  MAC Address
3.  Type
4.  Ports

Example:

  VLAN   MAC Address   Type      Port
  ------ ------------- --------- ------
  1      PC1 MAC       Dynamic   G0/0
  1      PC3 MAC       Dynamic   G0/1

### Important distinction

ARP table:

``` text
IP -> MAC
```

Switch MAC address table:

``` text
MAC -> Port
```

> Do not confuse these two tables.

------------------------------------------------------------------------

## 15. Dynamic MAC Addresses

When a switch automatically learns a MAC address from incoming traffic,
it is a **dynamic MAC address**.

Dynamic MAC addresses are removed from the MAC address table after **5
minutes** if the switch does not receive traffic from that MAC address.

This is called **MAC address aging**.

------------------------------------------------------------------------

## 16. Clearing Dynamic MAC Addresses

### Clear all dynamic MAC addresses

``` text
clear mac address-table dynamic
```

### Clear a specific MAC address

``` text
clear mac address-table dynamic address <MAC-address>
```

### Clear entries learned on a specific interface

``` text
clear mac address-table dynamic interface <interface-id>
```

Example:

``` text
clear mac address-table dynamic interface gi0/0
```

------------------------------------------------------------------------

## 17. Switch Forwarding Behavior

A switch handles frames differently depending on whether it knows the
destination MAC address.

### Known Unicast

The destination MAC exists in the MAC address table.

The switch forwards the frame through the specific port associated with
that MAC address.

**It does not flood the frame.**

### Unknown Unicast

The destination MAC does not exist in the MAC address table.

The switch floods the frame out all interfaces except the interface on
which it was received.

### Broadcast

Destination MAC:

``` text
FFFF.FFFF.FFFF
```

The switch floods the frame out all interfaces except the interface on
which it was received.

### Remember

  Frame Type        Switch Action
  ----------------- --------------------------
  Known Unicast     Forward to specific port
  Unknown Unicast   Flood
  Broadcast         Flood

> **Broadcast and unknown unicast frames are flooded.**

------------------------------------------------------------------------

## 18. Ethernet Type / EtherType

Important EtherType values:

  Protocol   EtherType
  ---------- -----------
  IPv4       `0x0800`
  ARP        `0x0806`
  IPv6       `0x86DD`

The `0x` indicates hexadecimal.

------------------------------------------------------------------------

## 19. Ethernet Padding Example

Suppose a 36-byte ping is sent:

``` text
ping 192.168.1.3 size 36
```

The minimum Ethernet payload is 46 bytes.

Therefore:

``` text
46 - 36 = 10 bytes
```

So **10 bytes of padding** are added.

In Wireshark, these may appear as zeroes:

``` text
00 00 00 00 00 00 00 00 00 00
```

These are padding bytes added to meet the minimum Ethernet payload size.

------------------------------------------------------------------------

## 20. GNS3 vs Packet Tracer

### Packet Tracer

-   Network simulator
-   Free
-   Useful for CCNA practice
-   Can simulate many Cisco networking concepts

### GNS3

-   Runs actual Cisco IOS software virtually
-   More realistic in some ways
-   GNS3 itself is free
-   Requires your own Cisco IOS images

For CCNA, Packet Tracer is sufficient for most of the required practice.

------------------------------------------------------------------------

# Important Commands

### View ARP table

Windows/macOS/Linux:

``` bash
arp -a
```

Cisco IOS:

``` text
show arp
```

### View MAC address table

``` text
show mac address-table
```

### Clear all dynamic MAC addresses

``` text
clear mac address-table dynamic
```

### Clear a specific MAC address

``` text
clear mac address-table dynamic address <MAC-address>
```

### Clear MAC entries from an interface

``` text
clear mac address-table dynamic interface <interface-id>
```

### Test connectivity

``` text
ping <IP-address>
```

------------------------------------------------------------------------

# High-Yield CCNA Facts

  Concept                    Remember
  -------------------------- ------------------------------------------
  ARP                        Known IP -\> Find MAC
  ARP Request                Broadcast
  ARP Reply                  Unicast
  Ping                       ICMP Echo Request + Echo Reply
  ARP Table                  IP -\> MAC
  MAC Address Table          MAC -\> Port
  Minimum Ethernet Frame     64 bytes
  Minimum Ethernet Payload   46 bytes
  Padding                    Added when payload is less than 46 bytes
  Broadcast MAC              FFFF.FFFF.FFFF
  IPv4 EtherType             0x0800
  ARP EtherType              0x0806
  IPv6 EtherType             0x86DD
  Known Unicast              Forward to specific port
  Unknown Unicast            Flood
  Broadcast                  Flood
  Dynamic MAC Aging          5 minutes

------------------------------------------------------------------------

# The Complete Picture

The overall process is:

``` text
PC1 wants to communicate with PC3
        |
        v
PC1 knows PC3's IP address
        |
        v
PC1 does not know PC3's MAC address
        |
        v
ARP Request
(Broadcast)
        |
        v
Switch floods the frame
        |
        v
PC3 receives the ARP Request
        |
        v
ARP Reply
(Unicast)
        |
        v
PC1 learns PC3's MAC address
        |
        v
ICMP Echo Request
(Unicast)
        |
        v
PC3 receives the request
        |
        v
ICMP Echo Reply
(Unicast)
        |
        v
PC1 receives the reply
```

## Core Relationships

``` text
ARP
IP -> MAC

Switch MAC Address Table
MAC -> Port

Ping
ICMP Echo Request -> ICMP Echo Reply

ARP Request
Broadcast

ARP Reply
Unicast

Known Unicast
Specific port

Unknown Unicast
Flood

Broadcast
Flood
```
