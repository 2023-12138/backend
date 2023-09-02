from py_etherpad import EtherpadLiteClient
import datetime
import time
myPad = EtherpadLiteClient('4c87155dea77eb7c2927025bc807ee87304e5bf06239ba1439c17c1efa2e6c4e','http://43.138.59.36:10010/api')
# groupid=myPad.createGroup().get('groupID')
# # authorid=myPad.createAuthor("hhhh").get('authorID')
# print(groupid)
# authorid = myPad.createAuthor("abc").get('authorID')
# print(authorid)
# # # print(myPad.createGroupPad(groupid,"哈哈哈哈"))
# # # try:
# # #     print(myPad.createGroupPad(groupid,"哈哈哈哈"))
# # # except Exception as e:
# # #     print(e.args[0])
# #
# print(myPad.createSession(groupid,authorid,9999999999))
# padid=myPad.createGroupPad(groupid,"abc123").get('padID')
# print(padid)
# readonlyID=myPad.getReadOnlyID(padid).get('readOnlyID')
# print(readonlyID)
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
# myPad.setText("123",'''
# # 项目计划
# ## 1. 项目概述
# 1.1 项目名称
# 在这个部分，写明项目的名称。
# 1.2 项目目标
# 在这个部分，描述项目的目标和预期成果。
# 1.3 项目范围
# 在这个部分，明确项目的范围和所涉及的工作内容。
# 1.4 项目目标受众
# 在这个部分，说明项目的目标受众，即项目成果将影响或服务的人群。
# 2. 项目计划2.1 关键里程碑
# 在这个部分，列出项目的关键里程碑，包括计划开始和完成的日期。
# 2.2 项目阶段和任务
# 在这个部分，将项目划分为不同的阶段，并为每个阶段列出相应的任务和预计时间。
# 2.3 项目资源
# 在这个部分，明确项目所需的各种资源，包括人力资源、物资和设备等。
# 2.4 项目风险管理
# 在这个部分，描述项目风险管理计划，包括风险识别、评估和应对策略等。
# 2.5 项目沟通计划
# 在这个部分，说明项目的沟通计划，包括沟通渠道、频率和相关人员等。
# 2.6 项目质量计划
# 在这个部分，描述项目的质量计划，包括质量标准、质量控制和质量保证措施等。
# 2.7 项目预算
# 在这个部分，列出项目的预算，包括成本估算和资源分配等。
# 2.8 项目验收标准
# 在这个部分，明确项目的验收标准，即达到何种程度才能被认为是成功完成。
# 3. 项目团队3.1 项目组织结构
# 在这个部分，说明项目的组织结构，包括项目经理、团队成员和相关职责等。
# 3.2 关键角色和责任
# 在这个部分，列出项目中的关键角色和责任，确保每个角色的职责清晰明确。
# 3.3 人员资源计划
# 在这个部分，描述项目的人员资源计划，包括人员需求、招聘和培训等。
# 4. 项目监控和评估4.1 进度监控
# 在这个部分，描述项目进度的监控方法和工具，以及定期报告和评估的频率。
# 4.2 质量监控
# 在这个部分，说明项目质量的监控方法和工具，以及定期检查和评估的方式。
# 4.3 风险监控
# 在这个部分，描述项目风险的监控方法和工具，以及及时应对和调整的措施。
# 4.4 成本监控
# 在这个部分，说明项目成本的监控方法和工具，以及定期审计和调整的方式。
# 5. 变更管理5.1 变更控制流程
# 在这个部分，描述项目的变更控制流程，包括变更申请、评估和批准的步骤。
# 5.2 变更影响评估
# 在这个部分，说明如何评估变更对项目目标、进度、成本和质量的影响。
# 5.3 变更通知和沟通
# 在这个部分，描述变更通知和沟通的方式和流程，确保变更信息能够及时传达给相关人员。
# 6. 项目关闭6.1 项目交付物
# 在这个部分，列出项目的交付物和完成标准，确保项目交付物符合预期要求。
# 6.2 项目总结和评估
# 在这个部分，描述项目的总结和评估过程，包括项目成功度评估和经验教训总结等。
# 6.3 后续行动
# 在这个部分，说明项目结束后需要执行的后续行动，如文档归档、知识转移和资源清理等。
# ''')
#
# myPad.deletePad("项目计划书")
# myPad.deletePad("项目管理")
# myPad.deletePad("架构设计说明书")
# myPad.deletePad("工作周报")
# template='会议纪要'
# myPad.copyPad(template,"123",True)
# print(myPad.getReadOnlyID("123"))
myPad.copyPad("g.AtnBIuFp96IMbsvW$会议","会议22",True)
print(myPad.getReadOnlyID("会议"))