import time
import manageMongodb
import checkDataformat
import CGUScholarLabel


def LabelCrawl(label):  # if empty ,updatelabel is null
    print('label : ' + label + 'start')

    labellist = CGUScholarLabel.get_labelIDlist(label)
    check_labelformat = checkDataformat.labelinfoformat(labellist)

    # label list 為空或格式錯誤時回傳False,格式錯誤修正後回傳rewriteInfo
    if(check_labelformat == True):
        try:
            fix_labelformat = checkDataformat.errorfixlabelinfoformat(
                labellist)
            labellist = fix_labelformat
            manageMongodb.add_labeluserIDinfo(labellist)
        except:
            print('label ' + label + 'crawl fail!')
    else:
        print('label ' + label + 'crawl fail!')

    print('label ' + label + 'final')
