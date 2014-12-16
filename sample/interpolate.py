import sys
import os
import time
import math

sys.path.append(os.pardir)
from RS30X import RS30XController
from RS30X import RS30XParameter

SPEED_MAX = 240.0 / 1000.0 # deg per msec
CONTROL_PERIOD = 20.0 # msec

#
# functions
#
def interpolate(con, ids, src, dest):
    reqcnt = getRequiredPeriods(src, dest)
    con.log("interpolate: src = %f, dest = %f, requiredPeriods = %d", src, dest, reqcnt) 
    
    trajectory = []
    for i in range(1, reqcnt + 1, 1):
        pos = getTrajectory(src, dest, i, reqcnt) 
        con.log("interpolate: src = %f, dest = %f, period = %d, periodMax = %d, pos = %f", src, dest, i, reqcnt, pos)
        trajectory.append(pos)

    for i in range(reqcnt):
        if i < (reqcnt -1):
            pos = convPosToTenthDeg(trajectory[i + 1])
            con.move(createTargetParams(ids, pos, int(CONTROL_PERIOD * 2))) 
            time.sleep(CONTROL_PERIOD / 1000.0)
        else:
            pos = convPosToTenthDeg(trajectory[i])
            con.move(createTargetParams(ids, pos, int(CONTROL_PERIOD))) 
            time.sleep(CONTROL_PERIOD / 500.0)

    return dest

def createTargetParams(ids, pos, time):
    params = []
    for id in ids:
        pos_ = pos
        if id % 2 == 0:
            pos_ = pos * -1
        params.append(RS30XParameter(id, pos_, time))
    return params

def convPosToTenthDeg(pos):
    return int(round(pos * 10.0, 0))

def getRequiredPeriods(src, dest):
    return int( math.ceil( abs ( ( 15.0 * ( dest - src ) / ( 8.0 * SPEED_MAX ) ) / CONTROL_PERIOD ) ) )

def getTrajectory(src, dest, period_, periodMax_):
    period = float(period_)
    periodMax = float(periodMax_)
    return src + ( dest - src ) * ( ( period / periodMax ) ** 3.0 ) * ( 10.0 - 15.0 * period / periodMax + 6.0 * ( ( period / periodMax ) ** 2.0 ) )

#
# main code
#
ids = range(1,7)

con = RS30XController()

src = 0.0

for id in ids:
    con.torqueOn(id)

for id in ids:
    con.move(id, src, 50)

time.sleep(3)

src = interpolate(con, ids, src, 30.0)
src = interpolate(con, ids, src, -60.0)
src = interpolate(con, ids, src, 90.0)
src = interpolate(con, ids, src, -120.0)
src = interpolate(con, ids, src, 150.0)
src = interpolate(con, ids, src, -120.0)
src = interpolate(con, ids, src, 90.0)

for id in ids:
    con.torqueOff(id)
