from make_hl_val import make_hl_val
from isnum import isnum

def get_table_float(dat,med,prop_used,val):    
    for mm in range(0,len(dat)):
        if isnum(dat[mm][-2]):
            ll = float(dat[mm][-2])
            med.append(str(ll))
            prop_used.append(dat[mm][-3])
        elif float(make_hl_val(dat[mm][-2])) != float(-9999):
            ll = make_hl_val(dat[mm][-2])
            med.append(str(ll))
            prop_used.append(dat[mm][-3])
    if len(med) > 0:
        #take the average if there are numbers in the list
        for rr in med:
            val = val + float(rr)
        val = val/len(med)
        #if there are no values it is -9999
    else:
        val = '-9999'
    return val