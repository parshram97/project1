import os
import subprocess
import logging
from datetime import datetime

logging.basicConfig(filename='system_cleaner.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# ANSI escape codes for color
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def clean_temporary_files():
    print(GREEN + "Cleaning temporary files..." + RESET)
    logging.info("Cleaning temporary files...")
    try:
        subprocess.run(["sudo", "rm", "-rf", "/tmp/*"])
        print(GREEN + "Temporary files cleaned." + RESET)
        logging.info("Temporary files cleaned.")
    except Exception as e:
        print(RED + f"An error occurred while cleaning temporary files: {e}" + RESET)
        logging.error(f"An error occurred while cleaning temporary files: {e}")

def clean_package_cache():
    print(GREEN + "Cleaning package cache..." + RESET)
    logging.info("Cleaning package cache...")
    try:
        subprocess.run(["sudo", "apt", "clean"])
        print(GREEN + "Package cache cleaned." + RESET)
        logging.info("Package cache cleaned.")
    except Exception as e:
        print(RED + f"An error occurred while cleaning package cache: {e}" + RESET)
        logging.error(f"An error occurred while cleaning package cache: {e}")

def clean_old_logs():
    print(GREEN + "Cleaning old log files..." + RESET)
    logging.info("Cleaning old log files...")
    try:
        subprocess.run(["sudo", "find", "/var/log", "-type", "f", "-mtime", "+7", "-delete"])
        print(GREEN + "Old log files cleaned." + RESET)
        logging.info("Old log files cleaned.")
    except Exception as e:
        print(RED + f"An error occurred while cleaning old log files: {e}" + RESET)
        logging.error(f"An error occurred while cleaning old log files: {e}")

def show_cache_files():
    print(GREEN + "Listing cache files..." + RESET)
    logging.info("Listing cache files...")
    try:
        subprocess.run(["sudo", "find", "/var/cache/apt/archives", "-type", "f", "-exec", "ls", "-lh", "{}", ";"])
        print(GREEN + "Cache files listed." + RESET)
        logging.info("Cache files listed.")
    except Exception as e:
        print(RED + f"An error occurred while listing cache files: {e}" + RESET)
        logging.error(f"An error occurred while listing cache files: {e}")

def show_deleted_files():
    print(GREEN + "Showing recently deleted files..." + RESET)
    logging.info("Showing recently deleted files...")
    try:
        subprocess.run(["sudo", "grep", "rm", "/var/log/syslog"])
        print(GREEN + "Recent deleted files listed." + RESET)
        logging.info("Recent deleted files listed.")
    except Exception as e:
        print(RED + f"An error occurred while showing recently deleted files: {e}" + RESET)
        logging.error(f"An error occurred while showing recently deleted files: {e}")

def interactive_confirmation(message):
    response = input(f"{message} [y/n]: ").lower()
    return response == 'y'

def backup_files(files, backup_dir):
    backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_dir, f"backup_{backup_timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    print(GREEN + "Creating backup..." + RESET)
    logging.info(f"Creating backup at {backup_dir}...")
    try:
        for file_path in files:
            file_name = os.path.basename(file_path)
            subprocess.run(["sudo", "cp", "-r", file_path, backup_dir])
            print(GREEN + f"Backed up: {file_name}" + RESET)
            logging.info(f"Backed up: {file_name}")
        print(GREEN + "Backup created successfully." + RESET)
        logging.info("Backup created successfully.")
    except Exception as e:
        print(RED + f"An error occurred while creating backup: {e}" + RESET)
        logging.error(f"An error occurred while creating backup: {e}")

def restore_files(backup_dir):
    print(GREEN + "Restoring files from backup..." + RESET)
    logging.info(f"Restoring files from backup directory: {backup_dir}")
    try:
        subprocess.run(["sudo", "cp", "-r", f"{backup_dir}/*", "/"])
        print(GREEN + "Files restored successfully." + RESET)
        logging.info("Files restored successfully.")
    except Exception as e:
        print(RED + f"An error occurred while restoring files: {e}" + RESET)
        logging.error(f"An error occurred while restoring files: {e}")

def schedule_cleaning():
    print(GREEN + "Scheduling automatic cleaning..." + RESET)
    logging.info("Scheduling automatic cleaning...")
    # Add code to implement scheduling (e.g., using cron)

def main_menu():
    print("\nLinux System Cleaner")
    print("====================")
    print("1. " + GREEN + "Clean Temporary Files" + RESET)
    print("2. " + GREEN + "Clean Package Cache" + RESET)
    print("3. " + GREEN + "Clean Old Log Files" + RESET)
    print("4. " + GREEN + "Show Cache Files" + RESET)
    print("5. " + GREEN + "Show Recently Deleted Files" + RESET)
    print("6. " + GREEN + "Backup Files" + RESET)
    print("7. " + GREEN + "Restore Files from Backup" + RESET)
    print("8. " + GREEN + "Schedule Automatic Cleaning" + RESET)
    print("9. " + RED + "Exit" + RESET)

    choice = input("Enter your choice: ")

    if choice == "1":
        if interactive_confirmation("Are you sure you want to clean temporary files?"):
            clean_temporary_files()
    elif choice == "2":
        if interactive_confirmation("Are you sure you want to clean package cache?"):
            clean_package_cache()
    elif choice == "3":
        if interactive_confirmation("Are you sure you want to clean old log files?"):
            clean_old_logs()
    elif choice == "4":
        show_cache_files()
    elif choice == "5":
        show_deleted_files()
    elif choice == "6":
        backup_dir = input("Enter backup directory path: ")
        files_to_backup = input("Enter files/directories to backup (separated by comma): ").split(",")
        if interactive_confirmation("Are you sure you want to backup files?"):
            backup_files(files_to_backup, backup_dir)
    elif choice == "7":
        backup_dir = input("Enter backup directory path: ")
        if interactive_confirmation("Are you sure you want to restore files from backup?"):
            restore_files(backup_dir)
    elif choice == "8":
        if interactive_confirmation("Are you sure you want to schedule automatic cleaning?"):
            schedule_cleaning()
    elif choice == "9":
        print("Exiting...")
        exit()
    else:
        print(RED + "Invalid choice. Please try again." + RESET)

if __name__ == "__main__":
    while True:
        main_menu()
