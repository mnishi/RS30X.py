import sys
from os import pardir
sys.path.append(pardir)

from RS30X import RS30XController
import time

id = 1

con = RS30XController()

con.init(id)

con.move(id, 900, 0)
time.sleep(2)

#con.getStatus(id)
#print con.getPosition(id)

con.move(id, -900, 0)
time.sleep(2)
#
#con.getStatus(id)
#print con.getPosition(id)
#
con.move(id, 900, 500)
time.sleep(5)
#
#con.getStatus(id)
#print con.getPosition(id)
#
con.move(id, -1200, 1000)
time.sleep(10)
#
con.getStatus(id)
print con.getPosition(id)
#
