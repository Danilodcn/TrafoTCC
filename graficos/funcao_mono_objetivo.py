import math
import numpy as np
import matplotlib.pyplot as plt

def f1():
    x = np.array([1, 1.5, 3, 5, 6, 7])
    y = np.array([600, 40, 500, 3, 13, 38])

    xx = np.linspace(0, 7.3, 10000)
    z = np.polyfit(x, y, 6)
    plt.plot(xx, np.polyval(z, xx), "b-")

    plt.plot(x, y, "ro")

    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    # plt.style.use("classic")

    plt.show()

def f2(fig, ax):
    r = [2, 2.5, 3, 3.4, 4]
    xx = np.linspace(min(r)*0.93, max(r)*1.04, 10000)
    p = np.poly1d(1)
    for r_i in r:
        # import ipdb; ipdb.set_trace()
        
        p *= np.poly1d([1, -r_i])
    p = np.polyint(p)
    p = p + np.poly1d(100)
    # fig, ax = plt.subplots()
    plt.plot(xx, np.polyval(p, xx), "b", label="função objetivo")
    plt.plot(r, np.polyval(p, r), "ro", label="máximos e mínimos")
    # plt.style.use("classic")
    print(p)

    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    # plt.xlim([1.8, 7])
    # plt.ylim([100, -100])
    
    plt.legend()
    x_min = 4

    plt.annotate('mínimo global', xy=(x_min, p(x_min)), xytext=(3.3, p(x_min)),
                arrowprops=dict(
                    arrowstyle="->"
                    ))

    x_min_ = 2

    plt.annotate('mínimo local', xy=(x_min_, p(x_min_)), xytext=(2.2, p(x_min_)*0.999),
                arrowprops=dict(
                    arrowstyle="->"
                    ))

    x_min_ = 3

    plt.annotate('mínimo local', xy=(x_min_, p(x_min_)), xytext=(2.5, p(x_min_)*0.999),
                arrowprops=dict(
                    arrowstyle="->"
                    ))

    x_max = 2.5

    plt.annotate('máximo global', xy=(x_max, p(x_max)), xytext=(1.8, p(x_max)),
                arrowprops=dict(
                    arrowstyle="->"
                    ))
    
    x_max = 3.4

    plt.annotate('máximo local', xy=(x_max, p(x_max)), xytext=(3.6, p(x_max)*1.0005),
                arrowprops=dict(
                    arrowstyle="->"
                    ))
    # ax.set_xticks(r)
    # ax.set_yticks([])

    


def f3(fig, ax):
    r = [2, 2.5, 3, 3.4, 4]
    xx = np.linspace(min(r)*0.93, max(r)*1.04, 10000)
    p = np.poly1d(1)
    for r_i in r:
        # import ipdb; ipdb.set_trace()
        
        p *= np.poly1d([1, -r_i])
    d = p
    p = np.polyint(p)
    p = p + np.poly1d(100)

    # i = list(xx).index(2.8005640564056407)
    plt.plot(xx, np.polyval(p, xx), "b", label="função objetivo")
    plt.plot(r, np.polyval(p, r), "ro", label="máximos e mínimos")
    # plt.style.use("classic")
    print(p)

    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    
    plt.legend()
    x_min = 4

    plt.annotate('mínimo global', xy=(x_min, p(x_min)), xytext=(3.3, p(x_min)),
                arrowprops=dict(
                    arrowstyle="->"
                    ))

    x_min_ = 2

    plt.annotate('mínimo local', xy=(x_min_, p(x_min_)), xytext=(2.2, p(x_min_)*0.999),
                arrowprops=dict(
                    arrowstyle="->"
                    ))

    x_min_ = 3

    plt.annotate('mínimo local', xy=(x_min_, p(x_min_)), xytext=(2.5, p(x_min_)*0.999),
                arrowprops=dict(
                    arrowstyle="->"
                    ))

    x_max = 2.5

    plt.annotate('máximo global', xy=(x_max, p(x_max)), xytext=(1.8, p(x_max)),
                arrowprops=dict(
                    arrowstyle="->"
                    ))
    
    x_max = 3.4

    plt.annotate('máximo local', xy=(x_max, p(x_max)), xytext=(3.6, p(x_max)*1.0005),
                arrowprops=dict(
                    arrowstyle="->"
                    ))
    



    X = [2.7, 3.3]
    Y = np.array([1, -1]) * 2
    for x, y in zip(X, Y):
        v1 = np.array([1, d(x)]) 
        v1 /= np.linalg.norm(v1)
        v1 *= y
        # print(np.linalg.norm(v1))
        # import ipdb; ipdb.set_trace()
        plt.quiver([x], [p(x)] , [v1[0]], [v1[1]], angles="xy", scale_units="xy", scale=12, color="brown")
        s = np.sum(X) / len(X)
        plt.annotate('', xy=(x, p(x)), xytext=(s, p(s)*1.0017),
                    arrowprops=dict(
                        arrowstyle="->",
                        
                        ))
        # x = 3.1
        plt.plot([x], [p(x)], "yo")
    
    plt.plot([x], [p(x)], "yo", label="pontos iniciais")

    x = 2.72
    plt.annotate('ponto de início', xy=(x, p(x)*1.00075))
    # x = 3.3
    # plt.quiver([x], [p(x)] , [-2], [-d(x)*2], angles="xy", scale_units="xy", scale=12)
    # plt.plot(xx, np.polyval(d, xx))

    
    # plt.style.use("classic")
    ax.set_xticks(r)
    ax.set_yticks([])
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    # plt.xlim([1.8, 7])
    # plt.ylim([100, -100])
    
    
fig, ax = plt.subplots()
# f2(fig, ax)
# fig, ax = plt.subplots()
f3(fig, ax)
plt.legend()
plt.savefig("./graficos/plot_funcao_mono_objetivo_.png")
plt.show()
# import ipdb; ipdb.set_trace()