

class Logger():
    def __init__(self, fileName, active=True):
        self.signature = "(" + fileName + "):"
        self.isActive = active
    def __call__(self, *args):
        if self.isActive:
            outputString = self.signature
            for arg in args:
                outputString += " " + str(arg)
            print(outputString)