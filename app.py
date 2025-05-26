from flask import Flask, jsonify, send_from_directory
import psutil
import cpuinfo
import GPUtil
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv('7606461880:AAGtzFYAcUjppyIsKKaEyqOGRBj1mWFbXeQ')
TELEGRAM_CHAT_ID = os.getenv('2071334805')

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    return {
        "brand": info.get('brand_raw', 'Unknown'),
        "arch": info.get('arch', 'Unknown'),
        "bits": info.get('bits', 'Unknown'),
        "hz_advertised": info.get('hz_advertised_friendly', 'Unknown'),
        "hz_actual": info.get('hz_actual_friendly', 'Unknown')
    }

def get_ram_info():
    ram = psutil.virtual_memory()
    return {
        "total_gb": round(ram.total / (1024**3), 2),
        "available_gb": round(ram.available / (1024**3), 2)
    }

def get_disk_info():
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2)
            })
        except PermissionError:
            continue
    return disks

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_list = []
    for gpu in gpus:
        gpu_list.append({
            "id": gpu.id,
            "name": gpu.name,
            "load_percent": round(gpu.load * 100, 1),
            "memory_free_mb": gpu.memoryFree,
            "memory_used_mb": gpu.memoryUsed,
            "temperature_c": gpu.temperature
        })
    return gpu_list

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram bot token or chat ID not set.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"Failed to send message: {response.text}")
    except Exception as e:
        print(f"Error sending telegram message: {e}")

def format_hardware_info(data):
    lines = []
    lines.append("*CPU Info:*")
    cpu = data['cpu']
    lines.append(f"- Brand: {cpu['brand']}")
    lines.append(f"- Arch: {cpu['arch']}")
    lines.append(f"- Bits: {cpu['bits']}")
    lines.append(f"- Advertised Hz: {cpu['hz_advertised']}")
    lines.append(f"- Actual Hz: {cpu['hz_actual']}")
    lines.append("\n*RAM Info:*")
    ram = data['ram']
    lines.append(f"- Total: {ram['total_gb']} GB")
    lines.append(f"- Available: {ram['available_gb']} GB")
    lines.append("\n*Disk Info:*")
    for d in data['disk']:
        lines.append(f"- Device: {d['device']} ({d['fstype']})")
        lines.append(f"  Mountpoint: {d['mountpoint']}")
        lines.append(f"  Total: {d['total_gb']} GB, Used: {d['used_gb']} GB, Free: {d['free_gb']} GB")
    lines.append("\n*GPU Info:*")
    if data['gpu']:
        for g in data['gpu']:
            lines.append(f"- {g['name']} (ID: {g['id']})")
            lines.append(f"  Load: {g['load_percent']}%")
            lines.append(f"  Memory Free: {g['memory_free_mb']} MB, Used: {g['memory_used_mb']} MB")
            lines.append(f"  Temperature: {g['temperature_c']} °C")
    else:
        lines.append("No GPU detected.")
    return "\n".join(lines)

@app.route('/')
def index():
    # نرسل ملف html من نفس المجلد بدل templates
    return send_from_directory('.', 'index.html')

@app.route('/hardware')
def hardware():
    data = {
        "cpu": get_cpu_info(),
        "ram": get_ram_info(),
        "disk": get_disk_info(),
        "gpu": get_gpu_info()
    }
    message = format_hardware_info(data)
    send_telegram_message(message)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
