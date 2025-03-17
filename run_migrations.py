"""
Script to create and apply database migrations automatically
"""
import os
import subprocess

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    return result.returncode == 0

if __name__ == "__main__":
    # Make migrations for the main_app models
    if run_command("python manage.py makemigrations main_app"):
        print("Migrations created successfully!")
    else:
        print("Failed to create migrations.")
        exit(1)
        
    # Apply migrations to create database tables
    if run_command("python manage.py migrate"):
        print("Migrations applied successfully!")
    else:
        print("Failed to apply migrations.")
        exit(1)
        
    # Collect static files
    if run_command("python manage.py collectstatic --noinput"):
        print("Static files collected successfully!")
    else:
        print("Failed to collect static files.")
        # Don't exit on error here, just continue
    
    print("Database setup complete. You can now run the application.")
