def writedeleteID(ID):
    path = 'recorddeleteID.txt'
    with open(path, 'a') as f:
        f.write(ID+'\n')

def writeadjustID(newest_ID,old_ID):
    path = 'recordadjustID.txt'
    with open(path, 'a') as f:
        f.write(newest_ID+'\t'+old_ID+'\n')
