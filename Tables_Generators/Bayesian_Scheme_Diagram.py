'''
Created on Nov 16, 2015

@author: vital
'''
from matplotlib import rc
rc("font", family="serif", size=11)
rc("text", usetex=True)

import daft
#Size: Ancho por alto
pgm = daft.PGM([9, 8], origin=[0.5, 0.5], observed_style="inner")

# Hierarchical parameters. Posicion: [Columna, Fila]
pgm.add_node(daft.Node("aH",        r"$a_{H}$", 1.9, 5.7,                   scale=1.5, observed=True))
pgm.add_node(daft.Node("aHe",       r"$a_{He}$", 8.1, 5.7,                  scale=1.5, observed=True))

pgm.add_node(daft.Node("xi",        r"$\xi$", 2.3, 6.6,                     scale=1.5, observed=True))
pgm.add_node(daft.Node("Te",        r"$T_{e}$", 3.1, 7.2,                   scale=1.5, observed=True))
pgm.add_node(daft.Node("chbeta",    r"$c\left(H\beta\right)$", 4, 7.6,      scale=1.5, observed=True))
pgm.add_node(daft.Node("yplus",     r"$y^{+}$", 5, 7.9,                     scale=1.5, observed=True))
pgm.add_node(daft.Node("eqwhbeta",  r"$Eqw_{H\beta}$", 6, 7.6,              scale=1.5, observed=True))
pgm.add_node(daft.Node("ne",        r"$n_e$", 6.9, 7.2,                     scale=1.5, observed=True))
pgm.add_node(daft.Node("tau",       r"$\tau$", 7.7, 6.6,                    scale=1.5, observed=True))

pgm.add_node(daft.Node("CR_cor",    r"$\frac{C}{R}$", 2.8, 5.7,             scale=1.6))
pgm.add_node(daft.Node("ftau_cor",  r"$f_{\tau}$", 7.2, 5.7,                scale=1.6))

pgm.add_node(daft.Node("EH",        r"$Em_{H}$", 3.7, 5.3,                  scale=1.6))
pgm.add_node(daft.Node("EHe",       r"$Em_{He}$", 6.3, 5.3,                 scale=1.6))

pgm.add_node(daft.Node("FH",        r"$F_{theo,\,H}$", 4.4, 3.5,            scale=2))
pgm.add_node(daft.Node("FHe",       r"$F_{theo,\,He}$", 5.6, 3.5,           scale=2))

pgm.add_node(daft.Node("hH",        r"$h_{H,\,\lambda}$", 2.8, 3.5,         scale=1.5, observed=True))
pgm.add_node(daft.Node("hHe",       r"$h_{He,\,\lambda}$", 7.2, 3.5,        scale=1.5, observed=True))

pgm.add_node(daft.Node("FobsH",     r"$F_{obs,\,H}$", 2.8, 2.5,             scale=1.5, observed=True))
pgm.add_node(daft.Node("FobsHe",    r"$F_{obs,\,He}$", 7.2, 2.5,            scale=1.5, observed=True))

# pgm.add_node(daft.Node("chiEw",     r"$\chi_{EW}^{2}$", 2, 4,           scale=1.4))
# pgm.add_node(daft.Node("ChiTem",    r"$\chi_{T}^{2}$", 6, 4,            scale=1.4))

Latex_Likelihood = r'$\mathcal{L}\left(\left(F_{\lambda}\left(\lambda\right)/F_{H\beta}\right)_{obs}\mid\theta\right)$'
# pgm.add_node(daft.Node("Likelihood", Latex_Likelihood, 4, 3.5,                 scale=1.2))
pgm.add_node(daft.Node("Likelihood", Latex_Likelihood, 5, 1.8, aspect=3.2, scale=2.1))

# Latent variable.
# pgm.add_node(daft.Node("w", r"$w_n$", 1, 1))

# Data.
# pgm.add_node(daft.Node("x", r"$x_n$", 2, 1, observed=True))

# Add in the edges.
# pgm.add_edge("aH", "CR_cor")
pgm.add_edge("Te", "CR_cor")
pgm.add_edge("xi", "CR_cor")

pgm.add_edge("ne", "ftau_cor")
pgm.add_edge("tau", "ftau_cor")
# pgm.add_edge("aHe", "ftau_cor")
pgm.add_edge("Te", "ftau_cor")

pgm.add_edge("Te", "EH")
pgm.add_edge("ne", "EH")
pgm.add_edge("Te", "EHe")
pgm.add_edge("ne", "EHe")

pgm.add_edge("CR_cor", "FH")
pgm.add_edge("ftau_cor", "FHe")
pgm.add_edge("EH", "FH")
pgm.add_edge("EHe", "FHe")
pgm.add_edge("aH", "FH")
pgm.add_edge("aHe", "FHe")
pgm.add_edge("chbeta", "FH")
pgm.add_edge("chbeta", "FHe")
pgm.add_edge("eqwhbeta", "FH")
pgm.add_edge("eqwhbeta", "FHe")
pgm.add_edge("yplus", "FHe")
pgm.add_edge("FH", "Likelihood")
pgm.add_edge("FHe", "Likelihood")
pgm.add_edge("hH", "FH")
pgm.add_edge("hHe", "FHe")
pgm.add_edge("FobsH", "Likelihood")
pgm.add_edge("FobsHe", "Likelihood")

# pgm.add_edge("ChiTem", "Likelihood")
# pgm.add_edge("chiEw", "Likelihood")



# pgm.add_edge("chbeta", "x")


# Render and save.
StoringDataFolder = '/home/vital/Dropbox/Astrophysics/Papers/Elemental_RegressionsSulfur/Images/'

pgm.render()
print StoringDataFolder + "poster.png"
# pgm.figure.savefig(StoringDataFolder + "nogray.pdf")
pgm.figure.savefig(StoringDataFolder + "poster.png", dpi=600)

print 'done'