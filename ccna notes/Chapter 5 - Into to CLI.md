Here are structured, comprehensive study notes based on the transcript provided from **Jeremy’s IT Lab (CCNA 200-301 - Day 4: Cisco IOS CLI)**.

---

# CCNA Study Notes: Introduction to Cisco IOS CLI

## 1. Connecting to Cisco Devices

### Access Methods & Interfaces

* **Cisco IOS:** Operating system running on Cisco network devices (routers, switches, firewalls). Unrelated to Apple's iOS.
* **CLI (Command-Line Interface):** Primary text-based interface used by network engineers to configure and manage network devices.
* **Console Port Connections:**
* **RJ-45 Console Port:** Requires a **Rollover Cable** (RJ-45 to DB9) plus a Serial-to-USB adapter for modern laptops.
* **USB Mini-B Console Port:** Connects directly via a USB cable.



### Rollover Cable Pinout

A rollover cable completely reverses the pinout from one end to the other:

* Pin 1 $\leftrightarrow$ Pin 8
* Pin 2 $\leftrightarrow$ Pin 7
* Pin 3 $\leftrightarrow$ Pin 6
* Pin 4 $\leftrightarrow$ Pin 5
* (And vice versa for Pins 5–8)

### Serial Connection Terminal Settings (Cisco Defaults)

When connecting via terminal emulation software (e.g., PuTTY), use the following default settings:

| Parameter | Default Value |
| --- | --- |
| **Baud Rate / Speed** | **9,600 bps** |
| **Data Bits** | **8** |
| **Parity** | **None** |
| **Stop Bits** | **1** |
| **Flow Control** | **None** |

---

## 2. Cisco IOS Execution Modes & Navigation

### Primary CLI Modes

1. **User EXEC Mode:**
* **Prompt:** `Router>`
* **Purpose:** Basic view-only access; highly restricted (cannot view sensitive configurations or make changes).


2. **Privileged EXEC Mode (Enable Mode):**
* **Prompt:** `Router#`
* **Purpose:** Full viewing rights (configurations, diagnostic commands), ability to restart devices, set clock, and save files.
* **Command to Enter:** `enable` (shortcut: `en`)
* **Command to Exit:** `disable` or `exit`


3. **Global Configuration Mode:**
* **Prompt:** `Router(config)#`
* **Purpose:** Primary mode used to make configuration changes that affect the device globally.
* **Command to Enter:** `configure terminal` (shortcut: `conf t`)
* **Command to Exit:** `exit` or `end` (or `Ctrl+C`)



### CLI Navigation Shortcuts & Syntax Rules

* **Question Mark (`?`):**
* `e?` (no space): Lists all available commands starting with the letter "e".
* `enable ?` (with space): Lists all valid parameters/arguments that can follow the command.


* **Tab Key:** Completes a partially typed command if unique.
* **Command Shortening:** Commands can be shortened to the fewest characters needed to uniquely identify them (e.g., `conf t` for `configure terminal`, `sh run` for `show running-config`).
* **The `do` Keyword:** Allows execution of Privileged EXEC commands from within configuration modes (e.g., `do show running-config` executed inside `Router(config)#`).
* **Negating Commands (`no`):** Prepended to a command to remove or disable a setting (e.g., `no service password-encryption`).

---

## 3. Configuration Files & Saving Changes

### Configuration File Types

* **Running-Config (`running-config`):**
* Stored in **RAM** (volatile memory).
* Represents the active, real-time configuration. Lost if the device reboots without saving.
* Viewed with: `show running-config` (or `sh run`)


* **Startup-Config (`startup-config`):**
* Stored in **NVRAM** (Non-Volatile RAM).
* Loaded into RAM as the `running-config` when the device boots up.
* Viewed with: `show startup-config`



### Methods to Save Configurations (Privileged EXEC)

All three commands copy the active running configuration to NVRAM:

1. `copy running-config startup-config` *(Official standard command)*
2. `write`
3. `write memory`

---

## 4. Securing Privileged EXEC Mode

### Password Configuration & Security Comparison

| Feature | `enable password <password>` | `enable secret <password>` |
| --- | --- | --- |
| **Storage Security** | Stored in **plain text** by default | Stored as a **strong hash (MD5, Type 5)** |
| **Precedence** | Lower | **Higher** (Overrides `enable password` if both are set) |
| **Affected by `service password-encryption`?** | Yes (Encrypted to weak Type 7) | No (Always securely hashed) |
| **Case Sensitivity** | Case-sensitive | Case-sensitive |

> **Note:** If both `enable secret` and `enable password` are configured on a device, IOS will ignore `enable password` and require the `enable secret`.

### Password Encryption Commands

#### Service Password-Encryption

* **Command:** `service password-encryption` (Global Config)
* **Function:** Encrypts all plain-text passwords stored in the configuration (e.g., `enable password`, line passwords) using Cisco Type 7 encryption.
* **Weakness:** Type 7 encryption is weak and easily reversed using online decrypters.
* **Disabling Behavior (`no service password-encryption`):**
* Existing encrypted Type 7 passwords **remain encrypted**.
* Future passwords entered will be saved in clear text.



---

## 5. Summary of Key CLI Commands

| Command | Mode | Description |
| --- | --- | --- |
| `enable` | User EXEC | Enters Privileged EXEC mode |
| `disable` | Privileged EXEC | Exits Privileged EXEC back to User EXEC mode |
| `configure terminal` | Privileged EXEC | Enters Global Configuration mode |
| `exit` | Any Configuration Mode | Steps back one mode level (or logs out from User EXEC) |
| `enable password <pass>` | Global Config | Sets an unencrypted (clear text) password for enable access |
| `enable secret <pass>` | Global Config | Sets an MD5-hashed secret password for enable access |
| `service password-encryption` | Global Config | Encrypts all clear-text passwords in `running-config` (Type 7) |
| `no <command>` | Global Config | Negates or removes a command setting |
| `do <command>` | Global Config | Executes Privileged EXEC level commands from Config modes |
| `show running-config` | Privileged EXEC | Displays current active configuration stored in RAM |
| `show startup-config` | Privileged EXEC | Displays boot configuration stored in NVRAM |
| `copy running-config startup-config` | Privileged EXEC | Saves active configuration to NVRAM |
