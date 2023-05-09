import sun2000_Modbus as mod
import sun2000_Logger as log
import sun2000_Export as out
import sys
import time


run = True

def logPrint(text):
    if "--noprint" in sys.argv:
        pass
    else:
        print(text)

#######################################################################################################

logPrint("Sun2000 Readout script")
logPrint("Starting Modbus")
modbusOpen, model = mod.Setup()
if modbusOpen == False:
    logPrint("Failed opening modbus")
    exit(1)
logPrint("Model: \t\t" +  model)

while True:
    output, success, mode = mod.ReadData()
    if "--nolog" in sys.argv:
        pass
    else:
        if success and ((mode == "Running") or (mode == "Other")):
            logPrint(output)
            log.logToCSV(output)
            out.sendToMqtt(output,mod.registers)
            time.sleep(0.5)
        
        elif success and (mode == "Idle"):
            logPrint("Zzzzz")
            out.sendToMqttStandby()
            time.sleep(1)
        
        else: 
            logPrint("FAIL")
            time.sleep(0.5)
