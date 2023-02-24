#---------------------------------------------------------------------------
# Module ----- gstalmem
# Project ---- GSTAL interpreter with debugger
# Developer -- Bryan Crawley
# Version ---- v0.1
#
# This class is for the data memory values.
#---------------------------------------------------------------------------

import struct
import sys


class DataCell:
    
    def __init__(self, value):
        if type(value) is int:
            trimmed = value & 0xFFFFFFFFFFFFFFFF
            self._content = trimmed.to_bytes(8, byteorder="big", signed=False)
        elif type(value) is float:
            self._content = struct.pack("!d", value)
        else:
            raise TypeError("'" + type(value).__name__ + "' object not a valid " + type(self).__name__ + " value")
    
    def int(self):
        value = int.from_bytes(self._content, byteorder="big", signed=True)
        return value

    def float(self):
        value = struct.unpack("!d", self._content)[0]
        return value
    
    def char(self): 
        value = chr(self.int())
        return value
    
    def bin(self): 
        return bin(int.from_bytes(self._content, byteorder=sys.byteorder))[2:]

    def hex(self): 
        return self._content.hex()
    

class CodeCell:

    _dictionary = { "ADI":(1,None),  "SBI":(2,None),  "MIL":(3,None),
                    "DVI":(4,None),  "NGI":(5,None),
                    
                    "ADF":(6,None),  "SBF":(7,None),  "MLF":(8,None),
                    "DVF":(9,None), "NGF":(10,None),
                    
                   "EQI":(11,None), "NEI":(12,None), "LTI":(13,None),
                   "LEI":(14,None), "GTI":(15,None), "GEI":(16,None),
                    
                   "EQF":(17,None), "NEF":(18,None), "LTF":(19,None),
                   "LEF":(20,None), "GTF":(21,None), "GEF":(22,None),
                    
                   "FTI":(23,None), "ITF":(24,None),
                    
                   "PTI":(25,None), "PTF":(26,None), "PTC":(27,None),
                   "PTL":(28,None), "INI":(29,None), "INF":(30,None),
                    
                   "LLI":(31,"i"),  "LLF":(32,"f"),  "ISP":(33,"n"),
                   "DSP":(34,"n"),  "STO":(35,None), "STM":(36,None),
                   "LOD":(37,None),
                    
                   "LAA":(38,"n"),  "LRA":(39,"n"),  "JMP":(40,"n"),
                   "JPF":(41,"n"),  "PAR":(42,"n"),  "CAL":(43,"n"),
                   "RET":(44,None), "NOP":(45,None), "HLT":(46,None)}

    def __init__(self, opcode, operand):
        if opcode not in self._dictionary:
            print("ASDFKJL;"); return
        else:
            opcode_value = self._dictionary[opcode]
            opcode_number = opcode_value[0]
            self._opcode = (opcode_number & 0xFF).to_bytes(1, byteorder="big", signed=False)
            if operand is None:
                self._operand = None
                return
            else:    
                self._operand = DataCell(operand)
                return
 