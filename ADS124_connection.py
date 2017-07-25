import spidev

def ADS124_transfer ( spi, list ) :
   """
   Transfer data over spi connection.

   Sends a list of bytes to the ADS124_S08 over spi, and returns the chips 
   response during the message.
   """
   spi.xfer(list)
   return list

def ADS124_connect () :
   """
   Open an spi connection to the ADS124_S08. 
   
   Settings should be customized to desired use.
   """
   spi = spidev.SpiDev()
   spi.open(0,0)
   spi.cshigh = False
   spi.mode = 0b01
   spi.max_speed_hz = 3814
   return spi

def ADS124_close ( spi ):
   spi.close()
   return
