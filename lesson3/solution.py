import os

class FileReader:
    def __init__(file):
        self.file = file

    def read():
        try:
            with open(self.file, 'r') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return ''
    


if __name__ == "__main__":
    pass
