import subprocess
import time
import webbrowser

print(" Starting Scholarship System...")

# -----------------------------
# Start Flask Backend
# -----------------------------
backend_process = subprocess.Popen(
    ["python", "-m","backend.app"],
    shell=True
)

print(" Backend started on port 5000")

# Wait for backend to load
time.sleep(3)

# -----------------------------
# Start Streamlit Frontend
# -----------------------------
frontend_process = subprocess.Popen(
    ["streamlit", "run", "frontend/app.py"],
    shell=True
)

print(" Streamlit frontend started")

# Wait and open browser automatically
time.sleep(5)
webbrowser.open("http://localhost:8501")

# Keep both running
backend_process.wait()
frontend_process.wait()
