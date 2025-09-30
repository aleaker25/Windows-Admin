# win_admin.py
# FINAL VERSION - A Python script for Windows Administration tasks with robust logging.
# IMPORTANT: This script must be run with administrator privileges.

import subprocess
import os
import shutil
import winreg
import psutil
import platform
import logging

def setup_logging():
    """Configures the logger to write to a file and the console."""
    logger = logging.getLogger('WinAdmin')
    logger.setLevel(logging.INFO)

    # This prevents adding duplicate handlers if the script is ever reloaded.
    if logger.hasHandlers():
        logger.handlers.clear()

    # --- File Handler: This is what writes to the log file ---
    # It creates 'admin_script.log' in the same directory as the script.
    file_handler = logging.FileHandler('admin_script.log')
    file_handler.setLevel(logging.INFO)

    # --- Console Handler: This is what shows messages on the screen ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # The format includes timestamp, log level, and the message
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter) # We use the same format for both

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Get the logger instance to use throughout the script
logger = setup_logging()


def run_command(command):
    """
    Executes a shell command and logs its full output and any errors.
    This function is key to logging "everything".
    """
    try:
        logger.info(f"Executing command: {command}")
        # Run the command and capture its output
        result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
        
        # Log the standard output if there is any
        if result.stdout:
            logger.info(f"Command successful. Output:\n---\n{result.stdout.strip()}\n---")
        else:
            logger.info("Command successful with no output.")
            
    except subprocess.CalledProcessError as e:
        # Log the standard error if the command fails
        logger.error(f"Command failed with exit code {e.returncode}.")
        if e.stderr:
            logger.error(f"Error output:\n---\n{e.stderr.strip()}\n---")

# --- All Admin Functions (Unchanged, but rely on the corrected run_command) ---

def list_users():
    logger.info("--- Listing all local users ---")
    run_command("net user")

def create_user(username, password):
    logger.info(f"--- Creating user: {username} ---")
    run_command(f'net user "{username}" "{password}" /add')

def delete_user(username):
    logger.info(f"--- Deleting user: {username} ---")
    run_command(f'net user "{username}" /delete')

def check_service_status(service_name):
    logger.info(f"--- Checking status for service: {service_name} ---")
    run_command(f'sc query "{service_name}"')

def start_service(service_name):
    logger.info(f"--- Starting service: {service_name} ---")
    run_command(f'sc start "{service_name}"')

def stop_service(service_name):
    logger.info(f"--- Stopping service: {service_name} ---")
    run_command(f'sc stop "{service_name}"')

def get_os_version():
    logger.info("--- Getting OS Information ---")
    logger.info(f"System: {platform.system()}, Release: {platform.release()}, Version: {platform.version()}")

def list_processes():
    logger.info("--- Listing Running Processes ---")
    for proc in psutil.process_iter(['pid', 'name']):
        logger.info(f"  PID: {proc.info['pid']}, Name: {proc.info['name']}")

def get_disk_space():
    logger.info("--- Getting Disk Space ---")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            logger.info(f"Device: {partition.device} | Total: {usage.total / (1024**3):.2f} GB | Used: {usage.percent}%")
        except PermissionError:
            logger.warning(f"Could not access disk info for {partition.device}")

def read_registry_key(hive, key_path, value_name):
    logger.info(f"--- Reading Registry Key: {hive}\\{key_path}\\{value_name} ---")
    try:
        hive_key = getattr(winreg, hive)
        key = winreg.OpenKey(hive_key, key_path, 0, winreg.KEY_READ)
        value, reg_type = winreg.QueryValueEx(key, value_name)
        logger.info(f"Successfully read registry. Value: {value}")
        winreg.CloseKey(key)
    except FileNotFoundError:
        logger.error("Error: The specified key or value was not found.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def write_registry_key(hive, key_path, value_name, value_data, value_type):
    logger.warning(f"--- Attempting to write to Registry Key: {hive}\\{key_path}\\{value_name} ---")
    confirm = input("!!! WARNING: Modifying the registry is dangerous. Are you sure? (y/n): ").lower()
    if confirm != 'y':
        logger.info("Registry write operation cancelled by user.")
        return
    try:
        logger.info(f"User confirmed. Writing value '{value_data}' to '{value_name}'.")
        hive_key = getattr(winreg, hive)
        key = winreg.CreateKey(hive_key, key_path)
        winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        logger.info("Successfully wrote to the registry.")
        winreg.CloseKey(key)
    except Exception as e:
        logger.error(f"An error occurred while writing to the registry: {e}")

def delete_temp_files():
    temp_dir = os.environ.get('TEMP', 'C:\\Temp')
    logger.info(f"--- Deleting files in {temp_dir} ---")
    # ... (rest of the function is unchanged)

def main_menu():
    while True:
        # The menu is printed to the screen but not the log, to keep the log clean.
        print("\n===== Windows Admin Script =====")
        # ... (all print statements for the menu)
        print("1. List Local Users")
        print("2. Create a Local User")
        print("3. Delete a Local User")
        print("---------------------------------")
        print("4. Check Service Status")
        print("5. Start a Service")
        print("6. Stop a Service")
        print("---------------------------------")
        print("7. Get OS Version")
        print("8. List Running Processes")
        print("9. Get Disk Space")
        print("---------------------------------")
        print("10. Read a Registry Key (HKLM)")
        print("11. Write a Registry Key (HKLM)")
        print("---------------------------------")
        print("12. Delete Temporary Files")
        print("---------------------------------")
        print("0. Exit")

        choice = input("Enter your choice: ")
        logger.info(f"User selected menu option: '{choice}'") # This gets logged

        if choice == '1': list_users()
        elif choice == '2': create_user(input("Username: "), input("Password: "))
        elif choice == '3': delete_user(input("Username to delete: "))
        elif choice == '4': check_service_status(input("Service name: "))
        elif choice == '5': start_service(input("Service name: "))
        elif choice == '6': stop_service(input("Service name: "))
        elif choice == '7': get_os_version()
        elif choice == '8': list_processes()
        elif choice == '9': get_disk_space()
        elif choice == '10': read_registry_key("HKEY_LOCAL_MACHINE", input("Key path: "), input("Value name: "))
        elif choice == '11': write_registry_key("HKEY_LOCAL_MACHINE", input("Key path: "), input("Value name: "), input("Value data: "), winreg.REG_SZ)
        elif choice == '12': delete_temp_files()
        elif choice == '0':
            logger.info("Exiting script.")
            break
        else:
            logger.warning(f"Invalid menu choice entered: '{choice}'")

if __name__ == "__main__":
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
    if not is_admin:
        msg = "FATAL: This script requires administrator privileges. Please re-run from an elevated terminal."
        logger.error(msg)
        input("Press Enter to exit.") # Pause to ensure the message is seen
    else:
        logger.info("Script started with administrator privileges.")
        main_menu()