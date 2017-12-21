import re
from enum import Enum
RE_EMAIL = re.compile('..*@.*\..*')
RE_NAME = re.compile(
    u"^[ \u4e00-\u9fa5_＿ａ-ｚＡ-Ｚa-zA-Z0-9０-９\`\~\!\@\#\$\%\^\&()\-\_\=\+\[\{\]\}\',.·￣！＠＃￥％……＆×（）－——＝＋【｛】｝、｜；：「」『』‘’”“，《。》、？～＄＾＊＿]+$"
)
ROLES = ((0, '管理员'), (1, '经理'), (2, '成员'))
STATUS = ((-1, "全部"), (0, "停用"), (1, "启用"))
ProjectStatus = (
    (1, '下单'),
    (2, '转发'),  # 转发已经完成
    (3, '设计报价'),
    (4, '审核'),  # 领导审核
    (5, '审核'),  # 客户签字
    (6, '审核'),  # 商务部审核
    (7, '发货'),  # 仓库发货
    (8, '实施'),  # 工程部实施
    (9, '签字'),  # 客户签字确认
    (0, '终止')  # 项目终止结束
)

class Step(object):
    def __init__(self, step):
        self.step = step

    def ok(self, group, role):
        pass

# 部门的项目权限
StatusByRole = {'1':
    {
        'group': ['商务部']
    },
    '2':
    {
        'group': ['设计部']
    },
    '3':
    {
        'group': ['设计部']
    },
    '4':
    {
        'group': ['管理员']
    },
    '5':
    {
        'group': ['商务部']
    },
    '6':
    {
        'group': ['仓库']
    },
    '7':
    {
        'group': ['工程部']
    },
    '8':
    {
        'group': []
    },
    '9':
    {
        'group': ['商务部', '管理员']
    }
}
projectStatus = dict(ProjectStatus) # 0: '下单'
projectStatusReverse = {y: x for x, y in ProjectStatus} #  '下单': 0
StatusInRole = dict()
for action, value in StatusByRole.items():
    for g in value['group']:
        if g not in StatusInRole:
            StatusInRole[g] = []
        StatusInRole[g].append(dict(name=action, value=action))

# 沟通中 实施中

# 工程部工作附件
ENGINEER_ATTACHMENT = (('admission', '进场凭证'), ('implement', '施工凭证'),
                       ('complete', '竣工凭证'), ('checked', '验收凭证'), ('other',
                                                                   '其他'))
READ = (("0", "未读"), ("1", "已读"))
GROUP = (("internal", "对内"), ("external", "对外"))

SOURCES = ((9, "荣誉资质"), (1, "合作伙伴"), (2, "操作视频"), (3, "文档下载"), (4, "合同"),
           (5, "签证"), (6, '常用软件'), (7, '设计方案'), (8, '说明文档'), (0, '全部文档'))

DOCUMENTS = ((0, "全部文档"), (1, "说明文档"), (2, "常用软件"), (3, "设计方案"), (4, "签证"),
             (5, '项目材料'))
CredentialKeyMap = dict((('email', "邮箱"), ('mobile', "手机")))

GENDER = (("male", "男"), ("female", "女"))

MESSAGE = ((0, '全部消息'), )

NEWS = ((0, '全部新闻'), (4, '首页公告'), (1, '公司新闻'), (2, '公益咨询'), (3, '咨询文章'))

ProjectLog = ((1, '签字'), (2, '审核'), (3, '协助申请'), (4, '工作日志'), (5, '设计报价'),
              (6, '发货'), (7, '驳回'), (8, '转发'))

ProjectLogMap = {y: x for (x, y) in ProjectLog}
ProjectLogMapReverse = {x: y for (x, y) in ProjectLog}

ProjectType = (('create', '新建项目'), ('maintain', '故障维护'), ('remove', '迁移、拆除'),
               ('exhibition', '展会协助'))