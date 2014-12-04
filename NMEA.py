class NMEA:
    @staticmethod
    def createData103(code, mode, rate):
        returnString = "$PSRF103,"+code+","+mode+","+rate+",01"
        charArray = list(returnString)
        byteXor=0
        for char in charArray:
            byteXor ^=ord(char)

        returnString += "*"+"%02X" % byteXor+"\r\n"+chr(0) 
        return returnString
