# BYODSHIELD

BYODSHIELD is a **proof of concept** for a non-intrusive method that ensures secured and authorized network access for schools with a BYOD (Bring Your Own Device) Program. This tool integrates with the UniFi API to manage RADIUS users and provides a simple way to set up and manage network access.

---

## Prerequisites

- Python 3.8 or higher
- Docker (if using the Docker setup)
- `pip` (Python package manager)

---

## Quickstart

### Step 1: Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/your-repo/BYODSHIELD.git
cd BYODSHIELD
```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Setup Options

### Option 1: Using Docker (For Local Environments)

1. **Run the Docker Container using docker-compose**

   Run the following command to build and start the Docker container:

   ```bash
   docker-compose up -d
   ```

2. **Access and Set Up UniFi**

   UniFi will be running on your local environment. Ensure that RADIUS is enabled and configured.

3. **Run Setup for Mock Users**

   Run the provided setup script to add mock RADIUS users:

   ```bash
   python setup.py
   ```

---

### Option 2: Manual Setup (For Real Environments)

1. **Configure Your Environment**

   Edit the `.env` file provided in the project root according to your needs:

   ```bash
   nano .env
   ```

   Example `.env` file:

   ```env
   UNIFI_HOST = 127.0.0.1
   UNIFI_PORT = 8443
   UNIFI_USERNAME = unifi
   UNIFI_PASSWORD = unifi
   UNIFI_SITE = default
   UNIFI_SSL_VERIFY = False
   ```

2. **Configure Your UniFi Setup**

   Make sure to enable RADIUS and add individual users. For an example of how to provision users, refer to `examples/provisioning.py`.

3. **Run the Application**

   Start the application with:

   ```bash
   python app.py
   ```

---

## Troubleshooting

- **UniFi API Issues**: Verify that the API URL and key in the `.env` file are correct.
- **Docker Issues**: Ensure Docker is installed and running on your system.
- **Dependency Issues**: Ensure all required Python packages are installed using `pip install -r requirements.txt`.

---

## Notes

- This is a **proof of concept** and is not intended for production use without further testing and security hardening.
- Ensure that the `mongodb` and `unifi/data` directories are properly set up with `.gitkeep` files to maintain the directory structure.

---

## License

This project is licensed under the DTL License. All rights are reserved by Ananya Timalsina. Any commercial or production use of this tool is strictly prohibited without the explicit permission of the owner.
