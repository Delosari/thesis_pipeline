"""
The Fergus model of exoplanet detection
=======================================
Besides being generally awesome, this example also demonstrates how you can
color the nodes and add arbitrary labels to the figure.
"""

from matplotlib import rc
rc("font", family="Times New Roman", size=14)
rc("text", usetex=True)

import daft
import pandas as pd

#Colors.
green_color     = {"ec": "#46a546"}
yellow_color    = {"ec": "#f89406"}

#Diagram object
pgm             = daft.PGM([10, 14], origin=[0, 0])

#Dict with node text
node_dict = {}
# node_dict['SpecComp']   = ''
# node_dict['Te']         = ''
# node_dict['ne']         = ''
# node_dict['cHbeta']     = ''
# node_dict['metals']     = ''
# node_dict['recomb']     = ''
# node_dict['tau']        = ''
# node_dict['y_plus']     = ''
# node_dict['emis']       = ''
# node_dict['recombFor']  = ''
# node_dict['emis_met']   = ''
# node_dict['ion_abund']  = ''
# node_dict['metalsFor']  = ''
# node_dict['nebular']    = ''
# node_dict['stellar']    = ''
# node_dict['nebularFor'] = ''
# node_dict['stellarFor'] = ''
# node_dict['z_star']     = ''
# node_dict['age_star']   = ''
# node_dict['stelar_lib'] = ''
# node_dict['cHbeta_ste'] = ''
# node_dict['neb_continua'] = ''
# node_dict['Tbal']         = ''

node_dict['SpecComp']   = 'Spectra comparison'
node_dict['Te']         = r'$T_{e}$'
node_dict['ne']         = r'$n_{e}$'
node_dict['cHbeta']     = r'$c(H\beta)$'
node_dict['metals']     = r''
node_dict['recomb']     = r''
node_dict['tau']        = r'$\tau$'
node_dict['y_plus']     = r'$y^{+}$, $y^{2+}$'
node_dict['emis']       = r'$E_{X}$'
node_dict['recombFor']  = r'$F1$'
node_dict['emis_met']   = r'$E_{X}$'
node_dict['ion_abund']  = r'$X^{y}$'
node_dict['metalsFor']  = r'$F2$'
node_dict['nebular']    = r'$''$'
node_dict['stellar']    = r'$''$'
node_dict['nebularFor'] = r'$F3$'
node_dict['stellarFor'] = r'$F4$'
node_dict['z_star']     = r'$z_{*}$'
node_dict['age_star']   = r'$log(t)$'
node_dict['stelar_lib'] = r'Bases'
node_dict['cHbeta_ste'] = r'$c(H\beta)$'
node_dict['neb_continua'] = 'nebContinua'
node_dict['Tbal']         = r'$T_{Balmer}$'


#Create the nodes big blocks
pgm.add_node(daft.Node("SpecComp",      node_dict['SpecComp'],  5,  7, scale=6, aspect=3))
pgm.add_node(daft.Node("Te",            node_dict['Te'],        5,  11.8, scale=2.5))
pgm.add_node(daft.Node("ne",            node_dict['ne'],        5,  10.5, scale=2.5))
pgm.add_node(daft.Node("cHbeta",        node_dict['cHbeta'],    5,  9.2, scale=2.5))
pgm.add_node(daft.Node("metals",        node_dict['recomb'],    2,  10.5, scale=7.5))
pgm.add_node(daft.Node("recomb",        node_dict['metals'],    8,  10.5, scale=7.5))
pgm.add_node(daft.Node("nebular",       node_dict['nebular'],   2.5,  3, scale=9))
pgm.add_node(daft.Node("stellar",       node_dict['stellar'],   7.5,  3, scale=9))

#Recomb Block nodes
pgm.add_node(daft.Node("emis",          node_dict['emis'],      0.9,10.8, scale=2.5))
pgm.add_node(daft.Node("y_plus",        node_dict['y_plus'],    2,  11.6, scale=2.5))
pgm.add_node(daft.Node("tau",           node_dict['tau'],       3.1,10.8, scale=2.5))
pgm.add_node(daft.Node("recombFor",     node_dict['recombFor'], 2,  10,  scale=1, aspect=3.2))

#Metals block nodes
pgm.add_node(daft.Node("emis_met",      node_dict['emis_met'],  7.3,11.4, scale=2.5))
pgm.add_node(daft.Node("ion_abund",     node_dict['ion_abund'], 8.7,11.4, scale=2.5))
pgm.add_node(daft.Node("metalsFor",     node_dict['metalsFor'], 8,  10,  scale=1, aspect=3.2))

#Nebular block nodes
pgm.add_node(daft.Node("nebularFor",    node_dict['nebularFor'],    3.25, 4.25, scale=2.5))
# pgm.add_node(daft.Node("nebularFor",    node_dict['nebularFor'],  2.5,  4.9,  scale=1, aspect=3.2))
pgm.add_node(daft.Node("neb_continua",  node_dict['neb_continua'],  2.5,  2.8,  scale=2.5, aspect=3.2))
pgm.add_node(daft.Node("Tbal",          node_dict['Tbal'],          1.5,  4.1,  scale=2.5))

#Stellar block nodes
pgm.add_node(daft.Node("stellarFor",    node_dict['stellarFor'],    6.75,  4.25,  scale=2.5))
# pgm.add_node(daft.Node("stellarFor",    node_dict['stellarFor'],    7.5,  4.9,  scale=1, aspect=3.2))
pgm.add_node(daft.Node("age_star",      node_dict['age_star'],      9,  2.8, scale=2.5))
pgm.add_node(daft.Node("z_star",        node_dict['z_star'],        6,  2.8, scale=2.5))
pgm.add_node(daft.Node("stelar_lib",    node_dict['stelar_lib'],    7.5,  2.8, scale=2.5))
pgm.add_node(daft.Node("cHbeta_ste",    node_dict['cHbeta_ste'],    8.5,  4.1, scale=2.5))

#Generate the conections
pgm.add_edge("Te",              "metals")
pgm.add_edge("Te",              "recomb")
pgm.add_edge("ne",              "metals")
pgm.add_edge("ne",              "recomb")
pgm.add_edge("cHbeta",          "metals")
pgm.add_edge("cHbeta",          "recomb")
pgm.add_edge("metals",          "SpecComp")
pgm.add_edge("recomb",          "SpecComp")
pgm.add_edge("emis",            "recombFor")
pgm.add_edge("y_plus",          "recombFor")
pgm.add_edge("tau",             "recombFor")
pgm.add_edge("emis_met",        "metalsFor")
pgm.add_edge("ion_abund",       "metalsFor")
pgm.add_edge("nebular",         "stellar")
pgm.add_edge("nebular",         "SpecComp")
pgm.add_edge("stellar",         "SpecComp")

pgm.add_edge("age_star",        "stelar_lib")
pgm.add_edge("z_star",          "stelar_lib")
pgm.add_edge("stelar_lib",      "stellarFor")
pgm.add_edge("cHbeta_ste",      "stellarFor")
pgm.add_edge("neb_continua",    "nebularFor")
pgm.add_edge("Tbal",            "nebularFor")

# #Create the nodes
# pgm.add_node(daft.Node("phi",           r"$\phi$",      1,      3, plot_params=yellow_color))
# pgm.add_node(daft.Node("speckle_coeff", r"$z_i$",       2,      3, plot_params=yellow_color))
# pgm.add_node(daft.Node("speckle_img",   r"$x_i$",       2,      2, plot_params=yellow_color))
# pgm.add_node(daft.Node("spec",          r"$s$",         4,      3, plot_params=green_color))
# pgm.add_node(daft.Node("shape",         r"$g$",         4,      2, plot_params=green_color))
# pgm.add_node(daft.Node("planet_pos",    r"$\mu_i$",     3,      3, plot_params=green_color))
# pgm.add_node(daft.Node("planet_img",    r"$p_i$",       3,      2, plot_params=green_color))
# pgm.add_node(daft.Node("pixels",        r"$y_i ^j$",    2.5,    1, observed=True))
# 
# #Generate the conections
# pgm.add_edge("phi",             "speckle_coeff")
# pgm.add_edge("speckle_coeff",   "speckle_img")
# pgm.add_edge("speckle_img",     "pixels")
# pgm.add_edge("spec",            "planet_img")
# pgm.add_edge("shape",           "planet_img")
# pgm.add_edge("planet_pos",      "planet_img")
# pgm.add_edge("planet_img",      "pixels")
# 
# # And a plate.
# pgm.add_plate(daft.Plate([1.5, 0.2, 2, 3.2],    label=r"exposure $i$", shift=-0.1))
# pgm.add_plate(daft.Plate([2, 0.5, 1, 1],        label=r"pixel $j$", shift=-0.1))

# Render and save.
pgm.render()
pgm.figure.savefig("/home/vital/Dropbox/Astrophysics/Seminars/Cloudy School 2017/fitting_diagram.pdf")


