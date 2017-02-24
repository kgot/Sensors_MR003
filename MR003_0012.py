# Library for the MR003-1.2 temperature sensor from microbot.
#
# Based the on Adafruit_Python_MCP9808 library [1]
# [1]: https://github.com/adafruit/Adafruit_Python_MCP9808
# 
# Depends on the Adafruit Python GPIO Library for its I2C abstraction [2]
# [2]: https://github.com/adafruit/Adafruit_Python_GPIO

import logging
import math

# Default I2C address for device.
MR003_0012_I2CADDR_DEFAULT = 0x48

# Register addresses.
MR003_0012_REG_TEMP = 0x0
MR003_0012_REG_CONFIG = 0x1
MR003_0012_REG_TEMP_HYST = 0x2
MR003_0012_REG_TEMP_SET = 0x3

# Configuration register values.
MR003_0012_REG_CONFIG_ONESHOT = 0x80
MR003_0012_REG_CONFIG_ADCRES = 0x60
MR003_0012_REG_CONFIG_FAULTQUEUE = 0x18
MR003_0012_REG_CONFIG_ALERTPOL = 0x04
MR003_0012_REG_CONFIG_COMPINT = 0x02
MR003_0012_REG_CONFIG_SHUTDOWN = 0x01

class MR003_0012(object):
    """Initialize device."""
    def __init__(self, address = MR003_0012_I2CADDR_DEFAULT, i2c = None, **kwargs):
        self._logger = logging.getLogger('MR003_0012')
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._device = i2c.get_i2c_device(address, **kwargs)

    def readTempC(self):
        """Read sensor and return its value in degrees celsius."""
        # Read temperature register value.
        t = self._device.readU16BE(MR003_0012_REG_TEMP)
        self._logger.debug('Raw ambient temp register value: 0x{0:04X}'.format(t & 0xFFFF))
        # Scale and convert to signed value.
        temp = (t >> 4 & 0x7FF0) / 16.0
        if t & 0x8000:
            temp = -temp
        return temp
