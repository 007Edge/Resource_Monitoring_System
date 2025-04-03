from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import psutil
import time
import os
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Store historical data (simple in-memory for now)
history = {'cpu': [], 'memory': [], 'disk': [], 'network': []}

# Gather detailed system and process data
def get_system_data():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads', 'io_counters']):
        try:
            io = proc.io_counters() if hasattr(proc, 'io_counters') else None
            processes.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_percent'],
                'threads': proc.info['num_threads'],
                'disk_read': io.read_bytes / 1024 / 1024 if io else 0,  # MB
                'disk_write': io.write_bytes / 1024 / 1024 if io else 0  # MB
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    net = psutil.net_io_counters()
    disk = psutil.disk_io_counters()

    data = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'net_sent': net.bytes_sent / 1024 / 1024,  # MB
        'net_recv': net.bytes_recv / 1024 / 1024,  # MB
        'disk_read': disk.read_bytes / 1024 / 1024 if disk else 0,  # MB
        'disk_write': disk.write_bytes / 1024 / 1024 if disk else 0,  # MB
        'uptime': time.time() - psutil.boot_time(),
        'processes': sorted(processes, key=lambda x: x['cpu'], reverse=True)[:15]  # Top 15 by CPU
    }

    # Store historical data (limit to 60 entries ~ 1 minute)
    for key in ['cpu', 'memory', 'disk', 'network']:
        history[key].append(data[f'{key}_usage'] if key != 'network' else data['net_sent'] + data['net_recv'])
        if len(history[key]) > 60:
            history[key].pop(0)

    return data

# Route for the dashboard
@app.route('/')
def index():
    return render_template('index.html')

# API to kill a process
@app.route('/kill/<int:pid>', methods=['POST'])
def kill_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return jsonify({'status': 'success', 'message': f'Process {pid} terminated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# API to start a process (example: notepad on Windows)
@app.route('/start', methods=['POST'])
def start_process():
    try:
        process_name = request.json.get('name', 'notepad.exe')  # Default to notepad
        os.startfile(process_name) if os.name == 'nt' else os.system(f'{process_name} &')
        return jsonify({'status': 'success', 'message': f'Started {process_name}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Background task for real-time updates
def background_task():
    while True:
        data = get_system_data()
        socketio.emit('update', data)
        # Check for alerts
        if data['cpu_usage'] > 80 or data['memory_usage'] > 80:
            socketio.emit('alert', {'message': f"High usage detected! CPU: {data['cpu_usage']}%, Memory: {data['memory_usage']}%"})
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    socketio.start_background_task(background_task)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)