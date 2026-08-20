import psutil
import platform
import subprocess
def get_disks() -> dict:
    disks = psutil.disk_partitions(all=True)

    response = []

    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        if len(disk.device) < 1:
            continue

        if not disk.device.startswith("/dev/"):
            continue

        mountpoint = disk.mountpoint
        total = f"{usage.total / 1024**3:.2f}"
        used = f"{usage.used / 1024**3:.2f}"
        free = f"{usage.free / 1024**3:.2f}"
        percent = f"{usage.percent:.1f}%"
        disk_dictionary = {}
        disk_dictionary[mountpoint] = {
            "total": total,
            "used": used,
            "free": free,
            "percent": percent
        }
        response.append(disk_dictionary)
    return response

def get_system_usage() -> dict:

    # CPU (Central Processing Unit)
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_cores = psutil.cpu_count(False)
    cpu_max_freq = psutil.cpu_freq(False).max
    cpu_name = platform.processor()


    if len(cpu_name) < 1:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    cpu_name = line.split(":", 1)[1].strip()
                    break
    with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq") as f:
        cpu_max_freq = int(f.read()) / 1000


    if len(cpu_name) < 1:
        cpu_name = "Unknown CPU."

    # RAM (Random Access Memory)
    mbconvert = (1024 ** 2)

    ram = psutil.virtual_memory()

    # GiB
    available_ram_gb = round(ram.available / 1024**3, 2)
    used_ram_gb = round(ram.used / 1024**3, 2)
    total_ram_gb = round(ram.total / 1024**3, 2)

    # MiB
    available_ram = round(ram.available / mbconvert)
    used_ram = round(ram.used / mbconvert)
    total_ram = round(ram.total / mbconvert)

    response = {
        "cpu": {
            "name": cpu_name,
            "usagepercent": cpu_percent,
            "cores": cpu_cores,
            "maxfrequency": cpu_max_freq
        },
        "ram": {
            "gigabytes": {
                "available": available_ram_gb,
                "used": used_ram_gb,
                "total": total_ram_gb
            },
            "megabytes": {
                "available": available_ram,
                "used": used_ram,
                "total": total_ram
            },
        },
        "disk": get_disks()
    }
    return response

def get_ips():
    final = ""
    try:
        public = subprocess.check_output(
            ["curl", "https://api4.ipify.org"],timeout=3, text=True
        )
        local = subprocess.check_output(
            ["ip", "route", "get", "1.1.1.1"], text=True
        )
        local = local.split()[6]
        return f"🏠 {local}  •  🌐 {public}"
    except Exception:
        return local.split()[6]

