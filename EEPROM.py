import core 
import spidev

class EEPROM_RPiBasic(core.EEPROM_connection):
   """
   Implementation of ADS124_connection for a basic raspberry pi setup.

   Requires spidev to be installed on the pi. Uses the first of the two spi outputs
   on the raspberry pi.
   """

   def __init__(self):
      self.EEPROM_connect()

   def EEPROM_transfer(self,to_send):
      """
      Transfer data over spi connection.

      Sends a list of bytes to the EEPROM over spi, and returns the chips 
      response during the message.
      """
      data = self.spi.xfer2(to_send)
      return data

   def EEPROM_connect(self) :
      """
      Open an spi connection to the EEPROM. 
   
      Settings should be customized to desired use.
      """
      self.spi = spidev.SpiDev()
      self.spi.open(0,1)
      self.spi.cshigh = False
      self.spi.mode = 0b00
      self.spi.max_speed_hz = 3814
      return

   def ADS124_close(self):
      self.spi.close()
      return
