from matplotlib import rc
rc("font", family="serif", size=11)
rc("text", usetex=True)

import daft
#Size: Ancho por alto
pgm = daft.PGM([7, 7], origin=[0.5, 0.5], observed_style="inner")

# Hierarchical parameters. Posicion: [Columna, Fila]
pgm.add_node(daft.Node("aH",        r"$a_{H}$", 1, 7,                   scale=1.2))
pgm.add_node(daft.Node("ne",        r"$n_e$", 2, 7,                     scale=1.2))
pgm.add_node(daft.Node("chbeta",    r"$c\left(H\beta\right)$", 3, 7,    scale=1.2))
pgm.add_node(daft.Node("xi",        r"$\xi$", 5, 7,                     scale=1.2))
pgm.add_node(daft.Node("tau",       r"$\tau$", 6, 7,                    scale=1.2))
pgm.add_node(daft.Node("aHe",       r"$a_{He}$", 7, 7,                  scale=1.2))

pgm.add_node(daft.Node("FH",        r"$F_{H}$", 2, 5.5,                  scale=1.4))
pgm.add_node(daft.Node("FHe",       r"$F_{He}$", 6, 5.5,                 scale=1.4))
pgm.add_node(daft.Node("Te",        r"$T_{e}", 4, 5.5,                   scale=1.2))

pgm.add_node(daft.Node("chiEw",     r"$\chi_{EW}^{2}$", 2, 4,           scale=1.4))
pgm.add_node(daft.Node("ChiTem",    r"$\chi_{T}^{2}$", 6, 4,            scale=1.4))

Latex_Likelihood = r'$\mathcal{L}\left(\left(F_{\lambda}\left(\lambda\right)/F_{H\beta}\right)_{obs}\mid\theta\right)$'
# pgm.add_node(daft.Node("Likelihood", Latex_Likelihood, 4, 3.5,                 scale=1.2))
pgm.add_node(daft.Node("Likelihood", Latex_Likelihood, 4, 3.1, aspect=3.2, observed=True, scale=1.6))

# Latent variable.
# pgm.add_node(daft.Node("w", r"$w_n$", 1, 1))

# Data.
# pgm.add_node(daft.Node("x", r"$x_n$", 2, 1, observed=True))

# Add in the edges.
pgm.add_edge("aH", "FH")
pgm.add_edge("ne", "FH")
pgm.add_edge("chbeta", "FH")
pgm.add_edge("xi", "FH")
pgm.add_edge("tau", "FH")
pgm.add_edge("Te", "FH")

pgm.add_edge("ne", "FHe")
pgm.add_edge("chbeta", "FHe")
pgm.add_edge("xi", "FHe")
pgm.add_edge("tau", "FHe")
pgm.add_edge("aHe", "FHe")
pgm.add_edge("Te", "FHe")

pgm.add_edge("Te", "ChiTem")

pgm.add_edge("FH", "Likelihood")
pgm.add_edge("FHe", "Likelihood")

pgm.add_edge("ChiTem", "Likelihood")
pgm.add_edge("chiEw", "Likelihood")



# pgm.add_edge("chbeta", "x")


# Render and save.
StoringDataFolder   = '/home/vital/Workspace/X_ModelData/MCMC_databases/' 

pgm.render()
# pgm.figure.savefig(StoringDataFolder + "nogray.pdf")
pgm.figure.savefig(StoringDataFolder + "nogray.png", dpi=150)

print 'done'