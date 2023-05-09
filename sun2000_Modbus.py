import minimalmodbus
import datetime as dt

status_map = { 
    0x0000  : "Idle: Initializing",
    0x0001  : "Idle: Detecting ISO",
    0x0002  : "Idle: Detecting irradiation",
    0x0003  : "Idle: Grid detecting",
    0x0100  : "Starting",
    0x0200  : "On-grid",
    0x0201  : "On-grid: Power limit",
    0x0202  : "On-grid: self derating",
    0x0300  : "Shutdown: Fault",
    0x0301  : "Shutdown: Command",
    0x0302  : "Shutdown: OVGR",
    0x0303  : "Shutdown: Communication disconnected",
    0x0304  : "Shutdown: Power limit",
    0x0305  : "Shutdown: Start manually",
    0x0306  : "Shutdown: DC switch OFF",
    0x0401  : "Grid dispatch: cos(Phi)-P curve",
    0x0402  : "Grid dispatch: Q-U curve",
    0xa000  : "Idle: No irradiation",
    0x0500  : "Spot-check",
    0x0501  : "Spot-checking",
    0x0600  : "Inspecting",
    0x0700  : "AFCI self-check",
    0x0800  : "IV scanning",
    0x0900  : "DC input detection"
    }

registers = [
#   Reg name, address, length, decimals
    ["VoltA"         , 32069, 1, 1],
    ["VoltB"         , 32070, 1, 1],
    ["VoltC"         , 32071, 1, 1],
    ["CurrA"         , 32072, 2, 3],
    ["CurrB"         , 32074, 2, 3],
    ["CurrC"         , 32076, 2, 3],
    ["PeakPower"     , 32078, 2, 3],
    ["ActPower"      , 32080, 2, 3],
    ["PV1Volt"       , 32016, 1, 1],
    ["PV1Curr"       , 32017, 1, 2],
    ["PV2Volt"       , 32018, 1, 1],
    ["PV2Curr"       , 32019, 1, 2],
    ["PV3Volt"       , 32020, 1, 1],
    ["PV3Curr"       , 32021, 1, 2],
    ["PV4Volt"       , 32022, 1, 1],
    ["PV4Curr"       , 32023, 1, 2],
    ["Efficiency"    , 32086, 1, 2],
    ["Temperature"   , 32087, 1, 1],
    ["E-Total"       , 32106, 2, 2],
    ["E-Day"    	 , 32114, 2, 2],
]
Model_Name = [30000,15] # address, length
state = 32089
startup_Time = 32091
shutdown_Time = 32093
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) 

def Setup():
    instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) #usb, com port
    instrument.serial.timeout = 0.6
    instrument.serial.baudrate = 19200
    open = True
    try:
        name = instrument.read_string(Model_Name[0],Model_Name[1])
    except:
        open = False
    return open, name
   
def ReadData():
    success = True
    readOut = []
    readOut.append(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3])
    try:
        status = status_map[instrument.read_register(state)]
        readOut.append(status)
    except:
        success = False
        mode = "Error"
        return [], success, mode

    if status in {"Idle: Initializing", "Idle: Detecting ISO", "Idle: Detecting irradiation", "Idle: Grid detecting", "Starting", "On-grid", "On-grid: Power limit", "On-grid: self derating"}:
        mode = "Running"
    if status == "Idle: No irradiation":
        mode = "Idle"
    else:
        mode = "Other"

    #mode = "Running"  ##Test

    if mode == "Running" or mode == "Other":
        for x in range(0,len(registers)):
            if registers[x][2] == 1:
                try:
                    readData = instrument.read_register(    registeraddress = registers[x][1],
                                                                number_of_decimals = registers[x][3]
                    )
                except:
                    success = False
                    pass
            else:
                try:
                    readData = instrument.read_long(registers[x][1]) / (10 ** registers[x][3]) 
                except:
                    success = False
                    pass
            if registers[x][1]=="Efficiency":
                if mode == "Running":
                    pass
                else:
                    readData = 0
            readOut.append(readData)
        return readOut, success, mode
    else:
        return [], success, mode 
