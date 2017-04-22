# iot_joule_auto_demo
An IOT example using the Intel® Joule platform as a remote telemetry device with Python and Intel® DAAL

Folder structure info:
- data_generator: a stub script to make data in the absense of sensors/hardware
- data_storage: the location of the data storage component and moving window analysis
- main_telem: the location of the main telemetry logic

**Summary**:

This demo simulates a remote telemetry device located on a race car, providing data to the driver and to the race engineers in the pits.  It takes windowed sensor data, feeds it to various online (streaming) algorithms for in-vehicle alarms, and allows for remote processing for race engineers by allowing the data to be kept local to the car itself.  

**Implementation**:

In order to take full advantage of the Intel® Joule hardware, _multiprocessing_ is used to access all 4 cores of the CPU.  The data collection and storage utilizes a queue, and the machine learning tasks are done with asynchronous processes.  
