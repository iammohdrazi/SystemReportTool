from flask import Flask, render_template_string, send_file, make_response
import platform, psutil, socket, webbrowser, os
from time import ctime
from threading import Timer
from datetime import datetime
import logging

app = Flask(__name__)
LOG_FILE = "system_report.log"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s %(message)s')

def format_bytes(bytes_value):
    return f"{bytes_value / (1024 ** 3):.2f} GB"

def collect_system_data():
    sys_info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Boot Time": ctime(psutil.boot_time())
    }

    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "Per-Core Usage": psutil.cpu_percent(percpu=True, interval=1),
        "Total CPU Usage": psutil.cpu_percent()
    }

    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    mem_info = {
        "Virtual": {
            "Total": format_bytes(vm.total),
            "Available": format_bytes(vm.available),
            "Used": format_bytes(vm.used),
            "Free": format_bytes(vm.free),
            "Usage %": vm.percent
        },
        "Swap": {
            "Total": format_bytes(swap.total),
            "Used": format_bytes(swap.used),
            "Free": format_bytes(swap.free),
            "Usage %": swap.percent
        }
    }

    disks = []
    for p in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disks.append({
                "Device": p.device,
                "Mount": p.mountpoint,
                "FS": p.fstype,
                "Total": format_bytes(usage.total),
                "Used": format_bytes(usage.used),
                "Free": format_bytes(usage.free),
                "Usage": f"{usage.percent}%"
            })
        except:
            continue

    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "Unavailable"
    net_io = psutil.net_io_counters()
    net_info = {
        "Hostname": socket.gethostname(),
        "IP Address": ip,
        "Bytes Sent": f"{net_io.bytes_sent / (1024 ** 2):.2f} MB",
        "Bytes Received": f"{net_io.bytes_recv / (1024 ** 2):.2f} MB"
    }

    batt = psutil.sensors_battery()
    if batt:
        battery = {
            "Percent": f"{batt.percent}%",
            "Plugged In": batt.power_plugged,
            "Time Left (min)": batt.secsleft // 60 if batt.secsleft > 0 else "N/A"
        }
    else:
        battery = {"Status": "Battery not available"}

    return sys_info, cpu_info, mem_info, disks, net_info, battery

@app.route("/")
def system_report():
    sys_info, cpu_info, mem_info, disks, net_info, battery = collect_system_data()
    return render_template_string(TEMPLATE,
        sys_info=sys_info, cpu_info=cpu_info,
        mem_info=mem_info, disks=disks,
        net_info=net_info, battery=battery)

@app.route("/download_report")
def download_report():
    sys_info, cpu_info, mem_info, disks, net_info, battery = collect_system_data()

    content = ["System Report", "="*40, f"Generated: {datetime.now()}", ""]
    content += ["\n[System Info]"] + [f"{k}: {v}" for k, v in sys_info.items()]
    content += ["\n[CPU Info]"] + [f"{k}: {v}" for k, v in cpu_info.items() if not isinstance(v, list)]
    content += [f"Core {i}: {v}%" for i, v in enumerate(cpu_info["Per-Core Usage"])]
    content += ["\n[Memory Info]"]
    for k, v in mem_info.items():
        content.append(f"{k} Memory:")
        content += [f"  {ik}: {iv}" for ik, iv in v.items()]
    content += ["\n[Disk Info]"]
    for disk in disks:
        content += [f"  {k}: {v}" for k, v in disk.items()]
        content.append("")
    content += ["\n[Network Info]"] + [f"{k}: {v}" for k, v in net_info.items()]
    content += ["\n[Battery Info]"] + [f"{k}: {v}" for k, v in battery.items()]

    file_name = "system_report.txt"
    with open(file_name, "w") as f:
        f.write("\n".join(content))

    logging.info("System report generated and downloaded.")
    return send_file(file_name, as_attachment=True)

@app.route("/download_logs")
def download_logs():
    logging.info("Log file downloaded.")
    return send_file(LOG_FILE, as_attachment=True)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>System Report Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .card { transition: all 0.3s ease; }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            border-color: #3B82F6;
        }
        .section-icon {
            font-size: 1.2rem;
            margin-right: 0.5rem;
            color: #3B82F6;
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-900">
    <div class="max-w-7xl mx-auto px-4 py-6">
        <h1 class="text-4xl font-extrabold text-center text-blue-800 mb-10 tracking-tight">
            💻 System Report Dashboard
        </h1>

        <div class="flex justify-center gap-4 mb-10">
            <a href="/download_report" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded shadow">
                📄 Download Report
            </a>
            <a href="/download_logs" class="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded shadow">
                📁 Download Logs
            </a>
        </div>

        {% macro section(title, icon, data) %}
        <div class="card bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:border-blue-500">
            <h2 class="text-lg font-semibold mb-4 text-gray-700 flex items-center">
                <span class="section-icon">{{ icon }}</span>{{ title }}
            </h2>
            <ul class="space-y-2 text-sm">
                {% for key, value in data.items() %}
                <li class="border-b pb-2">
                    <div class="font-medium text-gray-700">{{ key }}</div>
                    <div class="text-gray-800 break-words">{{ value }}</div>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endmacro %}

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {{ section("System Info", "🖥️", sys_info) }}
            {{ section("Network Info", "🌐", net_info) }}
            {{ section("Battery Info", "🔋", battery) }}
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="card bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:border-blue-500">
                <h2 class="text-lg font-semibold mb-4 text-gray-700 flex items-center">
                    <span class="section-icon">🧠</span>CPU Info
                </h2>
                <ul class="space-y-1 text-sm text-gray-800">
                    <li><strong>Physical Cores:</strong> {{ cpu_info['Physical Cores'] }}</li>
                    <li><strong>Logical CPUs:</strong> {{ cpu_info['Logical CPUs'] }}</li>
                    {% for core in cpu_info['Per-Core Usage'] %}
                    <li><strong>Core {{ loop.index0 }}:</strong> {{ core }}%</li>
                    {% endfor %}
                    <li><strong>Total CPU Usage:</strong> {{ cpu_info['Total CPU Usage'] }}%</li>
                </ul>
            </div>

            <div class="card bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:border-blue-500">
                <h2 class="text-lg font-semibold mb-4 text-gray-700 flex items-center">
                    <span class="section-icon">💾</span>Memory Info
                </h2>
                {% for title, values in mem_info.items() %}
                    <h3 class="text-md font-bold text-blue-600 mt-4 mb-2">{{ title }} Memory</h3>
                    <ul class="space-y-1 text-sm text-gray-800">
                    {% for k, v in values.items() %}
                        <li><strong>{{ k }}:</strong> {{ v }}</li>
                    {% endfor %}
                    </ul>
                {% endfor %}
            </div>
        </div>

        <div class="card bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:border-blue-500">
            <h2 class="text-lg font-semibold mb-4 text-gray-700 flex items-center">
                <span class="section-icon">📦</span>Disk Info
            </h2>
            <div class="grid sm:grid-cols-2 gap-6">
                {% for disk in disks %}
                <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 text-sm text-gray-800">
                    <p><strong>Device:</strong> {{ disk.Device }}</p>
                    <p><strong>Mount:</strong> {{ disk.Mount }}</p>
                    <p><strong>FS:</strong> {{ disk.FS }}</p>
                    <p><strong>Total:</strong> {{ disk.Total }}</p>
                    <p><strong>Used:</strong> {{ disk.Used }}</p>
                    <p><strong>Free:</strong> {{ disk.Free }}</p>
                    <p><strong>Usage:</strong> {{ disk.Usage }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
    app.run(debug=True)
