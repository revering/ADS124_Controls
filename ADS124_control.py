import ADS124_connection
import math

class ADS124:
   """Class for creating commands for the ADS124S08 chip
   
   Needs ADS124_connect(), ADS124_close(), and ADS124_transfer methods to exist.
   ADS124_connect() must return an spi connection object, ADS124_transfer() 
   must write and simultaneously recieve the number of bytes given.
   Does not check if connection exists or is responding.
   
   """     	
   def __init__(self):
      self.spi = ADS124_connection.ADS124_connect()

   def __del__(self):
      ADS124_connection.ADS124_close( self.spi )

   def ADS124_Start(self):
      """ Start analog to digital conversion in chip """
      ADS124_connection.ADS124_transfer(self.spi,[0x8])   
      return

   def ADS124_Stop(self): 	
      """ Stop analog to digital conversion in chip """
      ADS124_connection.ADS124_transfer(self.spi,[0xa])  
      return

   def ADS124_Reset(self):
      ADS124_connection.ADS124_transfer(self.spi,[0x6]) 
      return

   def ADS124_ReadData(self):
      """ 
      Request chip to read out data. 

      Request + readout cycle takes two bytes longer than direct 
      data read, but avoids any potential offset issues.
      """
      list = ADS124_connection.ADS124_transfer(self.spi,[0x12, 0,0,0])
      return list[1:4]

   def ADS124_ReadReg( self, reg, n ):
      """ Read n bytes starting at register reg """
      b = ( 0x20 | reg )
      to_send = [b, n-1]
      i = int(0) 
      while (i < n):
         to_send.append(0)
         i = i + 1
         ADS124_connection.ADS124_transfer(self.spi,to_send)
      return to_send[2:n+2]
	
   def ADS124_RDD(self):
      """ 
      Direct data read. 

      Chip continuously reads data while started, so can use this method to 
      read default output stream of data. May see offset errors if not 
      careful with clock or commands given.
      """
      list=ADS124_connection.ADS124_transfer(self.spi, [0,0,0])
      return list

   def ADS124_WriteReg( self, reg , n, values ):
      """ 
      Write n blocks starting at register reg.

      Arguments:
      reg - The beginning register to write
      n - The total number of registers to write
      Values - A list of n bytes.
      """
      b = (0x40 | reg)
      list = [b, n-1]
      to_write = list + values
      ADS124_connection.ADS124_transfer(self.spi,to_write)
      return

   def ADS124_Setup(self):
      """ Default setup for readout. Should be customized for desired operation """
      self.ADS124_Reset()
      self.ADS124_SetIDACMag(1000)
      self.ADS124_EnableIntRef()
      self.ADS124_SetGPIOType(0,"GPIO")
      self.ADS124_SetGPIOType(1,"GPIO")
      self.ADS124_DisableGain()
      return

   def ADS124_EnableIntRef(self):
      """ 
      Turns on and selects internal reference.
      
      Internal reference must be on in order to use excitation current sources.
      Can use an external reference with internal excitation current, but the 
      internal reference must be on. Defaults to off.
      """
      setting = self.ADS124_ReadReg(0x5,1)
      self.ADS124_WriteReg(0x5,1,[((setting[0]>>2)<<2)|2])
      self.ADS124_RefSelect(2)
      return

   def ADS124_DisableIntRef(self):
      setting = self.ADS124_ReadReg(0x5,1)
      self.ADS124_WriteReg(0x5,1,[(setting[0]>>2)<<2])
      return

   def ADS124_GetIntRef(self):
      return self.ADS124_ReadReg(0x5,1)[0]%4

   def ADS124_RefSelect(self, N):
      """
      Selects source of reference input.

      N must be 0, 1, or 2. 2 = internal reference, 
      1 = REFP1,REFN1, 0 = REFP0,REFN0 (default).
      """
      setting = self.ADS124_ReadReg(0x5,1)
      pre = setting[0]>>4
      post = setting[0] % 4
      pre *= 16
      self.ADS124_WriteReg(0x5,1,[pre|(N*4)|post])
      return

   def ADS124_GetRefSelect(self):
      """Returns the currently selected internal reference"""
      return (self.ADS124_ReadReg(0x5,1)[0]%16)>>2
 
   def ADS124_RegDump(self):
      """Prints the current contents of all 18 registers"""
      regs = self.ADS124_ReadReg(0,18)
      print [hex(a) for a in regs]
      return

   def ADS124_SetGPIOType( self, gpio, IO ):
      """
      Set pins to be inputs or GPIO

      Select gpio between 0 and 3, corresponding to GPIO[gpio] pins. 
      IO must be input or output.
      """
      setting = self.ADS124_ReadReg(0x11, 1)
      if gpio > 3:
         print "Maximum GPIO value is 3."
         return
      pre = setting[0] >> (gpio + 1)
      pre = pre << (gpio+1)
      if gpio != 0:
         post = setting[0] % (2**gpio)
      else: 
         post = 0
      if IO == 'Input':
         val = 0
      elif IO == 'GPIO':
         val = 1   
      else:
         print "Specify IO as \'Input\' or \'GPIO\'"
         return
      val *= 2**gpio
      self.ADS124_WriteReg(0x11,1,[(pre|val|post)])
      return

   def ADS124_GetGPIOType(self, gpio):
      """Return the current setting for the given GPIO[gpio] pin"""
      return (self.ADS124_ReadReg(0x11,1)[0]>>(gpio))%2

   def ADS124_SetGPIOValue(self, gpio, value): 
      """Set the given GPIO to be low (0) or high (1)"""
      if value!=0 and value!=1:
         print "Setting must be 1 or 0."
         return
      if value>3 or value<0:
         print "Pin must be in range 0 - 3."
         return 
      list = self.ADS124_ReadReg(0x10, 1) 
      pre = list[0] >> (gpio+1)
      pre = pre << (gpio+1)
      post = list[0]%(2**gpio)
      value *= 2**gpio
      self.ADS124_WriteReg(0x10, 1, [pre|value|post])
      return

   def ADS124_GetGPIOValue(self, gpio):
      """Returns the input/output data for the selected gpio"""
      return (self.ADS124_ReadReg(0x10,1)[0]>>(gpio))%2

   def ADS124_SetPosInput(self, pin):
      """Selects the positive input to the ADC"""
      setting = self.ADS124_ReadReg(0x2,1)
      neg = setting[0] % 16
      pin *= 16
      self.ADS124_WriteReg(0x2, 1, [(pin | neg)])
      return

   def ADS124_GetPosInput(self):
      """Returns the current positive input of the ADC"""
      return self.ADS124_ReadReg(0x2,1)[0]<<4

   def ADS124_SetNegInput( self, pin ):
      """Selects the negative input to the ADC"""
      setting = self.ADS124_ReadReg(0x2,1)
      pos = setting[0] - (setting[0] % 16)
      self.ADS124_WriteReg(0x2, 1,[(pos | pin)])
      return

   def ADS124_GetNegInput(self):
      """Returns the current negative input of the ADC"""
      return self.ADS124_ReadReg(0x2,1)[0]%16

   def ADS124_SetIDAC1( self, pin ):
      """
      Set the excitation current source for IDAC1

      Both excitation current sources can be set to the same pin. The resulting 
      current will be the current setting, not the sum of the two.
      The internal reference must be on in order to use the excitation current.
      """
      setting = self.ADS124_ReadReg(0x7,1)
      two = setting[0] - (setting[0] % 16)
      self.ADS124_WriteReg(0x7, 1, [(two | pin)])
      return
 
   def ADS124_GetIDAC1(self):
      """Return the current pin used for the excitation current"""
      return self.ADS124_ReadReg(0x7,1)[0]%16

   def ADS124_SetIDAC2( self, pin ):
      """
      Set the excitation current source for IDAC2

      Both excitation current sources can be set to the same pin. The resulting 
      current will be the current setting, not the sum of the two.
      The internal reference must be on in order to use the excitation current.
      """
      setting = self.ADS124_ReadReg(0x7,1)
      one = setting[0] % 16
      pin *= 16
      self.ADS124_WriteReg(0x7, 1, [(pin | one)])
      return

   def ADS124_GetIDAC2(self):
      """Return the current pin used for the excitation current"""
      return self.ADS124_ReadReg(0x7,1)[0]<<4

   def ADS124_EnableGain( self ):
      """Enable on the PGA"""
      setting = self.ADS124_ReadReg(0x3, 1)
      gain = setting[0] % 8
      delay = setting[0] - (setting[0] % 32)
      self.ADS124_WriteReg( 0x3, 1, [(delay | 0x8 | gain)])
      return

   def ADS124_DisableGain( self ): 
      """Disable and bypass the PGA"""
      setting = self.ADS124_ReadReg(0x3, 1)
      gain = setting[0] % 8
      delay = setting[0] - (setting[0] % 32)
      self.ADS124_WriteReg( 0x3, 1, [(delay | gain)])
      return

   def ADS124_GetGain(self):
      """Return whether the gain is enabled or disabled"""
      return self.ADS124_ReadReg(0x3,1)[0]%8

   def ADS124_SetGain( self, gain ):
      """
      Set the magnitude of the gain.

      Gain must be enabled to take effect. Possible gain values range from 1-128 in 
      powers of two (1,2,4,8, etc.).
      """
      setting = self.ADS124_ReadReg(0x3, 1)
      config = setting[0] - (setting[0] % 8)
      if gain>1 :
         gain = int(math.log(gain,2))
      else:
         gain = 0
      print config | gain
      self.ADS124_WriteReg( 0x3, 1, [(config | gain)])
      return

   def ADS124_GetGainValue(self):
      """Return the current gain magnitude"""
      return 2**(self.ADS124_ReadReg(0x3,1)[0]%8)

   def ADS124_SetVBias( self, pin, value ):
      """Select pins to bias. 1 to enable for the selected pin, 0 to disable."""
      setting = self.ADS124_ReadReg(0x8,1)
      if pin == "com":
         pin = 6
      if (pin>6) | (pin<0) :
         print "Pin must be 0 - 5 or com"
         return
      pre = setting[0]>>(pin+1) 
      pre = pre << (pin+1)
      post = setting[0]%(2**pin) 
      value = value << pin
      self.ADS124_WriteReg(0x8,1,[(pre|value|post)])
      return

   def ADS124_GetVBias(self, pin):
      """Return 1 if bias is enabled for the selected pin, 0 otherwise."""
      if pin == "com":
        pin = 6
      return self.ADS124_ReadReg(0x8,1)[0]%(2**(pin+1))>>pin

   def ADS124_SetVBiasLevel( self, num ):
      """
      Set the bias voltage level for all biased pins.
      
      num = 0 : bias = (AVDD+AVSS)/2 (default)
      num = 1 : bias = (AVDD+AVSS)/12
      """
      if ((num != 0) and (num != 1)):
         print "Setting must be 0 (AVDD/2) or 1 (AVDD/12)"
         return
      setting = self.ADS124_ReadReg(0x8,1)
      post = setting[0]%128
      num = num << 7
      self.ADS124_WriteReg(0x8,1,[num|post])
      return 

   def ADS124_GetVBiasLevel(self):
      """Return the bias voltage level for all pins"""
      setting = self.ADS124_ReadReg(0x8,1)[0]>>7
      if(setting == 0): return "(AVDD+AVSS)/2"
      return"(AVDD+AVSS)/12"

   def ADS124_SetIDACMag( self, num ):
      """Set the magnitude of current for both IDAC's in micro amps."""
      if num < 10:
         val = 0 
         cur = 0
      elif num < 50:
         val = 1 
         cur = 10
      elif num < 100:
         val = 2 
         cur = 50
      elif num < 250:
         val = 3 
         cur = 100
      elif num < 500:
         val = 4 
         cur = 250
      elif num < 750:
         val = 5 
         cur = 500
      elif num < 1000:
         val = 6 
         cur = 750
      elif num < 1500:
         val = 7 
         cur = 1000
      elif num < 2000:
         val = 8  
         cur = 1500
      elif num == 2000:
         val = 9 
         cur = 2000
      else:
         val = 0 
         cur = 0
      self.ADS124_WriteReg(0x6,1,[val])
      return

   def ADS124_GetIDACMag(self):
      """Returns the active excitation current magnitude in micro amps"""
      return self.ADS124_ReadReg(0x6,1)[0]

   def ADS124_ReadVolt(self):
      """
      Returns the value of the ADC converted to volts.

      Does not account for gain. Assumes reference voltage is 2.5V.
      """
      data = self.ADS124_ReadData()
      voltage = ((data[0]%128)<<16)+(data[1]<<8)+data[2]
      if((data[0]>>7)==1): voltage = voltage*-1
      vref = 2.5
      return voltage*vref/(2**23)

   def ADS124_SystemOffCal(self):
      ADS124_connection.ADS124_transfer(self.spi, [0x19])
      return


