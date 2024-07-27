Introduction
============

Python library using smbus2 for the Adafruit AHT10 or AHT20 Humidity and Temperature Sensor

Based on original solution from Adafruit repo: https://github.com/adafruit/Adafruit_CircuitPython_AHTx0

Dependency lightweight

Dependencies
=============
This library depends on:

* smbus2

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the library locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ahtx0/>`_. To install for current user:

.. code-block:: shell

    pip3 install pyAHTx0

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install pyAHTx0

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install pyAHTx0

Usage Example
=============

.. code-block:: python3

    import py_AHTx0

    # aht10 - init
    port = 1
    address = 0x38

    aht10_sensor = py_AHTx0.AHTx0(port, address)

    while True:
        print(aht10_sensor.temperature)
        print(aht10_sensor.relative_humidity)
        time.sleep(2)


Documentation
=============


calibrate() → bool

    Ask the sensor to self-calibrate. Returns True on success, False otherwise

property relative_humidity: int

    The measured relative humidity in percent.

reset() → None

    Perform a soft-reset of the AHT

property status: int

    The status byte initially returned from the sensor, see datasheet for details

property temperature: int

    The measured temperature in degrees Celsius.
