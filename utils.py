import numpy as np
import matplotlib.pyplot as plt

def euclidean_distance(a, b):
    # простая евклидова метрика
    return np.hypot(a[0]-b[0], a[1]-b[1])

def calculate_distance_matrix(depot, customers):
    n = len(customers)
    mat = np.zeros((n+1, n+1))
    pts = [(depot.x, depot.y)] + [(c.x, c.y) for c in customers]
    for i in range(n+1):
        for j in range(n+1):
            mat[i][j] = euclidean_distance(pts[i], pts[j])
    return mat

def plot_routes(depot, customers, routes, title="Маршруты доставки"):
    # быстрый график маршрутов
    plt.figure(figsize=(9,7))
    plt.scatter(depot.x, depot.y, c='red', s=160, marker='s', label='Depot')
    for cust in customers:
        plt.scatter(cust.x, cust.y, c='blue', s=40)
        plt.text(cust.x+0.2, cust.y+0.2, f"C{cust.id}", fontsize=8)

    colors = ['green','orange','purple','brown','pink','gray','olive','cyan']
    for i, route in enumerate(routes):
        if not route: continue
        col = colors[i % len(colors)]
        # депо -> first
        plt.plot([depot.x, customers[route[0]].x],[depot.y, customers[route[0]].y], c=col)
        for k in range(len(route)-1):
            p1 = customers[route[k]]
            p2 = customers[route[k+1]]
            plt.plot([p1.x,p2.x],[p1.y,p2.y], c=col)
        last = customers[route[-1]]
        plt.plot([last.x, depot.x],[last.y, depot.y], c=col)

    plt.title(title)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()