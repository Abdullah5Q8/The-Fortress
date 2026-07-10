"""SPI bridge to the MCP3008 10-bit ADC (analog sensors -> Raspberry Pi)."""

from spidev import SpiDev


class MCP3008:
    def __init__(self, bus=0, device=0):
        self.spi = SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1_000_000

    def read(self, channel=0):
        """Read one channel (0-7) and return it scaled to 0-100 (%)."""
        if not 0 <= channel <= 7:
            raise ValueError("MCP3008 channel must be 0-7")
        # Start bit, single-ended mode + channel, padding byte
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        raw = ((adc[1] & 3) << 8) + adc[2]  # 10-bit result (0-1023)
        return round(raw / 10.23)

    def close(self):
        self.spi.close()
