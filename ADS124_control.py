import ADS124_connection
import math

class ADS124:
	
        def __init__(self):
	   self.spi = ADS124_connection.ADS124_connect()

	def __del__(self):
	   ADS124_connection.ADS124_close( self.spi )

	def ADS124_Start(self):

	   ADS124_connection.ADS124_transfer(self.spi,[0x8])   

	   return

	def ADS124_Stop(self): 
	
	   ADS124_connection.ADS124_transfer(self.spi,[0xa])  

	   return

	def ADS124_Reset(self):

	   ADS124_connection.ADS124_transfer(self.spi,[0x6]) 

	   return

	def ADS124_ReadData(self):
	
	   list = ADS124_connection.ADS124_transfer(self.spi,[0x12, 0,0,0])

	   return list[1:4]

	def ADS124_ReadReg( self, reg, bytes ):
 
	   b = ( 0x20 | reg )
	   to_send = [b, bytes-1]
	   i = int(0) 

	   while (i < bytes):
		to_send.append(0)
	        i = i + 1
	
	   ADS124_connection.ADS124_transfer(self.spi,to_send)
	 
	   return to_send[2:bytes+2]
	
	def ADS124_RDD(self):

	   list=ADS124_connection.ADS124_transfer(self.spi, [0,0,0,0,0,0,0])
	   return list

	def ADS124_WriteReg( self, reg , blocks, values ):

	   b = (0x40 | reg)
	   list = [b, blocks-1]
	   to_write = list + values
	   ADS124_connection.ADS124_transfer(self.spi,to_write)

	   return

	def ADS124_Setup(self):
  
 	   self.ADS124_Reset()
	   self.ADS124_SetIDACMag(1000)
           self.ADS124_EnableIntRef()
           self.ADS124_SetGPIOType(0,"GPIO")
	   self.ADS124_SetGPIOType(1,"GPIO")
           self.ADS124_DisableGain()
	   return

        def ADS124_EnableIntRef(self):
	   setting = self.ADS124_ReadReg(0x5,1)
	   self.ADS124_WriteReg(0x5,1,[((setting[0]>>2)<<2)|2])
           self.ADS124_RefSelect(2)
	   return

        def ADS124_DisableIntRef(self):
	   setting = self.ADS124_ReadReg(0x5,1)
	   self.ADS124_WriteReg(0x5,1,[(setting[0]>>2)<<2])
	   return

        def ADS124_RefSelect(self, N):
	   setting = self.ADS124_ReadReg(0x5,1)
	   pre = setting[0]>>4
	   post = setting[0] % 4
           pre *= 16
	   self.ADS124_WriteReg(0x5,1,[pre|(N*4)|post])
	   return

	def ADS124_RegDump(self):
	   regs = self.ADS124_ReadReg(0,18)
	   print [hex(a) for a in regs]
	   return

	def ADS124_SetGPIOType( self, gpio, IO ):
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

	def ADS124_SetGPIOValue( self, gpio, value ): 
	   list = self.ADS124_ReadReg(0x10, 1) 
	   if gpio == 1:
	      if (list[0] % 2) == 1:
	         if value == 0:
	            list[0] = list[0] - 1
	      else:
	         if value == 1:
	            list[0] = list[0] + 1   
	   if gpio == 2:
	      if (list[0] % 4) < 2 :
	         if value == 1:
	            list[0] = list[0] + 2
	      else:
	         if value == 0:
	            list[0] = list[0] - 2

	   self.ADS124_WriteReg(0x10, 1, list)
	   return

	def ADS124_SetPosInput( self, pin ):
	   setting = self.ADS124_ReadReg(0x2,1)
	   neg = setting[0] % 16
           pin *= 16
	   self.ADS124_WriteReg(0x2, 1, [(pin | neg)])
	   return

	def ADS124_SetNegInput( self, pin ):
	   setting = self.ADS124_ReadReg(0x2,1)
           pos = setting[0] - (setting[0] % 16)
	   self.ADS124_WriteReg(0x2, 1,[(pos | pin)])
           return

	def ADS124_SetIDAC1( self, pin ):
	   setting = self.ADS124_ReadReg(0x7,1)
	   two = setting[0] - (setting[0] % 16)
	   self.ADS124_WriteReg(0x7, 1, [(two | pin)])
	   return

	def ADS124_SetIDAC2( self, pin ):
	   setting = self.ADS124_ReadReg(0x7,1)
	   one = setting[0] % 16
	   pin *= 16
	   self.ADS124_WriteReg(0x7, 1, [(pin | one)])
	   return

	def ADS124_EnableGain( self ):
	   setting = self.ADS124_ReadReg(0x3, 1)
	   gain = setting[0] % 8
	   delay = setting[0] - (setting[0] % 32)
	   self.ADS124_WriteReg( 0x3, 1, [(delay | 0x8 | gain)])
	   return

	def ADS124_DisableGain( self ): 
	   setting = self.ADS124_ReadReg(0x3, 1)
	   gain = setting[0] % 8
	   delay = setting[0] - (setting[0] % 32)
	   self.ADS124_WriteReg( 0x3, 1, [(delay | gain)])
	   return

	def ADS124_SetGain( self, gain ):
	   setting = self.ADS124_ReadReg(0x3, 1)
	   config = setting[0] - (setting[0] % 8)
           if gain>1 :
              gain = int(math.log(gain,2))
	   else:
              gain = 0
           print config | gain
	   self.ADS124_WriteReg( 0x3, 1, [(config | gain)])
	   return

	def ADS124_SetVBias( self, pin, value ):
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

	def ADS124_SetVBiasLevel( self, num ):
	   if ((num != 0) and (num != 1)):
	      print "Setting must be 0 (AVDD/2) or 1 (AVDD/12)"
	      return
	   setting = self.ADS124_ReadReg(0x8,1)
	   post = setting[0]%128
	   num = num << 7
	   self.ADS124_WriteReg(0x8,1,[num|post])
	   return 

	def ADS124_SetIDACMag( self, num ):
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
	   print "Exitation current set to ", cur, "micro Amps."
	   return
