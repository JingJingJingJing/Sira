from enum import Enum

class Token_Type(Enum):
    identify = "identify"
    reserved = "reserved"
    number = "number"
    symbol = "symbol"

class Token():
    def __init__(self, value, type):
        self.value = value
        self.type = type