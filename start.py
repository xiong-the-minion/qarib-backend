#!/usr/bin/env python
"""
Qarib Backend Startup Script

This script handles the complete startup process for the Qarib backend:
1. Installs dependencies
2. Runs database migrations
3. Imports transcript files (via migration)
4. Starts the Django development server

Usage:
    python start.py
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors gracefully"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"⚠️  Warning: {result.stderr}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_virtual_environment():
    """Check if we're in a virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return True
    else:
        print("⚠️  Warning: No virtual environment detected")
        print("Consider creating one with: python -m venv venv")
        return True  # Don't fail, just warn


def install_dependencies():
    """Install Python dependencies"""
    if not os.path.exists("requirements.txt"):
        print("⚠️  Warning: requirements.txt not found, skipping dependency installation")
        return True
    
    return run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    )


def run_migrations():
    """Run Django database migrations"""
    return run_command(
        "python manage.py migrate",
        "Running database migrations"
    )


def start_server():
    """Start the Django development server"""
    print(f"\n🚀 Starting Django development server...")
    print(f"📍 Server will be available at: http://127.0.0.1:8000")
    print(f"📍 Admin interface: http://127.0.0.1:8000/admin/")
    print(f"📍 API endpoints: http://127.0.0.1:8000/api/")
    print("\n" + "="*50)
    print("Press Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    try:
        # Start the server in the foreground
        subprocess.run([
            sys.executable, "manage.py", "runserver", "127.0.0.1:8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    return True


def main():
    """Main startup function - does everything automatically"""
    print("🎯 Qarib Backend Startup Script")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check virtual environment
    check_virtual_environment()
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    print(f"📁 Working directory: {project_dir}")
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        sys.exit(1)
    
    # Start the server
    if not start_server():
        sys.exit(1)


if __name__ == "__main__":
    main()
