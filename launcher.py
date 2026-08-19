#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def main():
    current_os = platform.system()
    print(f"[*] Detected Operating System: {current_os}")

    # Define target commands or scripts based on OS if needed
    if current_os == "Windows":
        target_command = ["cmd.exe", "/c", "echo Running Windows tasks..."]
    elif current_os == "Darwin": # macOS
        target_command = ["echo", "Running macOS tasks..."]
    else:
        print("[!] Unsupported operating system.")
        sys.exit(1)

    # Execute the command/script cleanly
    try:
        result = subprocess.run(target_command, check=True)
        print("[+] Execution completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Execution failed with error code {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
