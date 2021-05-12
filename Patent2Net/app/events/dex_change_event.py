
class DexChangeEvent:
    """
    general event when the dex is updated. 
    This event must be called if no other event is called to describe a modification of the dex
    """

    NAME = "DEX_CHANGE_EVENT"

    def __init__(self, directory, key, prevData, newData):
        self.directory = directory
        self.key = key
        self.prevData = prevData
        self.newData = newData
        
    def serialize(self):
        return {
            "name": self.NAME,
            "data": {
                "directory": self.directory,
                "key": self.key,
                "prevData": self.prevData,
                "newData": self.newData
            }
        }

    @staticmethod
    def deserialize(serializedHook):
        data = serializedHook["data"]
        directory = data["directory"] if "directory" in data else None
        key = data["key"] if "key" in data else None
        prevData = data["prevData"] if "prevData" in data else None
        newData = data["newData"] if "newData" in data else None

        return DexChangeEvent(directory, key, prevData, newData)
 