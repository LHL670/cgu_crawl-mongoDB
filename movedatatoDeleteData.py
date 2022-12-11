import recordtxt
import deleteandrecordmongoDB
import manageMongodb
def from_CGUScholar_com_to_DeleteData(user_ID):
	recordtxt.writedeleteID(user_ID)
	deleteandrecordmongoDB.movetodeleteDB('articles',user_ID)
	deleteandrecordmongoDB.movetodeleteDB('cguscholar',user_ID)
	manageMongodb.delete_jsonfileby_id('articles', user_ID)
	manageMongodb.delete_jsonfileby_id('cguscholar', user_ID)
