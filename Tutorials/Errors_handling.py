from CodeTools.PlottingManager                          import myPickle
pv                          = myPickle()

# logging.basicConfig(level=logging.ERROR)
# import traceback
# 
# 'errors log'
# error_log = []
# 
# try: 
#     x = 0 
#     y = 1 
#     z = y / x 
#     z = z + 1 
#     print "z=%d" % (z) 
# except:
#     print '\n-Error logged\n'
#     error_log.append([0, traceback.format_exc()])
# #     error_log.append(logging.exception("Values at Exception: x=%d y=%d " % (x,y)))
# 
# if len(error_log) != 0:
#     print '-These objects treatment produced a script error:\n'
#     for z in range(len(error_log)):
#         print '--Object', error_log[0][0],':\n'
#         print error_log[0][1]

import traceback
  
try: 
    x = 0 
    y = 1 
    z = y / x 
    z = z + 1 
    print "z=%d" % (z) 
except:
    pv.log_error('coso')
 
pv.display_errors()