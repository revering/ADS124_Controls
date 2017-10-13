import ADS124_RPiBasic
import core 
import time
import tool_functions as f
import EEPROM
"""Script for interacting with the ADS124_S08 control chip"""

done = False
ready = False
connection = ADS124_RPiBasic.ADS124_RPiBasic()
con = core.ADS124(connection)

ECON = EEPROM.EEPROM_RPiBasic()
econ = core.EEPROM(ECON)

filename = "default.txt"
nsamples = 100
delay = 0.1

while(not done):
   if not ready: 
      f.setup(con)
      print ""
      f.commands()
      print ""
      f.status(con)
      ready = True
   try:
      command = raw_input('\nEnter a command: ')
      print ""
      if command == "0" or command == "q" : done = True
      elif command == "1": f.SetPosIn(con)
      elif command == "2": f.SetNegIn(con)
      elif command == "3": f.SetExSc(con)
      elif command == "4": f.SetExMag(con)
      elif command == "5": f.SwitchIntRef(con)
      elif command == "6": f.SetVRef(con)
      elif command == "7": f.SetVBias(con)
      elif command == "8": f.ReadSample(con)
      elif command == "9": 
         settings = f.RSetup(con, filename, nsamples, delay)
         filename = settings[0]
         nsamples = settings[1]
         delay = settings[2]
      elif command == "10": f.ReadSamples(con, filename, nsamples, delay)
      elif command == "c" or command == "h" : f.commands()
      elif command == "s": f.status(con)
      elif command == "r": f.reset(con)
      elif command == "l":
         preset = f.load(con)
         filename = preset[0]
         nsamples = preset[1]
         delay = preset[2]
      elif command == "sv": f.save(con, filename, nsamples, delay)
      elif command == "ch": 
         RTD = raw_input("Enter RTD to read from: ")
         try:
            num = int(RTD)
            if 0<num<25:
               f.SetChannel(con,num)
            else:
               print "RTD entered must be an integer from 1 to 24"
         except ValueError:
            print("RTD entered must be an integer from 1 to 24")     
      elif command == "t": f.ReadAll(con)
      elif command == "tr" : f.ReadAllRepeat(con,econ)
      elif command == "g" : f.GPIO(con)
      elif command == "EEPROM": f.EEPromMem(econ)
      else : print "Command not recognized"
   except KeyboardInterrupt:
      print "\nClosing"
      done = True     
f.stop(con)



