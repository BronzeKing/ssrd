import re
RE_EMAIL = re.compile('..*@.*\..*')
RE_NAME = re.compile(
    u"^[ \u4e00-\u9fa5_＿ａ-ｚＡ-Ｚa-zA-Z0-9０-９\`\~\!\@\#\$\%\^\&()\-\_\=\+\[\{\]\}\',.·￣！＠＃￥％……＆×（）－——＝＋【｛】｝、｜；：「」『』‘’”“，《。》、？～＄＾＊＿]+$"
)
# 0 - 9  内部员工
# 11-19 行业用户
# 20-29 分销商
ROLES = ((0, "ADMIN"), (1, 'BOSS'), (10, '市场部'), (11, '市场部组长'), (12, '市场部组员'),
         (20, '工程部'), (21, '工程部经理'), (22, '工程部组长'), (23, '工程部组员'),
         (31, "行业用户"), (32, "分销商"), (41, "个人用户"), (42, "常规用户"))
STATUS = ((-1, "全部"), (0, "停用"), (1, "启用"))
ORDER_STATUS = ((1, "用户下订单"), (2, "商务部对接转发"), (3, "设计部上传方案报价"), (4, "领导审核"),
                (5, "客户审核上传确认"), (6, "商务部审核"), (7, '仓库发货'), (8, "工程部实施"),
                (9, "客户签字确认"), (0, '终止'))

# 沟通中 实施中

# 工程部工作附件
ENGINEER_ATTACHMENT = (('admission', '进场凭证'), ('implement', '施工凭证'),
                       ('complete', '竣工凭证'), ('checked', '验收凭证'), ('other',
                                                                   '其他'))
READ = (("0", "未读"), ("1", "已读"))

SOURCES = ((0, "荣誉资质"), (1, "合作伙伴"), (2, "操作视频"), (3, "文档下载"), (4, "合同"),
           (5, "签证"), (6, '常用软件'), (7, '设计方案'), (8, '说明文档'), (-1, '全部文档'))
CredentialKeyMap = dict((('email', "邮箱"), ('mobile', "手机")))

GENDER = (("male", "男"), ("female", "女"))

MESSAGE = ((0, '全部消息'), )

NEWS = ((0, '全部新闻'), (1, '公司新闻'), (2, '公益咨询'), (3, '咨询文章'))

ProjectLog = ((1, '签字'), (2, '审核'), (3, '协助申请'), (4, '工作日志'), (5, '设计报价'),
              (6, '发货'))
ProjectLogMap = {y: x for (x, y) in ProjectLog}

ProjectType = (('create', '新建项目'), ('maintain', '故障维护'), ('remove', '迁移、拆除'))