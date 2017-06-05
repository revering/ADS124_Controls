import spidev

def ADS124_transfer ( spi, list ) :

	spi.xfer(list)

	return list

def ADS124_connect () :
	spi = spidev.SpiDev()
	spi.open(0,0)
        spi.cshigh = False
	spi.mode = 0b01
	spi.max_speed_hz = 3814

	return spi

def ADS124_close ( spi ):

	spi.close()

	return
