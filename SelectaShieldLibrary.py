import RPi.GPIO as GPIO
import time

nX1EN, nX2EN, nX3EN = 2, 3, 4
LED_WRITE, MOT_WRITE = 17, 27

D0, D1, D2, D3, D4, D5 = 7, 8, 25, 24, 23, 18
DataBus = (D0, D1, D2, D3, D4, D5)

def setDataDir(DataDirection):
    global DataBus
    for DataPin in DataBus:
        GPIO.setup(DataPin, DataDirection, initial = GPIO.LOW)
   
def readData():
    global DataBus
    Data = []
    for Bit in range(6):
        Data[Bit] = list(DataBus)[Bit]
    return Data

class SelectaPi:
    def __init__(self, HomeAllMotors=True, DrinkNames=("", "", "", "", "", "")):
        self.SlotNames = DrinkNames
        
        self.FULL = True
        self.EMPTY = False
        
        self.ENCODER_BUTTON = nX1EN
        self.LEVEL_BUTTON = nX2EN
        self.SELECT_BUTTON = nX3EN
        
        self.ON = GPIO.HIGH
        self.OFF = GPIO.LOW
        
        GPIO.setmode(GPIO.BCM)
        
        setDataDir(GPIO.IN)
        for EnablePin in (nX1EN, nX2EN, nX3EN):
            GPIO.setup(EnablePin, GPIO.OUT, initial = GPIO.HIGH)
        for WritePin in (LED_WRITE, MOT_WRITE)
            GPIO.setup(WritePin, GPIO.OUT, initial = GPIO.LOW)
        
        #Turn off all LEDs
        setLEDs((0, 0, 0, 0, 0, 0))
        #Turn off all Motors
        setMotors((0, 0, 0, 0, 0, 0))
        
        if (HomeAllMotors == True):
            for MotorNum in range(6):
                if(readButton(self.ENCODER_BUTTON, MotorNum) == self.ON):
                    setMotor(self.ON, MotorNum)
                    time.sleep(0.01)
                    
                    while(readButton(self.ENCODER_BUTTON, MotorNum) == self.ON):
                        time.sleep(0.01)
                    
                    setMotor(self.OFF, MotorNum)
    
    def getSlotName(self, SlotNumber):
        if (SlotNumber >= 1) and (SlotNumber <= 6):
            return list(self.SlotNames)[(SlotNumber - 1)]
        else:
            return ""
    
    def getSlotNumber(self, SlotName):
        SlotNumber = 1
        for _SlotName in self.SlotNames:
            if _SlotName == SlotName:
                return SlotNumber
            else:
                SlotNumber += 1
        return 0
    
    def setSlotName(self, SlotNumber, SlotName):
        if (SlotNumber >= 1) and (SlotNumber <= 6):
            SlotNamesList = list(self.SlotNames)
            SlotNamesList[(SlotNumber - 1)] = SlotName
            self.SlotNames = tuple(SlotNamesList)
    
    def checkSlotLevels(self):
        GPIO.output(nX2EN, GPIO.LOW)
        
        Data = readData()
        
        GPIO.output(nX2EN, GPIO.HIGH)
        
        return Data
    
    def checkSlotLevel(self, Slot):
        if str(type(Slot)) == "<class 'str'>":
            Slot = getSlotNumber(Slot)
        if (str(type(Slot)) == "<class 'int'>") and ((SlotNumber >= 1) and (SlotNumber <= 6)):
            return checkSlotLevels()[(Slot - 1)]
    
    def readButtons(self, SwitchFunction):
        GPIO.output(SwitchFunction, GPIO.LOW)
        
        Data = readData()
        
        GPIO.output(SwitchFunction, GPIO.HIGH)
        
        return Data
    
    def readButton(self, SwitchFunction, ButtonNum):
        return readButtons(SwitchFunction)[(ButtonNum - 1)]
    
    def setLEDs(self, LEDValues):
        setDataDir(GPIO.OUT)
        
        if (str(type(LEDValues)) == "<class 'tuple'>"):
            LEDValues = list(LEDValues)
        
        for Bit in range(6):
            GPIO.output(list(DataBus)[Bit], LEDValues[Bit])
        
        GPIO.output(LED_WRITE, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(LED_WRITE, GPIO.LOW)
        time.sleep(0.001)
        
        for Bit in range(6):
            GPIO.output(list(DataBus)[Bit], self.OFF)
        
        setDataDir(GPIO.IN)
    
    def setLED(self, LEDValue, LEDNum):
        setDataDir(GPIO.OUT)
        
        GPIO.output(list(DataBus)[(LEDNum - 1)], LEDValue)
        
        GPIO.output(LED_WRITE, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(LED_WRITE, GPIO.LOW)
        time.sleep(0.001)
        
        GPIO.output(list(DataBus)[(LEDNum - 1)], self.OFF)
        
        setDataDir(GPIO.IN)
    
    def setMotors(self, MotorValues):
        setDataDir(GPIO.OUT)
        
        if (str(type(MotorValues)) == "<class 'tuple'>"):
            MotorValues = list(MotorValues)
        
        for Bit in range(6):
            GPIO.output(list(DataBus)[Bit], MotorValues[Bit])
        
        GPIO.output(MOT_WRITE, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(MOT_WRITE, GPIO.LOW)
        time.sleep(0.001)
        
        for Bit in range(6):
            GPIO.output(list(DataBus)[Bit], self.OFF)
        
        setDataDir(GPIO.IN)
    
    def setMotor(self, MotorValue, MotorNum):
        setDataDir(GPIO.OUT)
        
        GPIO.output(list(DataBus)[(MotorNum - 1)], MotorValue)
        
        GPIO.output(MOT_WRITE, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(MOT_WRITE, GPIO.LOW)
        time.sleep(0.001)
        
        GPIO.output(list(DataBus)[(MotorNum - 1)], self.OFF)
        
        setDataDir(GPIO.IN)
    
    def ExecuteMotorCycles(self, Cycles, MotorNum):
        for cycleNum in range(Cycles):
            setMotor(self.ON, MotorNum)
            time.sleep(0.01)
            
            while(readButton(self.ENCODER_BUTTON, MotorNum) == self.ON):
                time.sleep(0.01)
            
            setMotor(self.OFF, MotorNum)