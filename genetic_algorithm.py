import numpy as np
import random
from utils import calculate_distance_matrix


class GeneticAlgorithm:
    # простой ГА для VRP
    def __init__(self, depot, customers, vehicles, population_size=100, generations=500, mutation_rate=0.1, crossover_rate=0.8):
        self.depot=depot
        self.customers=customers
        self.vehicles=vehicles
        self.num_customers=len(customers)
        self.num_vehicles=len(vehicles)
        self.population_size=population_size
        self.generations=generations
        self.mutation_rate=mutation_rate
        self.crossover_rate=crossover_rate
        self.distance_matrix=calculate_distance_matrix(depot, customers)

    def initialize_population(self):
        pop=[]
        for _ in range(self.population_size):
            routes=[[] for _ in range(self.num_vehicles)]
            ids=list(range(self.num_customers))
            random.shuffle(ids)
            for cid in ids[:]:
                loads=[sum(self.customers[c].demand for c in r) for r in routes]
                v_idx = int(np.argmin(loads))
                if loads[v_idx] + self.customers[cid].demand <= self.vehicles[v_idx].capacity:
                    routes[v_idx].append(cid)
                    ids.remove(cid)
                else:
                    for v in range(self.num_vehicles):
                        if loads[v] + self.customers[cid].demand <= self.vehicles[v].capacity:
                            routes[v].append(cid)
                            ids.remove(cid)
                            break
            pop.append(routes)
        return pop

    def fitness(self, routes):
        total=0
        for r in routes:
            if not r: continue
            total += self.distance_matrix[0][r[0]+1]
            for i in range(len(r)-1):
                total += self.distance_matrix[r[i]+1][r[i+1]+1]
            total += self.distance_matrix[r[-1]+1][0]
        return total

    def select_parents(self, pop, fits):
        # турнир: берём 3 и выбираем лучшего
        def t():
            cand = random.sample(list(zip(pop, fits)), 3)
            return min(cand, key=lambda x: x[1])[0]
        return t(), t()

    def crossover(self, p1, p2):
        child=[]
        for i in range(self.num_vehicles):
            a=p1[i]
            b=p2[i]
            if not a or not b:
                child.append(a[:] if a else b[:])
                continue
            s=random.randint(0, len(a)-1)
            e=random.randint(s, len(a)-1)
            seg=a[s:e+1]
            rem=[c for c in b if c not in seg]
            child.append(seg+rem)
        return child

    def mutate(self, routes):
        for r in routes:
            if len(r)>1 and random.random() < self.mutation_rate:
                i,j = random.sample(range(len(r)),2)
                r[i], r[j] = r[j], r[i]
        return routes

    def repair_solution(self, routes):
        # если что-то сломалось по вместимости — перераспределяем
        all_c = set()
        for r in routes:
            all_c.update(r)
        new_routes=[[] for _ in range(self.num_vehicles)]
        for cid in all_c:
            for v in range(self.num_vehicles):
                load = sum(self.customers[c].demand for c in new_routes[v])
                if load + self.customers[cid].demand <= self.vehicles[v].capacity:
                    new_routes[v].append(cid)
                    break
        return new_routes

    def evolve(self):
        pop = self.initialize_population()
        best=None
        best_fit=float('inf')
        for gen in range(self.generations):
            fits = [self.fitness(ind) for ind in pop]
            new_pop=[]
            best_idx = int(np.argmin(fits))
            new_pop.append(pop[best_idx])
            if fits[best_idx] < best_fit:
                best_fit = fits[best_idx]
                best = pop[best_idx]
            while len(new_pop) < self.population_size:
                p1,p2 = self.select_parents(pop, fits)
                if random.random() < self.crossover_rate:
                    child = self.crossover(p1,p2)
                else:
                    child = [r[:] for r in p1]
                child = self.mutate(child)
                child = self.repair_solution(child)
                new_pop.append(child)
            pop = new_pop
            if gen % 50 == 0:
                print(f"Поколение {gen}: Лучший фитнес = {best_fit}")
        return best, best_fit