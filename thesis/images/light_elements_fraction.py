from matplotlib import rcParams, pyplot as plt
import numpy as np


size_dict = {'figure.figsize':(7, 3), 'axes.titlesize':20, 'axes.labelsize':16, 'legend.fontsize':16, 'font.family':'Times New Roman', 'mathtext.default':'regular', 'xtick.labelsize':20, 'ytick.labelsize':20}

rcParams.update(size_dict)

fig, ax = plt.subplots()

# Example data
people = ['$X_{P}$', '$Y_{P}$', r'$\frac{D}{H}$', '$\\frac{^{3}He_{P}}{H}$', '$\\frac{^{3}Li_{P}}{H}$']
people = ['$X_{P}$', '$Y_{P}$', r'$D/H$', '$^{3}He_{P}/H$', '$Li_{P}/H$']

y_pos = np.arange(len(people))
performance = [0.752, 0.247, 2.58e-5,10.04e-5,4.68e-10]
colours = ['#008DB8', '#00AAAA', '#00C69C', '#00E28E', '#00FF80', ]

for i in range(len(people)):
    ax.barh(y_pos[i], performance[i], align='center', color=colours[i], ecolor='black')

ax.set_yticks(y_pos)
ax.set_yticklabels(people)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xscale('log')
ax.set_xlabel('')
ax.set_title('')
# plt.show()
plt.savefig('/home/vital/Dropbox/Astrophysics/Thesis/images/primordial_abundances', dpi=150, bbox_inches='tight', pad_inches=0.2)

# import matplotlib.pyplot as plt
# import numpy as np
#
# data = ((3, 1000), (10, 3), (100, 30), (500, 800), (50, 1))
#
# dim = len(data[0])
# w = 0.75
# dimw = w / dim
#
# fig, ax = plt.subplots()
# x = np.arange(len(data))
# for i in range(len(data[0])):
#     y = [d[i] for d in data]
#     b = ax.bar(x + i * dimw, y, dimw, bottom=0.001)
#
# ax.set_xticks(x + dimw / 2, map(str, x))
# ax.set_yscale('log')
#
# ax.set_xlabel('x')
# ax.set_ylabel('y')
#
# plt.show()

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
#
# group_names = ['Hydrogen', '$Y_{P} = 0.247$', r'$\frac{D}{H}=2.58\cdot10^{-5}$', '$\frac{^{3}He_{P}}{H}=10.04\cdot10^{-5}$', '$\frac{^{3}Li_{P}}{H}=4.68\cdot10^{-10}$']
# group_values = [0.752, 0.247, 2.58e-5,10.04e-5,4.68e-10]
#
# counts = pd.Series(group_values,
#                    index=group_names)
#
# explode = (0, 0, 0.3, 0.4, 0.6)
# colors = ['#008DB8', '#00AAAA', '#00C69C', '#00E28E', '#00FF80', ]
#
# counts.plot(kind='pie', fontsize=17, colors=colors, explode=explode)
# plt.axis('equal')
# plt.ylabel('')
# plt.legend(labels=counts.index, loc="best")
# plt.show()


import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
#
# group_names = ['2-3 km', '3-5 km', '5-7 km', '7-10 km', '10-20 km', '20-50 km',
#                '50-75 km', '75-100 km', '>100 km']
#
# counts = pd.Series([1109, 696, 353, 192, 168, 86, 74, 65, 53],
#                    index=['20-50 km', '50-75 km', '10-20 km', '75-100 km',
#                           '3-5 km', '7-10 km', '5-7 km', '>100 km', '2-3 km'])
#
# explode = (0, 0, 0, 0.1, 0.1, 0.2, 0.3, 0.4, 0.6)
# colors = ['#191970', '#001CF0', '#0038E2', '#0055D4', '#0071C6', '#008DB8', '#00AAAA',
#           '#00C69C', '#00E28E', '#00FF80', ]
#
# counts.plot(kind='pie', fontsize=17, colors=colors, explode=explode)
# plt.axis('equal')
# plt.ylabel('')
# plt.legend(labels=counts.index, loc="best")
# plt.show()