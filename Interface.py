import ADS124_control
import time
import Interface_functions as f

"""Script for interacting with the ADS124_S08 control chip"""

done = False
ready = False
con = ADS124_control.ADS124()
filename = "default.txt"
nsamples = 100
delay = 0.01

while(not done):
   if not ready: 
      f.setup(con)
      f.commands()
      f.status(con)
      ready = True
   command = input('Enter a command: ')
   if command == "0": done = True
   elif command == "1": f.SetPosIn(con)
   elif command == "2": f.SetNegIn(con)
   elif command == "3": f.SetExSc(con)
   elif command == "4": f.SetExMag(con)
   elif command == "5": f.SetVRef(con)
   elif command == "6": f.SetVBias(con)
   elif command == "7": f.ReadSample(con)
   elif command == "8": f.RSetup(con, filename, nsamples, delay)
   elif command == "9": f.ReadSamples(con, filename, nsamples, delay)
   elif command == "c": f.commands()
   elif command == "s": f.status(con)
   elif command == "r": f.reset(con)
   elif command == "l": f.load(con)
   elif command == "sv": f.save(con)
   else : print "Command not recognized"

f.stop(con)



