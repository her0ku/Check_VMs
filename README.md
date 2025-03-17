## VM and Sandbox Detection Tool
A Python script to detect virtual machine (VM) and sandbox environments using multiple detection methods.

## Features
Process-based detection: Checks for known VM-related processes (VirtualBox, VMware, Xen, QEMU)
Driver-based detection: Identifies virtualization drivers (Windows only)
MAC address analysis: Detects VM-specific MAC address prefixes

System information checks:
DMI data analysis (Linux)
WMI queries for hardware information (Windows)

Resource analysis:
Low memory detection (<2GB)
Low physical CPU core count (<2 cores)

![Result](https://github.com/user-attachments/assets/cca74f83-dfee-4505-ac65-6a2a52ac6ba1)
