import os
import csv
import re

class FileReader:
    def __init__(self, file):
        self.file = file

    def read(self):
        try:
            with open(self.file, 'r') as file:
                return file.read()
            
        except IOError:
            return ""
    
class CarBase:
    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.carrying = float(carrying)
        self.photo_file_name = photo_file_name

    def get_photo_file_ext(self):
        file_ext = os.path.splitext(self.photo_file_name)[-1]
        return file_ext

class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        car_type = "car"
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        car_type = "truck"
        super().__init__(car_type, brand, photo_file_name, carrying)
        try:
            self.body_length, self.body_width, self.body_height = [float(i) for i in body_whl.split('x')]
        except ValueError:
            self.body_length, self.body_width, self.body_height = [0.0,0.0,0.0]
    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        car_type = "spec_machine"
        super().__init__(car_type, brand, photo_file_name, carrying)
        self.extra = extra


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        valid_ext = re.compile(r'^.+(\.((jpg)|(jpeg)|(png)|(gif)))$')
        for row in reader:
            while len(row) < 7:
                row.append('')
            car_type, brand, passenger_seats_count, photo_file_name, body_whl, carrying, extra = row
            if car_type == '' or photo_file_name == '' or brand == '' or carrying == '':
                continue
            if not (valid_ext.search(photo_file_name)):
                continue
            if car_type == 'car' and str.isdigit(passenger_seats_count) and body_whl == '' and extra == '':
                car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
            elif car_type == 'truck' and passenger_seats_count == '' and extra == '':
                car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
            elif car_type == 'spec_machine' and extra != '' and body_whl == '' and passenger_seats_count == '':
                car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))
    return car_list

    

if __name__ == "__main__":
    # reader = FileReader('ttt.txt')
    # texxt = reader.read()
    # print(texxt)
    car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
    print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count, sep='\n')
    truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
    print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length, truck.body_width, truck.body_height, sep='\n')
    spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
    print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying, spec_machine.photo_file_name, spec_machine.extra, sep='\n')
    print(spec_machine.get_photo_file_ext())
    cars = get_car_list('lesson3/coursera_week3_cars.csv')
    print(len(cars))
    for car in cars:
        print(type(car))
    print(cars[0].passenger_seats_count)
    print(cars[1].get_body_volume())

