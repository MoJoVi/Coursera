"""
Задача:
Создать иерархию классов для сортировки данных об автомобилях.
У любого объекта есть обязательный атрибут car_type.
Он означает тип объекта и может принимать одно из значений:
car, truck, spec_machine.

Также у любого объекта из иерархии есть фото в виде имени файла
— обязательный атрибут photo_file_name.

В базовом классе нужно реализовать метод get_photo_file_ext
для получения расширения файла (“.png”, “.jpeg” и т.д.) с фото.
Расширение файла можно получить при помощи os.path.splitext.

Для грузового автомобиля необходимо разделить характеристики кузова
на отдельные составляющие body_length, body_width, body_height.
Разделитель — латинская буква x. Характеристики кузова могут
быть заданы в виде пустой строки, в таком случае все составляющие
равны 0. Обратите внимание на то, что характеристики кузова должны быть
вещественными числами.

Также для класса грузового автомобиля необходимо реализовать метод
get_body_volume, возвращающий объем кузова в метрах кубических.

Все обязательные атрибуты для объектов Car, Truck и SpecMachine
перечислены в таблице ниже, где 1 - означает, что атрибут
обязателен для объекта, 0 - атрибут должен отсутствовать.

Атрибуты \ Типы машин    Car	    Truck	   SpecMachine
car_type	              1	          1	           1
photo_file_name	          1           1	           1
brand	                  1	          1	           1
carrying	              1           1	           1
passenger_seats_count	  1	          0	           0
body_width	              0	          1	           0
body_height	              0	          1	           0
body_length	              0	          1	           0
extra	                  0	          0	           1

Далее необходимо реализовать функцию, на вход которой подается
имя файла в формате csv. Файл содержит данные аналогичные строкам
из таблицы. Вам необходимо прочитать этот файл построчно при помощи
модуля стандартной библиотеки csv. Затем проанализировать строки и
создать список нужных объектов с автомобилями и специальной техникой.
Функция должна возвращать список объектов.

У каждого объекта из иерархии должен быть свой набор атрибутов и методов.
У класса легковой автомобиль не должно быть метода get_body_volume в
отличие от класса грузового автомобиля.

Функция, которая парсит строки входного массива, должна
называться get_car_list.
"""


import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]

    def __str__(self):
        """
        Перегрузил метод __str__ для удобства отображения, хоть этого и нет
        в задании, но так намного проще отображать данные о машинах
        :return:
        """
        res_string = ''
        for key, value in self.__dict__.items():
            res_string += f'{key}: {value}, '
        return res_string[:-2] + '.\n'


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)

        if body_whl:
            self.body_length, self.body_width, self.body_height \
                = [float(whl) for whl in body_whl.split('x')]
        else:
            self.body_length = self.body_width = self.body_height = 0.0

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra


def sorting_args(args, ix):
    return [args[0], args[2], float(args[4]), args[ix]]


def get_car_list(csv_filename):
    cars = {
        'car': [1, Car],
        'truck': [3, Truck],
        'spec_machine': [5, SpecMachine]
    }
    car_list = []

    try:
        with open(csv_filename, encoding='utf8') as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)  # пропускаем заголовок
            for row in reader:
                if [elem for elem in row if elem]:  # Проверяем не является ли список пустым
                    model = row.pop(0)
                    args = sorting_args(row, cars[model][0])  # Сортируем аргументы
                    car_list.append(cars[model][1](*args))

    except FileNotFoundError:
        return None
    else:
        return car_list


if __name__ == '__main__':
    cars = get_car_list('coursera_week3_cars.csv')
    for car in cars:
        print(car)
