import numpy as np

# Простые модели: Depot, Vehicle, Customer
class Depot:
    def __init__(self, x, y):
        # координаты склада
        self.x = x
        self.y = y

class Vehicle:
    def __init__(self, capacity, cost_per_unit_distance=1.0):
        # вместимость и примерная стоимость
        self.capacity = capacity
        self.cost_per_unit_distance = cost_per_unit_distance

class Customer:
    def __init__(self, id, x, y, demand):
        # id нужен для вывода и индексации
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand