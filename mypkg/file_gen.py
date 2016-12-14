month=['nov','dec']
day_cnt = [11,9]

for i in range(0,2):
    if i == 0:
        for j in range(0,day_cnt[i]):
            fid = open(month[0]+str(20+j)+'.txt','w+')
            fid.close()
    else:
        for j in range(0,day_cnt[i]):
            fid = open(month[1]+str(1+j)+'.txt','w+')
            fid.close()