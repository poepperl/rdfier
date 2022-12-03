import os

def getUncoPath():
    TOS_PATH = os.path.dirname(__file__)
    return TOS_PATH[:30]

UNCO_PATH = getUncoPath()