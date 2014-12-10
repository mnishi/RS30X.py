import sys
import os
import time

sys.path.append(os.pardir)
from RS30X import RS30XController
from RS30X import RS30XParameter

id = 1

con = RS30XController()

con.torqueOn(id)

con.move(id, 0, 0)
time.sleep(2)

con.move(id, 900)
time.sleep(2)

con.move(id, -150)
time.sleep(2)

con.move(id, 900, 500)
time.sleep(5)

con.move(id, -1200, 1000)
time.sleep(10)

con.move(
        RS30XParameter(1, 100),
        RS30XParameter(2, 100),
        RS30XParameter(5, 500)
        )
time.sleep(10)

con.torqueOff(id)
