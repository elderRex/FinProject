def print_perf(time,filename,time_unit,processed_item,custom_item_line):
    print '----------------------------------------------------------------'
    print 'Program : '+filename+' Successfully Executed '
    print 'Time Consumed : ' + time + ' / ' + time_unit
    print 'Total Number of ' + custom_item_line+' '+str(processed_item)
    print '----------------------------------------------------------------'