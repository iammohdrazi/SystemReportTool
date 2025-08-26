import os
import platform
import psutil
import socket
from datetime import datetime
from time import ctime

def get_system_info():
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Boot Time": ctime(psutil.boot_time())
    }

def get_cpu_info():
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "Per-Core Usage": psutil.cpu_percent(percpu=True, interval=1),
        "Total CPU Usage": psutil.cpu_percent()
    }
    return cpu_info

def get_memory_info():
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "Virtual Memory": {
            "Total": vm.total,
            "Available": vm.available,
            "Used": vm.used,
            "Free": vm.free,
            "Usage %": vm.percent
        },
        "Swap Memory": {
            "Total": swap.total,
            "Used": swap.used,
            "Free": swap.free,
            "Usage %": swap.percent
        }
    }

def get_disk_info():
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        disks.append({
            "Device": partition.device,
            "Mountpoint": partition.mountpoint,
            "File System": partition.fstype,
            "Total": usage.total,
            "Used": usage.used,
            "Free": usage.free,
            "Usage %": usage.percent
        })
    return disks

def get_network_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.error:
        ip_address = "Unavailable"
    net_io = psutil.net_io_counters()
    return {
        "Hostname": hostname,
        "IP Address": ip_address,
        "Bytes Sent": net_io.bytes_sent,
        "Bytes Received": net_io.bytes_recv
    }

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return {
            "Percent": battery.percent,
            "Plugged In": battery.power_plugged,
            "Time Left (min)": battery.secsleft // 60 if battery.secsleft > 0 else "N/A"
        }
    return {"Battery": "Not available"}

def format_bytes(bytes_value):
    return f"{bytes_value / (1024 ** 3):.2f} GB"

def write_report():
    report_dir = os.path.join(os.path.dirname(__file__), "report")
    os.makedirs(report_dir, exist_ok=True)

    filename = os.path.join(
        report_dir,
        f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(filename, "w") as f:
        f.write("===== SYSTEM REPORT =====\n\n")

        f.write("[System Info]\n")
        for key, val in get_system_info().items():
            f.write(f"{key}: {val}\n")
        f.write("\n")

        f.write("[CPU Info]\n")
        cpu = get_cpu_info()
        f.write(f"Physical Cores: {cpu['Physical Cores']}\n")
        f.write(f"Logical CPUs: {cpu['Logical CPUs']}\n")
        for i, usage in enumerate(cpu["Per-Core Usage"]):
            f.write(f"Core {i}: {usage}%\n")
        f.write(f"Total CPU Usage: {cpu['Total CPU Usage']}%\n\n")

        f.write("[Memory Info]\n")
        mem = get_memory_info()
        for section, values in mem.items():
            f.write(f"{section}:\n")
            for key, val in values.items():
                if "Usage" in key:
                    f.write(f"  {key}: {val}%\n")
                else:
                    f.write(f"  {key}: {format_bytes(val)}\n")
        f.write("\n")

        f.write("[Disk Info]\n")
        for disk in get_disk_info():
            f.write(f"Device: {disk['Device']} | Mount: {disk['Mountpoint']} | FS: {disk['File System']}\n")
            f.write(f"  Total: {format_bytes(disk['Total'])} | Used: {format_bytes(disk['Used'])} | Free: {format_bytes(disk['Free'])} | Usage: {disk['Usage %']}%\n")
        f.write("\n")

        f.write("[Network Info]\n")
        net = get_network_info()
        f.write(f"Hostname: {net['Hostname']}\n")
        f.write(f"IP Address: {net['IP Address']}\n")
        f.write(f"Bytes Sent: {net['Bytes Sent'] / (1024 ** 2):.2f} MB\n")
        f.write(f"Bytes Received: {net['Bytes Received'] / (1024 ** 2):.2f} MB\n\n")

        f.write("[Battery Info]\n")
        battery = get_battery_info()
        for key, val in battery.items():
            f.write(f"{key}: {val}\n")

    return filename

if __name__ == "__main__":
    report_path = write_report()
    print(f"\nSystem report generated:\n{report_path}")
