from py_etherpad import EtherpadLiteClient
import datetime
import time
myPad = EtherpadLiteClient('08ed388c84d03eebf6745356d5e61534843cbf75fb48ef5e8628c4b24a9150a1','http://43.138.59.36:10010/api')
groupid=myPad.createGroup().get('groupID')
# authorid=myPad.createAuthor("hhhh").get('authorID')
print(groupid)
authorid = myPad.createAuthor("sadasd").get('authorID')
print(authorid)
# # print(myPad.createGroupPad(groupid,"哈哈哈哈"))
# # try:
# #     print(myPad.createGroupPad(groupid,"哈哈哈哈"))
# # except Exception as e:
# #     print(e.args[0])
#
print(myPad.createSession(groupid,authorid,9999999999))
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
