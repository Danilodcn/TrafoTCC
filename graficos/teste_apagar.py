from functools import partial
from math import log
import numpy as np
from numpy import exp
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline


curva_BH = {
        "B": [-1.85, -1.8, -1.7, -1.6, -1.5, -1.4, -1.3, -1.2, -1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.85],
        "H": [-712.275, -362.03, -118.623, -62.081, -42.888, -34.032, -28.97, -25.97, -22.476, -19.53, -16.387, -12.672, -8.03, 0, 8.03, 12.672, 16.387, 19.53, 22.476, 25.97, 28.97, 34.032, 42.888, 62.081, 118.623, 362.03, 712.275]
}

xi = np.asarray(curva_BH["H"])
yi = np.asarray(curva_BH["B"])

x = xi[len(xi) // 2:]
y = yi[len(yi) // 2:]

# x = np.array([1, 7, 20, 50, 79])
# y = np.array([10, 19, 30, 35, 51])

assert len(x) == len(y)

plt.plot(x, y, "ro")

# z = np.polyfit(x, y, 20)
# f = np.poly1d(z)
xx = np.linspace(-100, 850, 100000) 
#plt.plot(xx, np.polyval(z, xx), "b-")
# plt.plot(x, UnivariateSpline(x, y, k=4), "b-")
# func = lambda t, a, b, c, d: a*exp(-b*t) + c + d*t

# res = curve_fit(func, x, y)
# a, b, c, d = res[0]

# fun = partial(
#         func,
#         a=a,
#         b=b,
#         c=c,
#         d=d,
#         )

# Coefficients (with 95% confidence bounds):
a =       1.809  
b =   1.802e-05  
c =      -1.995 
d =    -0.03857 
print(a, b, c, d)
f = lambda t: a * exp(b * t) + c * exp(d * t)

yy = np.array(list(map(f, xx)))


plt.plot(xx, yy, "b-")


plt.xlim(-50, 800)
plt.ylim(-0.4, 2.5)
# plt.style.use("classic")
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.xlabel("Indução Magnética H [A/m]")
plt.ylabel("Fluxo Magnético B [T]")

Xlb = 90

plt.annotate('LB', xy=(Xlb, f(Xlb)), xytext=(75, 2.15),
            arrowprops=dict(
                arrowstyle="->"
                ))

Xla = 55

plt.annotate('LA', xy=(Xla, f(Xla)), xytext=(120, 1.15),
            arrowprops=dict(
                arrowstyle="->"
                ))

plt.savefig("./graficos/plot.png")
plt.show()
