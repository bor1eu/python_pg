import os.path
import tempfile

class File:
    def __init__(self, filename):
        """init file"""
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                pass
        self.filename = filename
        self.position = 0

    def read(self):
        """read data from file"""
        with open(self.filename, 'r') as f:
            data = f.read()
        return data

    def write(self, data):
        """write data to file"""
        with open(self.filename, 'w') as f:
            f.write(data)
        

    def __add__(self, other):
        result_filename = "_".join([os.path.split(self.filename)[-1],os.path.split(other.filename)[-1]])
        result = File(os.path.join(tempfile.gettempdir(),result_filename))
        result_data = self.read() + other.read()
        result.write(result_data)
        return result

    def __getitem__(self, key):
        with open(self.filename, 'r') as f:
            data = list(f)
        return data[key]

    def __str__(self):
        return self.filename

    # def __iter__(self):
    #     return self

    # def __next__(self):
    #     with open(self.filename, 'r') as f:
    #         f.seek(self.current_position)

    #         line = f.readline()
    #         if not line:
    #             self.position = 0
    #             raise StopIteration('EOF')

    #         self.position = f.tell()
    #         return line
              
            


if __name__ == "__main__":
    path_to_file = 'some'
    print(os.path.exists(path_to_file))
    file_obj = File(path_to_file)
    print(os.path.exists(path_to_file))
    print(file_obj.read())
    file_obj.write('some text')
    print(file_obj.read())
    file_obj.write('other text')
    print(file_obj.read())
    file_obj_1 = File(path_to_file + '_1')
    file_obj_2 = File(path_to_file + '_2')
    file_obj_1.write('line 1\n')
    file_obj_2.write('line 2\n')
    new_file_obj = file_obj_1 + file_obj_2
    print(isinstance(new_file_obj, File))
    print(new_file_obj)
    for line in new_file_obj:
        print(ascii(line))  
