# pv-emulator-backend
The application consists of three main parts:
1. **Flask API** (app) - Main program including an API to expose the functionality of the app to the control-panel (frontend). This contains all the Flask code as well as macro functions for executing the pvmodel and emulator.
2. **PV Model and Algorithms** (app/pvmodel) - responsible parameter calculation. The pvmodel package contains the parameter extraction algorithms as well as functions to organize and prepare the data. The SciPy and NumPy libraries are used to implement various mathematical functions.
3. **Hardware Interface** (app/emulator) - responsible hardware management and communication as well as realtime data display. Serial communication is realized with the Python serial library. Communication with the dashboard uses the Python client for Influx DB.
