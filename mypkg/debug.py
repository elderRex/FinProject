
def blocks():
    bl = []
    with open('../processed/lyft/blocklist.csv', 'r+') as blockfilel:
        for line in blockfilel:
            paras = line.split(' ')
            bl.append([float(paras[0]),float(paras[1])])
    bu = []
    with open('../processed/uberx/blocklist.csv', 'r+') as blockfileu:
        for line in blockfileu:
            paras = line.split(' ')
            bu.append([float(paras[0]), float(paras[1])])
    bl.sort()
    bu.sort()
    with open('../processed/lyft/blocklistc.csv', 'w+') as blockfilels:
        for i in range(0,len(bl)):
            blockfilels.write(str(bl[i][0])+' '+str(bl[i][1])+'\n')
    with open('../processed/uberx/blocklistc.csv', 'w+') as blockfileus:
        for i in range(0,len(bu)):
            blockfileus.write(str(bu[i][0])+' '+str(bu[i][1])+'\n')

blocks()