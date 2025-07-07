import matplotlib.pyplot as plt

def logistic_map(r, x0, steps):
    results = []
    x = x0
    for _ in range(steps):
        x = r * x * (1 - x)
        results.append(x)
    return results

def plot_chaos(start=2.5, end=4.0, step=0.005):
    x0 = 0.5
    steps = 100
    for r in [round(r, 3) for r in frange(start, end, step)]:
        values = logistic_map(r, x0, steps)[-50:]  # plot last 50 values
        plt.plot([r]*len(values), values, ',k', alpha=0.25)
    plt.title("Logistic Map Bifurcation Diagram")
    plt.xlabel("r")
    plt.ylabel("x")
    plt.show()

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

plot_chaos()
