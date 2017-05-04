'''
Created on Jun 12, 2014

@author: INAOE_Vital
'''
import os
import subprocess

os.chdir('/Users/INAOE_Vital/Starlight/')
Command = './Starlight_v04_Mac.exe < grid_example1.in'

print 'Declaring p'

p = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)



print 'Starting loop'
 
for line in p.stdout.readlines():
    print line,

print 'Launching retval'

retval = p.wait()


print 'Se acabo'
