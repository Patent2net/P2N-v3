
class ProgressHook:
    
    NAME = "PROGRESS"

    def __init__(self, directory, service, value, max_value):
        self.directory = directory
        self.service = service
        self.value = value
        self.max_value = max_value
        
    def serialize(self):
        return {
            "name": self.NAME,
            "data": {
                "directory": self.directory,
                "service": self.service,
                "value": self.value,
                "max_value": self.max_value
            }
        }

    @staticmethod
    def deserialize(serializedHook):

        if "name" in serializedHook and serializedHook["name"] == ProgressHook.NAME and "data" in serializedHook:
            data = serializedHook["data"]
            directory = data["directory"] if "directory" in data else None
            service = data["service"] if "service" in data else None
            value = data["value"] if "value" in data else None
            max_value = data["max_value"] if "max_value" in data else None

            return ProgressHook(directory, service, value, max_value)
            
        return None

def test():
    print("test")