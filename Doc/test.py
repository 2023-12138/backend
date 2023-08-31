from py_etherpad import EtherpadLiteClient
import datetime
import time
myPad = EtherpadLiteClient('4c87155dea77eb7c2927025bc807ee87304e5bf06239ba1439c17c1efa2e6c4e','http://43.138.59.36:10010/api')
groupid=myPad.createGroup().get('groupID')
# authorid=myPad.createAuthor("hhhh").get('authorID')
print(groupid)
authorid = myPad.createAuthor("abc").get('authorID')
print(authorid)
# # print(myPad.createGroupPad(groupid,"哈哈哈哈"))
# # try:
# #     print(myPad.createGroupPad(groupid,"哈哈哈哈"))
# # except Exception as e:
# #     print(e.args[0])
#
print(myPad.createSession(groupid,authorid,9999999999))
padid=myPad.createGroupPad(groupid,"abc123").get('padID')
print(padid)
readonlyID=myPad.getReadOnlyID(padid).get('readOnlyID')
print(readonlyID)
# padid=myPad.createGroupPad(groupid,"xixixi").get('padID')
# myPad.setText(padid,"adsadasdasdas")
# myPad.saveRevision(padid)
# myPad.setText(padid,"sdasdasd")
# myPad.setText(padid,"sdfdsfdsfdasdasd")
# myPad.saveRevision(padid)
# print(myPad.listSavedRevisions(padid))
# print(myPad.getText(padid,3))
# padid=myPad.createGroupPad(groupid,"abc").get('pid')
# print(padid)
# myPad.setText("hhha","sdasdasd")
