import os
# os.environ["CC"] = "/usr/bin/gfortran"
# os.environ["CXX"] = "/usr/bin/gfortran"

# Using post-0.2.2 scipy_distutils to display fortran compilers
from numpy.distutils.fcompiler import new_fcompiler
compiler = new_fcompiler() # or new_fcompiler(compiler='intel')
compiler.dump_properties()

#Generate add.f wrapper
from numpy import f2py
with open("add.f90") as sourcefile:
    sourcecode = sourcefile.read()
    print 'Fortran code'
    print sourcecode

f2py.compile(sourcecode, modulename='add')
# f2py.compile(sourcecode, modulename='add', extra_args = '--fcompiler=/usr/bin/gfortran')
# f2py.compile(sourcecode, modulename='add')
# f2py -c --help-fcompiler
import add
print 'eso'