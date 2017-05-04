from matplotlib import rc
rc('font', family='serif', size=10)
rc('text', usetex=True)

import daft
#Size: Ancho por alto
pgm = daft.PGM([8, 4.5], origin=[0.5, 0.0], observed_style='inner')

# Hierarchical parameters. Posicion: [Columna, Fila]
pgm.add_node(daft.Node('SIIlines',  r'$[SII]$' + '\nlines',                     1.5, 4, scale=1.5, observed=True))
pgm.add_node(daft.Node('SIIIlines', r'$[SIII]$' + '\nlines',                    3.5, 4, scale=1.5, observed=True))
pgm.add_node(daft.Node('ArIIIlines',r'$[ArIII]$' + '\nlines',       5.5, 4, scale=1.5, observed=True))
pgm.add_node(daft.Node('ArIVlines', r'$[ArIV]$' + '\nlines',        7.5, 4, scale=1.5, observed=True))

pgm.add_node(daft.Node('TSII',      r'$T_{[SII]}$',                 1, 2.8,           scale=1.3))
pgm.add_node(daft.Node('ne',        r'$n_{e[SII]}$',                2, 2.8,           scale=1.3))
pgm.add_node(daft.Node('TSIII',     r'$T_{[SIII]}$',                4, 2.8,           scale=1.3))
pgm.add_node(daft.Node('TArIII',    r'$T_{[ArIII]}$',               5, 2.8,           scale=1.3))
pgm.add_node(daft.Node('TArIV',     r'$T_{[ArIV]}$',                7, 2.8,           scale=1.3))

pgm.add_node(daft.Node('[SII]',     r'$\left(\frac{S^{+}}{H^{+}}\right)$',          1.5, 1.5,         scale=1.2))
pgm.add_node(daft.Node('[SIII]',    r'$\left(\frac{S^{+2}}{H^{+}}\right)$',         3, 1.5,           scale=1.2))
pgm.add_node(daft.Node('[ArIII]',   r'$\left(\frac{Ar^{+2}}{H^{+}}\right)$',        6, 1.5,           scale=1.2))
pgm.add_node(daft.Node('[ArIV]',    r'$\left(\frac{Ar^{+3}}{H^{+}}\right)$',        8, 1.5,           scale=1.2))

pgm.add_node(daft.Node('[SIV]',    ' ' + r'$\left(\frac{S^{+3}}{H^{+}}\right)$',        7, 1,           scale=1.2))

pgm.add_node(daft.Node('SIHI',    ' ' + r'$\left(\frac{S}{H}\right)$',                           4.5, 0.5,           scale=1.2))

# Adding the edges
pgm.add_edge('SIIlines', 'ne')
pgm.add_edge('SIIlines', 'TSII')
pgm.add_edge('SIIlines', '[SII]')

pgm.add_edge('SIIIlines', 'TSIII')
pgm.add_edge('SIIIlines', '[SIII]')

pgm.add_edge('ArIIIlines', 'TArIII')
pgm.add_edge('ArIIIlines', '[ArIII]')

pgm.add_edge('ArIVlines', 'TArIV')
pgm.add_edge('ArIVlines', '[ArIV]')


pgm.add_edge('TSII', 'ne')
pgm.add_edge('TSIII', 'ne')

pgm.add_edge('TSIII', 'TArIII')
pgm.add_edge('TArIII', 'TArIV')
pgm.add_edge('TSIII', '[SIII]')
pgm.add_edge('TArIII', '[ArIII]')
pgm.add_edge('TArIV', '[ArIV]')


pgm.add_edge('ne', '[SII]')
# pgm.add_edge('ne', '[SIII]')
# pgm.add_edge('ne', '[ArIII]')
# pgm.add_edge('ne', '[ArIV]')

pgm.add_edge('[ArIII]', '[SIV]')
pgm.add_edge('[ArIV]',  '[SIV]')

pgm.add_edge('[SII]',   'SIHI')
pgm.add_edge('[SIII]',  'SIHI')
pgm.add_edge('[SIV]',   'SIHI')


# pgm.add_edge('chbeta', 'x')


# Render and save.
StoringDataFolder   = '/home/vital/Workspace/X_ModelData/' 

pgm.render()
# pgm.figure.savefig(StoringDataFolder + 'nogray.pdf')
pgm.figure.savefig(StoringDataFolder + '_SIHI_abundance.png', dpi=150)

print 'done'