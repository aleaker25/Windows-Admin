# Windows Admin Toolkit

🧰 A versatile Python script designed to simplify common Windows administration tasks. This utility provides a user-friendly, menu-driven interface to perform a range of essential system management functions, complete with comprehensive logging for all actions.

---
## Features

* **User Account Management**
    * 👤 **List Users:** View all local user accounts on the machine.
    * ➕ **Create User:** Add a new local user account with a specified password.
    * ➖ **Delete User:** Remove an existing local user account.

* **Service Control**
    * 📊 **Check Service Status:** Query the current state of any Windows service (e.g., Running, Stopped).
    * ▶️ **Start Service:** Initiate a stopped Windows service.
    * ⏹️ **Stop Service:** Halt a running Windows service.

* **System Information & Auditing**
    * 🖥️ **Get OS Information:** Retrieve detailed OS information, including version, release, and architecture.
    * 📋 **List Running Processes:** Display a list of all currently active processes and their PIDs.
    * 💾 **Check Disk Space:** View usage statistics for all connected disk partitions (Total, Used, and Free space).

* **Windows Registry Interaction**
    * 📖 **Read Registry Key:** Safely read a value from a specified key in the Windows Registry.
    * ✍️ **Write Registry Key:** Create or modify a value in the Windows Registry (use with caution!).

* **File System Management**
    * 🗑️ **Clear Temporary Files:** Clean out the user's temporary files directory to free up disk space.

---
## Prerequisites

Before running the script, you need to have Python installed and the `psutil` library.

Install `psutil` using pip:
```bash
pip install psutil
