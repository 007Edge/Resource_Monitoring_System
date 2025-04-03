# Resource_Monitoring_System
Advanced Real-Time Process Monitoring Dashboard
Overview
The Advanced Real-Time Process Monitoring Dashboard is a professional-grade application built with Python (Flask) for the backend and a dynamic HTML + JavaScript (Chart.js + Socket.IO) frontend. It provides real-time monitoring and management of system processes, displaying CPU, memory, disk, and network usage with interactive charts. The dashboard also allows process management with functionalities to terminate processes and start new ones.

Features
Real-Time Performance Monitoring:

CPU Usage: Graph displays live CPU utilization percentage.

Memory Usage: Monitors current memory consumption.

Disk Usage: Displays disk read/write activity.

Network Usage: Tracks incoming and outgoing network traffic.

Process Management:

View Processes: Lists all running processes with details:

Process ID (PID)

Name

CPU and Memory usage

Threads

Disk Read/Write activity

Kill Process: Terminate any running process by PID.

Start New Process: Launch new processes dynamically.

Interactive Charts:

Real-time updating charts using Chart.js.

Smooth and responsive line graphs with color-coded usage metrics.

Dynamic data refresh every second.

Search & Sort Functionality:

Search bar to filter processes by name or ID.

Sortable table columns for better process management.

Enhanced user experience with a responsive and interactive UI.

Tech Stack
Backend:

Python (Flask) for the server.

psutil for system performance metrics.

Socket.IO for real-time communication.

Frontend:

HTML, CSS, and JavaScript.

Chart.js for interactive real-time charts.

Socket.IO to receive real-time updates.



The server will start at http://127.0.0.1:5000.

Usage
Access the Dashboard:

Open your browser and go to:

http://127.0.0.1:5000
You will see two tabs:

Performance: Displays real-time charts for CPU, Memory, Disk, and Network usage.

Processes: Lists all running processes with controls to terminate or start processes.

Process Actions:

Kill Process: Click the "Kill" button next to any process to terminate it.

Start New Process: Use the "Start New Process" button to launch a new application by providing its name (e.g., notepad.exe on Windows).

Data Flow Architecture
pgsql
Copy
Edit
+---------------------------+
|    Python (Flask Server)   |
|   - Collects System Stats  |
|   - Manages Processes      |
+---------------------------+
            |
            | Socket.IO
            ▼
+---------------------------+
|    Frontend (HTML, JS)     |
|   - Real-time Charts       |
|   - Display Processes      |
|   - User Actions (Kill/Run)|
+---------------------------+
File Structure

/process-monitor-system
 ├── /templates
 │     └── index.html          # Frontend (UI) - Real-time Dashboard
 ├── app.py                   # Flask Server (Backend)
 ├── requirements.txt         # Project Dependencies
 ├── README.txt               # Project Documentation


Contributing
Feel free to contribute by creating pull requests.
For major changes, open an issue first to discuss what you want to add.
