# iot_joule_auto_demo
An IOT example using the Intel® Joule platform as a remote telemetry device with Python and Intel® DAAL

Folder structure info:
- data_generator: a stub script to make data in the absense of sensors/hardware
- data_storage: the location of the data storage component and moving window analysis
- main_telem: the location of the main telemetry logic

**Summary**:

This demo simulates a remote telemetry device located on a race car, providing data to the driver and to the race engineers in the pits.  It takes windowed sensor data, feeds it to various online (streaming) algorithms for in-vehicle alarms, and allows for remote processing for race engineers by allowing the data to be kept local to the car itself.

**Implementation**:

In order to take full advantage of the Intel® Joule hardware, _multiprocessing_ is used to access all 4 cores of the CPU on the Joule.  The data collection and storage utilizes a queue, and the machine learning tasks are done with asynchronous processes.  The collection and storage process utilizes the multiprocessing queue to maintain light ordering (but not strict), and has a windowed sensor data of a few seconds implemented with a ring buffer.  Sensor reads are done with Intel's MRAA library for IoT devices, and the code is prioritized to not drop data when possible.  

**Hardware and OS**

The code is designed to run on Ubuntu Desktop 16.04 LTS, with the Intel® Distribution for Python\* as the Python environment.  Use of the scaffold code subs out the sensor reads with mocked data such that one may develop the code on other forms of OS (such as MacOS or Windows).  

The hardware used is the Intel® Joule 570x developer kit, used with the AC adapter and the heatsink installed.  In its current form, a display, mouse, and keyboard will be needed to use or demo the project.

**License**

MIT
