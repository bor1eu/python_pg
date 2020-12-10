class Value:
    def __init__(self, comms=None):
        # if comms is None:
        #     comms = 0
        # self.commission = comms
        self.value = None

    def __get__(self, obj, obj_type):
        return self.value

    def __set__(self, obj, value):
        self.value = int(value * (1 - obj.commission))
        # print(self.commission)

    # @staticmethod
    # def setComms(self, value):
    #     self.commission = value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
    
        

if __name__ == "__main__":
    new_account = Account(0.1)
    new_account.amount = 100

    print(new_account.amount)
    new_account.amount = 200
    print(new_account.amount)
    print(type(new_account.amount))