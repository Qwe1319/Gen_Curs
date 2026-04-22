from models import Depot, Vehicle, Customer
from genetic_algorithm import GeneticAlgorithm
from utils import plot_routes
import random

def input_depot():
    print("Введите координаты депо (x y):")
    x,y = map(float, input().split())
    return Depot(x,y)

def input_customers():
    customers=[]
    n = int(input("Введите количество клиентов: "))
    for i in range(n):
        print(f"Клиент {i}: введите x y demand")
        x,y,d = map(float, input().split())
        customers.append(Customer(i, x, y, int(d)))
    return customers

def input_vehicles():
    vs=[]
    m = int(input("Введите количество ТС: "))
    for i in range(m):
        cap = float(input(f"Грузоподъемность ТС {i+1}: "))
        vs.append(Vehicle(int(cap)))
    return vs

def input_ga_params():
    print("Параметры ГА (population_size generations mutation_rate crossover_rate) — Enter для дефолта:")
    s = input().strip()
    if not s:
        return 100,500,0.1,0.8
    a = s.split()
    return int(a[0]), int(a[1]), float(a[2]), float(a[3])

def main():
    print("Запуск — VRP с генетикой")
    depot = input_depot()
    customers = input_customers()
    vehicles = input_vehicles()
    pop,gens,mut,cross = input_ga_params()

    print(f"Клиентов: {len(customers)}, ТС: {len(vehicles)}")

    ga = GeneticAlgorithm(depot, customers, vehicles, pop, gens, mut, cross)
    best, dist = ga.evolve()

    print("\nРешение:")
    for i, r in enumerate(best):
        if r:
            load = sum(customers[c].demand for c in r)
            print(f"ТС {i+1} ({load}/{vehicles[i].capacity}): {[f'C{c}' for c in r]}")
        else:
            print(f"ТС {i+1}: -")
    print(f"Общая дистанция: {dist:.2f}")
    plot_routes(depot, customers, best, title=f"Маршруты (d={dist:.2f})")

if __name__ == '__main__':
    main()