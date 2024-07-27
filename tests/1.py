import py_AHTx0

# aht10 - init
port = 1
address = 0x38

aht10_sensor = py_AHTx0.AHTx0(port, address)
print(aht10_sensor.temperature)
print(aht10_sensor.relative_humidity)
