import sys
import os 
import time

sys.path.append(os.pardir)
from RS30X import RS30XController

id = 1

if len(sys.argv) < 2:
    print "usage: %s dest_id [ src_id ]\n" % os.path.basename(__file__)
    quit()
elif len(sys.argv) == 3:
    id = int(sys.argv[2])

dest_id = int(sys.argv[1])

con = RS30XController()

con.initMemMap(id)
con.setServoId(id, dest_id)
con.commitToFlashROM(dest_id)
con.restart(dest_id)
