import ADS124_control
import time

def setup(con):
   con.ADS124_Setup()
   con.ADS124_Start()
   return

def stop(con):
   con.ADS124_Stop()
   return

def status(con):
   print ("\nPositive input is {}".format(con.ADS124_GetPosInput())) 
   print ("Negative input is {}".format(con.ADS124_GetNegInput()))
   print ("Excitation Current Sourced from {}".format(con.ADS124_GetIDAC1()))
   exmag = con.ADS124_GetIDACMag()
   if exmag==1: exmag = 10
   elif exmag==2: exmag = 50
   elif exmag==3: exmag = 100
   elif exmag==4: exmag = 250
   elif exmag==5: exmag = 500
   elif exmag==6: exmag = 750
   elif exmag==7: exmag = 1000
   elif exmag==8: exmag = 1500
   elif exmag==9: exmag = 2000
   else: exmag=0
   print ("Excitation Current Magnitude is {} micro amps".format(exmag))
   ref = con.ADS124_GetIntRef()

   print ("Reference type is {}\n\n".format(con.ADS124_GetIntRef()))
#   print ("Bias voltage is {} from pin {}".format(con.ADS124_GetVBiasLevel(),con.ADS124_GetVBias()))
   return

def commands():
   print "\ns  : Status"
   print "c  : List commands"
   print "r  : Reset"
   print "l  : Load settings"
   print "sv : Save settings"
   print "0  : Exit "
   print "1  : Set positive input"
   print "2  : Set negative input"
   print "3  : Set exitation current source"
   print "4  : Set exitation current magnitude"
   print "5  : Set reference"
   print "6  : Setup bias voltage"
   print "7  : Read one sample"
   print "8  : Setup multiple readout"
   print "9  : Read multiple samples\n\n"
   return

def SetPosIn(con):
   userin = raw_input("Enter positive input pin assignment (0-12)\n")
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
   userin = raw_input("Enter negative input pin assignment (0-12)\n")
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
   userin = raw_input("Enter excitation current pin (0-12)\n")
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
   userin = raw_input("Enter excitation current magnitude in micro amps (0-2000)\n")
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
   userin = raw_input("Enter reference voltage source (int for internal, or 0-1\n")
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
   userin = raw_input("Switch which pin? (0-6 or \"com\") \n")
   if userin!="com":
      try:
         pin = int(userin)
      except ValueError:
         print("Input not recognized")
         return	 
      if (pin<0)|(pin>6):
         print("Pin must be 0-6 or \"com\"")
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
   volt = con.ADS124_ReadVolt()
   print("Voltage is %f." %volt)
   return

def RSetup(con, filename, nsamples, delay):
   readSetup(con, filename, nsamples, delay)
   userin = raw_input("Enter command\n")
   try:
      mag = int(userin)
   except ValueError:
      print("input not recognized\n")
      RSetup(con, filename, nsamples, delay)	 
   if (mag<0)|(mag>4):
      print("input must be between 0 and 4\n")
      RSetup(con, filename, nsamples, delay)
   elif mag==1:
      filename = raw_input("Enter new filename\n")
      RSetup(con, filename, nsamples, delay)
   elif mag==2:      
      userin = raw_input("Enter number of samples to take\n")
      try: 
         samples = int(userin)
         if samples>0: nsamples = samples
         else: print("Number of samples must be greater than zero") 
      except ValueError:
         print("Input %s not recognized as a number" %userin)      
      RSetup(con, filename, nsamples, delay)
   elif mag==3:
      userin = raw_input("Enter time delay between samples in seconds\n")
      try:
          floatin = float(userin)
          if floatin>0: delay = floatin
          else: print("Delay must be greater than zero seconds")
      except ValueError:
          print("Input %s not recognized as a time" %userin)
      RSetup(con, filename, nsamples, delay)
   return [filename, nsamples, delay]
   

def readSetup(con, filename, nsamples, delay):
   print("\nFilename = %s, Number of samples = %d, delay = %f" %(filename,nsamples,delay))
   print("1: Change filename\n2: Change number of samples\n3: Change delay time\n4: Return\n")
   return

def ReadSamples(con, filename, nsamples, delay):
   with open(filename, 'w') as f:
      for i in range(0,nsamples):
         v = con.ADS124_ReadVolt()
         f.write("%f " %v)
	 time.sleep(delay)
   return 

def reset(con):
   con.ADS124_Reset()
   return

def load(con):
   fname = raw_input("Enter a file to load\n")
   try:
      ifile = open(fname, 'r')
   except IOError:
      print("File %s not found." %fname)
      return
   setting = []
   i = 0
   delay = 0.1
   filename = "default.txt"
   nsamples = 100
   for line in ifile:
      if i<18:
         try:
            regdata = int(line)
         except ValueError:
            print("File %s not formatted as expected" %fname)
	    return
         if (regdata<0)|(regdata>255):
            print("File %s not formatted as expected" %fname)
	    return
         setting.append(regdata)
      elif i==18: filename = line
      elif i==19: 
         try:
            nsamples = int(line)
         except ValueError:
            print("File %s not formatted as expected" %fname)
            return
      elif i==20:
         try:
            delay = float(line)
         except ValueError:
            print("File %s not formatted as expected" %fname)
            return
      i = i+1
   if len(setting) != 18:
      print("File %s not formatted as expected. %d registers instead of 18." %(fname,len(setting)))
      return
   con.ADS124_WriteReg(0,18,setting)
   return [filename, nsamples, delay]

def save(con, datafname, nsamples, delay):
   fname = raw_input("Enter filename\n")
   try:
      ofile = open(fname, 'w')
   except IOError:
      print("Unable to open file %s" %fname)
      return
   setting = []
   for i in range(0,18): setting.append(con.ADS124_ReadReg(i,1))
   for i in range(0,len(setting)):
      ofile.write("%d\n" %setting[i][0])
   ofile.write("%s\n" %datafname)
   ofile.write("%d\n" %nsamples)
   ofile.write("%f" %delay)
   ofile.close()
   return


