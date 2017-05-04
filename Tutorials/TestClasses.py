from Tutorials import testlinfit as CT

a = CT.dry_parcel(85000,260,3)

print a.p

print a.T

print a.m

print a.moles()

print a.volume()

a.T = 280

print a.volume()
