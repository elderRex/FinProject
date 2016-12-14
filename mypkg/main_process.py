from custom_algo_pkg import slide_algo as sa
import sys
from custom_algo_pkg import block_partition as bp

'''

'''
def surge_svm(location,time,type='uber'):
    surge = 0
    return surge

def surge_lr(location,time,type='uber'):
    surge = 0
    return surge

def surge_slide(location,time,type='uber'):
    surge = sa.predict(location,time,type)
    return surge

def read_block_list():
    block_list = []
    bl = []
    with open(sys.path[0]+'/processed/lyft/blocklist.csv', 'r+') as blockfilel:
        for line in blockfilel:
            paras = line.split(' ')
            bl.append([float(paras[0]),float(paras[1])])
    bu = []
    with open(sys.path[0]+'/processed/uberx/blocklist.csv', 'r+') as blockfileu:
        for line in blockfileu:
            paras = line.split(' ')
            bu.append([float(paras[0]), float(paras[1])])
    block_list = [bu,bl]
    return block_list

'''
location[0] is center location for uber
location[1] is center location for lyft
blocklist reads in blocklists for uber in [0] and lyft in [1]
'''
def main(opts,ini_location,time):
    surge_u = 0
    surge_l = 0
    blocklist = read_block_list()
    print blocklist[0]
    print blocklist[1]
    #location = [0,0]
    location = bp.bp_user_assign_block(ini_location[0],ini_location[1],blocklist)
    print location
    if opts == 0:
        surge_u = surge_svm(location,time,'uber')
        surge_l = surge_svm(location,time,'lyft')
    elif opts == 1:
        surge_u = surge_lr(location,time,'uber')
        surge_l = surge_lr(location, time,'lyft')
    elif opts == 2:
        surge_u = surge_slide(location,time,'uber')
        surge_l = surge_slide(location, time,'lyft')
    elif opts == 3:
        surge_u = surge_svm(location,time,'uber')+surge_lr(location,time,'uber')+surge_slide(location,time,'uber')
        surge_l = surge_svm(location, time,'lyft') + surge_lr(location, time,'lyft') + surge_slide(location, time,'lyft')
        surge_u /= 3
        surge_l /= 3
    else:
        print "Come on, that's not gonna work with opts : " + str(opts)

    return [surge_u,surge_l]