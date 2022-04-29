import time
import manageMongodb
import checkDataformat
import CGUScholarLabel
import manageMongodb


def LabelCrawl(label):  # if empty ,updatelabel is null
    print('label start ' + label )

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
            print('label ' + label + ' format fail!')
            # manageMongodb.delete_jsonfileby_id('Label_Domain',  label)
    else:
        print('label ' + label + ' crawl fail!')
        time.sleep(60)
        # manageMongodb.delete_jsonfileby_id('Label_Domain',  label)
        manageMongodb.adjust_labelname(label)

    print('label final ' + label )
