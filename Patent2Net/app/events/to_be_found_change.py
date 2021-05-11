
class ToBeFoundChange:
    """Event used when the number of resources available for a request has been retrieved and recorded"""

    NAME = "TO_BE_FOUND_CHANGE"

    def __init__(self, directory, need_spliter, amount):
        self.directory = directory
        self.need_spliter = need_spliter
        self.amount = amount
        
    def serialize(self):
        return {
            "name": self.NAME,
            "data": {
                "directory": self.directory,
                "need_spliter": self.need_spliter,
                "amount": self.amount
            }
        }

    @staticmethod
    def deserialize(serializedHook):
        data = serializedHook["data"]
        directory = data["directory"] if "directory" in data else None
        need_spliter = data["need_spliter"] if "need_spliter" in data else None
        amount = data["amount"] if "amount" in data else None

        return ToBeFoundChange(directory, need_spliter, amount)
 