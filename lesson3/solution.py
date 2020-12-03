import os

class FileReader:
    def __init__(self, file):
        self.file = file

    def read(self):
        try:
            with open(self.file, 'r') as file:
                return file.read()
            
        except IOError:
            return ""
    


if __name__ == "__main__":
    reader = FileReader('ttt.txt')
    texxt = reader.read()
    print(texxt)
