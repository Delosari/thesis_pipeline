import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
plt.style.use('seaborn-darkgrid')
x = np.linspace(0, 5, 100)
mus = [1, 1, 0.75, 0.75]
sds = [1, 0.75, 1, 1.5]
for mu, sd in zip(mus, sds):
    pdf = st.lognorm.pdf(x, sd, scale=np.exp(mu))
    plt.plot(100* x, pdf, label=r'$\mu$ = {}, $\sigma$ = {}'.format(mu, sd))
plt.xlabel('x', fontsize=12)
plt.ylabel('f(x)', fontsize=12)
plt.legend(loc=1)
plt.show()

# import numpy as np
# import pylab as pl
# from scipy.stats import lognorm
# stddev = 50.0
# mean = 0.0
# dist=lognorm([stddev],loc=mean)
# x=np.linspace(0,500,500)
# pl.plot(x,dist.pdf(x))
# # pl.plot(x,dist.cdf(x))
# pl.show()

# import matplotlib.pyplot as plt
# import numpy as np
# import scipy.stats as st
# plt.style.use('seaborn-darkgrid')
# x = np.linspace(0, 20, 200)
# # alphas = [1., 2., 3., 7.5]
# # betas = [.5, .5, 1., 1.]
# alphas = [2.]
# betas = [10]
# for a, b in zip(alphas, betas):
#     pdf = st.gamma.pdf(x, a, scale=1.0/b)
#     plt.plot(x, pdf, label=r'$\alpha$ = {}, $\beta$ = {}'.format(a, b))
# plt.xlabel('x', fontsize=12)
# plt.ylabel('f(x)', fontsize=12)
# plt.legend(loc=1)
# plt.show()
#
# import matplotlib.pyplot as plt
# import numpy as np
# import scipy.stats as st
# plt.style.use('seaborn-darkgrid')
# x = np.linspace(0, 3, 100)
# for lam in [0.5, 1., 2., 10.]:
#     pdf = st.expon.pdf(x, scale=1.0/lam)
#     plt.plot(x, pdf, label=r'$\lambda$ = {}'.format(lam))
# plt.xlabel('x', fontsize=12)
# plt.ylabel('f(x)', fontsize=12)
# plt.legend(loc=1)
# plt.show()