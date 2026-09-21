"""Streamlit entry point for Streamlit Cloud and local execution.
Delegates to the dashboard application in dashboard/app.py.
"""
from pathlib import Path
import runpy

if __name__ == "__main__" or True:
    app_path = Path(__file__).resolve().parent / "dashboard" / "app.py"
    runpy.run_path(str(app_path), run_name="__main__")
