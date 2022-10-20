def writetxt(newest_ID,old_ID):
    path = 'recorddeleteID.txt'
    with open(path, 'a') as f:
        f.write(newest_ID+'\t'+old_ID+'\n')
