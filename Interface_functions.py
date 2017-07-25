import ADS124_control

def setup(con):
   con.ADS124_Setup()
   return

def stop(con):
   con.ADS124_Stop()
   return

def status(con):
   print ("Positive Input is {}".format(con.ADS124_GetPosInput())) 
   print ("Negative Input is {}".format(con.ADS124_GetNegInput()))
   print ("Excitation Current Sourced from {}".format(con.ADS124_GetIDAC1()))
   print ("Excitation Current Magnitude is {}".format(con.ADS124_GetIDACMag()))
   print ("Reference type is {}".format(con.ADS124_GetIntRef()))
#   print ("Bias voltage is {} from pin {}".format(con.ADS124_GetVBiasLevel(),con.ADS124_GetVBias()))
   return

def commands():
   print "s : status"
   print "c : List commands"
   print "0 : Exit "
   print "1 : Set positive input"
   print "2 : Set negative input"
   print "3 : Set exitation current source"
   print "4 : Set exitation current magnitude"
   print "5 : Set reference"
   print "6 : Setup bias voltage"
   print "7 : Read one sample"
   print "8 : Setup multiple readout"
   print "9 : Read multiple samples"
   return

def SetPosIn(con):
   userin = input("Enter positive input pin assignment (0-12)\n")
   try:
      pin = int(userin)
   except ValueError:
      print("Input not recognized")
      return
   if (pin<0)|(pin>12):
      print("Pin must be between 0 and 12")
      return
   con.ADS124_SetPosInput(pin)
   return

def SetNegIn(con):
   userin = input("Enter negative input pin assignment (0-12)\n")
   try:
      pin = int(userin)
   except ValueError:
      print("Input not recognized")
      return
   if (pin<0)|(pin>12):
      print("Pin must be between 0 and 12")
      return
   con.ADS124_SetNegInput(pin)
   return

def SetExSc(con):
   userin = input("Enter excitation current pin (0-12)\n")
   try:
      pin = int(userin)
   except ValueError:
      print("Input not recognized")
      return
   if (pin<0)|(pin>12):
      print("Pin must be between 0 and 12")
      return
   con.ADS124_SetIDAC1(pin)
   return
     
def SetExMag(con):
   userin = input("Enter excitation current magnitude in micro amps (0-2000)\n")
   try:
      mag = int(userin)
   except ValueError:
      print("Input not recognized")
      return
   if (mag<0)|(mag>2000):
      print("Current must be between 0 and 2000")
      return
   con.ADS124_SetIDACMag(mag)
   return

def SetVRef(con):
   userin = input("Enter reference voltage source (int for internal, or 0-1\n")
   if userin != "int":
      try:
         src = int(userin)
      except ValueError:
         print("Input not recognized")
         return
      if (src<0)|(src>1):
         print("Pin must be either 0 or 1")
         return
      con.ADS124_RefSelect(ref)
   else: con.ADS124_EnableIntRef()   
   return


def SetVBias(con):
   readVbias(con)
   userin = input("Switch which pin? (0-6 or \"com\") \n")
   if userin!="com":
      try:
         pin = int(userin)
      except ValueError:
         print("Input not recognized")
         return	 
      if (pin<0)|(pin>6):
         print("Current must be between 0 and 2000")
         return
   else: pin = 6
   pinval = con.ADS124_GetVBias(pin)	 
   con.ADS124_SetVBias(pin, not pinval)

def readVbias(con):
   for i in range(0,7):
      pinval = con.ADS124_GetVBias(i)
      print("Pin %d set to %d" %(i,pinval))
   return

def ReadSample(con):
   con.ADS124_Start()
   volt = con.ADS124_ReadVolt()
   print("Voltage is %d." %volt)
   return

def RSetup(con, filename, nsamples, delay):
   readSetup(con, filename, nsamples, delay)
   userin = input("Enter command\n")
   try:
      mag = int(userin)
   except ValueError:
      print("Input not recognized\n")
      RSetup(con, filename, nsamples, delay)	 
   if (userin<0)|(userin>4):
      print("Input must be between 0 and 4\n")
      RSetup(con, filename, nsamples, delay)
   elif userin==1:
      filename = input("Enter new filename\n")
      RSetup(con, filename, nsamples, delay)
   elif userin==2:
      nsamples = input("Enter number of samples to take\n")
      RSetup(con, filename, nsamples, delay)
   elif userin==3:
      delay = input("Enter time delay between samples\n")
      RSetup(con, filename, nsamples, delay)
   return
   

def readSetup(con, filename, nsamples, delay):
   print("Filename = %s, Number of samples = %d, delay = %f" %(filename,nsamples,delay))
   print("1: Change filename\n2: Change number of samples\n3: Change delay time\n4: Return")
   return

def ReadSamples(con, filename, nsamples, delay):
   return 


