class SplitStart:
    """Event used when the separation of a request starts"""
    
    NAME = "SPLIT_START"

    def __init__(self, directory):
        self.directory = directory

    def serialize(self):
        return {
            "name": self.NAME,
            "data": {
                "directory": self.directory
            }
        }

    @staticmethod
    def deserialize(serializedHook):
        data = serializedHook["data"]
        directory = data["directory"] if "directory" in data else None

        return SplitStart(directory)