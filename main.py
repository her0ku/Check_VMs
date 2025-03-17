import platform
import subprocess
import psutil

def check_vm_via_processes():
    vm_process_map = {
        'vboxservice': 'VirtualBox',
        'vboxtray': 'VirtualBox',
        'vmware-tray': 'VMware',
        'vmware-user': 'VMware',
        'vmware-vmx': 'VMware',
        'xenservice': 'Xen',
        'qemu-ga': 'QEMU',
        'vmtoolsd': 'VMware'
    }
    
    detected = []
    for proc in psutil.process_iter(['name']):
        name = proc.info['name'].lower()
        if name in vm_process_map:
            detected.append(vm_process_map[name])
    return list(set(detected))

def check_vm_via_drivers():
    driver_vendor_map = {
        'vboxguest': 'VirtualBox',
        'vm3dmp': 'VMware',
        'vmci': 'VMware',
        'vmmemctl': 'VMware',
        'vmusbmouse': 'VMware',
        'vmx_svga': 'VMware',
        'xen': 'Xen',
        'qemupciserial': 'QEMU'
    }
    
    if platform.system() == 'Windows':
        try:
            output = subprocess.check_output('driverquery', shell=True, text=True).lower()
            detected = []
            for driver, vendor in driver_vendor_map.items():
                if driver in output:
                    detected.append(vendor)
            return list(set(detected))
        except Exception:
            return []
    return []

def check_vm_via_mac():
    vm_mac_map = {
        '00:0C:29': 'VMware',
        '00:1C:14': 'VMware',
        '00:50:56': 'VMware',
        '08:00:27': 'VirtualBox',
        '0A:00:27': 'VirtualBox',
        '00:16:3E': 'Xen',
        '00:1A:4A': 'KVM'
    }
    
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac = addr.address.replace('-', ':').upper()
                for prefix, vendor in vm_mac_map.items():
                    if mac.startswith(prefix):
                        return [vendor]
    return []

def check_vm_via_system_info():
    vm_keyword_map = {
        'vmware': 'VMware',
        'virtualbox': 'VirtualBox',
        'qemu': 'QEMU',
        'kvm': 'KVM',
        'xen': 'Xen',
        'hyper-v': 'Hyper-V',
        'innotek': 'VirtualBox',
        'virtual machine': 'Generic VM'
    }
    
    system_info = []
    try:
        if platform.system() == 'Linux':
            with open('/sys/class/dmi/id/product_name', 'r') as f:
                system_info.append(f.read().lower())
            with open('/proc/cpuinfo', 'r') as f:
                system_info.append(f.read().lower())
        elif platform.system() == 'Windows':
            import wmi
            c = wmi.WMI()
            system_info.append(c.Win32_ComputerSystem()[0].Manufacturer.lower())
            system_info.append(c.Win32_BaseBoard()[0].Manufacturer.lower())
    except Exception:
        pass

    detected = []
    for info in system_info:
        for keyword, vendor in vm_keyword_map.items():
            if keyword in info:
                detected.append(vendor)
    return list(set(detected))

def check_vm_via_memory():
    mem = psutil.virtual_memory().total
    return ["Possible Sandbox"] if mem < 2 * 1024**3 else []

def check_vm_via_cpu_cores():
    return ["Possible Sandbox"] if psutil.cpu_count(logical=False) < 2 else []

def analyze_vm_environment():
    detection_methods = {
        "Running processes": check_vm_via_processes(),
        "MAC address": check_vm_via_mac(),
        "System info": check_vm_via_system_info(),
        "VM Drivers": check_vm_via_drivers(),
        "Low memory": check_vm_via_memory(),
        "Few CPU cores": check_vm_via_cpu_cores()
    }

    all_indicators = []
    for method, results in detection_methods.items():
        if results:
            all_indicators.extend(results)

    vm_types = list(set(all_indicators))
    return detection_methods, vm_types

if __name__ == "__main__":
    methods, vm_types = analyze_vm_environment()
    
    print("\nVM Detection Report:")
    print("=" * 40)
    for method, result in methods.items():
        print(f"{method + ':':<18} {', '.join(result) if result else 'No indicators found'}")

    print("\n" + "=" * 40)
    if vm_types:
        print(f"Final Detection: {', '.join(vm_types)}")
    else:
        print("No VM/Sandbox indicators detected")

