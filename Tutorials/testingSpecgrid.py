
import matplotlib.gridspec as gridspec
from matplotlib import pyplot as plt
from matplotlib import image, colors, cm, rcParams, pyplot as plt

# gs = gridspec.GridSpec(4, 3)
# # gs.update(wspace=0.05)
#
# ax1 = plt.subplot(gs[0, :])
# ax2 = plt.subplot(gs[1, :-1])
# ax3 = plt.subplot(gs[1:, -1])
# ax4 = plt.subplot(gs[-1, 0])
# ax5 = plt.subplot(gs[-1, -2])
#
# plt.show()

# ax1 = plt.subplot2grid((4, 3), (0, 0), colspan=3)
# ax2 = plt.subplot2grid((4, 3), (1, 0), colspan=2)
# ax3 = plt.subplot2grid((4, 3), (1, 2), rowspan=2)
# ax4 = plt.subplot2grid((4, 3), (2, 0))
# ax5 = plt.subplot2grid((4, 3), (2, 1))

# size_dict = {'figure.figsize': (2, 1), 'axes.titlesize': 20, 'axes.labelsize': 20, 'legend.fontsize': 14}
# rcParams.update(size_dict)
n_traces = 4
nColumns = 3
nRows = n_traces
nPlots = n_traces * 2

# fig = plt.figure(figsize=(8, ntraces*2))
#
# for i in range(ntraces):
#     axTrace = plt.subplot2grid((nRows, 3), (i, 0), colspan=2)
#     axPoterior = plt.subplot2grid((nRows, 3), (i, 2))
#     if i < ntraces - 1:
#         axTrace.get_xaxis().set_visible(False)
#         axTrace.set_xticks([])
#
#     axPoterior.yaxis.set_major_formatter(plt.NullFormatter())
#     axPoterior.set_yticks([])
#     axPoterior.set_aspect(0.8)
#
# plt.subplots_adjust(wspace=0, hspace=0.2)
# plt.show()

import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(8,n_traces*2))
gs = gridspec.GridSpec(n_traces * 2, 3)

# n_traces = 4
# gsMax = 4 * 2 = 8
#
# 0 0 i      2*i
# 1   :i+2   2*i +1
#
# 2 1 i+1
# 3   :i+3
#
# 4 2 i+2
# 5   :i+4
#
# 6 3 i+3
# 7   :i+5

# 0, 2, 4, 6
# 2, 4, 6, 8
#
# 2*(1+i)
# x[i*(i+1):2*(1+i)]
gs.update(wspace = 0.2, hspace=0.5)
for i in range(n_traces):

    axTrace = fig.add_subplot(gs[2*i:2*(1+i),:2])
    axPoterior = fig.add_subplot(gs[2*i:2*(1+i),2])


    if i < n_traces - 1:
        axTrace.get_xaxis().set_visible(False)
        axTrace.set_xticks([])

    axPoterior.yaxis.set_major_formatter(plt.NullFormatter())
    axPoterior.set_yticks([])
    #axPoterior.set_aspect(1, anchor='C')
    #axPoterior.set_anchor("S")


plt.show()