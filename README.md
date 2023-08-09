# Photovoltaic Emulator Backend

This repository hosts the backend for a Photovoltaic Emulator hardware device, which was designed as part of the final year undergraduate project at the University of Moratuwa.

The design of the software is modular, ensuring each unit can be individually developed, tested, and reused. 
We've built this entire system on a foundation of open-source technologies.

## 🔍 Software Overview

### Backend: 
  - **Function**: Enables photovoltaic module parameter extraction, handles serial communication with the hardware (Microcontroller Unit), and exposes an API for the UI and dashboard.
  - **Technology Stack**: `Python` + `Flask`.
  
  The backend (this repository) is a Python web API implemented using the Flask web microframework. The choice of Python is due to its robust scientific computing libraries needed for parameter extraction. The backend is divided into three components:

  1. **Flask API**: Provides the interface for frontend communication and overseeing PV model and emulator operations.
  2. **PV Model and Algorithms**: Parameter calculations, heavily reliant on the `SciPy` and `NumPy` libraries for various mathematical implementations.
  3. **Hardware Interface**: Hardware management and communication, delivering a real-time data display. Uses Python serial library for serial communications with the hardware. Interactions with the dashboard are done through the Python client for Influx DB.


### Control Panel (UI): 
  - **Repository Link**: https://github.com/sathira10/pv-emulator-backend
  - **Function**: Accepts user-input of pv module data, displays calculated SDM parameters, and triggers hardware emulation.
  - **Technology Stack**: `JavaScript` + `React` (`Next.js`).

### Dashboard:
  - **Function**: Provides a real-time display of crucial parameters, including voltage, current, and reference voltage.
  - **Technology Stack**: `Influx DB` + `Grafana`.


## 🚀 Getting Started

**Note**: If you're using Windows, you might need to adjust some commands. (environment variables and virtual environment activation)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/sathira10/pv-emulator-backend.git
   cd pv-emulator-backend
   ```

2. **(Optional) Create a virtual environment**:

   ```bash
   virtualenv venv
   source venv/bin/activate
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask application**:

   ```bash
   export FLASK_APP=app/app.py
   export FLASK_ENV=development
   flask run
   ```

   This will start the Flask API on the default port (usually 5000) and in development mode.


5. **Test the API**

   Access the backend API at [http://127.0.0.1:5000](http://127.0.0.1:5000). If everything is set up correctly, you should see a message saying that the API is online.


## 🌐 Using the API with the Frontend UI

If the backend API is active and online, you can seamlessly integrate it with the frontend UI available [here](https://github.com/sathira10/pv-emulator). 
This will ebable youto interract with the API and Calculate parameters and curves for the single diode model for any given PV module.

Note that only the `pvmodel` functionality will be accessible through this interface. The `emulator` section requires the physical hardware device. 
However, this setup provides a comprehensive platform for PV module parameter extraction.

## 🎓 Project Members

- Sathira Tennakoon
- Imasha Balahewa
- Hasitha Umayanga

For a detailed dive into the project, you can read our published paper on [IEEE Xplore](https://ieeexplore.ieee.org/document/10000216).