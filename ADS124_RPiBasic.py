import core 
import spidev

class ADS124_RPiBasic(core.ADS124_connection):
   """
   Implementation of ADS124_connection for a basic raspberry pi setup.

   Requires spidev to be installed on the pi. Uses the first of the two spi outputs
   on the raspberry pi.
   """

   def __init__(self):
      self.ADS124_connect()

   def ADS124_transfer(self,to_send):
      """
      Transfer data over spi connection.

      Sends a list of bytes to the ADS124_S08 over spi, and returns the chip's 
      response during the message.
      """
      data = self.spi.xfer2(to_send)
      return data

   def ADS124_connect(self) :
      """
      Open an spi connection to the ADS124_S08. 
   
      Settings should be customized to desired use.
      """
      self.spi = spidev.SpiDev()
      self.spi.open(0,0)
      self.spi.cshigh = False
      self.spi.mode = 0b01
      self.spi.max_speed_hz = 3814
      return

   def ADS124_close(self):
      self.spi.close()
      return
