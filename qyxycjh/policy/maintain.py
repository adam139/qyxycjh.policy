# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from my315ok.socialorgnization.content.orgnization import IOrgnization,IOrgnization_annual_survey

from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder
from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility

orglist =[
"湘潭市企业联合会",
"湘潭市珠算协会",
"湘潭市科技情报学会",
"湘潭市建设工程造价管理协会",
"湘潭市建筑业协会",
"湘潭市计划生育协会",
"湘潭市民营企业家协会",
"湘潭市财政会计学会",
"湘潭市金融学会",
"湘潭市红十字会",
"湘潭市职工技术协会",
"湘潭市老科技工作者协会",
"湘潭市餐饮行业协会",
"江南工业集团有限公司职工技术协会",
"湘潭钢铁集团有限公司职工技术协会",
"湘乡铝厂职工技术协会",
"湘潭电厂职工技术协会",
"湘潭电业局职工技术协会",
"湘潭市土木建筑学会",
"湘潭市科技成果与技术市场协会",
"湘潭市印刷行业协会",
"湘潭市新闻工作者协会",
"湘潭市体育总会",
"湘潭公路管理局职工技术协会",
"江麓机电科技有限公司职工技术协会",
"湘潭市就业促进会",
"湘潭市消费者委员会",
"湘潭市基督教三自爱国运动委员会",
"湘潭市天主教爱国会",
"湘潭市佛教协会",
"湘潭市职工文化协会",
"湘潭市伊斯兰教协会",
"湘潭市道教协会",
"湘潭市思想政治工作研究会",
"湘潭市秘书学会",
"湘潭市商标广告协会",
"湘潭市外商投资企业协会",
"湘潭市电机工程学会",
"湘潭市青年企业家协会",
"湘潭市美术家协会",
"湘潭高新区个体劳动者私营企业协会",
"湘潭市作家协会",
"湘潭市翻译工作者协会",
"湘潭海外联谊会",
"湘潭市黄埔军校同学会",
"湘潭市老年书画家协会",
"湘潭市检察学会",
"湘潭市房地产业协会",
"湘潭市预算会计学会",
"湘潭市杂文学会",
"湘潭市农村经济学会",
"湘潭市档案学会",
"湘潭市税务学会",
"湘潭市交通学会",
"湘潭市护理学会",
"湘潭市烟草学会",
"湘潭市医学会",
"湘潭市中医药学会",
"湘潭市畜牧水产学会",
"湘潭市药学会",
"湘潭市粮食经济科技学会",
"湘潭市预防医学会",
"湘潭市林学会",
"湘潭市民俗文化学会",
"湘潭市价格协会",
"湘潭市卫生经济学会",
"湘潭市审计学会",
"湘潭市企业家协会",
"湘潭市统计学会",
"湘潭市干部教育研究会",
"湘潭市农学会",
"湘潭市诗词协会",
"湘潭市教育学会",
"湘潭市勘察设计协会",
"湘潭市集邮协会",
"湘潭市水利学会",
"湘潭市书法家协会",
"湘潭市抗癌协会",
"湘潭市老年学学会",
"湘潭市基层卫生协会",
"湘潭市戏剧家协会",
"湘潭市金融会计学会",
"湘潭市青年文学艺术家协会",
"湘潭市足球协会",
"湘潭市图书馆学会",
"湘潭海峡两岸经贸发展促进会",
"湘潭市企事业文学艺术界联合会",
"湘潭市人民对外友好协会",
"湘潭市希望工程促进会",
"湘潭市慈善总会",
"湘潭市社会组织促进会",
"湘潭市汽车维修协会",
"湘潭市建设有中国特色社会主义理论研究会",
"湘潭市机械化自动化学会",
"湘潭毛泽东思想研究会",
"湘潭市礼友经发联谊会",
"湘潭市学会工作研究会",
"湘潭市党建学会",
"湘潭市女检察官协会",
"湘潭市职工困难互助会",
"湘潭齐白石研究会",
"湘潭市钱币学会",
"湘潭市人民代表大会制度研究会",
"湘潭市花卉盆景协会",
"湘潭市注册会计师协会",
"湘潭市工商行政管理学会",
"湘潭市政策科学研究会",
"湘潭市少年儿童文学艺术家协会",
"湘潭市接待服务协会",
"湘潭市延安精神研究会",
"湘潭市纪检监察学会",
"湘潭市海外交流协会",
"湘潭市个体劳动者私营企业协会",
"湘潭市楹联学会",
"湘潭市摄影家协会",
"湘潭市音乐家协会",
"湘潭市社会福利事务管理协会",
"湘潭市律师协会",
"湘潭市警察协会",
"湘潭市专业技术人员奖励工作促进会",
"湘潭市见义勇为奖励促进会",
"湘潭市刑法学会",
"湘潭市广播电视学会",
"湘潭市港澳台侨经济文化交流促进会",
"湘潭市企业信用促进会",
"湘潭市社会科学学会工作研究会",
"湘潭市妇女人才联谊会",
"湘潭市摩托车商会",
"湘潭银行业协会",
"湘潭市旅游协会",
"湘潭市建设工程质量安全监督协会",
"湘潭市民间商会",
"湘潭保险行业协会",
"湘潭市机械工程学会",
"湘潭市农业机械学会",
"湘潭市计算机学会",
"湘潭市犯罪学研究会",
"湘潭市青少年科技教育协会",
"湘潭市建设监理协会",
"湘潭市市场发展促进会",
"湘潭市内部审计师协会",
"湘潭市房地产开发协会",
"湘潭雨湖诗社",
"湘潭市反邪教协会",
"湘潭市社区发展协会",
"湘潭市茶叶行业协会",
"湘潭市文明单位工作协会",
"湘潭市民间文艺家协会",
"湘潭市统一战线理论研究会",
"湘潭市文学研究会",
"湘潭市机械工业协会",
"湘潭市建设教育协会",
"湘潭市医疗保险学会",
"湘潭市企业职工养老保险协会",
"湘潭金桥公路职工技术协会",
"湘潭市文艺评论家协会",
"湘潭市消防协会",
"湘潭市民商法学会",
"湘潭市环境科学学会",
"湘潭市国际标准舞协会",
"湘潭市再生资源行业协会",
"湘潭市棋类协会",
"湘潭市服务业促进会",
"湘潭市气象学会",
"湘潭市风景园林协会",
"湘潭市民办教育协会",
"湘潭市设计艺术家协会",
"湘潭市养猪协会",
"湘潭市收藏协会",
"湘潭高新区消费者协会",
"湘潭市电力行业协会",
"湘潭市室内装饰行业协会",
"湘潭市学生体育协会",
"湘潭市建设工程招标投标协会",
"湘潭市机动车驾驶员培训协会",
"湘潭市曲艺家协会",
"湘潭市职业安全健康协会",
"湘潭市法官协会",
"湘潭市道路运输协会",
"湘潭市饲料行业协会",
"湘潭市酒业协会",
"湘潭市京剧票友协会",
"湘潭市武术协会",
"湘潭市游泳协会",
"湘潭市革命老区经济开发促进会",
"湘潭市金属材料商会",
"湘潭市国库工作研究会",
"湘潭市直机关书画家协会",
"湘潭市妇幼保健与优生优育协会",
"湘潭市花鸟画家协会",
"湘潭市汽车商会",
"湘潭市国土资源学会",
"湘潭市矿山装备行业协会",
"湘潭市粮食行业协会",
"湘潭市舞蹈家协会",
"湘潭市不动产业商会",
"湘潭市电子信息行业协会",
"湘潭市家用电器商会",
"湘潭环境保护协会",
"湘潭市老年保健协会",
"湘潭市经纪人协会",
"湘潭市计量测试检定所职工技术协会",
"湘潭市狩猎协会",
"湘潭市眼镜商会",
"湘潭市性病艾滋病防治协会",
"湘潭市诚信协会",
"湘潭市龙舟协会",
"湘潭市莲城书画研究会",
"湘潭市农业机械流通行业协会",
"湘潭市关心下一代爱心助学协会",
"湘潭市少数民族联谊会",
"湘潭市互联网上网服务协会",
"湘潭市物流与采购协会",
"湘潭市家居装饰材料商会",
"湘潭市五金机电商会",
"湘潭市女作家协会",
"湘潭离心机有限公司职工技术协会",
"湘潭市钢材深加工产业协会",
"湘潭市百货业商会",
"湘潭市知识分子联谊会",
"湘潭市国际税收研究会",
"湘潭市基层法律服务工作者协会",
"湘潭市质量协会",
"湘潭市侨商投资企业协会",
"湘潭市人民政协理论研究会",
"湘潭市法制新闻协会",
"湘潭市宝庆商会",
"湘潭市演讲与口才协会",
"湘潭市食品行业协会",
"湘潭市城乡规划协会",
"湘潭市司法鉴定协会",
"湘潭市禁毒协会",
"湘潭市咨询业协会",
"湘潭市红色文化研究会",
"湘潭市网球协会",
"湘潭市志愿者协会",
"湘潭市心理学会",
"湘潭市发明协会",
"湘潭市鸟类爱好者协会",
"湘潭市浙江商会",
"湘潭市自行车运动协会",
"湘潭市家政服务协会",
"湘潭市九华慈善会",
"湘潭市外经贸企业协会",
"湘潭市传统文化研究会",
"湘潭市当代音乐促进会",
"湘潭市民间艺术研究会",
"湘潭市《周易》文化研究会",
"湘潭市商务联合会",
"湘潭市汽车行业协会",
"湘潭市福建商会",
"湘潭市湘沪商务促进会",
"湘潭市九华示范区个体劳动者私营企业协会",
"湘潭市门球协会",
"湘潭市机关党建研究会",
"湘潭市卫生系统思想政治工作研究会",
"湘潭市桥牌协会",
"湘潭市燃气燃烧器具行业协会",
"湘潭市物业服务协会",
"湘潭市住房和城乡建设局职工技术协会",
"湘潭市医院协会",
"湘潭市冬泳协会",
"湘潭市羽毛球协会",
"湘潭市汽车用品商会",
"湘潭市残疾人企业家协会",
"湘潭市义工联合会",
"湘潭市衡阳商会",
"湘潭市建筑器材租赁商会",
"湘潭市出租汽车行业协会",
"湘潭市红木文化鉴赏协会",
"湘潭市电子商务协会",
"湘潭市国学研究会",
"湘潭市体育舞蹈协会",
"湘潭市青山桥乡土文化研究会",
"湘潭市水文职工技术协会",
"湘潭市农产品流通行业协会",
"湘潭市林业产业协会",
"湘潭市自驾游协会",
"湘潭市青年书法家协会",
"湘潭市浏阳商会",
"湘潭市登山协会",
"湘潭市蔬菜协会",
"湘潭市莲城清风义工协会",
"湘潭市市容环境卫生协会",
"湘潭市政法系统文学艺术工作者联合会",
"湘潭市渣土行业协会",
"湘潭市家具行业协会",
"湘潭市艺术收藏家协会",
"湘潭市岳阳商会",
"湘潭市石料行业协会",
"湘潭市隐山湖湘文化源研究会",
"湘潭市户外运动协会",
"湘潭市柔力球协会",
"湘潭市经济技术开发区（九华）消费者协会",
"湘潭市育婴师协会",
"湘潭市留学归国人员联谊会",
"湘潭市江西商会",
"湘潭市莲城志愿者协会",
"湘潭市科技模型运动协会",
"湘潭市德孝文化研究会",
"湘潭市巫家拳协会",
"湘潭市油画学会",
"湘潭市文化产业协会",
"湘潭市导游协会",
"湘潭市空竹运动协会",
"湘潭文化与发展研究会",
"湘潭市地方金融行业协会",
"湘潭市数据学会",
"湘潭市中小微企业金融促进会",
"湘潭市肾病互助协会",
"湘潭市孝亲敬老志愿者协会",
"湘潭市瑾源文化研究会",
"湘潭市爱立方志愿者协会",
"湘潭市快递行业协会",
"湘潭市陀螺协会",
"湘潭市沉香协会",
"湘潭市砖瓦行业协会",
"湘潭市预拌混凝土行业协会",
"湘潭韶山精神研究会",
"湘潭市关爱帕金森病志愿者协会",
"湘潭市婚庆行业协会",
"湘潭市佛学文化研究会",
"湘潭市钓鱼协会",
"湘潭市蜂业协会",
"湘潭市跑步协会",
"湘潭市生态农业产业商会",
"湘潭市松木及竹木家具行业协会",
"湘潭市信鸽协会",
"湘潭市益智实验中学",
"湘潭文理专修学院",
"湘潭市泽民中医类风湿病研究中心",
"湘潭融城设计艺术职业学校",
"湘潭新华电脑学校",
"湘潭厨师、服务师培训中心",
"湘潭市桑榆老年公寓",
"湘潭市旅游职业培训中心",
"湘潭市少儿特长启蒙学校",
"湘潭市民生社区综合服务中心",
"湘潭市精益眼视光研究所",
"湘潭市糖尿病中医中药临床研究中心",
"湘潭市飞翔职业技能培训中心",
"湘潭佳程涉外职业培训学校",
"湘潭市世纪风职业培训学校",
"湘潭市红十字建春医院",
"湘潭市红十字湘仁医院",
"湘潭市体育健康服务指导中心",
"湘潭天英职业技能培训学校",
"湘潭市华顺职业培训中心",
"湘潭市同升国济职业技能培训学校",
"湘潭千里马职业教育培训中心",
"湖南吉利汽车职业技术学院",
"湖南软件职业学院",
"湖南汽车工程师专修学院",
"湘潭新时代医院",
"湘潭市金康白癜风中医中药临床治疗研究中心",
"湘潭湘商文化研究中心",
"湘潭市银海职业技能培训学校",
"湘潭市美术创作中心",
"湘潭易道馆跆拳道培训中心",
"湘潭市人力资源培训学校",
"湘潭市创益扶困咨询中心",
"湘潭市永胜工程机械培训学校",
"湘潭市工商适应技术学校",
"湘潭市中凯人机速记职业培训中心",
"湘潭市金梦园养老服务中心",
"湘潭市阳光青少年俱乐部",
"湘潭市荆鹏职业教育培训中心",
"湘潭德盛职业技能培训学校",
"湘潭市飞扬跆拳道培训中心",
"湘潭市童心幼儿园",
"湘潭市昭山示范区童之园幼儿园",
"湘潭市易家湾南天幼儿园",
"湘潭市昭山示范区健康幼儿园",
"湘潭市江南悦意残疾人托养服务中心",
"湘潭市雨湖区九华杉山幼儿园",
"湘潭市雨湖区九华红旗好贝贝幼儿园",
"湘潭有色二十三冶医院",
"湘潭市雨湖区九华小星星幼儿园",
"湘潭爱民医院",
"湘潭市雨湖区九华启明星幼儿园",
"湘潭市雨湖区九华晨光幼儿园（科大园）",
"湘潭市雨湖区九华爱贝斯幼儿园",
"湘潭市俊丝美容职业技能培训学校",
"湘潭市雨湖区九华晨光幼儿园（杉山园）",
"湘潭市岳塘区高新第一幼儿园",
"湘潭市红太阳艺术团",
"湘潭市恒企职业技能培训学校",
"湘潭市海纳职业技能培训学校",
"湘潭市衣加衣公益服务中心",
         
          ]
def set_belendto(context):
    "process organizations list "
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IOrgnization.__identifier__}
    bns = pc(query)

#title value is bytestr that encoded by utf-8        

    for i in bns:
            title = i.Title
            if title in orglist:
                if i.orgnization_belondtoArea =="xiangtanshi":continue
                obj = i.getObject()
                obj.belondto_area = "xiangtanshi"
                obj.reindexObject()          

    return "pass" 


def batchcreatannualreport(context):
    """批量创建缺失的年检报告，仅限于市本级,仅用于2014年度年检"""
    from plone import namedfile
    import datetime
    catalog = getToolByName(context, "portal_catalog")
    wf = getToolByName(context, "portal_workflow")
    hege = ["湘潭市科技情报学会",
"湘潭市建设工程造价管理协会",
"湘潭市金融学会",
"湘潭市餐饮行业协会",
"江南工业集团有限公司职工技术协会",
"湘潭钢铁集团有限公司职工技术协会",
"湘乡铝厂职工技术协会",
"湘潭电厂职工技术协会",
"湘潭市土木建筑学会",
"湘潭市体育总会",
"湘潭公路管理局职工技术协会",
"江麓机电科技有限公司职工技术协会",
"湘潭市消费者委员会",
"湘潭市基督教三自爱国运动委员会",
"湘潭市天主教爱国会",
"湘潭市佛教协会",
"湘潭市职工文化协会",
"湘潭市道教协会",
"湘潭市外来投资企业协会",
"湘潭市电机工程学会",
"湘潭市作家协会",
"湘潭市翻译工作者协会",
"湘潭市老年书画家协会",
"湘潭市检察学会",
"湘潭市房地产业协会",
"湘潭市杂文学会",
"湘潭市农村经济学会",
"湘潭市档案学会",
"湘潭市税务学会",
"湘潭市护理学会",
"湘潭市烟草学会",
"湘潭市医学会",
"湘潭市中医药学会",
"湘潭市药学会",
"湘潭市粮食经济科技学会",
"湘潭市预防医学会",
"湘潭市林学会",
"湘潭市民俗文化学会",
"湘潭市统计学会",
"湘潭市农学会",
"湘潭市诗词协会",
"湘潭市集邮协会",
"湘潭市书法家协会",
"湘潭市基层卫生协会",
"湘潭市戏剧家协会",
"湘潭市金融会计学会",
"湘潭市青年文学艺术家协会",
"湘潭市足球协会",
"湘潭市图书馆学会",
"湘潭市企事业文学艺术界联合会",
"湘潭市人民对外友好协会",
"湘潭市汽车维修协会",
"湘潭市机械化自动化学会",
"湘潭市礼友经发联谊会",
"湘潭市学会工作研究会",
"湘潭齐白石研究会",
"湘潭市钱币学会",
"湘潭市人民代表大会制度研究会",
"湘潭市注册会计师协会",
"湘潭市少年儿童文学艺术家协会",
"湘潭市接待服务协会",
"湘潭市延安精神研究会",
"湘潭市纪检监察学会",
"湘潭市海外交流协会",
"湘潭市个体劳动者私营企业协会",
"湘潭市楹联家协会",
"湘潭市摄影家协会",
"湘潭市音乐家协会",
"湘潭市警察协会",
"湘潭市见义勇为奖励促进会",
"湘潭市刑法学会",
"湘潭市企业信用促进会",
"湘潭市妇女人才联谊会",
"湘潭银行业协会",
"湘潭市旅游协会",
"湘潭市民间商会",
"湘潭保险行业协会",
"湘潭市机械工程学会",
"湘潭市农业机械学会",
"湘潭市犯罪学研究会",
"湘潭雨湖诗社",
"湘潭市反邪教协会",
"湘潭市茶叶行业协会",
"湘潭市文明单位工作协会",
"湘潭市民间文艺家协会",
"湘潭市文学研究会",
"湘潭市医疗保险学会",
"湘潭市文艺评论家协会",
"湘潭市再生资源行业协会",
"湘潭市棋类协会",
"湘潭市服务业促进会",
"湘潭市气象学会",
"湘潭市风景园林协会",
"湘潭市收藏协会",
"湘潭高新区消费者协会",
"湘潭市电力行业协会",
"湘潭市学生体育协会",
"湘潭市机动车驾驶员培训协会",
"湘潭市曲艺家协会",
"湘潭市职业安全健康协会",
"湘潭市道路运输协会",
"湘潭市京剧票友协会",
"湘潭市武术协会",
"湘潭市游泳协会",
"湘潭市金属材料商会",
"湘潭市国库工作研究会",
"湘潭市直机关书画家协会",
"湘潭市妇幼保健与优生优育协会",
"湘潭市花鸟画家协会",
"湘潭市汽车商会",
"湘潭市矿山装备行业协会",
"湘潭市粮食行业协会",
"湘潭市不动产业商会",
"湘潭市电子信息行业协会",
"湘潭市家用电器商会",
"湘潭市老年保健协会",
"湘潭市经纪人协会",
"湘潭市计量测试检定所职工技术协会",
"湘潭市狩猎协会",
"湘潭市眼镜商会",
"湘潭市龙舟协会",
"湘潭市莲城书画研究会",
"湘潭市农业机械流通行业协会",
"湘潭市关心下一代爱心助学协会",
"湘潭市少数民族联谊会",
"湘潭市物流与采购联合会",
"湘潭市五金机电商会",
"湘潭市女作家协会",
"湘潭离心机有限公司职工技术协会",
"湘潭市国际税收研究会",
"湘潭市基层法律服务工作者协会",
"湘潭市侨商投资企业协会",
"湘潭市人民政协理论研究会",
"湘潭市宝庆商会",
"湘潭市食品行业协会",
"湘潭市城乡规划协会",
"湘潭市禁毒协会",
"湘潭市咨询业协会",
"湘潭市鸟类爱好者协会",
"湘潭市浙江商会",
"湘潭市自行车运动协会",
"湘潭市家政服务协会",
"湘潭市九华慈善会",
"湘潭市传统文化研究会",
"湘潭市民间艺术研究会",
"湘潭市商务联合会",
"湘潭市汽车行业协会",
"湘潭市福建商会",
"湘潭市物业服务协会",
"湘潭市医院协会",
"湘潭市冬泳协会",
"湘潭市羽毛球协会",
"湘潭市汽车用品商会",
"湘潭市残疾人企业家协会",
"湘潭市义工联合会",
"湘潭市衡阳商会",
"湘潭市建筑器材租赁商会",
"湘潭市出租汽车行业协会",
"湘潭市电子商务协会",
"湘潭市国学研究会",
"湘潭市体育舞蹈协会",
"湘潭市青山桥乡土文化研究会",
"湘潭市水文职工技术协会",
"湘潭市林业产业协会",
"湘潭市浏阳商会",
"湘潭市市容环境卫生协会",
"湘潭市石料行业协会",
"湘潭市经济技术开发区（九华）消费者协会",
"湘潭市育婴师协会",
"湘潭市留学归国人员联谊会",
"湘潭市江西商会",
"湘潭市巫家拳协会",
"湘潭市油画学会",
"湘潭市空竹运动协会",
"湘潭市地方金融行业协会",
"湘潭市数据学会",
"湘潭市中小微企业金融促进会",
"湘潭市肾病互助协会",
"湘潭市《周易》文化研究会",
"湘潭市企业联合会",
"湘潭市企业家协会",
"湘潭市花卉盆景协会",
"湘潭市律师协会",
"湘潭市广播电视学会",
"湘潭市科技模型运动协会",
"湘潭市统一战线理论研究会",
"湘潭市珠算协会",
"湘潭市财政会计学会",
"湘潭市计算机学会",
"湘潭市国土资源学会",
"湘潭市莲城清风义工协会",
"湘潭市老科技工作者协会",
"湘潭市蔬菜协会",
"湘潭市家具行业协会",
"湘潭市青年企业家协会",
"湘潭市希望工程促进会",
"湘潭市志愿者协会",
"湘潭市建筑业协会",
"湘潭市抗癌协会",
"湘潭市当代音乐促进会",
"湘潭市政法系统文学艺术工作者联合会",
"湘潭市渣土行业协会",
"湘潭市孝亲敬老志愿者协会",
"湘潭市社会福利事务管理协会",
"湘潭市慈善总会",
"湘潭市室内装饰行业协会",
"湘潭环境保护协会",
"湘潭市家居装饰材料商会",
"湘潭市钢材深加工产业协会",
"湘潭市思想政治工作研究会",
"湘潭市莲城志愿者协会",
"湘潭市柔力球协会",
"湘潭市卫生经济学会",
"湘潭海外联谊会",
"湘潭市知识分子联谊会",
"湘潭市质量协会",
"湘潭市九华示范区个体劳动者私营企业协会",
"湘潭市门球协会",
"湘潭市燃气燃烧器具行业协会",
"湘潭市糖尿病中医中药临床研究中心",
"湘潭市世纪风职业培训学校",
"湘潭市红十字建春医院",
"湘潭天英职业技能培训学校",
"湘潭易道馆跆拳道培训中心",
"湘潭市工商适应技术学校",
"湘潭市飞扬跆拳道培训中心",
"湘潭市童心幼儿园",
"湘潭市雨湖区九华杉山幼儿园",
"湘潭市雨湖区九华红旗好贝贝幼儿园",
"湘潭有色二十三冶医院",
"湘潭市雨湖区九华小星星幼儿园",
"湘潭市雨湖区九华启明星幼儿园",
"湘潭市雨湖区九华爱贝斯幼儿园",
"湘潭市雨湖区九华晨光幼儿园（杉山园）",
"湘潭市创益扶困咨询中心",
"湘潭市易家湾南天幼儿园",
"湘潭爱民医院",
"湘潭文理专修学院",
"湘潭市泽民中医类风湿病研究中心",
"湘潭新华电脑学校",
"湘潭市精益眼视光研究所",
"湘潭佳程涉外职业培训学校",
"湘潭市红十字湘仁医院",
"湘潭市华顺职业培训中心",
"湘潭市同升国济职业技能培训学校",
"湘潭千里马职业教育培训中心",
"湖南吉利汽车职业技术学院",
"湖南软件职业学院",
"湖南汽车工程师专修学院",
"湘潭新时代医院",
"湘潭市银海职业技能培训学校",
"湘潭市人力资源培训学校",
"湘潭市中凯人机速记职业培训中心",
"湘潭市阳光青少年俱乐部",
"湘潭德盛职业技能培训学校",
"湘潭市昭山示范区童之园幼儿园",
"湘潭市江南悦意残疾人托养服务中心",
"湘潭市岳塘区高新第一幼儿园",
"湘潭市红太阳艺术团",
"湘潭市金康白癜风中医中药临床治疗研究中心",
"湘潭市恒企职业技能培训学校",
"湘潭市荆鹏职业教育培训中心",
"湘潭市昭山示范区健康幼儿园",
                ]
    jibenhege = [
                    "湘潭市民营企业家协会",
"湘潭市科技成果与技术市场协会",
"湘潭市伊斯兰教协会",
"湘潭高新区个体劳动者私营企业协会",
"湘潭市勘察设计协会",
"湘潭市水利学会",
"湘潭市工商行政管理学会",
"湘潭市房地产开发协会",
"湘潭市互联网上网服务协会",
"湘潭市司法鉴定协会",
"湘潭市爱立方志愿者协会",
"湘潭市德孝文化研究会",
"湘潭市商标广告协会",
"湘潭市建设工程质量安全监督协会",
"湘潭市建设监理协会",
"湘潭市网球协会",
"湘潭市桥牌协会",
"湘潭市演讲与口才协会",
"湘潭市登山协会",
"湘潭市女检察官协会",
"湘潭市印刷行业协会",
"湘潭市户外运动协会",
"湘潭市干部教育研究会",
"湘潭市青年书法家协会",
"湘潭市美术家协会",
"湘潭市审计学会",
"湘潭市职工技术协会",
"湘潭市设计艺术家协会",
"湘潭市湘沪商务促进会",
"湘潭市岳阳商会",
"湘潭市舞蹈家协会",
"湘潭市隐山湖湘文化源研究会",
"湘潭市民办教育协会",
"湘潭市发明协会",
"湘潭市内部审计师协会",
"湘潭市摩托车商会",
"湘潭市养猪协会",
"湘潭市外贸企业协会",
"湘潭市红色文化研究会",
"湘潭市百货业商会",
"湘潭市导游协会",
"湘潭市社会组织促进会",
"湘潭市体育健康服务指导中心",
"湘潭市俊丝美容职业技能培训学校",
"湘潭市旅游职业培训中心",
"湘潭市少儿特长启蒙学校",
"湘潭市益智实验中学",
"湘潭湘商文化研究中心",
"湘潭市飞翔职业技能培训中心",
"湘潭市金梦园养老服务中心",
"湘潭厨师、服务师培训中心",
"湘潭市永胜工程机械培训学校",
"湘潭融城设计艺术职业学校"
                    ]
    buhege = [
"湘潭市新闻工作者协会",
"湘潭市就业促进会",
"湘潭市预算会计学会",
"湘潭海峡两岸经贸发展促进会",
"湘潭市职工困难互助会",
"湘潭市专业技术人员奖励工作促进会",
"湘潭市市场发展促进会",
"湘潭市建设教育协会",
"湘潭金桥公路职工技术协会",
"湘潭市消防协会",
"湘潭市环境科学学会",
"湘潭市建设工程招标投标协会",
"湘潭市法官协会",
"湘潭市饲料行业协会",
"湘潭市酒业协会",
"湘潭市性病艾滋病防治协会",
"湘潭市诚信协会",
"湘潭市法制新闻协会",
"湘潭市心理学会",
"湘潭市机关党建研究会",
"湘潭市瑾源文化研究会",
"湘潭市住房和城乡建设局职工技术协会",
"湘潭市建设有中国特色社会主义理论研究会",
"湘潭市毛泽东思想研究会",
"湘潭市价格协会",
"湘潭市秘书学会",
"湘潭市社区发展协会",
"湘潭市革命老区经济开发促进会",
"湘潭市教育学会",
"湘潭市青少年科技教育协会",
"湘潭市交通学会",
"湘潭市畜牧水产学会",
"湘潭市社会科学学会工作研究会",
"湘潭市政策科学研究会",
"湘潭市民商法学会",
"湘潭市艺术收藏家协会",
"湘潭市红木文化鉴赏协会",
"湘潭市农产品流通行业协会",
"湘潭市自驾游协会",
"湘潭市文化产业协会",
"湘潭市民生社区综合服务中心",
"湘潭市美术创作中心",
"湘潭市雨湖区九华晨光幼儿园（科大园）"
                  
                  ]

    query = {"object_provides":IOrgnization.__identifier__,
             "orgnization_belondtoArea":"xiangtanshi"}
#             "orgnization_orgnizationType":"minfei"}
    bns = catalog(query)

    for i in bns:
            title = i.Title            
            brains = catalog({'path':i.getPath(),'id':'2014','object_provides':IOrgnization_annual_survey.__identifier__})
            num = len(brains)
#            import pdb
#            pdb.set_trace()
            if num == 0:
                newid = "2014"
#                import pdb
#                pdb.set_trace()
#                if not isinstance(newid, unicode):
#                    newid = unicode(newid, 'utf-8')
#                surveyid = IUserPreferredFileNameNormalizer(self.request).normalize(newid)
                item =createContentInContainer(i.getObject(),"my315ok.socialorgnization.orgnizationsurvey",checkConstraints=False,id=newid)
                item.title = title
                if title in jibenhege:
                    item.annual_survey = "jibenhege"
                    item.sponsor_comments = item.agent_comments = u"基本合格"
                    
                elif title in hege:                                                                                
                    item.annual_survey = "hege"
                    item.sponsor_comments = item.agent_comments = u"合格"                    
                elif title in buhege:
                    item.annual_survey = "buhege"
                    item.sponsor_comments = item.agent_comments = u"不合格" 
                else:
                    continue                                                                              
                item.year = "2014"
                item.sponsor_audit_date = datetime.datetime.today() + datetime.timedelta(-20)
                item.agent_audit_date = datetime.datetime.today() + datetime.timedelta(-15)
#                import pdb
#                pdb.set_trace()
                item.report = namedfile.NamedBlobFile(u'已提交纸质年检报告', filename=u"2014report.doc")            
                wf.doActionFor(item, 'publish', comment="publish" )
                item.reindexObject()
    return "pass"       
