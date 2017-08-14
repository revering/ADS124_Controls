import ADS124_RPiBasic
import core 
import time

"""
Script which measures 100 samples over ten seconds, then reports the average and standard deviation.

Better to use "read samples" in tool, as this lacks ability to easily change and save settings.
"""
con = ADS124_RPiBasic.ADS124_RPiBasic()
x = core.ADS124(con)

#x.ADS124_RegDump()
#x.ADS124_Setup()
x.ADS124_SetIDACMag(1000)
x.ADS124_DisableGain()
x.ADS124_SetPosInput(4)
x.ADS124_SetNegInput(1)
x.ADS124_SetIDAC1(4)
x.ADS124_SetVBias(1,1)
x.ADS124_EnableIntRef()
x.ADS124_RefSelect(2)
x.ADS124_Start()
volts = []
sum = 0.0
samples = 100

for a in range(0,samples):
    volts.append(x.ADS124_ReadVolt())
    time.sleep(0.1)
    
for n in volts:
    sum += n

avg = sum/samples
stddev = 0.0

for m in volts:
    stddev+=((m-avg)**2)

stddev /= samples-1
stddev = stddev**0.5

print avg
print stddev

