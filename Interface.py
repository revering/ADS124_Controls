import ADS124_control
import time

"""Script for interacting with the ADS124_S08 control chip"""

done = False
setup = False
con = ADS124_control.ADS124()
filename = "default.txt"
nsamples = 100
delay = 0.01

while(not done):
   if not setup: 
      setup(con)
      commands()
      status(con)
      setup = True
   command = input('Enter a command: ')
   if command == 0: done = True
   elif command == 1: SetPosIn(con)
   elif command == 2: SetNegIn(con)
   elif command == 3: SetExSc(con)
   elif command == 4: SetExMag(con)
   elif command == 5: SetVRef(con)
   elif command == 6: SetVBias(con)
   elif command == 7: ReadSample(con)
   elif command == 8: RSetup(con, filename, nsamples, delay)
   elif command == 9: ReadSamples(con, filename, nsamples, delay)
   elif command == "c": commands(con)
   elif command == "s": status(con)
   else : print "Command not recognized"

stop(con)


def setup(con):
   con.ADS124_control.ADS124_Setup()
   return

def stop(con):
   con.ADS124_control.ADS124_Stop()
   return

def status(con):
   print ("Positive Input is {}".format(con.ADS124_control.ADS124_GetPosInput())) 
   print ("Negative Input is {}".format(con.ADS124_control.ADS124_GetNegInput()))
   print ("Excitation Current Sourced from {}".format(con.ADS124_control.ADS124_GetIDAC1()))
   print ("Excitation Current Magnitude is {}".format(con.ADS124_control.ADS124_GetIDACMag()))
   print ("Reference type is {}".format(con.ADS124_control.ADS124_GetIntRef()))
   print ("Bias voltage is {} from pin {}".format(con.ADS124_control.ADS124_GetVBiasLevel(),con.ADS124_control.ADS124_GetVBias()))
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
   userin = input("Enter positive input pin assignment (0-12)")
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
   userin = input("Enter negative input pin assignment (0-12)")
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
   userin = input("Enter excitation current pin (0-12)")
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
   userin = input("Enter excitation current magnitude in micro amps (0-2000)")
   try:
      mag = int(userin)
   except ValueError:
      print("Input not recognized")
      return
   if (mag<0)|(mag>2000):
      print("Current must be between 0 and 2000")
      return
   con.ADS124_SetIDACMag(pin)
   return

def SetVRef(con):
   userin = input("Enter reference voltage source (int for internal, or 0-1")
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
   userin = input("Switch which pin?")
   if userin!="com":
      try:
         pin = int(userin)
      except ValueError:
         print("Input not recognized")
         return	 
      if (pin<0)|(pin>6):
         print("Current must be between 0 and 2000")
         return
   pinval = con.ADS124_GetVBias(pin)	 
   con.ADS124_SetIDACMag(pin, not pinval)

def readVbias(con):
   for i in range(0,6):
      pinval = con.ADS124_GetVBias(pin)
      print("Pin %d set to %d" %(i,pinval))
   return

def ReadSample(con):
   con.ADS124_Start()
   volt = con.ADS214_ReadVolt()
   print("Voltage is %d." %volt)
   return

def RSetup(con, filename, nsamples, delay):
   readSetup(con, filename, nsamples, delay)
   userin = input("Enter command")
   try:
      mag = int(userin)
   except ValueError:
      print("Input not recognized")
      RSetup(con, filename, nsamples, delay)	 
   if (userin<0)|(userin>3):
      print("Input must be between 0 and 3")
      RSetup(con, filename, nsamples, delay)
   elif userin==1:
      filename = input("Enter new filename")
      RSetup(con, filename, nsamples, delay)
   elif userin==2:
      nsamples = input("Enter number of samples to take")
      RSetup(con, filename, nsamples, delay)
   elif userin==3:
      delay = input("Enter time delay between samples")
      RSetup(con, filename, nsamples, delay)
   return
   

def readSetup(con, filename, nsamples, delay):
   print("Filename = %s, Number of samples = %d, delay = %d" %(filename,nsamples,delay))
   print("1: Change filename\n 2: Change number of samples\n 3: Change delay time\n 4: Return")
   return









