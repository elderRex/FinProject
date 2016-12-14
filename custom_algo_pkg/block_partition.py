'''
Partition blocks based on GPS location
'''

import math

def bp_dist(ulat,ulng,blat,blng):
    dist = math.sqrt(pow((ulat-blat),2)+pow((ulng-blng),2))
    return dist

'''
Obtain the Block center that is closest to the user location

location[0] is center location for uber
location[1] is center location for lyft
'''
def bp_user_assign_block(ulat,ulng,blocklist):
    mindistu = [10000000,[0,0]]
    mindistl = [10000000,[0,0]]
    for bus in blocklist[0]:
        dist = bp_dist(ulat,ulng,bus[0],bus[1])
        if dist < mindistu[0]:
            mindistu[0] = dist
            mindistu[1][0] = bus[0]
            mindistu[1][1] = bus[1]
    for bls in blocklist[1]:
        dist = bp_dist(ulat,ulng,bls[0],bls[1])
        if dist < mindistl[0]:
            mindistl[0] = dist
            mindistl[1][0] = bls[0]
            mindistl[1][1] = bls[1]

    return [mindistu[1],mindistl[1]]

