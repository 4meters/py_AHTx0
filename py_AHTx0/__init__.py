"""
Raspberry Pi AHTx0 Driver.
"""
import smbus2
import time

__version__ = "0.1.0"

DEFAULT_PORT = 0x38
AHTX0_I2CADDR_DEFAULT: int = 0x38

AHTX0_CMD_SOFTRESET: int = 0xBA  # Soft reset command

AHT10_CMD_CALIBRATE: int = 0xE1  # Calibration command for AHT10 sensor
AHT20_CMD_CALIBRATE: int = 0xBE

AHTX0_STATUS_BUSY: int = 0x80  # Status bit for busy
AHTX0_STATUS_CALIBRATED: int = 0x08

AHTX0_CMD_TRIGGER: int = 0xAC

class AHTx0:
    """
    Interface library for AHT10/AHT20 temperature+humidity sensors
    """

    def __init__(
            self, port: int, address: int = AHTX0_I2CADDR_DEFAULT
    ) -> None:
        time.sleep(0.02)  # 20ms delay to wake up
        self.address = int(address)
        self.bus = smbus2.SMBus(port)
        self._buf = bytearray(6)
        self.reset()
        if not self.calibrate():
            raise RuntimeError("Could not calibrate")
        self._temp = None
        self._humidity = None

    def reset(self) -> None:
        """Perform a soft-reset of the AHT"""
        self._buf[0] = AHTX0_CMD_SOFTRESET
        with self.bus as bus:
            bus.write_block_data(self.address, 0, self._buf[:1])
            #bus.write(self._buf, start=0, end=1)
        time.sleep(0.02)  # 20ms delay to wake up


    def calibrate(self) -> bool:
        """Ask the sensor to self-calibrate. Returns True on success, False otherwise"""
        self._buf[0] = AHT10_CMD_CALIBRATE
        self._buf[1] = int(0x08)
        self._buf[2] = int(0x00)
        calibration_failed = False
        with self.bus as bus:
            try:
                # Newer AHT20's may not succeed with old command, so wrapping in try/except
                bus.write_block_data(self.address, int(0), self._buf[:3])
            except (RuntimeError, OSError):
                calibration_failed = True

        if calibration_failed:
            # try another calibration command for newer AHT20's
            # print("Calibration failed, trying AH20 command")
            time.sleep(0.01)
            self._buf[0] = AHT20_CMD_CALIBRATE
            with self.bus as bus:
                try:
                    bus.write_block_data(self.address, int(0), self._buf[:3])
                except (RuntimeError, OSError):
                    pass

        while self.status & AHTX0_STATUS_BUSY:
            time.sleep(0.01)
        if not self.status & AHTX0_STATUS_CALIBRATED:
            return False
        return True

    @property
    def status(self) -> int:
        """The status byte initially returned from the sensor, see datasheet for details"""
        with self.bus as bus:
            self._buf[0] = bus.read_byte(self.address)
        # print("status: "+hex(self._buf[0]))
        return self._buf[0]

    @property
    def relative_humidity(self) -> int:
        """The measured relative humidity in percent."""
        self._readdata()
        return self._humidity

    @property
    def temperature(self) -> int:
        """The measured temperature in degrees Celsius."""
        self._readdata()
        return self._temp

    def _readdata(self) -> None:
        """Internal function for triggering the AHT to read temp/humidity"""
        self._buf[0] = AHTX0_CMD_TRIGGER
        self._buf[1] = 0x33
        self._buf[2] = 0x00
        with self.bus as bus:
            bus.write_block_data(self.address, 0, self._buf[:3])
            # i2c.write(self._buf, start=0, end=3)
        while self.status & AHTX0_STATUS_BUSY:
            time.sleep(0.01)
        with self.bus as bus:
            self._buf = bus.read_i2c_block_data(self.address, 0, 7)
            # i2c.readinto(self._buf, start=0, end=6)

        self._humidity = (
                (self._buf[1] << 12) | (self._buf[2] << 4) | (self._buf[3] >> 4)
        )
        self._humidity = (self._humidity * 100) / 0x100000
        self._temp = ((self._buf[3] & 0xF) << 16) | (self._buf[4] << 8) | self._buf[5]
        self._temp = ((self._temp * 200.0) / 0x100000) - 50
