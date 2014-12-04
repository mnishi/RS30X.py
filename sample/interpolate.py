import sys
from os import pardir
sys.path.append(pardir)

from RS30X import RS30XController
import time
import math

SPEED_MAX = 240.0 / 1000.0 # deg per msec
CONTROL_PERIOD = 50.0 # msec

#
# functions
#
def interpolate(con, id, src, dest):
    reqcnt = getRequiredPeriods(src, dest)
    con.log("interpolate: src = %f, dest = %f, requiredPeriods = %d", src, dest, reqcnt) 
    
    trajectory = []
    for i in range(1, reqcnt + 1, 1):
        pos = getTrajectory(src, dest, i, reqcnt) 
        con.log("interpolate: src = %f, dest = %f, period = %d, periodMax = %d, pos = %f", src, dest, i, reqcnt, pos)
        trajectory.append(pos)

    for i in range(reqcnt):
        if i < (reqcnt -1):
            pos = convPosTo10deg(trajectory[i + 1])
            con.log("interpolate: period = %d, pos = %d", i + 1, pos) 
            con.move(id, pos, CONTROL_PERIOD * 2)
            time.sleep(CONTROL_PERIOD / 500.0)
        else:
            pos = convPosTo10deg(trajectory[i])
            con.log("interpolate: period = %d, pos = %d", i + 1, pos) 
            con.move(id, pos, CONTROL_PERIOD) 
            time.sleep(CONTROL_PERIOD / 1000.0)

    return dest

def convPosTo10deg(pos):
    return int(round(pos * 10.0, 0))

def getRequiredPeriods(src, dest):
    return int( math.ceil( abs ( ( 15.0 * ( dest - src ) / ( 8 * SPEED_MAX ) ) / CONTROL_PERIOD ) ) )

def getTrajectory(src, dest, period_, periodMax_):
    period = period_ * 1.0
    periodMax = periodMax_ * 1.0
    return src + ( dest - src ) * ( ( period / periodMax ) ** 3 ) * ( 10 - 15 * period / periodMax + 6 * ( ( period / periodMax ) ** 2 ) )
#
# main code
#
id = 1

con = RS30XController()
con.init(id)
src = 0.0
con.move(id, src, 1000)
time.sleep(2)
src = interpolate(con, id, src, 90.0)
src = interpolate(con, id, src, -120.0)
src = interpolate(con, id, src, 150.0)

