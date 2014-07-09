
class DiscreteController:
    def __init__(self, **kwargs):
        if "kp" in kwargs and "kd" in kwargs and "ki" in kwargs and "T" in kwargs:
            kp = kwargs["kp"]
            ki = kwargs["ki"]
            kd = kwargs["kd"]
            T = kwargs["T"]
            self.numerator = [kp+kd/T+ki*T, -kp-2*kd/T, kd/T]
            self.denominator = [1, -1, 0]
        elif "kp" in kwargs and "ki" in kwargs and "T" in kwargs:
            kp= kwargs["kp"]
            ki = kwargs["ki"]
            T = kwargs["T"]
            self.numerator = [kp+ki*T, -kp]
            self.denominator = [1, -1]
        elif "kp" in kwargs:
            kp = kwargs["kp"]
            self.numerator = [kp]
            self.denominator = [1]
        elif "num" in kwargs and "den" in kwargs:
            self.numerator = num
            self.denominator = den
        self.inputValues = [0]*len(self.numerator)
        self.outputValues = [0]*len(self.denominator)


    def inputValue(self, value):
        inLen = len(self.inputValues)
        for i in range(1, inLen):
            self.inputValues[inLen-i] = self.inputValues[inLen-i-1]
        self.inputValues[0] = value

        ouLen = len(self.outputValues)
        for i in range(1, ouLen):
            self.outputValues[ouLen-i] = self.outputValues[ouLen-i-1]

        outputValue = 0
        for i in range(0,inLen):
            outputValue+=self.inputValues[i]*self.numerator[i];

        for i in range(1,ouLen):
            outputValue += self.outputValues[i]*-self.denominator[i]
        self.outputValues[0] = outputValue

        return outputValue
