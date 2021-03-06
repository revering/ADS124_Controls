import core
import time

def setup(con):
   con.ADS124_Setup()
   con.ADS124_Start()
   return

def stop(con):
   con.ADS124_Stop()
   return

def status(con):
   print("Positive input is {}".format(con.ADS124_GetPosInput())) 
   print("Negative input is {}".format(con.ADS124_GetNegInput()))
   print("Excitation Current Sourced from {}".format(con.ADS124_GetIDAC1()))
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
   print("Excitation Current Magnitude is {} micro amps".format(exmag))
   refen = con.ADS124_GetIntRef()
   if refen==0: refon = "off"
   else: refon = "on"
   print("Internal reference is %s" %refon)
   ref = con.ADS124_GetRefSelect()
   if ref==2: reftype = "internal"
   elif ref==1: reftype = "REFP1 and REFN1"
   else: reftype = "REFP0 and REFN0"
   print("Selected reference is %s" %reftype)
#   print("Bias voltage is {} from pin {}".format(con.ADS124_GetVBiasLevel(),con.ADS124_GetVBias()))
   return

def commands():
   print "s  : Status"
   print "c  : List commands"
   print "r  : Reset"
   print "l  : Load settings"
   print "sv : Save settings"
   print "ch : Select channel"
   print "0  : Exit "
   print "1  : Set positive input"
   print "2  : Set negative input"
   print "3  : Set exitation current source"
   print "4  : Set exitation current magnitude"
   print "5  : Enable/disable internal reference"
   print "6  : Select reference"
   print "7  : Setup bias voltage"
   print "8  : Read one sample"
   print "9  : Setup multiple readout"
   print "10  : Read multiple samples"
   print "tr   : Reads all samples temps multiple times and stores to file"
   print "EEPROM : Opens EEProm menu for reading and writing"
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
   userin = raw_input("Enter reference voltage source (int for internal, or 0-1)\n")
   if userin != "int":
      try:
         src = int(userin)
      except ValueError:
         print("Input not recognized")
         return
      if (src<0)|(src>1):
         print("Pin must be either 0 or 1")
         return
      con.ADS124_RefSelect(src)
   else: 
      con.ADS124_EnableIntRef()  
      con.ADS124_RefSelect(2)
   print("") 
   return

def SwitchIntRef(con):
   userin = raw_input("Enter 1 to switch internal reference on or 0 to switch off\n")
   try:
      val = int(userin)
   except ValueError:
      print "Input not recognized"
      return
   if val==1: con.ADS124_EnableIntRef()
   elif val==0: con.ADS124_DisableIntRef()
   else: print "Input must be one or zero\n"
   return



def ReadEEPromOptions():
   print "1: Read Printed ID number"
   print "2: Read Serial Number"
   print "3: Write Printed ID number"
   print "4: exits the menu"


def SetVBias(con):
   readVbias(con)
   userin = raw_input("\nSwitch which pin? (0-6, \"com\", any other input to exit) \n")
   if userin!="com":
      try:
         pin = int(userin)
      except ValueError:
         return	 
      if (pin<0)|(pin>6):
         return
   else: pin = 6
   pinval = con.ADS124_GetVBias(pin)	 
   con.ADS124_SetVBias(pin, not pinval)
   print ""
   readVbias(con)

def readVbias(con):
   for i in range(0,7):
      pinval = con.ADS124_GetVBias(i)
      if pinval == 1:
         status = "on"
      else:
         status = "off"
      print("Pin %d VBias is %s" %(i,status))
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
   con.ADS124_Start()
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
      elif i==18: filename = line.strip()
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

def SetChannel(con, num):
   num -= 1
   con.ADS124_SetNegInput(12)
   while num>7:
      num = num-8
   con.ADS124_SetPosInput(7-num)
   con.ADS124_SetIDAC1(7-num)
   return
 
def ReadAll(con):
   for i in range(1,9):
      SetChannel(con,i)
      time.sleep(0.1)
      v = con.ADS124_ReadVolt()
      print("AIN%d is at %f volts." %(8-i,v))

   return 

def EEPromMem(econ):
   ReadEEPromOptions()
   userin = raw_input("\n")
   try:
      Input = int(userin)
   
      if Input==1:
         print "The id written on the board is: "+econ.LabelId()
      elif Input==2:
         sn=econ.SerialId()
         print "The Serial number is: %02x:%02x:%02x:%02x:%02x"%(sn[0],sn[1],sn[2],sn[3],sn[4])
      elif Input==3:
         idstr = str(raw_input("Label from the circuit board (starts with DI) "))
         for i in range(16):
            if i<len(idstr):
              x=ord(idstr[i])
            else: x=0
            econ.WriteEnable()
            econ.WriteReg(i,x)
            time.sleep(0.1)
      elif Input==4:
         return
      EEPromMem(econ)
   except ValueError:
      return

def ReadAllRepeat(con, econ):
   inputs = []
   nsamples = 50
   print "The id written on the board is: "+econ.LabelId()
   sn=econ.SerialId()
   print "The Serial Number is : %02x:%02x:%02x:%02x:%02x"%(sn[0],sn[1],sn[2],sn[3],sn[4])
   SerialString = (str(sn[0])+str(sn[1])+str(sn[2])+str(sn[3])+str(sn[4]))
   FileName ="TempsForWId_"+econ.LabelId()+"_SN_"+SerialString.strip()+".txt"
   print repr(FileName)
   with open(FileName.strip(),"w") as f:
      f.write("The id written on the board is: "+econ.LabelId()+"\n")
      f.write("The Serial Number is : %02x:%02x:%02x:%02x:%02x\n"%(sn[0],sn[1],sn[2],sn[3],sn[4]))
      for i in range(8):
         inputs.append([[],0,0])
      for i in range(nsamples):
         for j in range(8):
            SetChannel(con,j+1)
            time.sleep(0.1)
            v = con.ADS124_ReadVolt()
            inputs[j][0].append(v)
            inputs[j][1] = inputs[j][1]+v
      for j in range(8):
         inputs[j][1]/=nsamples
         for n in inputs[j][0]:
            inputs[j][2]+=((n-inputs[j][1])**2)
         inputs[j][2]/=nsamples-1
         inputs[j][2]=inputs[j][2]**0.5
         print ("AIN%d is at %f +- %f volts." %(7-j, inputs[j][1], inputs[j][2]))
         f.write("AIN%d is at %f +- %f volts.\n" %(7-j, inputs[j][1], inputs[j][2]))
   return

def GPIO(con):
   ShowGPIO(con)
   userin = raw_input("Enter command\n")
   try:
      mag = int(userin)
      if (mag<0)|(mag>3):
         print("Input must be between 0 and 3\n")
         GPIO(con)
      elif mag==1:
         pinin = raw_input("Enter GPIO to setup\n")
         valin = raw_input("Enter new GPIO setting (1 for GPIO, 0 for input)\n")
         try: 
            pin = int(pinin)
            val = int(valin)
            if (pin<0)|(pin>3):
               print("Pin not valid")
            elif (val<0)|(val>1):
               print("Setting must be zero or one.")
            else: 
               con.ADS124_SetGPIOType(pin,val)
         except ValueError:
            print("Input not recognized")
         GPIO(con)
      elif mag==2:      
         userin = raw_input("Enter GPIO to change\n")
         valin = raw_input("Enter new value (0 for off, 1 for on)\n")
         try: 
            pin = int(userin)
            val = int(valin)
            if (pin<0)|(pin>3):
               print("Pin not valid")
            elif (val<0)|(val>1):
               print("Setting must be zero or one.")
            else: 
               con.ADS124_SetGPIOValue(pin,val)
         except ValueError:
            print("Input not recognized")      
         GPIO(con)
   except ValueError:
      print("\nInput not recognized")
      GPIO(con)
   return  

def ShowGPIO(con):
   for i in range(0,4):
      gpio = con.ADS124_GetGPIOType(i)
      if gpio == 1:
         print("GPIO %d is set as a GPIO, set to %d" %(i,con.ADS124_GetGPIOValue(i)))
      else:
         print("GPIO %d is set as an input." %(i)) 
   print("\n1: Change GPIO Type\n2: Change GPIO Value\n3: Return\n")
   return


