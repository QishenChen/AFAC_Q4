# 区域性股权市场跨链数据规范

# Specification for regional equity markets cross-chain data

2024-11-20 发布

2024-11-20 实施

## 目次

前言....II

引言.... III

1 范围.... 1  
2 规范性引用文件.... 1  
3 术语和定义 …… 1  
4 跨链数据分类.... 2  
5 主体对象信息 2  
6 账户对象信息.... 3  
7 产品对象信息.... 4  
8 转让报告对象信息....6  
9 登记对象信息....6  
10 资金结算对象信息 …… 7  
11 信披对象信息....8  
12 财务报表信息 9  
13 监管信息.... 10

附录A（规范性）跨链数据模型 11

A.1 主体模型设计 …… 11  
A.2 账户模型设计 23  
A.3 产品模型设计....26  
A.4 转让报告模型设计 38  
A.5 登记模型设计 42  
A.6 资金结算模型设计.... 49  
A.7 信披模型设计 …… 51  
A.8 财务报表模型设计 61  
A.9 监管模型设计 86  
A.10 枚举项信息 90  
A.11 预定义类型信息.... 131

参考文献....133

## 前言

本文件按照GB/T 1.1—2020《标准化工作导则 第1部分：标准化文件的结构和起草规则》的规定起草。

请注意本文件的某些内容可能涉及专利。本文件的发布机构不承担识别专利的责任。

本文件由全国金融标准化技术委员会证券分技术委员会（SAC/TC 180/SC4）提出。

本文件由全国金融标准化技术委员会（SAC/TC 180）归口。

本文件起草单位：中国证券监督管理委员会科技监管司、中国证券监督管理委员会市场监管二司、中证信息技术服务有限责任公司、深圳证券通信有限公司、南京大学、同济大学、北京股权交易中心有限公司、江苏股权交易中心有限责任公司、上海股权托管交易中心股份有限公司、浙江省股权交易中心有限公司、深圳前海股权交易中心有限公司、上海边界智能科技有限公司、中诚区块链研究院（南京）有限公司、南京数字金融产业研究院有限公司、梧桐链数字科技研究院（苏州）有限公司、中钞信用卡产业发展有限公司杭州区块链技术研究院。

本文件主要起草人：彭枫、赵滨、谷新萍、王凤冬、李宇、陈柏峰、王继伟、杨博、马堃、曹恒、太贤美、陈莹、马小峰、李思颖、陈小泉、王强、朱培、周耀亮、林智辰、葛浩、陶祖国、邵洪峰、孙北北、胡爽峰、肖东、迟云蔚、万强、叶蔚、张一锋、王加楠。

## 引言

区域性股权市场是服务所在省级行政区域内中小微企业的私募股权市场，是多层次资本市场体系重要组成部分，是地方扶持中小微企业政策措施的综合运用平台，也是一类地方金融组织。同时要看到，区域性股权市场也存在功能发挥不畅、地方监管制度体系不完善、业务系统多样异构、数据规范性差、业务规则不完备等问题。区块链具有数据透明、不易篡改、可追溯等技术优势，在促进数据共享、优化业务流程、降低运营成本、提升协同效率、建设可信体系等方面具有积极作用。基于监管链和地方业务链的双层架构，可以更好支持区域性股权市场企业赋能服务、业务创新并逐步实现穿透式监管。为建成物理分散、逻辑统一的区域性股权市场新型金融基础设施，有必要定义监管链与各地方业务链的跨链对接数据规范。

本规范在全面调研区域性股权市场业务规范和各地方业务种类、业务流程、业务数据的基础上，充分考虑区域性股权市场的主要业务情况，从主体、账户、产品、转让报告、登记、资金结算、信披、财务报表、监管九个维度对业务数据信息进行了定义和详细描述。基于以上信息，建立了区域性股权市场逻辑统一的跨链数据规范。

# 区域性股权市场跨链数据规范

## 1 范围

本文件规定了区域性股权市场中地方业务链与监管链跨链对接的数据规范，包含跨链数据分类、主体对象信息要求、账户对象信息要求、产品对象信息要求、转让报告对象信息要求、登记对象信息要求、资金结算对象信息要求、信披对象信息要求、财务报表对象信息要求、监管对象信息要求。

本文件适用于证券期货业机构在区域性股权市场中进行地方业务链及与地方业务链对接的地方业务系统建设或服务运营。

注：本文件不适用于涉及国家秘密的数据。

## 2 规范性引用文件

下列文件中的内容通过文中的规范性引用而构成本文件必不可少的条款。其中，注日期的引用文件，仅该日期对应的版本适用于本文件；不注日期的引用文件，其最新版本（包括所有的修改单）适用于本文件。

GB/T 2260 中华人民共和国行政区划代码

GB/T 11457 信息技术 软件工程术语

GB/T 12406 表示货币的代码

GB/T 18391.1 信息技术 元数据注册系统（MDR） 第1部分：框架

GB/T 20000.1 标准化工作指南 第1部分：标准化和相关活动的通用术语

GB/T 25069 信息安全技术 术语

## 3 术语和定义

GB/T 11457、GB/T 18391.1、GB/T 20000.1、GB/T 25069界定的以及下列术语和定义适用于本文件。

3.1

跨链 cross chain

实现在区块链之间的双向信息交互、信息验证与服务调用的技术。

3.2

属性 attribute

一个对象或实体的特征。

[来源：GB/T 18391.1，3.1.1]

3.3

类 class

具有相同属性、操作、方法、关系和语义的对象集合的描述。

[来源：GB/T 18391.1，3.1.2]

## 3.4

## 数据 data

信息的可再解释的形式化表示，以适用于通信、解释或处理。

注：数据可以由人工或自动的方式加工、处理。

[来源：GB/T 18391.1，3.2.6]

## 3.5

## 数据类型 datatype

一些可区分的值的集合，这种区别由这些值的性质以及对这些值的运算所表征。

[来源：GB/T 18391.1，3.3.11]

## 3.6

## 值 value

数据的值。

[来源：GB/T 18391.1，3.3.37]

## 3.7

值域 value domain; VD

允许值的集合。

[来源：GB/T 18391.1，3.3.38]

## 4 跨链数据分类

本文件涉及的跨链数据类型按主题划分为9个维度，主要包括实际业务中所涉及的主体（投资方、融资方、中介机构等）、账户（包含证券账户与资金账户）、非公开发行融资与挂牌产品、转让报告、登记、资金结算、信披等。

数据形成主体、账户、产品、转让报告、登记、资金结算、信披、财务报表、监管等数据分类。根据数据结构分类方案，按照对象类分为若干级别分类，基于该对象的实际业务填写必要或非必要的所有源数据的值。

## 5 主体对象信息

主体对象用于记录区域性股权市场各类参与方，既包括融资企业、投资方、中介机构，也包括交易市场、登记托管机构等。主体对象信息划分为1级到5级属性分类，属性分类应符合表1的内容。其中包括机构或个人主体的基本信息及通用信息、资质信息等；基于该主体的实际业务填写必要或非必要的所有源数据的值，如：姓名、统一社会信用代码、行政区域、资质类别、角色类型等。

表 1 主体对象信息分类表

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td><td>4级分类</td><td>5级分类</td></tr><tr><td>主体信息</td><td>主体基本信息</td><td>主体通用信息</td><td>—</td><td>—</td></tr><tr><td rowspan="11">主体信息</td><td rowspan="6">主体基本信息</td><td rowspan="6">主体资质信息</td><td>资质信息</td><td>—</td></tr><tr><td>资质认证信息</td><td>—</td></tr><tr><td rowspan="4">投资者适当性信息</td><td>投资者适当性信息</td></tr><tr><td>适当性分类信息</td></tr><tr><td>适当性基本信息</td></tr><tr><td>适当性文件信息</td></tr><tr><td rowspan="4">机构主体信息</td><td rowspan="4">机构基本信息</td><td>基本信息描述</td><td>—</td></tr><tr><td>人员构成统计信息</td><td>—</td></tr><tr><td>子公司/分支机构信息</td><td>—</td></tr><tr><td>主要人员信息</td><td>—</td></tr><tr><td>个人主体信息</td><td>个人主体基本信息</td><td>—</td><td>—</td></tr></table>

表 1 中第 3 级至 5 级分类的具体信息要求如下:

——3级分类：

- 主体通用信息应符合 A.1.1.1;  
- 个人主体基本信息应符合 A.1.3。

——4级分类-主体资质信息：

- 资质信息应符合 A.1.1.2.1;  
- 资质认证信息应符合 A.1.1.2.2。

——4级分类-机构基本信息：

- 基本信息描述应符合 A.1.2.1;  
- 人员构成统计信息应符合 A.1.2.2;  
- 子公司/分支机构信息应符合 A.1.2.3;  
- 主要人员信息应符合 A.1.2.4。

——5级分类-投资者适当性信息：

- 投资者适当性信息应符合 A.1.1.2.3，a）投资者适当性信息；  
- 适当性分类信息应符合 A.1.1.2.3，b）适当性分类信息；  
- 适当性基本信息应符合 A.1.1.2.3, c) 适当性基本信息;  
- 适当性文件信息应符合 A.1.1.2.3，d）适当性文件信息。

## 6 账户对象信息

账户对象用于记录市场主体开展证券和资金转让、托管等业务时在区域性股权市场开立的账户信息，包括证券账户、资金账户、游客账户三类。账户对象信息划分为1级到3级属性分类，应符合表2的要求。例如：2级子类包括账户基本信息、账户生命周期信息、账户关联信息。

用户根据实际业务的类别和信息层级，主要分为账户基本信息（含账户所属主体、账户类型、状态等）、账户生命周期（开户、销户、冻结、解冻）及账户关联信息（如：资金账户与证券账户关联关系、关联的账户主体与开户文件等）。

表 2 账户对象信息分类

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td></tr><tr><td rowspan="6">账户信息</td><td>账户基本信息</td><td>—</td></tr><tr><td rowspan="4">账户生命周期信息</td><td>开户信息</td></tr><tr><td>销户信息</td></tr><tr><td>冻结信息</td></tr><tr><td>解冻信息</td></tr><tr><td>账户关联信息</td><td>—</td></tr></table>

表2中第2级至3级分类的具体信息要求如下:

——2级分类：

- 账户基本信息应符合 A.2.1;  
- 账户关联信息应符合 A.2.3。

——3级分类-账户生命周期信息：

- 开户信息应符合 A.2.2.1;  
- 销户信息应符合 A.2.2.2;  
- 冻结信息应符合 A.2.2.3;  
- 解冻信息应符合 A.2.2.4。

## 7 产品对象信息

产品对象用于记录在区域性股权市场非公开发行转让、登记托管的各类证券和其他金融产品。产品对象信息划分为1级到4级属性分类，应符合表3的要求。例如：2级子类包括基本信息、产品标的信息、非公开发行信息、转让信息、托管信息、服务状态信息。产品对象对各类产品进行全生命周期管理，包括挂牌类产品、非公开发行类产品（股权、股份、可转债/合规发行的其他债券品种等）、托管类产品。

表 3 产品对象信息分类

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td><td>4级分类</td></tr><tr><td rowspan="12">产品信息</td><td rowspan="5">基本信息</td><td>产品基本信息</td><td>—</td></tr><tr><td rowspan="3">服务方信息</td><td>服务方基本信息</td></tr><tr><td>服务方收费</td></tr><tr><td>增信信息</td></tr><tr><td>产品文件信息</td><td>—</td></tr><tr><td rowspan="3">产品标的信息</td><td>资金用途信息</td><td>—</td></tr><tr><td>经营用途信息</td><td>—</td></tr><tr><td>投资组合信息</td><td>—</td></tr><tr><td rowspan="4">非公开发行信息</td><td>非公开发行基本信息</td><td>—</td></tr><tr><td>备案信息</td><td>—</td></tr><tr><td>私募股权非公开发行信息</td><td>—</td></tr><tr><td>可转债/合规发行的其他债券品种发行信息</td><td>可转债/合规发行的其他债券品种发行基本信息</td></tr><tr><td rowspan="8">产品信息</td><td>非公开发行信息</td><td>可转债/合规发行的其他债券品种发行信息</td><td>逾期信息</td></tr><tr><td rowspan="3">转让信息</td><td>转让状态信息</td><td>—</td></tr><tr><td>挂牌信息</td><td>—</td></tr><tr><td>摘牌信息</td><td>—</td></tr><tr><td>托管信息</td><td>—</td><td>—</td></tr><tr><td rowspan="3">服务状态信息</td><td>服务基本信息</td><td>—</td></tr><tr><td rowspan="2">停止服务信息</td><td>转板信息</td></tr><tr><td>收购信息</td></tr></table>

表3中第2级至4级分类的具体信息要求如下:

——2级分类：

\- 托管信息应符合 A.3.5。

——3级分类-基本信息：

- 产品基本信息应符合 A.3.1.1;  
- 产品文件信息应符合 A.3.1.3。

——3级分类-产品标的信息：

- 资金用途信息应符合 A.3.2.1;  
- 经营用途信息应符合 A.3.2.2;  
- 投资组合信息应符合 A.3.2.3。

——3级分类-非公开发行信息：

- 非公开发行基本信息应符合 A.3.3.1;  
- 备案信息应符合 A.3.3.2;  
- 私募股权非公开发行信息应符合 A.3.3.3。

——3级分类-转让信息：

- 转让状态信息应符合 A.3.4.1;  
- 挂牌信息应符合 A.3.4.2;  
- 摘牌信息应符合 A.3.4.3。

——3级分类-服务状态信息：

\- 服务基本信息应符合 A.3.6.1。

——4级分类-服务方信息：

- 服务方基本信息应符合A.3.1.2.1;  
- 服务方收费应符合 A.3.1.2.2;  
- 增信信息应符合 A.3.1.2.3。

——4级分类-可转债/合规发行的其他债券品种发行信息：

- 可转债/合规发行的其他债券品种发行基本信息应符合 A.3.3.4.1;  
- 逾期信息应符合 A.3.3.4.2。

——4级分类-停止服务信息：

- 转板信息应符合 A.3.6.2.1;  
- 收购信息应符合 A.3.6.2.2。

## 8 转让报告对象信息

转让报告对象用于记录在区域性股权市场开展的证券交易以及相关的场外金融交易。转让报告对象信息划分为1级到4级属性分类，应符合表4的要求，例如：2级子类包括转让基本信息、转让成交信息、交易中介信息。

表 4 转让报告对象信息

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td><td>4级分类</td></tr><tr><td rowspan="9">转让报告信息</td><td rowspan="4">转让基本信息</td><td>基本信息描述</td><td>—</td></tr><tr><td rowspan="3">转让资产信息</td><td>交易资产托管状态</td></tr><tr><td>已托管交易资产转让</td></tr><tr><td>未托管交易资产转让</td></tr><tr><td rowspan="4">转让成交信息</td><td>成交内容信息</td><td>—</td></tr><tr><td>融资类转让成交方信息</td><td>—</td></tr><tr><td>其他交易类型的转让成交方信息</td><td>—</td></tr><tr><td>成交核验信息</td><td>—</td></tr><tr><td>交易中介信息</td><td>—</td><td>—</td></tr></table>

表4中第2级至4级分类的具体信息要求如下：

——2级分类：

\- 交易中介信息应符合 A.4.3。

——3级分类-转让基本信息：

\- 基本信息描述应符合 A.4.1.1。

——3 级分类-转让成交信息：

- 成交内容信息应符合 A.4.2.1;  
- 融资类转让成交方信息应符合 A.4.2.2;  
- 其他交易类型的转让成交方信息应符合 A.4.2.3;  
- 成交核验信息应符合 A.4.2.4。

——4级分类-转让资产信息：

- 交易资产托管状态应符合 A.4.1.2.1;  
- 已托管交易资产转让应符合 A.4.1.2.2;  
- 未托管交易资产转让应符合 A.4.1.2.3。

## 9 登记对象信息

登记对象用于记录区域性股权市场参与主体的证券及其他权益的登记情况。登记对象信息划分为1级到4级属性分类，应符合表5的要求。

表 5 登记对象信息

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td><td>4级分类</td></tr><tr><td>登记信息</td><td>登记基本信息</td><td>—</td><td>—</td></tr><tr><td rowspan="11">登记信息</td><td rowspan="7">权利登记</td><td rowspan="7">权利基本信息</td><td>权利登记基本信息描述</td></tr><tr><td>确权记录</td></tr><tr><td>代持信息描述</td></tr><tr><td>可用登记</td></tr><tr><td>质押登记</td></tr><tr><td>冻结登记</td></tr><tr><td>状态信息描述</td></tr><tr><td rowspan="4">名册登记</td><td>名册基本信息</td><td>—</td></tr><tr><td>股东名册</td><td>—</td></tr><tr><td>金融债权人名册</td><td>—</td></tr><tr><td>基金投资人名册</td><td>—</td></tr></table>

表5中第2级至4级分类的具体信息要求如下:

——2级分类：

\- 登记基本信息应符合 A.5.1。

——3级分类-名册登记：

- 名册基本信息应符合 A.5.3.1;  
- 股东名册应符合 A.5.3.2;  
- 金融债权人名册应符合 A.5.3.3;  
- 基金投资人名册应符合 A.5.3.4。

——4级分类-权利基本信息：

• 权利登记基本信息描述应符合 A.5.2.1.1;  
- 确权记录应符合 A.5.2.1.2;  
- 代持信息描述应符合 A.5.2.1.3;  
- 可用登记应符合 A.5.2.1.4;  
- 质押登记应符合 A.5.2.1.5;  
- 冻结登记应符合 A.5.2.1.6;  
- 状态信息描述应符合 A.5.2.1.7。

## 10 资金结算对象信息

资金结算对象记录与转让、资金托管、派息等相关的资金结算内容，资金结算对象信息划分为1级到2级属性分类，应符合表6的要求。

表 6 资金结算对象信息

<table><tr><td>1级分类</td><td>2级分类</td></tr><tr><td rowspan="3">资金结算信息</td><td>资金结算基本信息</td></tr><tr><td>转出方信息</td></tr><tr><td>转入方信息</td></tr></table>

表6中第2级分类的具体信息要求如下:

——资金结算基本信息应符合 A.6.1;

——转出方信息应符合 A.6.2;

——转入方信息应符合 A.6.3。

## 11 信披对象信息

基于区域性股权市场的广义信披概念，信披对象记录市场主体12大类信息，包括信披基本信息、企业信息、企业报告信息、公告信息、重大事件信息、诚信档案、财务信息、企业经营信息、第三方拓展信息、历史沿革、中介业务开展情况、风险处置情况等，信披对象信息划分为1级到3级属性分类，应符合表7的要求。

表 7 信披对象信息

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td></tr><tr><td rowspan="16">信披信息</td><td>信披基本信息</td><td>—</td></tr><tr><td>企业信息</td><td>—</td></tr><tr><td>企业报告信息</td><td>—</td></tr><tr><td>公告信息</td><td>—</td></tr><tr><td>重大事件信息</td><td>—</td></tr><tr><td rowspan="2">诚信档案</td><td>事项基本信息</td></tr><tr><td>事项明细信息</td></tr><tr><td rowspan="2">财务信息</td><td>基本财务信息</td></tr><tr><td>财务报表文件</td></tr><tr><td rowspan="2">企业经营信息</td><td>经营基本信息</td></tr><tr><td>投融资信息</td></tr><tr><td>第三方拓展信息</td><td>—</td></tr><tr><td rowspan="2">历史沿革</td><td>历史沿革基本信息</td></tr><tr><td>上市挂牌信息</td></tr><tr><td>中介业务开展情况</td><td>—</td></tr><tr><td>风险处置情况</td><td>—</td></tr></table>

表7中第2级至3级分类的具体信息要求如下:

——2 级分类:

- 信披基本信息应符合 A.7.1;  
- 企业信息应符合 A.7.2;  
- 企业报告信息应符合 A.7.3;  
- 公告信息应符合 A.7.4;  
- 重大事件信息应符合 A.7.5;  
- 第三方拓展信息应符合 A.7.9;  
- 中介业务开展情况应符合 A.7.11;  
- 风险处置情况应符合 A.7.12。

——3级分类-诚信档案：

- 事项基本信息应符合 A.7.6.1;  
- 事项明细信息应符合 A.7.6.2。

——3级分类-财务信息：

- 基本财务信息应符合 A.7.7.1;  
- 财务报表文件应符合 A.7.7.2。

——3级分类-企业经营信息：

- 经营基本信息应符合 A.7.8.1;  
- 投融资信息应符合 A.7.8.2。

——3级分类-历史沿革：

- 历史沿革基本信息应符合 A.7.10.1;  
- 上市挂牌信息应符合 A.7.10.2。

## 12 财务报表信息

财务报表用于记录区域性股权市场及其服务企业一定时期资金、利润状况的会计报表。财务报表对象信息划分为1级到4级属性分类，应符合表8的要求。

表 8 财务报表对象信息

<table><tr><td>1级分类</td><td>2级分类</td><td>3级分类</td><td>4级分类</td></tr><tr><td rowspan="15">财务报表信息</td><td>财务报表基本信息</td><td>—</td><td>—</td></tr><tr><td rowspan="3">运营机构财务简况</td><td>运营机构利润简况</td><td>—</td></tr><tr><td>运营机构资产负债简况</td><td>—</td></tr><tr><td>运营机构现金流简况</td><td>—</td></tr><tr><td rowspan="11">企业合并财务报表</td><td>企业报表调整说明</td><td>—</td></tr><tr><td rowspan="5">企业合并资产负债表</td><td>流动资产</td></tr><tr><td>非流动资产</td></tr><tr><td>流动负债</td></tr><tr><td>非流动负债</td></tr><tr><td>所有者权益(或股东权益)</td></tr><tr><td>企业合并利润表</td><td>—</td></tr><tr><td rowspan="4">企业合并现金流量表</td><td>经营活动产生的现金流量</td></tr><tr><td>投资活动产生的现金流量</td></tr><tr><td>筹资活动产生的现金流量</td></tr><tr><td>补充材料</td></tr></table>

表8中第2级至4级分类的具体信息要求如下：

——2 级分类:

\- 财务报表基本信息应符合 A.8.1。

——3级分类-运营机构财务简况：

- 运营机构利润简况应符合 A.8.2.1;  
- 运营机构资产负债简况应符合 A.8.2.2;

\- 运营机构现金流简况应符合 A.8.2.3。

——3级分类-企业合并财务报表：

- 企业报表调整说明应符合 A.8.3.1;  
- 企业合并利润表应符合 A.8.3.3。

——4级分类-企业合并资产负债表:

- 流动资产应符合 A.8.3.2.1;  
- 非流动资产应符合 A.8.3.2.2;  
- 流动负债应符合 A.8.3.2.3;  
- 非流动负债应符合 A.8.3.2.4;  
- 所有者权益（或股东权益）应符合A.8.3.2.5。

——4级分类-企业合并现金流量表:

- 经营活动产生的现金流量应符合 A.8.3.4.1;  
- 投资活动产生的现金流量应符合 A.8.3.4.2;  
- 筹资活动产生的现金流量应符合 A.8.3.4.3;  
- 补充材料应符合 A.8.3.4.4。

## 13 监管信息

监管对象用于记录在对于区域性股权市场监管对象执行的具体政策记录、监管措施记录及自律监管措施记录等。监管对象信息划分为1级到2级属性分类，应符合表9的要求。

表 9 监管对象信息

<table><tr><td>1级分类</td><td>2级分类</td></tr><tr><td rowspan="5">监管信息</td><td>基本信息</td></tr><tr><td>业务规则及执行信息</td></tr><tr><td>地方法规政策文件及落实信息</td></tr><tr><td>重大事项报告及措施信息</td></tr><tr><td>监管措施执行信息</td></tr></table>

表 9 中第 2 级分类的具体信息要求如下:

——基本信息应符合 A.9.1;  
——业务规则及执行信息应符合 A.9.2;  
——地方法规政策文件及落实信息应符合 A.9.3;  
——重大事项报告及措施信息应符合 A.9.4;  
——监管措施执行信息应符合 A.9.5。

# 附录 A

# (规范性)

# 跨链数据模型

## A.1 主体模型设计

## A.1.1 主体基本信息

## A.1.1.1 主体通用信息

主体通用信息包括主体标识、主体对象类型、主体行政区域、主体信息维护时间、备注、投资者统一编码等字段数据类型，应满足表A.1的要求。此处，主体标识为数据标识符。主体对象类型和主体行政区域为枚举值域。

表 A.1 主体通用信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>主体标识</td><td>subject_id</td><td>全局对象主体标识</td><td>CHARACTER</td><td>128</td><td>地方链不填</td><td>—</td></tr><tr><td>主体对象类型</td><td>subject_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_主体类型</td></tr><tr><td>主体行政区域</td><td>subject_main_administrative_region</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_境内外类别</td></tr><tr><td>主体信息维护时间</td><td>subject_create_time</td><td>—</td><td>TIME</td><td>20</td><td>必填</td><td>—</td></tr><tr><td>备注</td><td>subject_remark</td><td>—</td><td>CHARACTER</td><td>256</td><td>—</td><td>—</td></tr><tr><td>投资者统一编码</td><td>subject_investor_code</td><td>—</td><td>CHARACTER</td><td>16</td><td>—</td><td>—</td></tr></table>

## A.1.1.2 主体资质信息

## A. 1. 1. 2. 1 资质信息

资质信息包括资质类别、市场角色类型、中介资质类型、金融资质类型等字段数据类型，应满足表A.2的要求。

表 A.2 资质信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>资质类别</td><td>subject_qualification_category</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_主体资质类别</td></tr><tr><td>市场角色类型</td><td>subject_market_roles_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_市场角色类型</td></tr><tr><td>中介资质类型</td><td>subject_intermediary_qualification</td><td>以数组形式添加:[1,2,3]</td><td>整型数组</td><td>—</td><td>不必填</td><td>枚举_中介类型</td></tr><tr><td>金融资质类型</td><td>subject_financial_qualification_type</td><td>资质类别为2时选择</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_金融资质类型</td></tr></table>

## A. 1. 1. 2. 2 资质认证信息

资质认证信息包括资质代码、资质认证文件、资质认证方、资质认证时间、资质审核方、资质认证描述、审核时间、资质状态等字段数据类型，应满足表A.3的要求。

表 A.3 资质认证信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>资质代码</td><td>subject_qualification_code</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>资质认证文件</td><td>subject_role_qualification_certification_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>资质认证方</td><td>subject_qualification_autenticator</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>资质认证时间</td><td>subject_certification_time</td><td>—</td><td>TIME</td><td>20</td><td>不必填</td><td>—</td></tr><tr><td>资质审核方</td><td>subject_qualification_reviewer</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>资质认证描述</td><td>Subject_certification_description</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>审核时间</td><td>subject_review_time</td><td>—</td><td>TIME</td><td>20</td><td>不必填</td><td>—</td></tr><tr><td>资质状态</td><td>subject_qualification_status</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 1. 1. 2. 3 投资者适当性信息

投资者适当性信息包括投资者适当性信息、适当性分类信息、适当性基本信息、适当性文件信息：a）投资者适当性信息包括适当性类别、适当性认证子类、适当性认证描述、适当性证明文件、适当性认证方主体引用、适当性认证方主体名称、适当性认证时间、适当性认证状态等字段数据类型，应满足表A.4的要求。

表 A.4 投资者适当性信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>适当性类别</td><td>subject_investor_qualification</td><td>市场角色类型为投资方</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_适当性类别</td></tr><tr><td>适当性认证子类</td><td>subject_investor_qualification_sub</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>适当性认证描述</td><td>subject_investor_qualification_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>适当性证明文件</td><td>subject_investor_qualification_certi ficate</td><td>投资方填写用于证明适当性的文件</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>适当性认证方主体引用</td><td>subject_investor_qualification_certi fier_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>适当性认证方主体名称</td><td>subject_investor_qualification_certi fier_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>适当性认证时间</td><td>subject_investor_qualification_certi ficate_time</td><td>—</td><td>TIME</td><td>20</td><td>不必填</td><td>—</td></tr><tr><td>适当性认证状态</td><td>subject_investor_qualification_status</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr></table>

b) 适当性分类信息包括投资者类别、普通投资者风险承受能力类别、其他适当性类别等字段数据类型，应满足表 A.5 的要求。

表 A.5 适当性分类信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>投资者类别</td><td>Subject_investor_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_投资者类别</td></tr><tr><td>普通投资者风险承受能力类别</td><td>Subject_investor_risk_asscement_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_普通投资者风险承受能力类别</td></tr><tr><td>其他适当性类别</td><td>Subject_other_suitability_type</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

c) 适当性基本信息包括收入来源、可支配年收入情况、资产情况、债务情况、投资知识情况、投资经验、投资期限、金融行业及相关工作经历年限、投资品种、期望收益、风险偏好、可承受的损失等字段数据类型，应满足表 A.6 的要求。

表 A.6 适当性基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>收入来源</td><td>Subject_source_of_income</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_收入来源</td></tr><tr><td>可支配年收入情况</td><td>subject_disposable_annual_income</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_可支配年收入情况</td></tr><tr><td>资产情况</td><td>subject_asset_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_资产情况</td></tr><tr><td>债务情况</td><td>subject_debt_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_债务情况</td></tr><tr><td>投资知识情况</td><td>subject_investment_knowledge_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_投资知识情况</td></tr><tr><td>投资经验</td><td>subject_investment_experience</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_投资经验</td></tr><tr><td>投资期限</td><td>subject_investment_term</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_投资期限</td></tr><tr><td>金融行业及相关工作经历年限</td><td>subject_financial_industry_related_working_years</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_金融行业及相关工作经历年限</td></tr><tr><td>投资品种</td><td>subject_type_of_investment</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_投资品种</td></tr><tr><td>期望收益</td><td>subject_income_expectation</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_期望收益</td></tr><tr><td>风险偏好</td><td>subject_risk_of_preference</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_风险偏好</td></tr><tr><td>可承受的损失</td><td>subject_affordable_of_loss</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_可承受的损失</td></tr></table>

d) 适当性文件信息包括投资者基本信息表、投资者风险承受能力评估问卷、其他适当性证明文件等字段数据类型，应满足表 A.7 的要求。

表 A.7 适当性文件信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>投资者基本信息表</td><td>subject_investor_basic_information_form</td><td>—</td><td>FILE_OBJECT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>投资者风险承受能力评估问卷</td><td>subject_risk_assessment_questionnaire_for_investor</td><td>—</td><td>FILE_OBJECT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>其他适当性证明文件</td><td>subject_other_investor_documentary_evidence</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A.1.2 机构基本信息

## A.1.2.1 基本信息描述

基本信息描述包括公司全称、英文名称、公司简称、英文简称、机构性质、所有制性质、法定类型、经济类型、股份制企业类型、规模类型、企业标签、证件类型及证件号码、企业统一编码、注册日期、营业执照、经营范围、企业所属行业、企业所属行业-管理型分类、企业所属行业-大类、企业所属行业-中类、主营业务、公司简介、注册资本、注册资本币种、实收资本、实收资本币种、注册地址、注册地所在省份、注册地所在市、注册地所在区、办公地址、联系地址、联系电话、企业传真、邮政编码、互联网地址、电子邮箱、公司章程、主管单位、股东总数（个）、纳税人识别号、发票开户行、发票账号、发票地址、发票电话、核准时间、参保人数、企业状态、注销原因、注销日期、吊销原因、吊销日期、企业曾用名、人员规模等字段数据类型，应满足表A.8的要求，其中行政区划应满足GB/T 2260的要求，货币应满足GB/T 12406的要求。

表 A.8 基本信息描述

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>公司全称</td><td>subject_company_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>英文名称</td><td>subject_company_english_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>公司简称</td><td>subject_company_short_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>英文简称</td><td>subject_company_short_english_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>机构性质</td><td>subject_organization_nature</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_机构性质</td></tr><tr><td>所有制性质</td><td>subject_ownership_nature</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_所有制性质</td></tr><tr><td>法定类型</td><td>subject_legal_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_法定类型</td></tr><tr><td>经济类型</td><td>subject_economic_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_经济类型</td></tr><tr><td>股份制企业类型</td><td>subject_company_type</td><td>经济类型为股份制企业时必填</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_股份制企业类型</td></tr><tr><td>规模类型</td><td>subject_scale_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_规模类型</td></tr><tr><td>企业标签</td><td>enterprise_Label</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_企业标签</td></tr><tr><td>证件类型及证件号码</td><td>subject_document_information</td><td>只可选1或者同时提供2/3/4,枚举值用于标记type类型;数据格式为:{{"type":1,"code":"12312312"},{"type":2,"code":"12312312"}]</td><td>OBJET_SET</td><td>—</td><td>不必填</td><td>枚举_机构代码类型</td></tr><tr><td>企业统一编码</td><td>subject_company_code</td><td>辖区编码+企业主体编码+企业分层(类)编码</td><td>CHARACTER</td><td>32</td><td>—</td><td>—</td></tr><tr><td>注册日期</td><td>subject_registry_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>营业执照</td><td>subject_business_license</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>经营范围</td><td>subject_business_scope</td><td>填写企业营业执照主营业务</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr><tr><td>企业所属行业</td><td>subject_industry</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_企业所属行业分类</td></tr><tr><td>企业所属行业-管理型分类</td><td>subject_industry_classification_management</td><td>—</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_企业所属行业管理型分类</td></tr><tr><td>企业所属行业-大类</td><td>subject_industry_classification_division</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_企业所属行业大类</td></tr><tr><td>企业所属行业-中类</td><td>subject_industry_classification_group</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_企业所属行业中类</td></tr><tr><td>主营业务</td><td>subject_company_business</td><td>—</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr><tr><td>公司简介</td><td>subject_company_profile</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>注册资本</td><td>subject_regi stered_capital</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>注册资本币种</td><td>subject_regi stered_capital_currency</td><td>符合GB/T 12406规定</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>实收资本</td><td>subject_paid_in_capital</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>实收资本币种</td><td>subject_paid_in_capital_currency</td><td>符合GB/T 12406规定</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>注册地址</td><td>subject_regi stered_address</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>注册地所在省份</td><td>subject_province</td><td>符合GB/T 2260规定</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>注册地所在市</td><td>subject_city</td><td>符合GB/T 2260规定</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>注册地所在区</td><td>subject_dist rict</td><td>符合GB/T 2260规定</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>办公地址</td><td>subject_office_address</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>联系地址</td><td>subject_cont act_address</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>联系电话</td><td>subject_cont act_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>企业传真</td><td>subject_enterprise_fax</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>邮政编码</td><td>subject_post al_code</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>互联网地址</td><td>subject_internet_address</td><td>企业官网地址</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>电子邮箱</td><td>subject_mail_box</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>公司章程</td><td>subject_association_articles</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>主管单位</td><td>subject_regulator</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>股东总数(个)</td><td>subject_shareholders_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>纳税人识别号</td><td>subject_taxpayer_id_number</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>发票开户行</td><td>subject_invoice_bank</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>发票账号</td><td>subject_invoice_account_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>发票地址</td><td>subject_invoice_address</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>发票电话</td><td>subject_invoice_telephone_number</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>核准时间</td><td>subject_approval_time</td><td>—</td><td>TIME</td><td>20</td><td>不必填</td><td>—</td></tr><tr><td>参保人数</td><td>subject_insured_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>企业状态</td><td>subject_company_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_企业状态</td></tr><tr><td>注销原因</td><td>subject_company_status_deregistration</td><td>简述,限定在300字以内</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>注销日期</td><td>subject_company_status_deregistration_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>吊销原因</td><td>subject_company_status_windingup</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>吊销日期</td><td>subject_company_status_windingup_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>企业曾用名</td><td>subject_name_used_before</td><td>以数组形式添加: ["曾用名 1", "曾用名 2"]</td><td>字符型数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>人员规模</td><td>subject_personnel_size</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 1.2.2 人员构成统计信息

人员构成统计信息包括统计截止日期、员工人数、拥有 CPA 人数、通过司考人数、通过证券从业资格考试人数、通过其他执业资格考试人数等字段数据类型，应满足表 A.9 的要求。

表 A.9 人员构成统计信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>统计截止日期</td><td>subject_staff fing_stats_enddate</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>员工人数</td><td>subject_staff fing_staff_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>拥有CPA人数</td><td>subject_staff fing_number_of_CPA</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>通过司考人数</td><td>subject_staff fing_number_of_NJEC</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>通过证券从业资格考试人数</td><td>subject_staff fing_number_of_SAC</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>通过其他执业资格考试人数</td><td>subject_staff fing_number_of_other_certificate</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 1.2.3 子公司/分支机构信息

子公司/分支机构信息包括子公司/分支机构设立方式、子公司/分支机构主体引用、持股比例等字段数据类型，应满足表 A.10 的要求。

表 A.10 子公司/分支机构信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>子公司/分支机构设立方式</td><td>subject_subsidiary_establishment_mode</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_公司或机构的设立方式</td></tr><tr><td>子公司/分支机构主体引用</td><td>subject_staffing_staff_number</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>持股比例</td><td>subjectStaffing_number_of_CPA</td><td>—</td><td>DECIMAL</td><td>8,4</td><td>不必填</td><td>—</td></tr></table>

## A. 1.2.4 主要人员信息

主要人员信息包括任职开始日期、任职结束日期、国籍、证件类型、证件号码、证件地址、持股比例、持股数量、联系方式、主要人员备注等字段数据类型，应满足表 A.11 的要求。

表 A.11 主要人员信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>任职开始日期</td><td>subject_key_personnel_appointment_start</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>任职结束日期</td><td>subject_key_personnel_appointment_end</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>国籍</td><td>subject_key_personnel_nationality</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>证件类型</td><td>subject_document_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_个人身份证件类型</td></tr><tr><td>证件号码</td><td>subject_key_personnel_id</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>证件地址</td><td>subject_key_personnel_address</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>持股比例</td><td>subject_key_personnel_shareholding_ratio</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>持股数量</td><td>subject_key_personnel_shareholding</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>联系方式</td><td>subject_key_personnel_contact</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>主要人员备注</td><td>subject_key_personnel_re mark</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 1.3 个人主体基本信息

个人主体基本信息包括个人姓名、个人身份证类型、个人身份证件号、个人证件地址、个人联系地址、个人联系电话、个人手机号、个人传真、邮政编码、电子邮箱、学历、职业、个人所属行业、出生日期、性别、工作单位、投资年限、投资经历、籍贯、省份、城市等字段数据类型，应满足表A.12的要求。

表 A.12 个人主体基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>个人姓名</td><td>subject_investor_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>个人身份证类型</td><td>subject_id_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_个人身份证件类型</td></tr><tr><td>个人身份证件号</td><td>subject_id_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>个人证件地址</td><td>subject_id_address</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>个人联系地址</td><td>subject_contact_address</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>个人联系电话</td><td>subject_contact_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>个人手机号</td><td>subject_cellphone_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>个人传真</td><td>subject_personal_fax</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>邮政编码</td><td>subject_postal_code</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>电子邮箱</td><td>subject_id_doc_mailbox</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>学历</td><td>subject_education</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_学历</td></tr><tr><td>职业</td><td>subject_occupation</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_职业</td></tr><tr><td>个人所属行业</td><td>subject_industry</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_企业所属行业管理型分类</td></tr><tr><td>出生日期</td><td>subject_birthday</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>性别</td><td>subject_gender</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_性别</td></tr><tr><td>工作单位</td><td>subject_work_unit</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>投资年限</td><td>subject_investment_period</td><td>—</td><td>CHARACTER</td><td>8</td><td>不必填</td><td>—</td></tr><tr><td>投资经历</td><td>subject_investment_experience</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>籍贯</td><td>subject_native_place</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>省份</td><td>subject_province</td><td>符合GB/T 2260规定</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>城市</td><td>subject_city</td><td>符合GB/T 2260规定</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr></table>

## A.2 账户模型设计

## A.2.1 账户基本信息

账户基本信息包括账户所属主体引用、开户机构主体引用、账号、账户类型、账户用途、账户状态、账户信息维护时间等字段数据类型，应满足表A.13的要求。

表 A.13 账户基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>账户所属主体引用</td><td>account_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>开户机构主体引用</td><td>account_depository_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>账号</td><td>account_number</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>账户类型</td><td>account_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_账户类型</td></tr><tr><td>账户用途</td><td>account_purpose</td><td>以数组形式添加:[1,2,3]</td><td>整型数组</td><td>—</td><td>必填</td><td>枚举_账户用途</td></tr><tr><td>账户状态</td><td>account_status</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_账户状态</td></tr><tr><td>账户信息维护时间</td><td>account_create_time</td><td>—</td><td>TIME</td><td>‘T’ 10 HH:mm:ssX</td><td>必填</td><td>—</td></tr></table>

## A.2.2 账户生命周期信息

## A.2.2.1 开户信息

开户信息包括账户创建日期、账户开户日期、账户开户文件、开户代理人姓名、开户代理人电话等字段数据类型，应满足表A.14的要求。

表 A.14 开户信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>账户创建日期</td><td>account_establish_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>账户开户日期</td><td>account_open_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>账户开户文件</td><td>account_open_doc</td><td>主体申请开户凭证(含委托)开户机构开户确认凭证</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>开户代理人姓名</td><td>account_open_agency_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>开户代理人电话</td><td>account_open_agency_phone</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.2.2.2 销户信息

销户信息包括账户销户日期、账户销户文件、销户代理人姓名、销户代理人电话等字段数据类型，应满足表A.15的要求。

表 A.15 销户信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>账户销户日期</td><td>account_close_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>账户销户文件</td><td>account_close_doc</td><td>账户主体申请凭证(含委托)开户机构确认凭证</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>销户代理人姓名</td><td>account_closing_agent_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>销户代理人电话</td><td>account_closing_agent_contact_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.2.2.3 冻结信息

冻结信息包括账户冻结日期、账户冻结文件、冻结申请方名称、冻结事由描述等字段数据类型，应满足表A.16的要求。

表 A.16 冻结信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>账户冻结日期</td><td>account_frozen_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>账户冻结文件</td><td>account_frozen_doc</td><td>股权冻结执行通知书或其他</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>冻结申请方名称</td><td>account_frozen_applicant_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>冻结事由描述</td><td>account_frozen_event_description</td><td>300字以内描述</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A.2.2.4 解冻信息

解冻信息包括账户解冻日期、账户解冻文件、解冻申请方名称、解冻事由描述等字段数据类型，应满足表A.17的要求。

表 A.17 解冻信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>账户解冻日期</td><td>account_thaw_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>账户解冻文件</td><td>account_thaw_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>解冻申请方名称</td><td>account_thaw_applicant_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>解冻事由描述</td><td>account_thaw_event_description</td><td>300字以内描述</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A.2.3 账户关联信息

账户关联信息包括关联关系、关联账户对象引用等字段数据类型，应满足表A.18的要求。

表 A.18 账户关联信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>关联关系</td><td>account_association</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_关联关系</td></tr><tr><td>关联账户对象引用</td><td>account_associated_account_ref</td><td>资金账户关联证券账户对象引用或游客账户关联的证券账户对象引用</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr></table>

## A.3 产品模型设计

## A. 3.1 基本信息

## A. 3.1.1 产品基本信息

产品基本信息包括产品交易场所类别、交易场所主体引用、交易场所主体名称、交易场所板块名称、非公开发行主体引用、非公开发行主体名称、非公开发行主体类型、产品代码、产品全称、产品简称、产品功能、产品类型、最大账户数量、信息披露方式、产品规模单位、产品规模币种、产品规模总额、浏览范围、联系人、联系信息、备注、产品信息维护时间等字段数据类型，应满足表A.19的要求。

表 A.19 产品基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>产品交易场所类别</td><td>product_trading_market_category</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_交易场所类别</td></tr><tr><td>交易场所主体引用</td><td>product_mark_et_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>交易场所主体名称</td><td>product_mark_et_subject_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>交易场所板块名称</td><td>product_plate_trading_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行主体引用</td><td>product_non_public_issuer_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>非公开发行主体名称</td><td>product_non_public_issuer_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>非公开发行主体类型</td><td>product_non_public_issuer_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_非公开发行方类型</td></tr><tr><td>产品代码</td><td>product_code</td><td>转板产品非必填</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>产品全称</td><td>product_name</td><td>—</td><td>CHARACTER</td><td>128</td><td>必填</td><td>—</td></tr><tr><td>产品简称</td><td>product_name_abbreviation</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>产品功能</td><td>product_type_function</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_产品功能</td></tr><tr><td>产品类型</td><td>product_type</td><td>转板产品非必填</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_产品类型</td></tr><tr><td>最大账户数量</td><td>product_account_number_max</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>信息披露方式</td><td>product_info_disclosure_way</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_信息披露方式</td></tr><tr><td>产品规模单位</td><td>product_scale_unit</td><td>有限责任公司股权挂牌转让,为货币价值</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_产品规模单位</td></tr><tr><td>产品规模币种</td><td>product_scale_currency</td><td>符合GB/T 12406规定</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>产品规模总额</td><td>product_scale</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>浏览范围</td><td>product_customer_browsing_right</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_非公开发行范围</td></tr><tr><td>联系人</td><td>product_issuer_contact_person</td><td>个人或机构中文名称</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>联系信息</td><td>product_issuer_contact_info</td><td>电话/邮箱/地址</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>备注</td><td>product_remark</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>产品信息维护时间</td><td>product_create_time</td><td>—</td><td>TIME</td><td>20</td><td>必填</td><td>—</td></tr></table>

## A. 3.1.2 服务方信息

## A. 3.1.2.1 服务方基本信息

服务方基本信息包括服务方分类、服务方主体引用、服务方主体名称等字段数据类型，应满足表A.20的要求。

表 A.20 服务方基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>服务方分类</td><td>service_provider_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_服务方分类</td></tr><tr><td>服务方主体引用</td><td>service_provider_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>服务方主体名称</td><td>service_provider_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 3.1.2.2 服务方收费

服务方收费包括收费币种、收费金额等字段数据类型，应满足表A.21的要求。

表 A.21 服务方收费

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>收费币种</td><td>service_provider_type</td><td>符合 GB/T 12406 规定</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>收费金额</td><td>service_provider_charge_amount</td><td>—</td><td>DECIMAL</td><td>18,4</td><td>不必填</td><td>—</td></tr></table>

## A. 3.1.2.3 增信信息

增信信息包括增信方性质、增信方式等字段数据类型，应满足表A.22的要求。

表 A.22 增信信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>增信方性质</td><td>product_credit_enhancement_party_property</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_增信方性质</td></tr><tr><td>增信方式</td><td>product_credit_enhancement_method</td><td>—</td><td>NUMBER_ARRAY</td><td>—</td><td>不必填</td><td>枚举_增信方式</td></tr></table>

## A. 3.1.3 产品文件信息

产品文件信息包括审查意见书、发行文件、其他产品文件等字段数据类型，应满足表A.23的要求。

表 A.23 产品文件信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>审查意见书</td><td>product_examine_opinion_book</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>发行文件</td><td>product_released_document</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>其他产品文件</td><td>product_issue_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.2 产品标的信息

## A. 3.2.1 资金用途信息

资金用途信息包括资金用途类型、资金用途子类、资金用途描述、资金用途说明文件清单等字段数据类型，应满足表A.24的要求。

表 A.24 资金用途信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>资金用途类型</td><td>product_fund_use_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_资金用途类型</td></tr><tr><td>资金用途子类</td><td>product_fund_sub_category</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_资金用途子类</td></tr><tr><td>资金用途描述</td><td>product_description_fund_use</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>资金用途说明文件清单</td><td>product_document_describing_funds</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.2.2 经营用途信息

经营用途信息包括经营用途名称、经营用途详情、经营用途说明文件清单等字段数据类型，应满足表A.25的要求。

表 A.25 经营用途信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>经营用途名称</td><td>product_business_purpose_name</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>经营用途详情</td><td>product_business_purpose_details</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>经营用途说明文件清单</td><td>product_business_purpose_documents</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.2.3 投资组合信息

投资组合信息包括投资产品类型、投资比例范围、投资产品详情、投资产品详情说明文件清单等字段数据类型，应满足表A.26的要求。

表 A.26 投资组合信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>投资产品类型</td><td>product_investment_product_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_投资产品类型</td></tr><tr><td>投资比例范围</td><td>product_investment_proportion_range</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>投资产品详情</td><td>product_Investment_product_details</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>投资产品详情说明文件清单</td><td>product_detailed_description_document</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.3 非公开发行信息

## A. 3. 3. 1 非公开发行基本信息

非公开发行基本信息包括非公开发行成功日期这一个字段数据类型，应满足表A.27的要求。

表 A.27 非公开发行基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>非公开发行成功日期</td><td>product_release_date</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3. 3. 2 备案信息

备案信息包括备案许可类型、备案日期、备案文件、备案审核通知文件、备案说明信息等字段数据类型，应满足表A.28的要求。

表 A.28 备案信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>备案许可类型</td><td>product_license_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_备案许可类型</td></tr><tr><td>备案日期</td><td>product_filing_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>备案文件</td><td>product_filing_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>备案审核通知文件</td><td>product_filing_examine_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>备案说明信息</td><td>product_filing_documentation</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3. 3. 3 私募股权非公开发行信息

私募股权非公开发行信息包括非公开发行范围、非公开发行类型、非公开发行股份类别、非公开发行说明信息、非公开发行价格、非公开发行价格定价标准、非公开发行前股数、非公开发行后股数、非公开发行后总市值、半年净利润、全年净利润、实际募集规模、募集开始日期、募集结束日期、非公开发行前注册资本、非公开发行后注册资本、实缴股数、认缴股数、无限售股数、限售股数等字段数据类型，应满足表A.29的要求。

表 A.29 私募股权非公开发行信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>非公开发行范围</td><td>product_not_public_issue_scope</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_非公开发行范围</td></tr><tr><td>非公开发行类型</td><td>product_not_public_issue_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_非公开发行类型</td></tr><tr><td>非公开发行股份类别</td><td>product_shares_issued_class</td><td>以数组形式添加:[1,2,3]</td><td>整型数组</td><td>—</td><td>必填,可多选</td><td>枚举_非公开发行股份类别</td></tr><tr><td>非公开发行说明信息</td><td>not_public_release_note_information</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行价格</td><td>product_not_public_issue_price</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行价格定价标准</td><td>product_not_public_issue_price_method</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行前股数</td><td>product_not_public_before_authorized_shares</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行后股数</td><td>product_not_public_after_authorized_shares</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行后总市值</td><td>product_not_public_after_issue_market_value</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>半年净利润</td><td>product_net_profit</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>全年净利润</td><td>product_annual_net_profit</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>实际募集规模</td><td>product_actual_raising_scale</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>募集开始日期</td><td>product_raising_start_time</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>募集结束日期</td><td>product_raising_end_time</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行前注册资本</td><td>product_not_public_registered_capital_before_issuance</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行后注册资本</td><td>product_not_public_registered_capital_issuance</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>实缴股数</td><td>product_paid_shares</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>认缴股数</td><td>product_shares_subscribed_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>无限售股数</td><td>product_unlimited_sales_number_shares</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>限售股数</td><td>product_restricted_shares_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr></table>

A. 3. 3. 4 可转债/合规发行的其他债券品种发行信息

A. 3. 3. 4. 1 可转债/合规发行的其他债券品种发行基本信息

可转债/合规发行的其他债券品种发行基本信息包括非公开发行范围、债权期限单位、债券期限、备案金额、是否分期非公开发行、票面利率下限、票面利率上限、分期期数、首期非公开发行金额、首期比例、首期利率、计息方式、计息方式备注、兑付方式、是否兑付完成、兑付方式备注、已兑付笔数、存量笔数、是否指定还款日、指定还款日、担保措施及方式、转股条件、转股价格的确定方式、转股约定价格、转股约定时间、转股期限、是否逾期、是否违约、违约开始时间、违约金额、赎回条款、非公开发行价格、产品面值、认购单位基数、非公开发行成功比例、募集资金划转条件、是否可转让、最大持有人数、认购上限份数、认购下限份数、赎回及回售条款、产品终止条件、存续期限、控制权变更调整、转换溢价、参考股价、实际募集规模、募集开始日期、募集结束日期、起息日期、到期日期、兑付金额、首次付息日期、非公开发行方主体信用评级、增信机构主体评级、担保安排、回售安排、股东禁售期限、债务重整、债务重组（包括展期）等字段数据类型，应满足表 A.30 的要求。

表 A. 30 可转债/合规发行的其他债券品种发行基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>非公开发行范围</td><td>product_scope_not_public_issue</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_非公开发行范围</td></tr><tr><td>债权期限单位</td><td>product_bond_duration_unit</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_债权期限单位</td></tr><tr><td>债券期限</td><td>product_bond_duration</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>备案金额</td><td>product_filing_amount</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>是否分期非公开发行</td><td>product_not_public_issue_by_stages</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>票面利率下限</td><td>product_bond_interest_rate_floor</td><td>票面利率上限/下限、首期比例、首期利率为百分比(%)</td><td>FLOAT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>票面利率上限</td><td>product_bond_interest_rate_cap</td><td>分期非公开发行时选择,票面利率上限/下限、首期比例、首期利率为百分比(%)</td><td>FLOAT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>分期期数</td><td>product_staging_frequency</td><td>分期非公开发行时选择,票面利率上限/下限、首期比例、首期利率为百分比(%)</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>首期非公开发行金额</td><td>product_initial_not_public_issue_amount</td><td>分期非公开发行时选择,票面利率上限/下限、首期比例、首期利率为百分比(%)</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>首期比例</td><td>product_initial_ratio</td><td>分期非公开发行时选择,票面利率上限/下限、首期比例、首期利率为百分比(%)</td><td>FLOAT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>首期利率</td><td>product_initial_interest_rate</td><td>分期非公开发行时选择,票面利率上限/下限、首期比例、首期利率为百分比(%)</td><td>FLOAT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>计息方式</td><td>product_interest_calculation_method</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_计息方式</td></tr><tr><td>计息方式备注</td><td>product_interest_calculation_method_remarks</td><td>计息方式为其他时手动填写</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>兑付方式</td><td>product_payment_method</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_兑付方式</td></tr><tr><td>是否兑付完成</td><td>product_payment_status</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>兑付方式备注</td><td>product_payment_method_remarks</td><td>兑付方式为其他时手动填写</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>已兑付笔数</td><td>product_cashhed_count</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>存量笔数</td><td>product_stock_count</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>是否指定还款日</td><td>product_is_appoint_repayment_date</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>指定还款日</td><td>product_appoint_repayment_date</td><td>指定还款日时填写</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>担保措施及方式</td><td>product_guarantee_measure</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转股条件</td><td>product_convertingshares_condition</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转股价格的确定方式</td><td>product_convertingshares_price_mode</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转股约定价格</td><td>product_agreed_convertingshares_price</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转股约定时间</td><td>product_agreed_convertingshares_time</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>转股期限</td><td>product_convertingshares_term</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>是否逾期</td><td>product_if_overdue</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>是否违约</td><td>product_if_default</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>违约开始时间</td><td>product_defa ult_start_time</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>违约金额</td><td>product_defa ult_amount</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>赎回条款</td><td>product_redemption</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行价格</td><td>product_not_public_issue_price</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>产品面值</td><td>product_face_value</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>认购单位基数</td><td>product_subcription_base</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行成功比例</td><td>product_succ essful_not_public_releas e_proportion</td><td>非公开发行成功比例为百分比(%)</td><td>FLOAT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>募集资金划转条件</td><td>product_fund_raising_conversion_condition</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>是否可转让</td><td>product_is_make_over</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>最大持有人数</td><td>product_number_of_holders_max</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>认购上限份数</td><td>product_subscription_upper_limit</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>认购下限份数</td><td>product_subcription_lower_limit</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>赎回及回售条款</td><td>product_redemption_clause</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>产品终止条件</td><td>product_termination_conditions</td><td>—</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr><tr><td>存续期限</td><td>product_duration</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>控制权变更调整</td><td>product_adjustment_chang e_control</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>转换溢价</td><td>product_conversion_premium</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>参考股价</td><td>product_conversion_price_ref</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>实际募集规模</td><td>product_actual_issue_size</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>募集开始日期</td><td>product_raising_start_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>募集结束日期</td><td>product_raising_end_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>起息日期</td><td>product_start_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>到期日期</td><td>product_due_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>兑付金额</td><td>product_amount_cashhed</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>首次付息日期</td><td>product_first_interest_payment_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行方主体信用评级</td><td>product_not_public_issuer_credit_rating</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_主体信用评级</td></tr><tr><td>增信机构主体评级</td><td>product_credit_enhancement_agency_credit_rating</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_主体信用评级</td></tr><tr><td>担保安排</td><td>product_guarantee_arrangement</td><td>—</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr><tr><td>回售安排</td><td>product_repo_arrangement</td><td>—</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr><tr><td>股东禁售期限</td><td>product_lockup</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>债务重整</td><td>product_debt_reforming</td><td>—</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr><tr><td>债务重组(包括展期)</td><td>product_debt_restructuring</td><td>(包括以资产清偿债务、将债务转为权益工具、调整债务本金、改变债务利息、变更还款期限、修改其他条款),前述条款单一方式或组合方式</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_债务重组</td></tr></table>

## A. 3. 3. 4. 2 逾期信息

逾期信息包括逾期期数、逾期开始时间、逾期金额等字段数据类型，应满足表A.31的要求。

表 A. 31 逾期信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>逾期期数</td><td>product_over due_period</td><td>每次募集成功生成一个唯一信息标识,标识本次募集信息,不同于产品对象标识</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>逾期开始时间</td><td>product_over due_start_time</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>逾期金额</td><td>product_over due_amount</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A.3.4 转让信息

## A. 3.4.1 转让状态信息

转让状态信息包括转让状态这一个字段数据类型，应满足表A.32的要求。

表 A. 32 转让状态信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转让状态</td><td>product_transfer_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_转让状态</td></tr></table>

## A. 3.4.2 挂牌信息

挂牌信息包括转让范围、机构持有人允许转让给个人、转让锁定天数、转让发布有效天数、产品风险级别、转让单位基数、挂牌代码、挂牌日期、挂牌备注信息等字段数据类型，应满足表A.33的要求。

表 A. 33 挂牌信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转让范围</td><td>product_transfer_scope</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_转让范围</td></tr><tr><td>机构持有人允许转让给个人</td><td>product_transfer_permission_institution_to_individual</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转让锁定天数</td><td>product_transfer_lockup_days</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转让发布有效天数</td><td>product_transfer_validity</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>产品风险级别</td><td>product_risk_level</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>转让单位基数</td><td>product_transfer_unit</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>挂牌代码</td><td>product_listing_code</td><td>可以与产品代码相同</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>挂牌日期</td><td>product_listing_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>挂牌备注信息</td><td>product_listing_remarks</td><td>500字以内描述文字</td><td>CHARACTER</td><td>2048</td><td>不必填</td><td>—</td></tr></table>

## A. 3.4.3 摘牌信息

摘牌信息包括摘牌日期、摘牌类型、摘牌原因、摘牌备注信息等字段数据类型，应满足表A.34的要求。

表 A. 34 摘牌信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>摘牌日期</td><td>product_delisting_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>摘牌类型</td><td>product_delisting_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_摘牌类型</td></tr><tr><td>摘牌原因</td><td>product_delisting_reason</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_摘牌原因</td></tr><tr><td>摘牌备注信息</td><td>product_delisting_remarks</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.5 托管信息

托管信息包括托管登记日期、托管文件、托管备注信息、解除托管登记日期、解除托管文件、解除托管备注信息等字段数据类型，应满足表A.35的要求。

表 A. 35 托管信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>托管登记日期</td><td>product_custodian_registration_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>托管文件</td><td>product_custodian_documents</td><td>1、账户主体申请凭证(含委托)2、开户机构确认凭证</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>托管备注信息</td><td>product_custodian_notes</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>解除托管登记日期</td><td>product_escrow_deregistration_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>解除托管文件</td><td>product_escrow_deregistration_document</td><td>1、账户主体申请凭证(含委托)2、开户机构确认凭证</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>解除托管备注信息</td><td>product_escrow_deregistration_remarks</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.6 服务状态信息

## A. 3.6.1 服务基本信息

服务基本信息包括服务状态、服务文件、服务开始时间、服务结束时间等字段数据类型，应满足表A.36的要求。

表 A. 36 服务基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>服务状态</td><td>product_service_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_服务状态</td></tr><tr><td>服务文件</td><td>product_service_documents</td><td>—</td><td>附件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>服务开始时间</td><td>product_service_status_start_date</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>服务结束时间</td><td>product_service_status_end_date</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 3.6.2 停止服务信息

## A. 3.6.2.1 转板信息

转板信息包括转板市场这一个字段数据类型，应满足表A.37的要求。

表 A. 37 转板信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转板市场</td><td>product_transfer_board_market</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_市场类型</td></tr></table>

## A. 3.6.2.2 收购信息

收购信息包括收购公司名称、收购公司统一编码、收购公司所在市场等字段数据类型，应满足表A.38的要求。

表 A. 38 收购信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>收购公司名称</td><td>product_acquisition_company_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>—</td><td>—</td></tr><tr><td>收购公司统一编码</td><td>product_acquisition_company_code</td><td>—</td><td>CHARACTER</td><td>32</td><td>—</td><td>—</td></tr><tr><td>收购公司所在市场</td><td>product_acquisition_company_market</td><td>—</td><td>NUMBER</td><td>—</td><td>—</td><td>枚举_市场类型</td></tr></table>

## A.4 转让报告模型设计

## A.4.1 转让基本信息

## A.4.1.1 基本信息描述

基本信息描述包括交易场所类别、转让类型、转让方式、转让描述信息、转让信息维护时间等字段数据类型，应满足表A.39的要求。

表 A. 39 基本信息描述

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>交易场所类别</td><td>transaction_market_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_交易场所类别</td></tr><tr><td>转让类型</td><td>transfer_type</td><td>非交易过户是指协议转让、继承、赠与、依法进行的财务分割、法人资格丧失等情形所涉及的证券过户</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_转让类型</td></tr><tr><td>转让方式</td><td>transfer_method</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_转让协议类型</td></tr><tr><td>转让描述信息</td><td>transfer_description</td><td>300字以内描述</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>转让信息维护时间</td><td>transfer_create_time</td><td>—</td><td>TIME</td><td>‘T’HH:mm:ssX</td><td>必填</td><td>—</td></tr></table>

## A.4.1.2 转让资产信息

## A. 4.1.2.1 交易资产托管状态

交易资产托管状态包括资产托管状态这一个字段数据类型，应满足表A.40的要求。

表 A. 40 交易资产托管状态

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>资产托管状态</td><td>transaction_product_custody_status</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_资产托管状态</td></tr></table>

## A. 4.1.2.2 已托管交易资产转让

已托管交易资产转让包括转让产品引用这一个字段数据类型，应满足表A.41的要求。

表 A.41 已托管交易资产转让

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转让产品引用</td><td>transfer_custody_product_ref</td><td>转让场所类别为1,必填</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr></table>

## A. 4.1.2.3 未托管交易资产转让

未托管交易资产转让包括转让资产名称、转让资产发行主体引用、转让资产发行主体名称、转让资产类型、转让资产规模单位、转让资产规模币种、转让资产规模总额、转让资产文件、转让资产描述信息等字段数据类型，应满足表A.42的要求。

表 A.42 未托管交易资产转让

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转让资产名称</td><td>transfer_product_name</td><td>交易场所类别不为1</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>转让资产发行主体引用</td><td>transfer_product_issuer_ref</td><td>交易场所类别为0时,选填</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>转让资产发行主体名称</td><td>transfer_product_issuer_name</td><td>交易场所类别为0时,选填</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>转让资产类型</td><td>transferproduct_asset_type</td><td>交易场所类别不为1,必填</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_转让资产类型</td></tr><tr><td>转让资产规模单位</td><td>transfer_product_asset_unit</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_产品规模单位</td></tr><tr><td>转让资产规模币种</td><td>transfer_product_asset_currency</td><td>符合GB/T 12406规定</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>转让资产规模总额</td><td>transfer_product_asset_value</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转让资产文件</td><td>transfer_product_asset_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转让资产描述信息</td><td>transfer_product_decription</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.4.2 转让成交信息

## A. 4.2.1 成交内容信息

成交内容信息包括转让成交流水号、成交币种、成交价格、成交数量、成交时间、转让成交描述信息、资金来源等字段数据类型，应满足表A.43的要求。

表 A.43 成交内容信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转让成交流水号</td><td>transfer_series_number</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>成交币种</td><td>transfer_settlement_currency</td><td>符合GB/T12406规定</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>成交价格</td><td>transfer_settlement_price</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>成交数量</td><td>transfer_settlement_quantity</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>成交时间</td><td>transfer_settlement_time</td><td>—</td><td>TIME</td><td>10‘T’ HH:mm:ssX</td><td>不必填</td><td>—</td></tr><tr><td>转让成交描述信息</td><td>transfer_settlement_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>资金来源</td><td>transfer_settlement_fund_source</td><td>枚举</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_资金来源</td></tr></table>

## A. 4.2.2 融资类转让成交方信息

融资类转让成交方信息包括非公开发行方主体引用、非公开发行方名称、投资方主体引用、投资方名称等字段数据类型，应满足表A.44的要求。

表 A.44 融资类转让成交方信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>非公开发行方主体引用</td><td>transaction_issuer_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行方名称</td><td>transaction_issuer_name</td><td>为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>投资方主体引用</td><td>transaction_investor_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>投资方名称</td><td>transaction_investor_name</td><td>为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 4.2.3 其他交易类型的转让成交方信息

其他交易类型的转让成交方信息包括原持有方主体引用、原持有方名称、对手方主体引用、对手方名称等字段数据类型，应满足表A.45的要求。

表 A. 45 其他交易类型的转让成交方信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细-说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>原持有方主体引用</td><td>transaction_investor_original_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>原持有方名称</td><td>transaction_investor_original_name</td><td>为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>对手方主体引用</td><td>transaction_investor_counterparty_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>对手方名称</td><td>transaction_investor_counterparty_name</td><td>为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 4.2.4 成交核验信息

成交核验信息包括委托文件、成交文件等字段数据类型，应满足表A.46的要求。

表 A. 46 成交核验信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>委托文件</td><td>transaction_orderplacing_verification_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>成交文件</td><td>transaction_verification_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 4.3 交易中介信息

交易中介信息包括中介类型、中介机构主体引用、中介机构服务描述、中介机构名称、中介机构收费币种、中介机构收费金额等字段数据类型，应满足表A.47的要求。

表 A.47 交易中介信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>中介类型</td><td>transaction_intermediary_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_中介类型</td></tr><tr><td>中介机构主体引用</td><td>transaction_intermediary_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>中介机构服务描述</td><td>transaction_intermediary_description</td><td>200字以内描述</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>中介机构名称</td><td>transaction_intermediary_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>中介机构收费币种</td><td>transaction_intermediary_charge_currency</td><td>符合GB/T 12406规定交易资产规模单位为2</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>中介机构收费金额</td><td>transaction_intermediary_charge_amount</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.5 登记模型设计

## A. 5.1 登记基本信息

登记基本信息包括登记对象类型、登记事项类型等字段数据类型，应满足表A.48的要求。

表 A. 48 登记基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>登记对象类型</td><td>register_object_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_登记对象类型</td></tr><tr><td>登记事项类型</td><td>register_event_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_登记事项类型</td></tr></table>

## A.5.2 权利登记

## A. 5.2.1 权利基本信息

## A. 5.2.1.1 权利登记基本信息描述

权利登记基本信息描述包括登记流水号、登记时间、登记主体引用、登记托管企业主体引用、登记主体类型、登记账户引用、登记权利类型、权利登记单位、登记币种、转让报告引用、登记产品引用、登记描述信息、登记信息维护时间、登记确权状态、代持状态、经办人姓名、经办人电话、经办人传真、经办人邮件等字段数据类型，应满足表A.49的要求。

表 A.49 权利登记基本信息描述

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>登记流水号</td><td>register_serial_number</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>登记时间</td><td>register_time</td><td>—</td><td>TIME</td><td>‘T’HH:mm:ssX</td><td>必填</td><td>—</td></tr><tr><td>登记主体引用</td><td>register_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>登记托管企业主体引用</td><td>register_esc_row_company_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>登记主体类型</td><td>register_subject_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_主体类型</td></tr><tr><td>登记账户引用</td><td>register_subject_account_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>登记权利类型</td><td>register_asset_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_登记权利类型</td></tr><tr><td>权利登记单位</td><td>register_asset_unit</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_权利登记单位</td></tr><tr><td>登记币种</td><td>register_asset_currency</td><td>符合GB/T 12406规定</td><td>CHARACTER</td><td>18</td><td>必填</td><td>枚举_币种类型</td></tr><tr><td>转让报告引用</td><td>register_transactionaction_ref</td><td>登记事项类型为2转让登记,必填</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>登记产品引用</td><td>register_product_ref</td><td>登记事项类型为1托管登记,必填;为2转让登记,选填</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>登记描述信息</td><td>register_description</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>登记信息维护时间</td><td>register_create_time</td><td>—</td><td>TIME</td><td>‘T’HH:mm:ssX</td><td>必填</td><td>—</td></tr><tr><td>登记确权状态</td><td>register_authentic_right_recognition_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_登记确权状态</td></tr><tr><td>代持状态</td><td>register_entrustment_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_代持状态</td></tr><tr><td>经办人姓名</td><td>register_operator_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>经办人电话</td><td>register_operator_contact_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>经办人传真</td><td>register_operator_fax</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>经办人邮件</td><td>register_operator_email</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 5.2.1.2 确权记录

确权记录包括登记确权日期、确权方式、确权方主体引用、确权方主体名称、确权代理方主体引用、确权代理方主体名称、确权文件、确权描述信息等字段数据类型，应满足表A.50的要求。

表 A. 50 确权记录

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>登记确权日期</td><td>register_authentic_right_recognition_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>确权方式</td><td>register_right_recognition_mode</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_确权方式</td></tr><tr><td>确权方主体引用</td><td>register_right_recognition_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>确权方主体名称</td><td>register_right_recognition_subject_name</td><td>确权方为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>确权代理方主体引用</td><td>register_right_recognition_agent_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>确权代理方主体名称</td><td>register_right_recognition_agent_subject_name</td><td>确权代理方为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>确权文件</td><td>register_right_recognition_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>确权描述信息</td><td>register_right_recognition_description</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A. 5.2.1.3 代持信息描述

代持信息描述包括代持份额、实际持有人主体引用、实际持有人名称、实际持有人证件类型（个人）、实际持有人证件号码（个人）、实际持有人证件类型及号码（机构）等字段数据类型，应满足表A.51的要求。

表 A.51 代持信息描述

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>代持份额</td><td>register_entrusting_share</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>实际持有人主体引用</td><td>register_actual_contributor_subject_ref</td><td>主体引用和后面三项信息可选其中一种,优先主体引用</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>实际持有人名称</td><td>register_actual_contributor_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>实际持有人证件类型(个人)</td><td>register_personal_actual_contributor_id_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_个人身份证件类型</td></tr><tr><td>实际持有人证件号码(个人)</td><td>register_personal_actual_contributor_id_number</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>实际持有人证件类型及号码(机构)</td><td>register_enterprise_actual_contributor_id</td><td>同机构主体</td><td>OBJET_SET</td><td>—</td><td>不必填</td><td>枚举_机构代码类型</td></tr></table>

## A. 5.2.1.4 可用登记

可用登记包括可用变动额、变动前可用余额、变动后可用余额等字段数据类型，应满足表A.52的要求。

表 A.52 可用登记

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>可用变动额</td><td>register_asset_balance_change</td><td>可以是正负值</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>变动前可用余额</td><td>register_asset_balance_before</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>变动后可用余额</td><td>register_asset_balance_after</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 5.2.1.5 质押登记

质押登记包括质押变动额、当前质押余额、变动后质押余额等字段数据类型，应满足表A.53的要求。

表 A. 53 质押登记

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>质押变动额</td><td>register_pledge_balance_change</td><td>可以是正负值</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>当前质押余额</td><td>register_pledge_balance_before</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>变动后质押余额</td><td>register_plged_balance_after</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 5.2.1.6 冻结登记

冻结登记包括冻结变动额、当前冻结余额、冻结后余额、冻结/解冻文件、冻结/解冻说明信息等字段数据类型，应满足表A.54的要求。

表 A.54 冻结登记

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>冻结变动额</td><td>register_frozen_balance_change</td><td>可以是正负值</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>当前冻结余额</td><td>register_frozen_balance</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>冻结后余额</td><td>register_frozen_balance_after</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>冻结/解冻文件</td><td>register_thaw_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>冻结/解冻说明信息</td><td>register_thaw_description</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 5.2.1.7 状态信息描述

状态信息描述包括持有状态、持有状态说明、持有属性、持有权利类型、业务来源、登记说明、登记文件、股权性质标签、转股数量、转股价格等字段数据类型，应满足表A.55的要求。

表 A. 55 状态信息描述

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>持有状态</td><td>register_asset_holding_status</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_持有状态</td></tr><tr><td>持有状态说明</td><td>register_asset_holding_status_description</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>持有属性</td><td>register_asset_holding_nature</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_非公开发行股份类别</td></tr><tr><td>持有权利类型</td><td>register_asset_equity_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_持有权利类型</td></tr><tr><td>业务来源</td><td>register_source_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_业务来源</td></tr><tr><td>登记说明</td><td>register_asset_note</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>登记文件</td><td>register_asset vérification_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>股权性质标签</td><td>register_equity_type_label</td><td>每个股份类别可以有多个标签</td><td>NUMBER_ARRAY</td><td>—</td><td>不必填</td><td>枚举_股权性质标签</td></tr><tr><td>转股数量</td><td>register_transfer_equity_number</td><td>业务来源为债转股时填写</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>转股价格</td><td>register_transfer_equity_price</td><td>业务来源为债转股时填写</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A.5.3 名册登记

## A. 5. 3. 1 名册基本信息

名册基本信息包括名册主体引用、产品引用、产品名称、产品描述、权利类型、登记日期等字段数据类型，应满足表A.56的要求。

表 A.56 名册基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>名册主体引用</td><td>register_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>产品引用</td><td>register_product_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>产品名称</td><td>register_product_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>产品描述</td><td>register_product_description</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>权利类型</td><td>register_list_asset_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_权利类型</td></tr><tr><td>登记日期</td><td>register_list_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr></table>

## A. 5.3.2 股东名册

股东名册包括股东主体引用、股东主体类型、股份性质、认缴金额、实缴金额、持股数量、持股比例等字段数据类型，应满足表A.57的要求。

表 A. 57 股东名册

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>股东主体引用</td><td>register_equity_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>股东主体类型</td><td>register_equity_subject_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_主体类型</td></tr><tr><td>股份性质</td><td>register_equity_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_股份性质</td></tr><tr><td>认缴金额</td><td>register_equity_capital</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>实缴金额</td><td>register_equity_capital_paidin</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>持股数量</td><td>register_equity_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>持股比例</td><td>register_equity_shareholding</td><td>—</td><td>FLOAT</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 5. 3. 3 金融债权人名册

金融债权人应符合《证券期货投资者适当性管理办法》《区域性股权市场监督管理试行办法》及相关监管要求。金融债权人名册包括金融债权人主体引用、金融债权人类型、认购数量、认购金额、金融债权人联系方式等字段数据类型，应满足表A.58的要求。

表 A. 58 金融债权人名册

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>金融债权人主体引用</td><td>financial_debt_holder_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>金融债权人类型</td><td>financial_debt_holder_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_主体类型</td></tr><tr><td>认购数量</td><td>register_debt_holder_subscription_quantity</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>认购金额</td><td>register_debt_holder_subscription_price</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>金融债权人联系方式</td><td>financial_debt_holder_contact_number</td><td>为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.5.3.4 基金投资人名册

基金投资人范围应符合《私募投资基金监督管理暂行办法》相关规定。基金投资人名册包括投资人主体引用、投资人主体名称、认购金额、认购数量、基金投资人分类等字段数据类型，应满足表A.59的要求。

表 A. 59 基金投资人名册

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>投资人主体引用</td><td>register_in investor_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>投资人主体名称</td><td>register_in investor_name</td><td>为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>认购金额</td><td>register Subscription_amount</td><td>—</td><td>DECIMAL</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>认购数量</td><td>register Subscription_number</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>基金投资人分类</td><td>register_fund_investors_classification</td><td>按角色类型</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_基金投资人分类</td></tr></table>

## A.6 资金结算模型设计

## A.6.1 资金结算基本信息

资金结算基本信息包括结算机构主体引用、结算类型、结算流水号、结算时间、转让产品引用、转让报告引用、结算币种、结算金额、结算说明、结算操作文件、资金结算信息维护时间等字段数据类型，应满足表A.60的要求。

表 A. 60 资金结算基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>结算机构主体引用</td><td>settlement_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>结算类型</td><td>settlement_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_结算类型</td></tr><tr><td>结算流水号</td><td>settlement_serial_number</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>结算时间</td><td>settlement_time</td><td>—</td><td>TIME</td><td>20</td><td>不必填</td><td>—</td></tr><tr><td>转让产品引用</td><td>settlement_product_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>转让报告引用</td><td>settlement_transfer_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>结算币种</td><td>settlement_currency</td><td>符合GB/T12406规定</td><td>CHARACTER</td><td>8</td><td>必填</td><td>枚举_币种类型</td></tr><tr><td>结算金额</td><td>settlement_value</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>必填</td><td>—</td></tr><tr><td>结算说明</td><td>settlement_note</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>结算操作文件</td><td>settlement_operation_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>资金结算信息维护时间</td><td>settlement_information_maintenance_time</td><td>—</td><td>TIME</td><td>20</td><td>必填</td><td>—</td></tr></table>

## A. 6.2 转出方信息

转出方信息包括转出方银行代号、转出方银行名称、转出方银行账号、转出方账户引用、转出方账户名称、转出方发生前金额、转出方发生后余额等字段数据类型，应满足表A.61的要求。

表 A.61 转出方信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转出方银行代号</td><td>settlement_out_bank_code</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>转出方银行名称</td><td>settlement_out_bank_name</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>转出方银行账号</td><td>settlement_out_bank_account</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>转出方账户引用</td><td>settlement_out_account_object_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>转出方账户名称</td><td>settlement_out_account_name</td><td>转出方为个人时,账户名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>转出方发生前金额</td><td>settlement_out_account_balance_before_transfer</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>转出方发生后余额</td><td>settlement_out_account_balance_after_transfer</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 6.3 转入方信息

转入方信息包括转入方银行代号、转入方银行名称、转入方银行账号、转入方账户引用、转入方账户名称、转入方发生前金额、转入方发生后余额等字段数据类型，应满足表A.62的要求。

表 A.62 转入方信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>转入方银行代号</td><td>settlement_in_bank_code</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>转入方银行名称</td><td>settlement_in_bank_name</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>转入方银行账号</td><td>settlement_in_bank_account</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>转入方账户引用</td><td>settlement_in_account_object_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>转入方账户名称</td><td>settlement_in_account_name</td><td>转入方为个人时,账户名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>转入方发生前金额</td><td>settlement_in_account_balance_before_transfer</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>转入方发生后余额</td><td>settlement_in_account_balance_after_transfer</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.7 信披模型设计

## A. 7.1 信披基本信息

信披基本信息包括信披对应主体引用、信披对应产品引用、信披类型、提报来源类型、提报来源主体引用、提报来源主体名称、提报时间、提报描述信息等字段数据类型，应满足表A.63的要求。

表 A.63 信披基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>信披对应主体引用</td><td>disclosure_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>信披对应产品引用</td><td>disclosure_product_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>信披类型</td><td>disclosure_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_信披类型</td></tr><tr><td>提报来源类型</td><td>disclosure_submit_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_提报来源类型</td></tr><tr><td>提报来源主体引用</td><td>disclosure_referer_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>提报来源主体名称</td><td>disclosure_referer_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>提报时间</td><td>disclosure_submit_date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr><tr><td>提报描述信息</td><td>disclosure_submit_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.7.2 企业信息

企业信息包括区域性股权市场主体引用、文件名称、文件、文件简述、代码、内容、开始日期、结束日期等字段数据类型，应满足表A.64的要求。

表 A.64 企业信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>区域性股权市场主体引用</td><td>disclosure_rem_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>文件名称</td><td>disclosure_doc_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>文件</td><td>disclosure_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>文件简述</td><td>disclosure_description</td><td>100字以内文件描述</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>代码</td><td>disclosure_code</td><td>—</td><td>CHARACTER</td><td>32</td><td>不必填</td><td>—</td></tr><tr><td>内容</td><td>disclosure_content</td><td>—</td><td>TEXT</td><td>—</td><td>必填</td><td>—</td></tr><tr><td>开始日期</td><td>disclosure_start_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>结束日期</td><td>disclosure_end_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr></table>

## A.7.3 企业报告信息

企业报告信息包括报告类型、报告名称、报告文件、报告简述、报告发布时间等字段数据类型，应满足表A.65的要求。

表 A.65 企业报告信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>报告类型</td><td>disclosure_enterprise report</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_财报会计期间类型</td></tr><tr><td>报告名称</td><td>disclosure_enterprise report_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>报告文件</td><td>disclosure_enterprise report_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>报告简述</td><td>disclosure_enterprise report_description</td><td>100字以内文件描述</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>报告发布时间</td><td>disclosure_enterprise report_date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr></table>

## A.7.4 公告信息

公告信息包括公告类型、公告名称、公告文件、公告简述、公告时间等字段数据类型，应满足表A.66的要求。

表 A.66 公告信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>公告类型</td><td>disclosure_announcement_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_公告类型</td></tr><tr><td>公告名称</td><td>disclosure_announcement_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>公告文件</td><td>disclosure_announcement_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>公告简述</td><td>disclosure_announcement_description</td><td>100字以内文件描述</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>公告时间</td><td>disclosure_announcement_date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr></table>

## A.7.5 重大事件信息

重大事件信息包括重大事件类型、事件名称、事件文件、事件简述、提报时间等字段数据类型，应满足表A.67的要求。

表 A.67 重大事件信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>重大事件类型</td><td>disclosure_majorevent_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_重大事件类型</td></tr><tr><td>事件名称</td><td>disclosure_majorevent_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>事件文件</td><td>disclosure_majorevent_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>事件简述</td><td>disclosure_majorevent_document_descr</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>提报时间</td><td>disclosure_majorevent_reporting_date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr></table>

## A.7.6 诚信档案

## A. 7.6.1 事项基本信息

事项基本信息包括认定方主体标识引用、认定方名称、鉴定方主体标识引用、鉴定方名称等字段数据类型，应满足表A.68的要求。

表 A. 68 事项基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>认定方主体标识引用</td><td>disclosure_identifier_ref</td><td>非必填,若不在系统中就填写名称</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>认定方名称</td><td>disclosure_identifier_name</td><td>认定方为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>鉴定方主体标识引用</td><td>disclosure_auditor_ref</td><td>非必填,若不在系统中就填写名称</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>鉴定方名称</td><td>disclosure_auditor_name</td><td>鉴定方为个人时,名称做脱敏处理</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.7.6.2 事项明细信息

事项明细信息包括事项编号、事项名称、事项文件、事项简述、事项类型、效力期限、开始日期、结束日期、状态等字段数据类型，应满足表A.69的要求。

表 A.69 事项明细信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>事项编号</td><td>disclosure_event_id</td><td>—</td><td>CHARACTER</td><td>64</td><td>不必填</td><td>—</td></tr><tr><td>事项名称</td><td>disclosure_event_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>事项文件</td><td>disclosure_event_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>事项简述</td><td>disclosure_event_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>事项类型</td><td>disclosure_event_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_事项类型</td></tr><tr><td>效力期限</td><td>disclosure_event_valid_time</td><td>—</td><td>CHARACTER</td><td>128</td><td>不必填</td><td>—</td></tr><tr><td>开始日期</td><td>disclosure_event_start_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>结束日期</td><td>disclosure_event_end_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>状态</td><td>disclosure_event_status</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_状态</td></tr></table>

## A.7.7 财务信息

## A. 7. 7. 1 基本财务信息

基本财务信息包括期间起始日期、期间截止日期、报表类型、期末总资产（元）、期末净资产（元）、总负债（元）、本期营业收入（元）、本期利润总额（元）、本期净利润（元）、现金流量（元）、是否有研发费用、研发费用（元）等字段数据类型，应满足表A.70的要求。

表 A. 70 基本财务信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>期间起始日期</td><td>disclosure_financial_start_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>期间截止日期</td><td>disclosure_financial_end_date</td><td>—</td><td>DATE</td><td>10</td><td>不必填</td><td>—</td></tr><tr><td>报表类型</td><td>disclosure_financial_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_报表周期类型</td></tr><tr><td>期末总资产(元)</td><td>disclosure_financial_periodend_total_asset</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>期末净资产(元)</td><td>disclosure_financial_periodend_net_asset</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>总负债(元)</td><td>disclosure_financial_periodend_total_liability</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>本期营业收入(元)</td><td>disclosure_financial_periodend_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>本期利润总额(元)</td><td>disclosure_financial_periodend_gross_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>本期净利润(元)</td><td>disclosure_financial_periodend_net_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>现金流量(元)</td><td>disclosure_financial_cashflow</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>是否有研发费用</td><td>disclosure_financial_whe ther_rd</td><td>—</td><td>BOOLEAN</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>研发费用(元)</td><td>disclosure_financial_rd_cost</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.7.7.2 财务报表文件

财务报表文件包括资产负债表名称、资产负债表、资产负债表简述、现金流量表名称、现金流量表、现金流量表简述、利润表名称、利润表、利润表简述、财务报表主体引用等字段数据类型，应满足表A.71的要求。

表 A. 71 财务报表文件

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>资产负债表名称</td><td>disclosure_financial_balance_sheet_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>资产负债表</td><td>disclosure_financial_balance_sheet</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>资产负债表简述</td><td>disclosure_financial_balance_sheet_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>现金流量表名称</td><td>disclosure_financial_cashflow_statement_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>现金流量表</td><td>disclosure_financial_cashflow_statement</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>现金流量表简述</td><td>disclosure_financial_cashflow_statement_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>利润表名称</td><td>disclosure_financial_income_statement_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>利润表</td><td>disclosure_financial_income_statement</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>利润表简述</td><td>disclosure_financial_income_statement_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>财务报表主体引用</td><td>disclosure_financial_statement_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr></table>

## A.7.8 企业经营信息

## A. 7.8.1 经营基本信息

经营基本信息包括业务概述、主营业务情况分析、非主营业务情况分析、资产及负债状况分析、主要股东情况分析、企业重大活动情况、经营报告名称、经营报告文件、经营报告简述、经营信息发布时间等字段数据类型，应满足表A.72的要求。

表 A. 72 经营基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>业务概述</td><td>disclosure_business_overview</td><td>—</td><td>CHARACTER</td><td>2048</td><td>必填</td><td>—</td></tr><tr><td>主营业务情况分析</td><td>disclosure_main_business_analysis</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>非主营业务情况分析</td><td>disclosure_main_business_analysis_no_n</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>资产及负债状况分析</td><td>disclosure_assets_and_liabilities_analysis</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>主要股东情况分析</td><td>disclosure_major_shareholders_analysis</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>企业重大活动情况</td><td>disclosure_major_events</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>经营报告名称</td><td>disclosure_business_report_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>经营报告文件</td><td>disclosure_business_report_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>经营报告简述</td><td>disclosure_business_report_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>经营信息发布时间</td><td>disclosure_business_report_date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr></table>

## A. 7.8.2 投融资信息

投融资信息包括投资情况分析、募集资金情况分析、重大资产和股权出售情况等字段数据类型，应满足表A.73的要求。

表 A. 73 投融资信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>投资情况分析</td><td>disclosure_investment_analysis</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>募集资金情况分析</td><td>disclosure_fund_raising_analysis</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>重大资产和股权出售情况</td><td>disclosure_sell_situation_analysis</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 7.9 第三方拓展信息

第三方拓展信息包括拓展信息名称、拓展信息文件、拓展信息简述、拓展信息发布时间等字段数据类型，应满足表A.74的要求。

表 A. 74 第三方拓展信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>拓展信息名称</td><td>disclosure_expand_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>拓展信息文件</td><td>disclosure_expand_doc</td><td>—</td><td>文件对象数组</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>拓展信息简述</td><td>disclosure_expand_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>必填</td><td>—</td></tr><tr><td>拓展信息发布时间</td><td>disclosure_expand_date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr></table>

## A. 7.10 历史沿革

## A. 7.10.1 历史沿革基本信息

历史沿革基本信息包括历史沿革事件类型、历史沿革事件子类、历史沿革事件名称、历史沿革事件简述、历史沿革事件发生时间、历史沿革事件文件等字段数据类型，应满足表A.75的要求。

表 A. 75 历史沿革基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>历史沿革事件类型</td><td>disclosure_historical_evolution_event_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_历史沿革事件类型</td></tr><tr><td>历史沿革事件子类</td><td>disclosure_historical_evolution_event_subtype</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_历史沿革事件子类</td></tr><tr><td>历史沿革事件名称</td><td>disclosure_historical_evolution_event_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>历史沿革事件简述</td><td>disclosure_historical_evolution_event_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>历史沿革事件发生时间</td><td>disclosure_historical_evolution_event_date</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>历史沿革事件文件</td><td>disclosure_historical_evolution_event_doc</td><td>—</td><td>FILE_OBJECT_ARRAY</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A. 7.10.2 上市挂牌信息

上市挂牌信息包括上市挂牌转让所这一个字段数据类型，应满足表A.76的要求。

表 A. 76 上市挂牌信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>上市挂牌转让所</td><td>disclosure_t raiding_mark et</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_市场类型</td></tr></table>

## A. 7.11 中介业务开展情况

中介业务开展情况包括中介业务类型、中介业务开展时间、中介业务文件、中介业务简介、利益冲突防范措施等字段数据类型，应满足表A.77的要求。

表 A. 77 中介业务开展情况

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>中介业务类型</td><td>disclosure_intermediary_business_type</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>中介业务开展时间</td><td>disclosure_intermediary_business_date</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>中介业务文件</td><td>disclosure_intermediary_doc</td><td>—</td><td>FILE_OBJECT_ARRAY</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>中介业务简介</td><td>disclosure_intermediary_business_description</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>利益冲突防范措施</td><td>interest_conflict_prevention_measures</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 7.12 风险处置情况

风险处置情况包括风险名称、风险处置文件、风险处置描述、提报时间等字段数据类型，应满足表A.78的要求。

表 A. 78 风险处置情况

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>风险名称</td><td>disclosure_risk_name</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>风险处置文件</td><td>disclosure_risk_disposal_doc</td><td>—</td><td>FILE_OBJECT_ARRAY</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>风险处置描述</td><td>disclosure_risk_disposal_description</td><td>—</td><td>TEXT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>提报时间</td><td>disclosure_reporting_time</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr></table>

## A.8 财务报表模型设计

## A.8.1 财务报表基本信息

财务报表基本信息包括财报主体标识引用、财报主体市场角色、报表所属期起、报表所属期止、财报周期类型、财报格式类型、审计单位、审计单位主体标识引用、审计意见等字段数据类型，应满足表A.79的要求。

表 A. 79 财务报表基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>财报主体标识引用</td><td>reporter_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>财报主体市场角色</td><td>subject_mark et_role</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_市场角色类型</td></tr><tr><td>报表所属期起</td><td>period_start date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr><tr><td>报表所属期止</td><td>period_end date</td><td>—</td><td>DATE</td><td>10</td><td>必填</td><td>—</td></tr><tr><td>财报周期类型</td><td>period_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_报表周期类型</td></tr><tr><td>财报格式类型</td><td>format_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_财报格式类型</td></tr><tr><td>审计单位</td><td>audit_institution</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>审计单位主体标识引用</td><td>audit_institution_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>审计意见</td><td>audit_opinion</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A.8.2 运营机构财务简况

## A.8.2.1 运营机构利润简况

运营机构利润简况包括营业总收入、主营业务收入、其他业务收入、营业成本、税金及附加、销售费用、管理费用、财务费用、研发费用、投资收益、公允价值变动收益、营业利润、利润总额、所得税、净利润、归属普通股东净利润、少数股东损益等字段数据类型，应满足表A.80的要求。

表 A.80 运营机构利润简况

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>营业总收入</td><td>total_business_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>主营业务收入</td><td>main_business_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他业务收入</td><td>other_sales_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业成本</td><td>operating_costs</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>税金及附加</td><td>tax_and_associated_charge_for_prime_operating</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>销售费用</td><td>selling_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>管理费用</td><td>administrative_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>财务费用</td><td>financial_expense</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>研发费用</td><td>research_and_development_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资收益</td><td>investment_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>公允价值变动收益</td><td>gain_on_fair_value_chang e</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业利润</td><td>operating_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>利润总额</td><td>total_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>所得税</td><td>income_tax</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>净利润</td><td>NP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>归属普通股东净利润</td><td>NP_common_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>少数股东损益</td><td>minority_interest_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8.2.2 运营机构资产负债简况

运营机构资产负债简况包括货币资金、转让性金融资产、衍生金融工具（资产）、应收账款及应收票据、其他应收款、存货、其他流动资产、流动资产合计、债权投资、其他债权投资、长期股权投资、其他权益工具投资、其他非流动金融资产、投资性房地产、固定资产总值、累计折旧及减值、固定资产净值、在建工程、使用权资产、无形资产、开发支出、商誉、非流动资产合计、总资产、短期借款、转让性金融负债、衍生金融工具（负债）、应付账款及应付票据、应交税费、其他流动负债、流动负债合计、长期借款、应付债券、其他非流动负债、非流动负债合计、总负债、股本、其他权益工具、资本公积、留存收益、其他综合收益、归属母公司股东权益、少数股东权益、股东权益合计、总负债及股东权益等字段数据类型，应满足表A.81的要求。

表 A.81 运营机构资产负债简况

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>货币资金</td><td>cash</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>转让性金融资产</td><td>trading_financial_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>衍生金融工具(资产)</td><td>financial_de rivatives_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收账款及应收票据</td><td>AR_and_NR</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他应收款</td><td>other_receivables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>存货</td><td>inventories</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他流动资产</td><td>other_CA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动资产合计</td><td>total_CA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>债权投资</td><td>debt_investments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他债权投资</td><td>other_debt_investments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期股权投资</td><td>LT_equity_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他权益工具投资</td><td>other_equity_instrument</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他非流动金融资产</td><td>other_non_current_financial_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资性房地产</td><td>real_estate_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产总值</td><td>total_FA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>累计折旧及减值</td><td>accumulated_depreciation_and_decrease</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产净值</td><td>net_worth_FA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>在建工程</td><td>CIP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>使用权资产</td><td>right_of_use_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>无形资产</td><td>IA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>开发支出</td><td>development_costs</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>商誉</td><td>goodwill</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动资产合计</td><td>total_NCA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>总资产</td><td>total_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>短期借款</td><td>ST_borrowing</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>转让性金融负债</td><td>trading_financial_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>衍生金融工具(负债)</td><td>financial_de rivatives_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付账款及应付票据</td><td>AP_and_NP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应交税费</td><td>tax_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他流动负债</td><td>other_CL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动负债合计</td><td>total_CL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期借款</td><td>LT_loans</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付债券</td><td>bond_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他非流动负债</td><td>other_NCL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动负债合计</td><td>total_NCL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>总负债</td><td>total_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>股本</td><td>number_of_common_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他权益工具</td><td>other_equity_instruments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资本公积</td><td>equity_investment_premium</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>留存收益</td><td>retained_earnings</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他综合收益</td><td>OCI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>归属母公司股东权益</td><td>parent_company_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>少数股东权益</td><td>minority_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>股东权益合计</td><td>option_rights</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>总负债及股东权益</td><td>total_liabilities_and_total_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.8.2.3 运营机构现金流简况

运营机构现金流简况包括销售商品、提供劳务收到的现金、购买商品、接受劳务支付的现金、经营活动产生的现金流量净额、收回投资收到的现金、取得投资收益收到的现金、处置固定资产、无形资产和其他长期资产收回的现金净额、购建固定资产、无形资产和其他长期资产支付的现金、投资支付的现金、投资活动产生的现金流量净额、吸收投资收到的现金、取得借款收到的现金、非公开发行债券收到的现金、偿还债务支付的现金、分配股利、利润或偿付利息支付的现金、筹资活动产生的现金流量净额等字段数据类型，应满足表A.82的要求。

表 A.82 运营机构现金流简况

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>销售商品、提供劳务收到的现金</td><td>cash_received_from_sales_of_goods_or_rendering_services</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>购买商品、接受劳务支付的现金</td><td>cash_paid_for_commodities_and_services</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动产生的现金流量净额</td><td>net_CFO</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>收回投资收到的现金</td><td>cash_receipts_from_investments_withdrawa</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>取得投资收益收到的现金</td><td>cash_receipts_from_return_on_investments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>处置固定资产、无形资产和其他长期资产收回的现金净额</td><td>net_cash_disposal_FA_IA_LTA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>购建固定资产、无形资产和其他长期资产支付的现金</td><td>cash_purchase_FA_IA_LTA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资支付的现金</td><td>cash_payment_for_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动产生的现金流量净额</td><td>net_investing_cashflow</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>吸收投资收到的现金</td><td>cash_received_for_attracted_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>取得借款收到的现金</td><td>cash_raised_from_loans</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行债券收到的现金</td><td>cash_proceeds_of_bond_issue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>偿还债务支付的现金</td><td>cash_debt_repayment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>分配股利、利润或偿付利息支付的现金</td><td>cash_distribution_of_dividend_profit_or_interest_payment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动产生的现金流量净额</td><td>net_financing_cash_flow</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.8.3 企业合并财务报表

## A. 8.3.1 企业报表调整说明

企业报表调整说明包括显示币种、原始币种、转换汇率、汇率类型、税率、税率说明、调整原因、调整说明、公告日期、数据来源等字段数据类型，应满足表A.83的要求。

表 A.83 企业报表调整说明

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>显示币种</td><td>display_currency</td><td>—</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>原始币种</td><td>original_currency</td><td>—</td><td>CHARACTER</td><td>16</td><td>不必填</td><td>枚举_币种类型</td></tr><tr><td>转换汇率</td><td>exchange_rate</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>汇率类型</td><td>exchange_rate_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_汇率类型</td></tr><tr><td>税率</td><td>tax_rate</td><td>—</td><td>DECIMAL</td><td>9,6</td><td>不必填</td><td>—</td></tr><tr><td>税率说明</td><td>tax_rate_explanation</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>调整原因</td><td>adjustment_reason</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>调整说明</td><td>adjustment_explanation</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>公告日期</td><td>announcement_date</td><td>—</td><td>DATE</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>数据来源</td><td>data_source</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr></table>

## A. 8.3.2 企业合并资产负债表

## A. 8. 3. 2. 1 流动资产

流动资产包括货币资金、转让性金融资产、衍生金融资产、应收票据及应收账款、应收票据、应收账款、应收款项融资、预付款项、其他应收款（合计）、应收股利、应收利息、其他应收款、买入返售金融资产、存货、消耗性生物资产、合同资产、划分为持有待售的资产、一年内到期的非流动资产、待摊费用、其他流动资产、其他金融类流动资产、流动资产差额（特殊报表科目）、流动资产差额（合计平衡项目）、流动资产合计等字段数据类型，应满足表A.84的要求。

表 A. 84 流动资产

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>货币资金</td><td>monetary_capital</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>转让性金融资产</td><td>trading_financial_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>衍生金融资产</td><td>financial_de rivative_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收票据及应收账款</td><td>NR_and_AR</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收票据</td><td>NR</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收账款</td><td>AR</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收款项融资</td><td>accounts_receivable_financing</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>预付款项</td><td>prepayment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他应收款(合计)</td><td>total_other_ receivables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收股利</td><td>dividend_receivable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应收利息</td><td>interest_receivable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他应收款</td><td>other_receivables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>买入返售金融资产</td><td>purchase_of_repurchasing_financial_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>存货</td><td>inventories</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>消耗性生物资产</td><td>including_consumable_biological_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>合同资产</td><td>contract_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>划分为持有待售的资产</td><td>disposable_assets_holding</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>一年内到期的非流动资产</td><td>NCA_within_one_year</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>待摊费用</td><td>unamortized_expenditures</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他流动资产</td><td>other_CA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他金融类流动资产</td><td>other_financial_CA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动资产差额(特殊报表科目)</td><td>diff_CA_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动资产差额(合计平衡项目)</td><td>diff_CA_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动资产合计</td><td>total_CA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8. 3. 2. 2 非流动资产

非流动资产包括发放贷款及垫款、以公允价值且其变动计入其他综合收益的金融资产、以摊余成本计量的金融资产、债权投资、其他债权投资、可供出售金融资产、其他权益工具投资、持有至到期投资、其他非流动金融资产、长期应收款、长期股权投资、投资性房地产、固定资产（合计）、固定资产、固定资产清理、在建工程（合计）、在建工程、工程物资、生产性生物资产、油气资产、使用权资产、无形资产、开发支出、商誉、长期待摊费用、递延所得税资产、其他非流动资产、非流动资产差额（特殊报表科目）、非流动资产差额（合计平衡项目）、非流动资产合计、资产差额（特殊报表科目）、资产差额（合计平衡项目）、资产总计等字段数据类型，应满足表A.85的要求。

表 A.85 非流动资产

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>发放贷款及垫款</td><td>issued_loan_and_advance</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>以公允价值且其变动计入其他综合收益的金融资产</td><td>FVOCI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>以摊余成本计量的金融资产</td><td>AMC</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>债权投资</td><td>debt_investments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他债权投资</td><td>other_debt_investments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>可供出售金融资产</td><td>AFS</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他权益工具投资</td><td>other_equity_instrument</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>持有至到期投资</td><td>HTM</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他非流动金融资产</td><td>other_non_current_financial_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期应收款</td><td>LT_receivables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期股权投资</td><td>LT_equity_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资性房地产</td><td>real_estate_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产(合计)</td><td>total_FA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产</td><td>FA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产清理</td><td>disposal_FA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>在建工程(合计)</td><td>total_CIP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>在建工程</td><td>construction_in_process</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>工程物资</td><td>engineering_materials</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>生产性生物资产</td><td>regenerating_biological_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>油气资产</td><td>oil_and_gas_reserves</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>使用权资产</td><td>right_of_use_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>无形资产</td><td>IA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>开发支出</td><td>development_costs</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>商誉</td><td>goodwill</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期待摊费用</td><td>LT_unamortized_expenditures</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>递延所得税资产</td><td>deferred_income_tax_asset</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他非流动资产</td><td>other_NCA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动资产差额(特殊报表科目)</td><td>diff_NCA_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动资产差额(合计平衡项目)</td><td>diff_NCA_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动资产合计</td><td>total_NCA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资产差额(特殊报表科目)</td><td>diff_total_assets_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资产差额(合计平衡项目)</td><td>diff_total_assets_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资产总计</td><td>total_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8. 3. 2. 3 流动负债

流动负债包括短期借款、转让性金融负债、衍生金融负债、应付票据及应付账款、应付票据、应付账款、预收款项、合同负债、应付手续费及佣金、应付职工薪酬、应交税费、其他应付款（合计）、应付利息、应付股利、其他应付款、划分为持有待售的负债、一年内到期的非流动负债、预提费用、递延收益-流动负债、应付短期债券、其他流动负债、其他金融类流动负债、流动负债差额（特殊报表科目）、流动负债差额（合计平衡项目）、流动负债合计等字段数据类型，应满足表A.86的要求。

表A.86 流动负债

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>短期借款</td><td>ST_borrowing</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>转让性金融负债</td><td>trading_financial_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>衍生金融负债</td><td>financial_de rivative_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付票据及应付账款</td><td>AP_and_NP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付票据</td><td>NP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付账款</td><td>AP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>预收款项</td><td>unearned_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>合同负债</td><td>liabilities_of_contracts</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付手续费及佣金</td><td>fees_and_commission_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付职工薪酬</td><td>salaries_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应交税费</td><td>various_tax_payables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他应付款(合计)</td><td>total_other_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付利息</td><td>interest_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付股利</td><td>dividend_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他应付款</td><td>other_payables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>划分为持有待售的负债</td><td>classified_as_liabilities_held_for_sale</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>一年内到期的非流动负债</td><td>NCL_within_one_year</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>预提费用</td><td>accrued_expenditures</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>递延收益-流动负债</td><td>deferred_income_CL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付短期债券</td><td>SL_bond_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他流动负债</td><td>other_CL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他金融类流动负债</td><td>other_financial_CL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动负债差额(特殊报表科目)</td><td>diff_CL_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动负债差额(合计平衡项目)</td><td>diff_CL_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>流动负债合计</td><td>total_CL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8. 3. 2. 4 非流动负债

非流动负债包括长期借款、应付债券、租赁负债、长期应付款（合计）、长期应付款、专项应付款、长期应付职工薪酬、预计负债、递延所得税负债、递延收益-非流动负债、其他非流动负债、非流动负债差额（特殊报表科目）、非流动负债差额（合计平衡项目）、非流动负债合计、负债差额（特殊报表科目）、负债差额（合计平衡项目）、负债合计等字段数据类型，应满足表A.87的要求。

表 A.87 非流动负债

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>长期借款</td><td>LT_borrowing</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>应付债券</td><td>bond_payable_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>租赁负债</td><td>lease_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期应付款(合计)</td><td>total_LT_payables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期应付款</td><td>LT_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>专项应付款</td><td>specific_item_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期应付职工薪酬</td><td>LT_salaries_payable</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>预计负债</td><td>accrued_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>递延所得税负债</td><td>deferred_income_tax_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>递延收益-非流动负债</td><td>deferred_income_NCL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他非流动负债</td><td>other_NCL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动负债差额(特殊报表科目)</td><td>diff_NCL_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动负债差额(合计平衡项目)</td><td>diff_NCL_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动负债合计</td><td>total_NCL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>负债差额(特殊报表科目)</td><td>diff_liabilities_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>负债差额(合计平衡项目)</td><td>diff_liabilities_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>负债合计</td><td>total_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8.3.2.5 所有者权益（或股东权益）

所有者权益（或股东权益）包括实收资本（或股本）、其他权益工具、优先股、永续债、资本公积金、（减）库存股、其他综合收益、专项储备、盈余公积金、一般风险准备、未分配利润、外币报表折算差额、未确认的投资损失、股东权益差额（特殊报表科目）、股东权益差额（合计平衡项目）、归属于母公司所有者权益合计、少数股东权益、所有者权益合计、负债及股东权益差额（特殊报表项目）、负债及股东权益差额（合计平衡项目）、负债和所有者权益总计等字段数据类型，应满足表A.88的要求。

表 A. 88 所有者权益（或股东权益）

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>实收资本(或股本)</td><td>paid_in_capital</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他权益工具</td><td>other_equity_instruments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>优先股</td><td>including_preference_shares</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>永续债</td><td>including_perpetual_debt</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资本公积金</td><td>capital_reserve</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)库存股</td><td>less_treasury_stock</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他综合收益</td><td>OCI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>专项储备</td><td>specific_reserve</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>盈余公积金</td><td>surplus_reserve</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>一般风险准备</td><td>generic_risk_reserve</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>未分配利润</td><td>undistributed_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>外币报表折算差额</td><td>converted_difference_on_foreign_currency_statements</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>未确认的投资损失</td><td>unidentified_investment_loss</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>股东权益差额(特殊报表科目)</td><td>diff_shareholders_equity_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>股东权益差额(合计平衡项目)</td><td>diff_shareholders_equity_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>归属于母公司所有者权益合计</td><td>parent_company_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>少数股东权益</td><td>minority_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>所有者权益合计</td><td>total_owners_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>负债及股东权益差额(特殊报表项目)</td><td>diff_liabilities_and_owners_equity_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>负债及股东权益差额(合计平衡项目)</td><td>diff_liabilities_and_owners_equity_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>负债和所有者权益总计</td><td>total_liabilities_and_owners_equity</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.8.3.3 企业合并利润表

企业合并利润表包括营业总收入、营业收入、营业总成本、营业成本、产品、地区、税金及附加、销售费用、管理费用、研发费用、财务费用、利息费用、（减）利息收入、（加）其他收益、投资净收益、对联营企业和合营企业的投资收益、以摊余成本计量的金融资产终止确认收益、净敞口套期收益、公允价值变动净收益、资产减值损失、信用减值损失、资产处置收益、汇兑净收益、（加）营业利润差额（特殊报表科目）、营业利润差额（合计平衡项目）、营业利润、（加）营业外收入、（减）营业外支出、非流动资产处置净损失、（加）利润总额差额（特殊报表科目）、利润总额差额（合计平衡项目）、利润总额、（减）所得税、（加）未确认的投资损失、（加）净利润差额（特殊报表科目）、净利润差额（合计平衡项目）、净利润、持续经营净利润、终止经营净利润、（减）少数股东损益、归属于母公司所有者的净利润、（加）其他综合收益、综合收益总额、（减）归属于少数股东综合收益总额、归属于母公司普通股东综合收益总额、每股收益、基本每股收益、稀释每股收益等字段数据类型，应满足表A.89的要求。

表 A. 89 企业合并利润表

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>营业总收入</td><td>total_operating_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业收入</td><td>operating_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业总成本</td><td>total_operating_costs</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业成本</td><td>operating_costs</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>产品</td><td>product</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>地区</td><td>area</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>税金及附加</td><td>tax_and_associated_charge_for_prime_operating</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>销售费用</td><td>selling_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>管理费用</td><td>administrative_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>研发费用</td><td>research_and_development_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>财务费用</td><td>financial_expense</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>利息费用</td><td>including_interest_expense</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)利息收入</td><td>less_interest_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)其他收益</td><td>add_other_investment_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资净收益</td><td>net_investment_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>对联营企业和合营企业的投资收益</td><td>incl_income_from_investment_to_joint_ventures</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>以摊余成本计量的金融资产终止确认收益</td><td>gains_from_the_derecognition_AMC</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>净敞口套期收益</td><td>net_exposure_hedging_gains_and_losses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>公允价值变动净收益</td><td>FVGL</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资产减值损失</td><td>impairment_losses_on_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>信用减值损失</td><td>impairment_losses_on_goodwill</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>资产处置收益</td><td>gain_on_disposal_of_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>汇兑净收益</td><td>exchang_net_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)营业利润差额(特殊报表科目)</td><td>diff_operating_profit_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业利润差额(合计平衡项目)</td><td>diff_operating_profit_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>营业利润</td><td>operating_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)营业外收入</td><td>add_non-operating_revenue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)营业外支出</td><td>less_non-operating_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非流动资产处置净损失</td><td>including_net_losses_on_disposal_NCA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)利润总额差额(特殊报表科目)</td><td>diff_total_profit_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>利润总额差额(合计平衡项目)</td><td>diff_total_profit_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>利润总额</td><td>total_profit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)所得税</td><td>less_income_tax</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)未确认的投资损失</td><td>add_unidentified_investment_loss</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)净利润差额(特殊报表科目)</td><td>diff_NP_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>净利润差额(合计平衡项目)</td><td>diff_NP_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>净利润</td><td>NP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>持续经营净利润</td><td>NP_continuing_operations</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>终止经营净利润</td><td>NP_discontinued_operations</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)少数股东损益</td><td>minority_interest_income</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>归属于母公司所有者的净利润</td><td>NP_parent_company</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)其他综合收益</td><td>OCI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>综合收益总额</td><td>TCI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)归属于少数股东综合收益总额</td><td>TCI_minority_shareholders</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>归属于母公司普通股东综合收益总额</td><td>TCI_common_shareholders</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>每股收益</td><td>EPS</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>基本每股收益</td><td>BEPS</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>稀释每股收益</td><td>DEPS</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8.3.4 企业合并现金流量表

## A. 8. 3. 4. 1 经营活动产生的现金流量

经营活动产生的现金流量包括销售商品、提供劳务收到的现金、收到的税费返还、收到其他与经营活动有关的现金、经营活动现金流入（金融类）、经营活动现金流入差额（特殊报表科目）、经营活动现金流入差额（合计平衡项目）、经营活动现金流入小计、购买商品、接受劳务支付的现金、支付给职工以及为职工支付的现金、支付的各项税费、支付其他与经营活动有关的现金、经营活动现金流出（金融类）、经营活动现金流出差额（特殊报表科目）、经营活动现金流出差额（合计平衡项目）、经营活动现金流出小计、经营活动产生的现金流量净额差额（合计平衡项目）、经营活动产生的现金流量净额等字段数据类型，应满足表A.90的要求。

表 A. 90 经营活动产生的现金流量

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>销售商品、提供劳务收到的现金</td><td>cash_received_from_sales_of_goods_or_rendering_services</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>收到的税费返还</td><td>refunds_of_taxes_and_levies</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>收到其他与经营活动有关的现金</td><td>other_CFO_received</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流入(金融类)</td><td>CFO_in</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流入差额(特殊报表科目)</td><td>diff_CFO_in_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流入差额(合计平衡项目)</td><td>diff_CFO_in_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流入小计</td><td>total_CFO_in</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>购买商品、接受劳务支付的现金</td><td>cash_paid_for_commodities_and_services</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>支付给职工以及为职工支付的现金</td><td>cash_paid_behalf_of_employees</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>支付的各项税费</td><td>various_tax es_paid</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>支付其他与经营活动有关的现金</td><td>other_CFO_p aid</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流出(金融类)</td><td>CFO_out</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流出差额(特殊报表科目)</td><td>diff_CFO_out_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流出差额(合计平衡项目)</td><td>diff_CFO_out_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动现金流出小计</td><td>total_CFO_out</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动产生的现金流量净额差额(合计平衡项目)</td><td>diff_CFO_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营活动产生的现金流量净额</td><td>CFO</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8. 3. 4. 2 投资活动产生的现金流量

投资活动产生的现金流量包括收回投资收到的现金、取得投资收益收到的现金、处置固定资产、无形资产和其他长期资产收回的现金净额、处置子公司及其他营业单位收到的现金净额、收到其他与投资活动有关的现金、投资活动现金流入差额（特殊报表科目）、投资活动现金流入差额（合计平衡项目）、投资活动现金流入小计、购建固定资产、无形资产和其他长期资产支付的现金、投资支付的现金、取得子公司及其他营业单位支付的现金净额、支付其他与投资活动有关的现金、投资活动现金流出差额（特殊报表科目）、投资活动现金流出差额（合计平衡项目）、投资活动现金流出小计、投资活动产生的现金流量净额差额（合计平衡项目）、投资活动产生的现金流量净额等字段数据类型，应满足表A.91的要求。

表 A. 91 投资活动产生的现金流量

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>收回投资收到的现金</td><td>cash_receipts_from_investments_withdrawal</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>取得投资收益收到的现金</td><td>cash_receipts_from_return_on_investments</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>处置固定资产、无形资产和其他长期资产收回的现金净额</td><td>net_cash_disposal_FA_IA_LTA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>处置子公司及其他营业单位收到的现金净额</td><td>net_cash_disposal_of_subsidiary_or_other_business_unit</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>收到其他与投资活动有关的现金</td><td>other_CFI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动现金流入差额(特殊报表科目)</td><td>diff_CFI_in_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动现金流入差额(合计平衡项目)</td><td>diff_CFI_in_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动现金流入小计</td><td>total_CFI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>购建固定资产、无形资产和其他长期资产支付的现金</td><td>cash_purchase_FA_IA_LTA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资支付的现金</td><td>cash_payment_for_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>取得子公司及其他营业单位支付的现金净额</td><td>net_cash_purchase_of_subsidiaries_and_other_associated_entities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>支付其他与投资活动有关的现金</td><td>other_investing_cash_outflow</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动现金流出差额(特殊报表科目)</td><td>diff_CFI_out_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动现金流出差额(合计平衡项目)</td><td>diff_CFI_out_balance_itemsdiff_CFI_out_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动现金流出小计</td><td>total_CFI_out</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动产生的现金流量净额差额(合计平衡项目)</td><td>diff_CFI_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资活动产生的现金流量净额</td><td>CFI</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8. 3. 4. 3 筹资活动产生的现金流量

筹资活动产生的现金流量包括吸收投资收到的现金、子公司吸收少数股东投资收到的现金、取得借款收到的现金、收到其他与筹资活动有关的现金、非公开发行债券收到的现金、筹资活动现金流入差额（特殊报表科目）、筹资活动现金流入差额（合计平衡项目）、筹资活动现金流入小计、偿还债务支付的现金、分配股利、利润或偿付利息支付的现金、子公司支付给少数股东的股利、利润、支付其他与筹资活动有关的现金、筹资活动现金流出差额（特殊报表科目）、筹资活动现金流出差额（合计平衡项目）、筹资活动现金流出小计、筹资活动产生的现金流量净额差额（合计平衡项目）、筹资活动产生的现金流量净额、汇率变动对现金的影响、直接法-现金及现金等价物净增加额差额（特殊报表科目）、直接法-现金及现金等价物净增加额差额（合计平衡项目）、现金及现金等价物净增加额、期初现金及现金等价物余额、期末现金及现金等价物余额等字段数据类型，应满足表A.92的要求。

表 A.92 筹资活动产生的现金流量

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>吸收投资收到的现金</td><td>cash_received_for_attracted_investment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>子公司吸收少数股东投资收到的现金</td><td>cash_received_investment_minority_shareholders_to_subsidiaries</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>取得借款收到的现金</td><td>cash_raised_from_loans</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>收到其他与筹资活动有关的现金</td><td>cash_received_from_other_financing_activities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>非公开发行债券收到的现金</td><td>cash_proceeds_of_bond_issue</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动现金流入差额(特殊报表科目)</td><td>diff_CFF_in_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动现金流入差额(合计平衡项目)</td><td>diff_CFF_in_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动现金流入小计</td><td>total_CFF_in</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>偿还债务支付的现金</td><td>cash_debt_repayment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>分配股利、利润或偿付利息支付的现金</td><td>cash_distribution_of_dividend_profit_or_interest_payment</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>子公司支付给少数股东的股利、利润</td><td>dividend_profit_paid_minority_shareholders_from_subsidiaries</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>支付其他与筹资活动有关的现金</td><td>including_other_financing_cash_outflow</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动现金流出差额(特殊报表科目)</td><td>diff_CFF_out_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动现金流出差额(合计平衡项目)</td><td>diff_CFF_out_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动现金流出小计</td><td>total_CFF_out</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动产生的现金流量净额差额(合计平衡项目)</td><td>diff_CFF_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>筹资活动产生的现金流量净额</td><td>CFF</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>汇率变动对现金的影响</td><td>effect_of_foreign_exchange_rate_changes_on_cash</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>直接法-现金及现金等价物净增加额差额(特殊报表科目)</td><td>net_increase_cash_and_cash_equivalents_direct_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>直接法-现金及现金等价物净增加额差额(合计平衡项目)</td><td>net_increase_cash_and_cash_equivalents_direct_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>现金及现金等价物净增加额</td><td>balance_of_cash_and_cash_equivalents_beginning_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>期初现金及现金等价物余额</td><td>balance_of_cash_and_cash_equivalents_beginning_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>期末现金及现金等价物余额</td><td>balance_of_cash_and_cash_equivalents_end_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A. 8. 3. 4. 4 补充材料

补充材料包括净利润、（加）资产减值准备、信用减值损失、固定资产折旧、油气资产折耗、生产性生物资产折旧、无形资产摊销、使用权资产折旧、长期待摊费用摊销、待摊费用减少、预提费用增加、处置固定资产、无形资产和其他长期资产的损失、固定资产报废损失、公允价值变动损失、财务费用、投资损失、递延所得税资产减少、递延所得税负债增加、存货的减少、经营性应收项目的减少、经营性应付项目的增加、未确认的投资损失、其他、间接法-经营活动现金流量净额差额（特殊报表科目）、间接法-经营活动现金流量净额差额（合计平衡项目）、间接法-经营活动产生的现金流量净额、债务转为资本、一年内到期的可转换公司债券、融资租入固定资产、现金的期末余额、（减）现金的期初余额、（加）现金等价物的期末余额、（减）现金等价物的期初余额、（加）间接法-现金净增加额差额（特殊报表科目）、间接法-现金净增加额差额（合计平衡项目）、间接法-现金及现金等价物净增加额等字段数据类型，应满足表A.93的要求。

表 A. 93 补充材料

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>净利润</td><td>NP</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)资产减值准备</td><td>depreciation_reserve_of_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>信用减值损失</td><td>impairment_losses_on_goodwill</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产折旧、油气资产折耗、生产性生物资产折旧</td><td>depreciation_charge</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>无形资产摊销</td><td>amortization_of_intangible_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>使用权资产折旧</td><td>amortisation_cost_ROU_assets</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>长期待摊费用摊销</td><td>amortization_of_LT_deferred_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>待摊费用减少</td><td>decrease_in_deferred_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>预提费用增加</td><td>increase_in_accrued_expenses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>处置固定资产、无形资产和其他长期资产的损失</td><td>losses_on_disposal_FA_IA_LTA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>固定资产报废损失</td><td>losses_on_discarding_FA</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>公允价值变动损失</td><td>losses_on_fair_value_change</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>财务费用</td><td>financial_expense</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>投资损失</td><td>investment_losses</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>递延所得税资产减少</td><td>decrease_of_deferred_income_tax_asset</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>递延所得税负债增加</td><td>increase_of_deferred_income_tax_liabilities</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>存货的减少</td><td>decrease_in_inventories</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营性应收项目的减少</td><td>decrease_of_operating_receivables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>经营性应付项目的增加</td><td>increase_of_operating_payables</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>未确认的投资损失</td><td>unidentified_investment_loss</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>其他</td><td>other_item</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>间接法-经营活动现金流量净额差额(特殊报表科目)</td><td>diff_CFO_indirect_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>间接法-经营活动现金流量净额差额(合计平衡项目)</td><td>diff_CFO_indirect_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>间接法-经营活动产生的现金流量净额</td><td>CFO_indirect_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>债务转为资本</td><td>debt_converted_to_share_capital</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>一年内到期的可转换公司债券</td><td>convertible_bonds_mature_within_one_year</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>融资租入固定资产</td><td>FA_acquired_under_financ e_leases</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>现金的期末余额</td><td>cash_end_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)现金的期初余额</td><td>cash_beginning_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)现金等价物的期末余额</td><td>cash_equivalents_end_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(减)现金等价物的期初余额</td><td>cash_equivalents_beginning_of_the_period</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>(加)间接法-现金净增加额差额(特殊报表科目)</td><td>diff_net_increase_cash_indirect_special_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>间接法-现金净增加额差额(合计平衡项目)</td><td>diff_net_increase_cash_indirect_balance_items</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr><tr><td>间接法-现金及现金等价物净增加额</td><td>net_increase_cash_and_cash_equivalents_indirect</td><td>—</td><td>DECIMAL</td><td>18,6</td><td>不必填</td><td>—</td></tr></table>

## A.9 监管模型设计

## A. 9.1 基本信息

基本信息包括交易市场主体引用、信息类型等字段数据类型，应满足表A.94的要求。

表 A.94 基本信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细-说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>交易市场主体引用</td><td>operating_institution_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>必填</td><td>—</td></tr><tr><td>信息类型</td><td>info_type</td><td>—</td><td>NUMBER</td><td>—</td><td>必填</td><td>枚举_监管报送信息类型</td></tr></table>

## A.9.2 业务规则及执行信息

业务规则及执行信息包括发布时间、生效时间、报告人主体引用、联系方式、报告时间、措施执行时间、规则类型、文件名称（链接文件）、具体内容、执行情况、备注等字段数据类型，应满足表A.95的要求。

表 A. 95 业务规则及执行信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>发布时间</td><td>publish_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>生效时间</td><td>effective_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>报告人主体引用</td><td>reporter_name_subject_ref</td><td>报告人(运营机构)</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>联系方式</td><td>contact_details</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>报告时间</td><td>report_time</td><td>—</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>措施执行时间</td><td>execution_time</td><td>—</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>规则类型</td><td>business_rule_type</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_业务规则文件类型</td></tr><tr><td>文件名称(链接文件)</td><td>file_name</td><td>—</td><td>FILE_OBJECT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>具体内容</td><td>file_content</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>执行情况</td><td>implementation</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>备注</td><td>remark</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A. 9.3 地方法规政策文件及落实信息

地方法规政策文件及落实信息包括发布单位、发布单位主体引用、文号、文件类型、文件名称、发布时间、生效时间、政策落实情况、废止时间、备注等字段数据类型，应满足表A.96的要求。

表 A. 96 地方法规政策文件及落实信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>发布单位</td><td>releasing_organization_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>发布单位主体引用</td><td>releasing_organization_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>文号</td><td>document_number</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>文件类型</td><td>file_type</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>文件名称</td><td>file_name</td><td>—</td><td>FILE_OBJECT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>发布时间</td><td>publish_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>生效时间</td><td>effective_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>政策落实情况</td><td>implementation</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>废止时间</td><td>expiry_time</td><td>—</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>备注</td><td>remark</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A.9.4 重大事项报告及措施信息

重大事项报告及措施信息包括报告人主体引用、联系方式、事件名称、报告时间、发生时间、地点、起因、目前状态、可能产生的影响及后果、已采取措施、拟进一步采取的措施、备注等字段数据类型，应满足表A.97的要求。

表 A.97 重大事项报告及措施信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>报告人主体引用</td><td>reporter_name_subject_ref</td><td>报告人(运营机构)</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>联系方式</td><td>contact_details</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>事件名称</td><td>major_events</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>报告时间</td><td>report_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>发生时间</td><td>occurring_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>地点</td><td>occurring_place</td><td>—</td><td>CHARACTER</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>起因</td><td>occurring_cause</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>目前状态</td><td>current_status</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>可能产生的影响及后果</td><td>possible_consequences_influence</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>已采取措施</td><td>taken_measures</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>拟进一步采取的措施</td><td>next_measure s</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>备注</td><td>remark</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A. 9.5 监管措施执行信息

监管措施执行信息包括报告人主体引用、联系方式、报告时间、采取的监管措施（文件链接）、监管机构名称、监管机构主体引用、违法违规、自律管理、监管措施对象、监管措施对象主体引用、违规情形、监管措施具体内容、采取监管措施时间、执行情况、备注等字段数据类型，应满足表A.98的要求。

表 A. 98 监管措施执行信息

<table><tr><td>中文名称</td><td>英文名称</td><td>详细说明</td><td>数据类型</td><td>数据长度</td><td>是否必填</td><td>枚举值说明</td></tr><tr><td>报告人主体引用</td><td>reporter_name_subject_ref</td><td>报告人(运营机构)</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>联系方式</td><td>contact_details</td><td>—</td><td>CHARACTER</td><td>512</td><td>不必填</td><td>—</td></tr><tr><td>报告时间</td><td>report_time</td><td>此处应指日期,可填零点</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>采取的监管措施(文件链接)</td><td>regulatory_measures_file</td><td>—</td><td>FILE_OBJECT</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>监管机构名称</td><td>regulator_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>监管机构主体引用</td><td>regulator_subject_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>违法违规</td><td>violation_of_laws_regulations</td><td>—</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_违法违规</td></tr><tr><td>自律管理</td><td>self_regulatory</td><td>当信息类型为5-自律管理执行时必填</td><td>NUMBER</td><td>—</td><td>不必填</td><td>枚举_自律管理</td></tr><tr><td>监管措施对象</td><td>regulated_object_name</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>监管措施对象主体引用</td><td>regulated_object_ref</td><td>—</td><td>CHARACTER</td><td>256</td><td>不必填</td><td>—</td></tr><tr><td>违规情形</td><td>violating_action</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>监管措施具体内容</td><td>sanction_content</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>采取监管措施时间</td><td>execution_time</td><td>—</td><td>DATETIME</td><td>—</td><td>不必填</td><td>—</td></tr><tr><td>执行情况</td><td>implementation</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr><tr><td>备注</td><td>remark</td><td>—</td><td>CHARACTER</td><td>1024</td><td>不必填</td><td>—</td></tr></table>

## A. 10 枚举项信息

枚举项信息包括枚举\_主体类型、枚举\_币种类型、枚举\_企业所属行业分类、枚举\_境内外类别、枚举\_主体资质类别、枚举\_市场角色类型、枚举\_中介类型、枚举\_金融资质类型、枚举\_适当性类别、枚举\_机构性质、枚举\_法定类型、枚举\_经济类型、枚举\_股份制企业类型、枚举\_规模类型、枚举\_企业标签、枚举\_机构代码类型、枚举\_企业状态、枚举\_个人身份证件类型、枚举\_学历、枚举\_职业、枚举\_性别、枚举\_账户类型、枚举\_账户用途、枚举\_账户状态、枚举\_关联关系、枚举\_产品功能、枚举\_产品类型、枚举\_信息披露方式、枚举\_产品规模单位、枚举\_服务方分类、枚举\_资金用途类型、枚举\_投资产品类型、枚举\_备案许可类型、枚举\_非公开发行范围、枚举\_非公开发行类型、枚举\_非公开发行股份类别、枚举\_债权期限单位、枚举\_计息方式、枚举\_兑付方式、枚举\_主体信用评级、枚举\_债务重组、枚举\_转让状态、枚举\_转让范围、枚举\_摘牌类型、枚举\_摘牌原因、枚举\_市场类型、枚举\_交易场所类别、枚举\_转让类型、枚举\_转让协议类型、枚举\_资产托管状态、枚举\_转让资产类型、枚举\_登记对象类型、枚举\_登记事项类型、枚举\_登记权利类型、枚举\_权利登记单位、枚举\_登记确权状态、枚举\_确权方式、枚举\_持有状态、枚举\_持有权利类型、枚举\_业务来源、枚举\_权利类型、枚举\_股份性质、枚举\_基金投资人分类、枚举\_结算类型、枚举\_信披类型、枚举\_提报来源类型、枚举\_财报会计期间类型、枚举\_公告类型、枚举\_重大事件类型、枚举\_事项类型、枚举\_状态、枚举\_报表周期类型、枚举\_企业所属行业管理型分类、枚举\_监管报送信息类型、枚举\_违法违规、枚举\_自律管理、枚举\_所有制性质、枚举\_公司或机构的设立方式、枚举\_财报格式类型、枚举\_业务规则文件类型、枚举\_投资者类别、枚举\_普通投资者风险承受能力类别、枚举\_收入来源、枚举\_可支配年收入情况、枚举\_资产情况、枚举\_债务情况、枚举\_投资知识情况、枚举\_投资经验、枚举\_投资期限、枚举\_投资品种、枚举\_期望收益、枚举\_风险偏好、枚举\_可承受的损失、枚举\_历史沿革事件类型、枚举\_历史沿革事件子类、枚举\_资金用途子类、枚举\_增信方式、枚举\_增信方性质、枚举\_非公开发行方类型、枚举\_资金来源、枚举\_企业所属行业大类、枚举\_企业所属行业中类、枚举\_股权性质标签、枚举\_代持状态、枚举\_金融行业及相关工作经历年限、枚举\_汇率类型、枚举\_服务状态等字段数据类型，应满足表A.99的要求。

表 A.99 枚举项信息

<table><tr><td>枚举项</td><td>枚举值</td><td>说明</td></tr><tr><td rowspan="2">枚举_主体类型</td><td>1</td><td>机构</td></tr><tr><td>2</td><td>个人</td></tr><tr><td rowspan="4">枚举_币种类型</td><td>156</td><td>人民币</td></tr><tr><td>840</td><td>美元</td></tr><tr><td>978</td><td>欧元</td></tr><tr><td>344</td><td>港币</td></tr><tr><td rowspan="3">枚举_企业所属行业分类</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>采矿业</td></tr><tr><td>2</td><td>制造业</td></tr><tr><td rowspan="18">枚举_企业所属行业分类</td><td>3</td><td>电力、热力、燃气及水生产和供应业</td></tr><tr><td>4</td><td>建筑业</td></tr><tr><td>5</td><td>批发和零售业</td></tr><tr><td>6</td><td>交通运输、仓储和邮政业</td></tr><tr><td>7</td><td>住宿和餐饮业</td></tr><tr><td>8</td><td>信息传输、软件和信息技术服务业</td></tr><tr><td>9</td><td>金融业</td></tr><tr><td>10</td><td>房地产业</td></tr><tr><td>11</td><td>租赁和商务服务业</td></tr><tr><td>12</td><td>科学研究和技术服务业</td></tr><tr><td>13</td><td>水利、环境和公共设施管理业</td></tr><tr><td>14</td><td>居民服务、修理和其他服务业</td></tr><tr><td>15</td><td>教育</td></tr><tr><td>16</td><td>卫生和社会工作</td></tr><tr><td>17</td><td>文化、体育和娱乐业</td></tr><tr><td>18</td><td>综合</td></tr><tr><td>19</td><td>农、林、牧、渔业</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_境内外类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>境内</td></tr><tr><td>2</td><td>境外</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_主体资质类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>市场角色</td></tr><tr><td>2</td><td>金融资质</td></tr><tr><td>3</td><td>账户资质</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="12">枚举_市场角色类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>服务企业</td></tr><tr><td>2</td><td>融资方</td></tr><tr><td>3</td><td>投资方</td></tr><tr><td>4</td><td>中介机构</td></tr><tr><td>5</td><td>登记结算机构</td></tr><tr><td>6</td><td>托管机构</td></tr><tr><td>7</td><td>交易市场/运营机构</td></tr><tr><td>8</td><td>普通服务用户</td></tr><tr><td>9</td><td>证券业协会</td></tr><tr><td>10</td><td>第三方托管机构</td></tr><tr><td>11</td><td>全国中小企业股份转让系统</td></tr><tr><td rowspan="7">枚举_市场角色类型</td><td>12</td><td>机构间私募产品报价与服务系统</td></tr><tr><td>30</td><td>证券业协会会员</td></tr><tr><td>31</td><td>证券业协会法定会员</td></tr><tr><td>32</td><td>证券业协会普通会员</td></tr><tr><td>33</td><td>证券业协会特别会员</td></tr><tr><td>40</td><td>运营机构会员</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="15">枚举_中介类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>推荐业务资格</td></tr><tr><td>2</td><td>财务顾问</td></tr><tr><td>3</td><td>受托管理人</td></tr><tr><td>4</td><td>专业服务业务资格</td></tr><tr><td>5</td><td>审计</td></tr><tr><td>6</td><td>法律</td></tr><tr><td>7</td><td>评估</td></tr><tr><td>8</td><td>转让服务业务资格</td></tr><tr><td>9</td><td>代理开户</td></tr><tr><td>10</td><td>居间介绍</td></tr><tr><td>11</td><td>投资咨询</td></tr><tr><td>12</td><td>担保机构</td></tr><tr><td>13</td><td>承销机构</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="17">枚举_金融资质类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>证券公司及子公司</td></tr><tr><td>2</td><td>证券公司资产管理产品</td></tr><tr><td>3</td><td>基金管理公司及子公司</td></tr><tr><td>4</td><td>基金管理公司及子公司产品</td></tr><tr><td>5</td><td>期货公司及子公司</td></tr><tr><td>6</td><td>期货公司及子公司产品</td></tr><tr><td>7</td><td>商业银行</td></tr><tr><td>8</td><td>银行理财产品</td></tr><tr><td>9</td><td>保险公司</td></tr><tr><td>10</td><td>保险产品</td></tr><tr><td>11</td><td>信托投资公司</td></tr><tr><td>12</td><td>信托产品</td></tr><tr><td>13</td><td>财务公司</td></tr><tr><td>14</td><td>依法登记的私募基金管理机构</td></tr><tr><td>15</td><td>依法备案的私募证券基金</td></tr><tr><td>16</td><td>社保基金</td></tr><tr><td rowspan="17">枚举_金融资质类型</td><td>17</td><td>企业年金</td></tr><tr><td>18</td><td>社会公益基金</td></tr><tr><td>19</td><td>财务顾问机构</td></tr><tr><td>20</td><td>资信评级机构</td></tr><tr><td>21</td><td>资产评估机构</td></tr><tr><td>22</td><td>会计师事务所</td></tr><tr><td>23</td><td>小额贷款公司</td></tr><tr><td>24</td><td>金融租赁公司</td></tr><tr><td>25</td><td>社会众筹机构</td></tr><tr><td>26</td><td>商业保理公司</td></tr><tr><td>27</td><td>金融资产管理公司</td></tr><tr><td>28</td><td>融资担保公司</td></tr><tr><td>29</td><td>典当行</td></tr><tr><td>30</td><td>投资咨询机构</td></tr><tr><td>31</td><td>符合条件的法人或其他组织</td></tr><tr><td>32</td><td>依法备案的私募股权基金</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_适当性类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>合格</td></tr><tr><td>2</td><td>豁免</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_机构性质</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>企业</td></tr><tr><td>2</td><td>国家行政机关</td></tr><tr><td>3</td><td>事业单位</td></tr><tr><td>4</td><td>合作组织</td></tr><tr><td>5</td><td>社会团体</td></tr><tr><td>6</td><td>农民专业合作社</td></tr><tr><td>7</td><td>个体工商</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_法定类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>合伙企业</td></tr><tr><td>2</td><td>独资企业</td></tr><tr><td>3</td><td>公司企业</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_经济类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>国有经济</td></tr><tr><td>2</td><td>集体经济</td></tr><tr><td>3</td><td>私营经济</td></tr><tr><td rowspan="5">枚举_经济类型</td><td>4</td><td>联营经济</td></tr><tr><td>5</td><td>股份制经济</td></tr><tr><td>6</td><td>外商投资经济</td></tr><tr><td>7</td><td>港澳台投资经济</td></tr><tr><td>255</td><td>其他经济</td></tr><tr><td rowspan="4">枚举_股份制企业类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>有限责任公司</td></tr><tr><td>2</td><td>股份有限公司</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_规模类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>大型企业</td></tr><tr><td>2</td><td>中型企业</td></tr><tr><td>3</td><td>小型企业</td></tr><tr><td>4</td><td>微型企业</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="24">枚举_企业标签</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>专精特新小巨人</td></tr><tr><td>2</td><td>专精特新中小企业</td></tr><tr><td>3</td><td>创新型中小企业</td></tr><tr><td>4</td><td>科技型中小企业</td></tr><tr><td>5</td><td>国家高新技术企业</td></tr><tr><td>6</td><td>万人计划</td></tr><tr><td>7</td><td>上市公司系</td></tr><tr><td>8</td><td>专利创业项目</td></tr><tr><td>9</td><td>专利巨头</td></tr><tr><td>10</td><td>世界500强企业</td></tr><tr><td>11</td><td>中国500强企业</td></tr><tr><td>12</td><td>中国专利奖</td></tr><tr><td>13</td><td>中国民营企业500强</td></tr><tr><td>14</td><td>中国青年科技奖</td></tr><tr><td>15</td><td>中央企业</td></tr><tr><td>16</td><td>制造业单项冠军</td></tr><tr><td>17</td><td>千人计划</td></tr><tr><td>18</td><td>双一流</td></tr><tr><td>19</td><td>国家科技奖</td></tr><tr><td>20</td><td>国家科技重大专项</td></tr><tr><td>21</td><td>国家级研发平台</td></tr><tr><td>22</td><td>国家重点研发计划</td></tr><tr><td>23</td><td>大专院校主管部门</td></tr><tr><td rowspan="30">枚举_企业标签</td><td>24</td><td>头部资本</td></tr><tr><td>25</td><td>技术先进型服务企业</td></tr><tr><td>26</td><td>技术创新示范企业</td></tr><tr><td>27</td><td>有专利</td></tr><tr><td>28</td><td>有产学研合作</td></tr><tr><td>29</td><td>有标准必要专利</td></tr><tr><td>30</td><td>有海外布局</td></tr><tr><td>31</td><td>独角兽</td></tr><tr><td>32</td><td>百人计划</td></tr><tr><td>33</td><td>瞪羚企业</td></tr><tr><td>34</td><td>知识产权海关备案</td></tr><tr><td>35</td><td>连续获投</td></tr><tr><td>36</td><td>长江学者</td></tr><tr><td>37</td><td>隐形冠军</td></tr><tr><td>38</td><td>院士</td></tr><tr><td>39</td><td>专利破零</td></tr><tr><td>40</td><td>专精特新企业</td></tr><tr><td>41</td><td>地方专利奖</td></tr><tr><td>42</td><td>有专利纠纷</td></tr><tr><td>43</td><td>有专利许可</td></tr><tr><td>44</td><td>有专利质押</td></tr><tr><td>45</td><td>有专利转让</td></tr><tr><td>46</td><td>有技术高管</td></tr><tr><td>47</td><td>有高价值发明专利</td></tr><tr><td>48</td><td>标准制定单位</td></tr><tr><td>49</td><td>被技术借鉴</td></tr><tr><td>252</td><td>“专精特新”专板企业</td></tr><tr><td>253</td><td>上市后备企业</td></tr><tr><td>254</td><td>无标签</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_机构代码类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>统一社会信用代码</td></tr><tr><td>2</td><td>组织机构代码证</td></tr><tr><td>3</td><td>营业执照</td></tr><tr><td>4</td><td>税务登记证</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="3">枚举_企业状态</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>存续</td></tr><tr><td>2</td><td>在业</td></tr><tr><td rowspan="7">枚举_企业状态</td><td>3</td><td>吊销</td></tr><tr><td>4</td><td>注销</td></tr><tr><td>5</td><td>迁入</td></tr><tr><td>6</td><td>迁出</td></tr><tr><td>7</td><td>停业</td></tr><tr><td>8</td><td>清算</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_个人身份证件类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>身份证</td></tr><tr><td>2</td><td>护照</td></tr><tr><td>3</td><td>港澳居民来往内地通行证</td></tr><tr><td>4</td><td>户口本</td></tr><tr><td>5</td><td>台胞证</td></tr><tr><td>6</td><td>香港永久性居民身份证</td></tr><tr><td>7</td><td>澳门居民身份证</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_学历</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>博士</td></tr><tr><td>2</td><td>硕士</td></tr><tr><td>3</td><td>学士</td></tr><tr><td>4</td><td>大专</td></tr><tr><td>5</td><td>中专</td></tr><tr><td>6</td><td>高中</td></tr><tr><td>7</td><td>初中及以下</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="8">枚举_职业</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>党政机关工作人员</td></tr><tr><td>2</td><td>企业事业单位职工</td></tr><tr><td>3</td><td>农民</td></tr><tr><td>4</td><td>个体工商户</td></tr><tr><td>5</td><td>学生</td></tr><tr><td>6</td><td>无业</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_性别</td><td>1</td><td>男</td></tr><tr><td>2</td><td>女</td></tr><tr><td rowspan="3">枚举_账户类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>证券账户</td></tr><tr><td>2</td><td>资金账户</td></tr><tr><td rowspan="2">枚举_账户类型</td><td>3</td><td>游客账户</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_账户用途</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>股份/股权</td></tr><tr><td>2</td><td>债券</td></tr><tr><td>4</td><td>可用金/保证金</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_账户状态</td><td>1</td><td>正常</td></tr><tr><td>2</td><td>注销</td></tr><tr><td>3</td><td>冻结</td></tr><tr><td>4</td><td>未实名认证</td></tr><tr><td rowspan="2">枚举_关联关系</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>资金账户与证券账户关联</td></tr><tr><td rowspan="6">枚举_产品功能</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>非公开发行融资</td></tr><tr><td>2</td><td>挂牌</td></tr><tr><td>3</td><td>托管</td></tr><tr><td>4</td><td>转板</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_产品类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>私募股权</td></tr><tr><td>2</td><td>私募股份</td></tr><tr><td>3</td><td>可转债/合规发行的其他债券品种</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_信息披露方式</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>非公开披露</td></tr><tr><td>2</td><td>定向披露</td></tr><tr><td>3</td><td>公开披露</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_产品规模单位</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>货币价值(元)</td></tr><tr><td>2</td><td>基金份额(份)</td></tr><tr><td>3</td><td>债权(张)</td></tr><tr><td>4</td><td>股数(股)</td></tr><tr><td>5</td><td>理财产品份额(份)</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="18">枚举_服务方分类</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>登记机构</td></tr><tr><td>2</td><td>持续服务机构</td></tr><tr><td>3</td><td>推荐商</td></tr><tr><td>4</td><td>信披义务人</td></tr><tr><td>5</td><td>托管机构</td></tr><tr><td>6</td><td>承销机构</td></tr><tr><td>7</td><td>保荐机构</td></tr><tr><td>8</td><td>管理人</td></tr><tr><td>9</td><td>受托管理人</td></tr><tr><td>10</td><td>担保机构</td></tr><tr><td>11</td><td>资产评估机构</td></tr><tr><td>12</td><td>律师事务所</td></tr><tr><td>13</td><td>会计师事务所</td></tr><tr><td>14</td><td>增信机构</td></tr><tr><td>15</td><td>信用评级机构</td></tr><tr><td>16</td><td>交易市场/运营机构</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_资金用途类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>经营类</td></tr><tr><td>2</td><td>投资类</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_投资产品类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>权益类产品</td></tr><tr><td>2</td><td>商品及金融衍生品类产品</td></tr><tr><td>3</td><td>混合类产品</td></tr><tr><td>4</td><td>固定收益类产品</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_备案许可类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>产品注册</td></tr><tr><td>2</td><td>产品备案</td></tr><tr><td>3</td><td>产品审核</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_非公开发行范围</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>普通</td></tr><tr><td>2</td><td>定向</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_非公开发行类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>首次</td></tr><tr><td rowspan="2">枚举_非公开发行类型</td><td>2</td><td>增发</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_非公开发行股份类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>自然人股</td></tr><tr><td>2</td><td>国家股</td></tr><tr><td>3</td><td>国有法人股</td></tr><tr><td>4</td><td>社会法人股</td></tr><tr><td>5</td><td>非法人机构股</td></tr><tr><td>6</td><td>外资法人股</td></tr><tr><td>7</td><td>外资自然人股</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_债权期限单位</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>年</td></tr><tr><td>2</td><td>月</td></tr><tr><td>3</td><td>日</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_计息方式</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>act/365</td></tr><tr><td>2</td><td>act/360</td></tr><tr><td>3</td><td>act/180</td></tr><tr><td>4</td><td>按月计息</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_兑付方式</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>按月付息,到期还本</td></tr><tr><td>2</td><td>按季付息,到期还本</td></tr><tr><td>3</td><td>按半年付息,到期还本</td></tr><tr><td>4</td><td>按年付息,到期还本</td></tr><tr><td>5</td><td>到期还本付息</td></tr><tr><td>6</td><td>等额本金</td></tr><tr><td>7</td><td>等额本息</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="8">枚举_主体信用评级</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>AAA</td></tr><tr><td>2</td><td>AA+</td></tr><tr><td>3</td><td>AA</td></tr><tr><td>4</td><td>AA-</td></tr><tr><td>5</td><td>A+</td></tr><tr><td>6</td><td>A</td></tr><tr><td>7</td><td>A-</td></tr><tr><td rowspan="14">枚举_主体信用评级</td><td>8</td><td>BBB+</td></tr><tr><td>9</td><td>BBB</td></tr><tr><td>10</td><td>BBB-</td></tr><tr><td>11</td><td>BB+</td></tr><tr><td>12</td><td>BB</td></tr><tr><td>13</td><td>BB-</td></tr><tr><td>14</td><td>B+</td></tr><tr><td>15</td><td>B</td></tr><tr><td>16</td><td>B-</td></tr><tr><td>17</td><td>CCC</td></tr><tr><td>18</td><td>CC</td></tr><tr><td>19</td><td>C</td></tr><tr><td>20</td><td>0</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_债务重组</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>以资产清偿债务</td></tr><tr><td>2</td><td>将债务转为权益工具</td></tr><tr><td>3</td><td>调整债务本金</td></tr><tr><td>4</td><td>改变债务利息</td></tr><tr><td>5</td><td>变更还款期限</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_转让状态</td><td>1</td><td>挂牌</td></tr><tr><td>2</td><td>摘牌</td></tr><tr><td rowspan="4">枚举_转让范围</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>普通</td></tr><tr><td>2</td><td>定向</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_摘牌类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>自愿终止</td></tr><tr><td>2</td><td>强制终止</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_摘牌原因</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>直接退市</td></tr><tr><td>2</td><td>转板</td></tr><tr><td>3</td><td>被上市公司或新三板挂牌公司收购兼并</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_市场类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>上交所主板</td></tr><tr><td rowspan="15">枚举_市场类型</td><td>2</td><td>上交所科创板</td></tr><tr><td>3</td><td>深交所主板</td></tr><tr><td>4</td><td>深交所创业板</td></tr><tr><td>5</td><td>区域性股权市场</td></tr><tr><td>6</td><td>北交所</td></tr><tr><td>7</td><td>新三板基础层</td></tr><tr><td>8</td><td>新三板创新层</td></tr><tr><td>9</td><td>香港证券交易所</td></tr><tr><td>10</td><td>纽约证券交易所</td></tr><tr><td>11</td><td>纳斯达克交易所</td></tr><tr><td>12</td><td>伦敦证券交易所</td></tr><tr><td>13</td><td>欧洲证券交易所</td></tr><tr><td>14</td><td>东京证券交易所</td></tr><tr><td>15</td><td>新加坡证券交易所</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="3">枚举_交易场所类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>区域性股权市场</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="11">枚举_转让类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>非公开发行融资</td></tr><tr><td>2</td><td>偿付回购</td></tr><tr><td>3</td><td>转让</td></tr><tr><td>4</td><td>证券转换</td></tr><tr><td>5</td><td>非交易过户</td></tr><tr><td>6</td><td>质押融资</td></tr><tr><td>7</td><td>还款解质押</td></tr><tr><td>8</td><td>介绍贷款融资</td></tr><tr><td>9</td><td>介绍贷款还款</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_转让协议类型</td><td>1</td><td>线上协议</td></tr><tr><td>2</td><td>线下协议</td></tr><tr><td rowspan="4">枚举_资产托管状态</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>股交中心登记托管</td></tr><tr><td>2</td><td>未托管</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_转让资产类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>私募股权</td></tr><tr><td>2</td><td>私募股份</td></tr><tr><td>3</td><td>可转债/合规发行的其他债券品种</td></tr><tr><td rowspan="3">枚举_转让资产类型</td><td>6</td><td>理财产品</td></tr><tr><td>7</td><td>知识产权</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_登记对象类型</td><td>1</td><td>权利登记</td></tr><tr><td>2</td><td>名册登记</td></tr><tr><td rowspan="4">枚举_登记事项类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>托管登记(包含托管和解托管)</td></tr><tr><td>2</td><td>转让登记</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_登记权利类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>财产权利</td></tr><tr><td>2</td><td>质权</td></tr><tr><td>3</td><td>抵押权</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_权利登记单位</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>货币价值(元)</td></tr><tr><td>2</td><td>基金份额(份)</td></tr><tr><td>3</td><td>债权(张)</td></tr><tr><td>4</td><td>股数(股)</td></tr><tr><td>5</td><td>理财产品份额(份)</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_登记确权状态</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>确权</td></tr><tr><td>2</td><td>未确权</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_确权方式</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>权利人确权</td></tr><tr><td>2</td><td>义务人确权</td></tr><tr><td>3</td><td>第三方确权</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_持有状态</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>流通股</td></tr><tr><td>2</td><td>非流通股</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_持有权利类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>普通股</td></tr><tr><td>2</td><td>优先股</td></tr><tr><td>3</td><td>混合股股票</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="14">枚举_业务来源</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>托管</td></tr><tr><td>2</td><td>解托管</td></tr><tr><td>3</td><td>买入</td></tr><tr><td>4</td><td>卖出</td></tr><tr><td>5</td><td>配股</td></tr><tr><td>6</td><td>红股</td></tr><tr><td>7</td><td>质押</td></tr><tr><td>8</td><td>解质押</td></tr><tr><td>9</td><td>冻结</td></tr><tr><td>10</td><td>解冻</td></tr><tr><td>11</td><td>债转股</td></tr><tr><td>12</td><td>减资</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_权利类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>股权</td></tr><tr><td>2</td><td>股份</td></tr><tr><td>3</td><td>债权</td></tr><tr><td>4</td><td>基金份额</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="8">枚举_股份性质</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>无限售条件流通股</td></tr><tr><td>2</td><td>已确权无限售条件流通股</td></tr><tr><td>3</td><td>有限售条件的流通股</td></tr><tr><td>4</td><td>高管锁定股</td></tr><tr><td>5</td><td>个人类限售股</td></tr><tr><td>6</td><td>机构类限售股</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_基金投资人分类</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>普通投资人</td></tr><tr><td>2</td><td>基金管理人</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_结算类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>交易结算</td></tr><tr><td>2</td><td>非交易结算</td></tr><tr><td>3</td><td>产品收益</td></tr><tr><td>255</td><td>其他</td></tr><tr><td>枚举_信披类型</td><td>0</td><td>空值</td></tr><tr><td rowspan="14">枚举_信披类型</td><td>1</td><td>企业信息</td></tr><tr><td>2</td><td>审查信息</td></tr><tr><td>3</td><td>监管信息</td></tr><tr><td>4</td><td>企业报告</td></tr><tr><td>5</td><td>企业公告</td></tr><tr><td>6</td><td>企业重大事件</td></tr><tr><td>7</td><td>企业诚信档案</td></tr><tr><td>8</td><td>企业财务信息</td></tr><tr><td>9</td><td>企业经营信息</td></tr><tr><td>10</td><td>第三方拓展信息</td></tr><tr><td>11</td><td>历史沿革</td></tr><tr><td>12</td><td>中介业务开展信息</td></tr><tr><td>13</td><td>风险处置</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="10">枚举_提报来源类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>交易所</td></tr><tr><td>2</td><td>监管机构</td></tr><tr><td>3</td><td>中介机构</td></tr><tr><td>4</td><td>企业(自身)</td></tr><tr><td>5</td><td>政务机关</td></tr><tr><td>6</td><td>金融机构</td></tr><tr><td>7</td><td>征信机构</td></tr><tr><td>8</td><td>数据服务企业</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_财报会计期间类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>年报</td></tr><tr><td>2</td><td>半年报</td></tr><tr><td>3</td><td>一季报</td></tr><tr><td>4</td><td>三季报</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_公告类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>股票限售及解除限售</td></tr><tr><td>2</td><td>公司基本信息变更</td></tr><tr><td>3</td><td>非公开发行</td></tr><tr><td>4</td><td>定期报告、会计差错更正</td></tr><tr><td>5</td><td>权益分派</td></tr><tr><td>6</td><td>股份冻结</td></tr><tr><td>7</td><td>股东持股变动</td></tr><tr><td>8</td><td>股东大会</td></tr><tr><td rowspan="10">枚举_公告类型</td><td>9</td><td>设购售子公司或其他资产</td></tr><tr><td>10</td><td>承诺书、追认会议决议</td></tr><tr><td>11</td><td>股票申报及转让价格异常</td></tr><tr><td>12</td><td>关联转让未回避表决</td></tr><tr><td>13</td><td>更换中介机构、会所更名</td></tr><tr><td>14</td><td>暂停转让、终止挂牌</td></tr><tr><td>15</td><td>其他公告</td></tr><tr><td>16</td><td>董监高、控股股东、实控人变更</td></tr><tr><td>17</td><td>会议届次调整、更正</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_重大事件类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>投资者资金存放、动用情形或者划转路径不符合《办法》第二十四条和省级人民政府实施细则、操作办法的规定</td></tr><tr><td>2</td><td>证券(或股权)转让、结算的重大异常事件</td></tr><tr><td>3</td><td>重大信息安全事件</td></tr><tr><td>4</td><td>其他影响或者可能影响市场安全稳定运行、损害投资者合法权益的重大事件</td></tr><tr><td>5</td><td>投资者在区域性股权市场内买卖证券的资金、投资者的证券被挪用</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="14">枚举_事项类型</td><td>00000</td><td>空值</td></tr><tr><td>10001</td><td>违法违规-机构-行政监管措施-责令改正</td></tr><tr><td>10002</td><td>违法违规-机构-行政监管措施-监管谈话</td></tr><tr><td>10003</td><td>违法违规-机构-行政监管措施-出具警示函</td></tr><tr><td>10004</td><td>违法违规-机构-行政监管措施-责令公开说明</td></tr><tr><td>10005</td><td>违法违规-机构-行政监管措施-责令参加培训</td></tr><tr><td>10006</td><td>违法违规-机构-行政监管措施-责令定期报告</td></tr><tr><td>10007</td><td>违法违规-机构-行政监管措施-认定为不适当人选</td></tr><tr><td>10008</td><td>违法违规-机构-行政监管措施-暂不受理与行政许可有关的文件</td></tr><tr><td>10009</td><td>违法违规-机构-行政监管措施-责令增加内部合规检查的次数</td></tr><tr><td>10010</td><td>违法违规-机构-行政监管措施-公开谴责</td></tr><tr><td>10011</td><td>违法违规-机构-行政监管措施-责令处分有关人员</td></tr><tr><td>10012</td><td>违法违规-机构-行政监管措施-责令停止职权或解除职务</td></tr><tr><td>10013</td><td>违法违规-机构-行政监管措施-责令更换董事、监事、高级管理人员或者限制其权利</td></tr><tr><td rowspan="33">枚举_事项类型</td><td>10014</td><td>违法违规-机构-行政监管措施-撤销任职资格</td></tr><tr><td>10015</td><td>违法违规-机构-行政监管措施-暂停核准新业务或者增设、收购营业性分支机构申请</td></tr><tr><td>10016</td><td>违法违规-机构-行政监管措施-限制证券期货经营机构业务活动</td></tr><tr><td>10017</td><td>违法违规-机构-行政监管措施-限制股东权利或者责令转让股权</td></tr><tr><td>10018</td><td>违法违规-机构-行政监管措施-临时接管</td></tr><tr><td>10019</td><td>违法违规-机构-行政监管措施-撤销、注销业务许可</td></tr><tr><td>10020</td><td>违法违规-机构-行政监管措施-其他</td></tr><tr><td>10101</td><td>违法违规-机构-行政处罚-责令改正</td></tr><tr><td>10102</td><td>违法违规-机构-行政处罚-警告</td></tr><tr><td>10103</td><td>违法违规-机构-行政处罚-没收违法所得、没收非法财物</td></tr><tr><td>10104</td><td>违法违规-机构-行政处罚-罚款</td></tr><tr><td>10105</td><td>违法违规-机构-行政处罚-吊销从业资格证书/撤销证券从业资格、期货从业资格</td></tr><tr><td>10106</td><td>违法违规-机构-行政处罚-暂扣或吊销许可证</td></tr><tr><td>10107</td><td>违法违规-机构-行政处罚-暂停或撤销资格/撤销董事、监管和高级管理人员任职资格</td></tr><tr><td>10108</td><td>违法违规-机构-行政处罚-责令停业</td></tr><tr><td>10109</td><td>违法违规-机构-行政处罚-责令关闭</td></tr><tr><td>10110</td><td>违法违规-机构-行政处罚-其他</td></tr><tr><td>10200</td><td>违法违规-机构-市场禁入-永久性</td></tr><tr><td>10201</td><td>违法违规-机构-市场禁入-1年</td></tr><tr><td>10202</td><td>违法违规-机构-市场禁入-2年</td></tr><tr><td>10203</td><td>违法违规-机构-市场禁入-3年</td></tr><tr><td>10204</td><td>违法违规-机构-市场禁入-4年</td></tr><tr><td>10205</td><td>违法违规-机构-市场禁入-5年</td></tr><tr><td>10206</td><td>违法违规-机构-市场禁入-6年</td></tr><tr><td>10207</td><td>违法违规-机构-市场禁入-7年</td></tr><tr><td>10208</td><td>违法违规-机构-市场禁入-8年</td></tr><tr><td>10209</td><td>违法违规-机构-市场禁入-9年</td></tr><tr><td>10210</td><td>违法违规-机构-市场禁入-10年</td></tr><tr><td>11001</td><td>违法违规-个人-行政监管措施-责令改正</td></tr><tr><td>11002</td><td>违法违规-个人-行政监管措施-监管谈话</td></tr><tr><td>11003</td><td>违法违规-个人-行政监管措施-出具警示函</td></tr><tr><td>11004</td><td>违法违规-个人-行政监管措施-责令公开说明</td></tr><tr><td>11005</td><td>违法违规-个人-行政监管措施-责令参加培训</td></tr><tr><td rowspan="31">枚举_事项类型</td><td>11006</td><td>违法违规-个人-行政监管措施-责令定期报告</td></tr><tr><td>11007</td><td>违法违规-个人-行政监管措施-认定为不适当人选</td></tr><tr><td>11008</td><td>违法违规-个人-行政监管措施-暂不受理与行政许可有关的文件</td></tr><tr><td>11009</td><td>违法违规-个人-行政监管措施-责令增加内部合规检查的次数</td></tr><tr><td>11010</td><td>违法违规-个人-行政监管措施-公开谴责</td></tr><tr><td>11011</td><td>违法违规-个人-行政监管措施-责令处分有关人员</td></tr><tr><td>11012</td><td>违法违规-个人-行政监管措施-责令停止职权或解除职务</td></tr><tr><td>11013</td><td>违法违规-个人-行政监管措施-责令更换董事、监事、高级管理人员或者限制其权利</td></tr><tr><td>11014</td><td>违法违规-个人-行政监管措施-撤销任职资格</td></tr><tr><td>11015</td><td>违法违规-个人-行政监管措施-暂停核准新业务或者增设、收购营业性分支机构申请</td></tr><tr><td>11016</td><td>违法违规-个人-行政监管措施-限制证券期货经营机构业务活动</td></tr><tr><td>11017</td><td>违法违规-个人-行政监管措施-限制股东权利或者责令转让股权</td></tr><tr><td>11018</td><td>违法违规-个人-行政监管措施-临时接管</td></tr><tr><td>11019</td><td>违法违规-个人-行政监管措施-撤销、注销业务许可</td></tr><tr><td>11020</td><td>违法违规-个人-行政监管措施-其他</td></tr><tr><td>11101</td><td>违法违规-个人-行政处罚-责令改正</td></tr><tr><td>11102</td><td>违法违规-个人-行政处罚-警告</td></tr><tr><td>11103</td><td>违法违规-个人-行政处罚-没收违法所得、没收非法财物</td></tr><tr><td>11104</td><td>违法违规-个人-行政处罚-罚款</td></tr><tr><td>11105</td><td>违法违规-个人-行政处罚-吊销从业资格证书/撤销证券从业资格、期货从业资格</td></tr><tr><td>11106</td><td>违法违规-个人-行政处罚-暂扣或吊销许可证</td></tr><tr><td>11107</td><td>违法违规-个人-行政处罚-暂停或撤销资格/撤销董事、监管和高级管理人员任职资格</td></tr><tr><td>11108</td><td>违法违规-个人-行政处罚-责令停业</td></tr><tr><td>11109</td><td>违法违规-个人-行政处罚-责令关闭</td></tr><tr><td>11110</td><td>违法违规-个人-行政处罚-其他</td></tr><tr><td>11200</td><td>违法违规-个人-市场禁入-永久性</td></tr><tr><td>11201</td><td>违法违规-个人-市场禁入-1年</td></tr><tr><td>11202</td><td>违法违规-个人-市场禁入-2年</td></tr><tr><td>11203</td><td>违法违规-个人-市场禁入-3年</td></tr><tr><td>11204</td><td>违法违规-个人-市场禁入-4年</td></tr><tr><td>11205</td><td>违法违规-个人-市场禁入-5年</td></tr><tr><td rowspan="25">枚举_事项类型</td><td>11206</td><td>违法违规-个人-市场禁入-6年</td></tr><tr><td>11207</td><td>违法违规-个人-市场禁入-7年</td></tr><tr><td>11208</td><td>违法违规-个人-市场禁入-8年</td></tr><tr><td>11209</td><td>违法违规-个人-市场禁入-9年</td></tr><tr><td>11210</td><td>违法违规-个人-市场禁入-10年</td></tr><tr><td>20001</td><td>自律管理-机构-自律管理措施-书面警示</td></tr><tr><td>20002</td><td>自律管理-机构-自律管理措施-监管谈话</td></tr><tr><td>20003</td><td>自律管理-机构-自律管理措施-要求限期改正</td></tr><tr><td>20004</td><td>自律管理-机构-自律管理措施-要求公开更正、澄清或说明</td></tr><tr><td>20005</td><td>自律管理-机构-自律管理措施-暂停证券账户交易</td></tr><tr><td>20006</td><td>自律管理-机构-自律管理措施-限制证券账户交易</td></tr><tr><td>20007</td><td>自律管理-机构-自律管理措施-其他</td></tr><tr><td>20101</td><td>自律管理-机构-纪律处分措施-警告/批评</td></tr><tr><td>20102</td><td>自律管理-机构-纪律处分措施-通报批评</td></tr><tr><td>20103</td><td>自律管理-机构-纪律处分措施-公开谴责</td></tr><tr><td>20104</td><td>自律管理-机构-纪律处分措施-认定为不适当人选</td></tr><tr><td>20105</td><td>自律管理-机构-纪律处分措施-暂停或限制交易/取消交易权限</td></tr><tr><td>20106</td><td>自律管理-机构-纪律处分措施-暂停或取消相关业务资格</td></tr><tr><td>20107</td><td>自律管理-机构-纪律处分措施-暂停部分会员权利</td></tr><tr><td>20108</td><td>自律管理-机构-纪律处分措施-暂停会员(或参与人)资格</td></tr><tr><td>20109</td><td>自律管理-机构-纪律处分措施-取消会员(或参与人)资格</td></tr><tr><td>20110</td><td>自律管理-机构-纪律处分措施-终止上市</td></tr><tr><td>20111</td><td>自律管理-机构-纪律处分措施-暂停执业</td></tr><tr><td>20112</td><td>自律管理-机构-纪律处分措施-停止执业</td></tr><tr><td>20113</td><td>自律管理-机构-纪律处分措施-训诫</td></tr><tr><td rowspan="7">枚举_事项类型</td><td>20114</td><td>自律管理-机构-纪律处分措施-其他</td></tr><tr><td>21001</td><td>自律管理-个人-自律管理措施-书面警示</td></tr><tr><td>21002</td><td>自律管理-个人-自律管理措施-监管谈话</td></tr><tr><td>21003</td><td>自律管理-个人-自律管理措施-要求限期改正</td></tr><tr><td>21004</td><td>自律管理-个人-自律管理措施-要求公开更正、澄清或说明</td></tr><tr><td>21005</td><td>自律管理-个人-自律管理措施-暂停证券账户交易</td></tr><tr><td>21006</td><td>自律管理-个人-自律管理措施-限制证券账户交易</td></tr><tr><td rowspan="14">枚举_事项类型</td><td>21007</td><td>自律管理-个人-自律管理措施-其他</td></tr><tr><td>21101</td><td>自律管理-个人-纪律处分措施-警告/批评</td></tr><tr><td>21102</td><td>自律管理-个人-纪律处分措施-通报批评</td></tr><tr><td>21103</td><td>自律管理-个人-纪律处分措施-公开谴责</td></tr><tr><td>21104</td><td>自律管理-个人-纪律处分措施-认定为不适当人选</td></tr><tr><td>21105</td><td>自律管理-个人-纪律处分措施-暂停或限制交易/取消交易权限</td></tr><tr><td>21106</td><td>自律管理-个人-纪律处分措施-暂停或取消相关业务资格</td></tr><tr><td>21107</td><td>自律管理-个人-纪律处分措施-暂停部分会员权利</td></tr><tr><td>21108</td><td>自律管理-个人-纪律处分措施-暂停会员(或参与人)资格</td></tr><tr><td>21109</td><td>自律管理-个人-纪律处分措施-取消会员(或参与人)资格</td></tr><tr><td>21110</td><td>自律管理-个人-纪律处分措施-暂停执业</td></tr><tr><td>21111</td><td>自律管理-个人-纪律处分措施-停止执业</td></tr><tr><td>21112</td><td>自律管理-个人-纪律处分措施-训诫</td></tr><tr><td>21113</td><td>自律管理-个人-纪律处分措施-其他</td></tr><tr><td rowspan="2">枚举_状态</td><td>1</td><td>生效</td></tr><tr><td>2</td><td>失效</td></tr><tr><td rowspan="6">枚举_报表周期类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>年报</td></tr><tr><td>2</td><td>半年报</td></tr><tr><td>3</td><td>季报</td></tr><tr><td>4</td><td>月报</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="14">枚举_企业所属行业管理型分类</td><td>0</td><td>空值</td></tr><tr><td>A</td><td>农、林、牧、渔业</td></tr><tr><td>B</td><td>采矿业</td></tr><tr><td>C</td><td>制造业</td></tr><tr><td>D</td><td>电力、热力、燃气及水生产和供应业</td></tr><tr><td>E</td><td>建筑业</td></tr><tr><td>F</td><td>批发和零售业</td></tr><tr><td>G</td><td>交通运输、仓储和邮政业</td></tr><tr><td>H</td><td>住宿和餐饮业</td></tr><tr><td>I</td><td>信息传输、软件和信息技术服务业</td></tr><tr><td>J</td><td>金融业</td></tr><tr><td>K</td><td>房地产业</td></tr><tr><td>L</td><td>租赁和商务服务业</td></tr><tr><td>M</td><td>科学研究和技术服务业</td></tr><tr><td rowspan="8">枚举_企业所属行业管理型分类</td><td>N</td><td>水利、环境和公共设施管理业</td></tr><tr><td>0</td><td>居民服务、修理和其他服务业</td></tr><tr><td>P</td><td>教育</td></tr><tr><td>Q</td><td>卫生和社会工作</td></tr><tr><td>R</td><td>文化、体育和娱乐业</td></tr><tr><td>S</td><td>公共管理、社会保障和社会组织</td></tr><tr><td>T</td><td>国际组织</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_监管报送信息类型</td><td>1</td><td>运营机构采取自律管理措施有关信息</td></tr><tr><td>2</td><td>运营机构制定或修订完成的有关业务规则和自律管理规则</td></tr><tr><td>3</td><td>发生影响或者可能影响区域性股权市场安全稳定运行、损害投资者合法权益的重大事件</td></tr><tr><td>4</td><td>证监会规定的其他信息和资料</td></tr><tr><td rowspan="4">枚举_违法违规</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>行政监管措施</td></tr><tr><td>2</td><td>行政处罚</td></tr><tr><td>3</td><td>市场禁入</td></tr><tr><td rowspan="3">枚举_自律管理</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>自律管理措施</td></tr><tr><td>2</td><td>纪律处分措施</td></tr><tr><td rowspan="6">枚举_所有制性质</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>中央国有控股</td></tr><tr><td>2</td><td>地方国有控股</td></tr><tr><td>3</td><td>外资</td></tr><tr><td>4</td><td>民营</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_公司或机构的设立方式</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>子公司</td></tr><tr><td>2</td><td>分支机构</td></tr><tr><td>3</td><td>联营公司</td></tr><tr><td>4</td><td>参股公司</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_财报格式类型</td><td>0</td><td>空值</td></tr><tr><td>10</td><td>合并财务报表(2019版)</td></tr><tr><td>11</td><td>合并资产负债表(2019版)</td></tr><tr><td>12</td><td>合并利润表(2019版)</td></tr><tr><td>13</td><td>合并现金流量表(2019版)</td></tr><tr><td>20</td><td>企业会计准则第33号——合并财务报表(2014)</td></tr><tr><td rowspan="5">枚举_财报格式类型</td><td>30</td><td>运营机构财务概况表</td></tr><tr><td>31</td><td>运营机构财务-利润简况</td></tr><tr><td>32</td><td>运营机构财务-现金流简况</td></tr><tr><td>33</td><td>运营机构财务-资产负债简况</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_业务规则文件类型</td><td>0</td><td>空值</td></tr><tr><td>10</td><td>挂牌类</td></tr><tr><td>30</td><td>登记托管类</td></tr><tr><td>40</td><td>信息披露类</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_投资者类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>专业投资者</td></tr><tr><td>2</td><td>普通投资者</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_普通投资者风险承受能力类别</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>C1</td></tr><tr><td>2</td><td>C2</td></tr><tr><td>3</td><td>C3</td></tr><tr><td>4</td><td>C4</td></tr><tr><td>5</td><td>C5</td></tr><tr><td rowspan="7">枚举_收入来源</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>工资、劳务报酬</td></tr><tr><td>2</td><td>生产经营所得</td></tr><tr><td>3</td><td>利息、股息、转让等金融性资产收入</td></tr><tr><td>4</td><td>出租、出售房地产等非金融性资产收入</td></tr><tr><td>5</td><td>无固定收入</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_可支配年收入情况</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>50万元以下</td></tr><tr><td>2</td><td>50万元-100万元</td></tr><tr><td>3</td><td>100万元-500万元</td></tr><tr><td>4</td><td>500万元-1000万元</td></tr><tr><td>5</td><td>1000万元以上</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_资产情况</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>不超过50万元人民币</td></tr><tr><td>2</td><td>50万-300万元人民币</td></tr><tr><td>3</td><td>300万-1000万元人民币</td></tr><tr><td rowspan="2">枚举_资产情况</td><td>4</td><td>1000万元人民币以上</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_债务情况</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>没有</td></tr><tr><td>2</td><td>长期定额债务</td></tr><tr><td>10</td><td>短期信用债务</td></tr><tr><td>12</td><td>相关借款</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_投资知识情况</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>有限:基本没有金融产品方面的知识</td></tr><tr><td>2</td><td>一般:对金融产品及相关风险具有基本的知识和理解</td></tr><tr><td>3</td><td>丰富:对金融产品及相关风险具有丰富的知识和理解</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_投资经验</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>除银行储蓄外,基本没有其他投资经验</td></tr><tr><td>2</td><td>购买过债券、保险等理财产品</td></tr><tr><td>3</td><td>参与过股票、基金等产品交易</td></tr><tr><td>4</td><td>参与过权证、期货、期权等产品的交易</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_投资期限</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>没有经验</td></tr><tr><td>2</td><td>少于2年</td></tr><tr><td>3</td><td>2-5年</td></tr><tr><td>4</td><td>5-10年</td></tr><tr><td>5</td><td>10年以上</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_投资品种</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>债券、货币市场基金、债券基金等固定收益类投资品种</td></tr><tr><td>2</td><td>股票、混合型基金、偏股型基金、股票型基金等权益类投资品种</td></tr><tr><td>3</td><td>期货、期权及其他金融衍生品</td></tr><tr><td>4</td><td>其他产品或服务</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="5">枚举_期望收益</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>尽可能保证本金安全,不在乎收益率比较低</td></tr><tr><td>2</td><td>产生一定的收益</td></tr><tr><td>3</td><td>产生较多的收益</td></tr><tr><td>4</td><td>实现资产大幅增长</td></tr><tr><td rowspan="7">枚举_期望收益</td><td>5</td><td>扩充规模</td></tr><tr><td>6</td><td>控制相关企业</td></tr><tr><td>7</td><td>维持现有规模效益</td></tr><tr><td>8</td><td>提高质量,降低成本</td></tr><tr><td>9</td><td>应对经营风险</td></tr><tr><td>10</td><td>承担社会义务</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_风险偏好</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>避免风险,不希望本金损失,希望获得稳定回报</td></tr><tr><td>2</td><td>保守投资,不希望本金损失,愿意承担一定幅度的收益波动</td></tr><tr><td>3</td><td>寻求资金的较高收益和成长性,愿意为此承担有限本金损失</td></tr><tr><td>4</td><td>希望赚取高回报,愿意为此承担较大本金损失</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_可承受的损失</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>10%以内</td></tr><tr><td>2</td><td>10%-30%</td></tr><tr><td>3</td><td>30%-50%</td></tr><tr><td>4</td><td>超过50%</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="12">枚举_历史沿革事件类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>企业改制</td></tr><tr><td>2</td><td>工商变更</td></tr><tr><td>3</td><td>重大股权变动</td></tr><tr><td>4</td><td>重大重组</td></tr><tr><td>5</td><td>重大融资</td></tr><tr><td>6</td><td>重大交易</td></tr><tr><td>7</td><td>权益分派</td></tr><tr><td>8</td><td>权益冻结</td></tr><tr><td>9</td><td>股权回购</td></tr><tr><td>10</td><td>上市计划关联事件</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_历史沿革事件子类</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>有限公司改股份公司</td></tr><tr><td>2</td><td>股份公司改有限公司</td></tr><tr><td>3</td><td>债务重组</td></tr><tr><td>4</td><td>并购重组</td></tr><tr><td>5</td><td>分红</td></tr><tr><td>6</td><td>派股</td></tr><tr><td rowspan="11">枚举_历史沿革事件子类</td><td>7</td><td>质押</td></tr><tr><td>8</td><td>冻结</td></tr><tr><td>9</td><td>新三板挂牌</td></tr><tr><td>10</td><td>交易所上市</td></tr><tr><td>11</td><td>已过会未上市</td></tr><tr><td>12</td><td>已申报 IPO</td></tr><tr><td>13</td><td>在辅导期</td></tr><tr><td>14</td><td>地方上市后备企业</td></tr><tr><td>15</td><td>新三板挂牌后已摘牌</td></tr><tr><td>16</td><td>上市后已退市</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="13">枚举_资金用途子类</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>项目投资</td></tr><tr><td>2</td><td>补充流动资金</td></tr><tr><td>3</td><td>补充资本金</td></tr><tr><td>4</td><td>财务性投资</td></tr><tr><td>5</td><td>偿还银行贷款</td></tr><tr><td>6</td><td>对外发放贷款或借与他人</td></tr><tr><td>7</td><td>房地产开发投资</td></tr><tr><td>8</td><td>公司经营性活动</td></tr><tr><td>9</td><td>基础设施建设</td></tr><tr><td>10</td><td>研发资金</td></tr><tr><td>11</td><td>资金周转</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_增信方式</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>保证</td></tr><tr><td>2</td><td>质押</td></tr><tr><td>3</td><td>抵押</td></tr><tr><td>4</td><td>承诺函</td></tr><tr><td>5</td><td>担保</td></tr><tr><td>6</td><td>到期回购</td></tr><tr><td>7</td><td>信用</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="6">枚举_增信方性质</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>地方国有企业</td></tr><tr><td>2</td><td>非公益性事业单位</td></tr><tr><td>3</td><td>国有企业(发行主体信用评级 AA)</td></tr><tr><td>4</td><td>金融机构</td></tr><tr><td>5</td><td>其他一般企业法人</td></tr><tr><td rowspan="10">枚举_增信方性质</td><td>6</td><td>其他一般企业法人及其他有清偿能力的组织或自然人</td></tr><tr><td>7</td><td>其他有清偿能力的组织或自然人</td></tr><tr><td>8</td><td>商业性担保机构</td></tr><tr><td>9</td><td>上市公司</td></tr><tr><td>10</td><td>政策性担保机构</td></tr><tr><td>11</td><td>政府融资平台</td></tr><tr><td>12</td><td>母公司</td></tr><tr><td>13</td><td>全体股东</td></tr><tr><td>14</td><td>自然人</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="28">枚举_非公开发行方类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>一般经营性企业</td></tr><tr><td>2</td><td>政府融资平台</td></tr><tr><td>3</td><td>商业银行</td></tr><tr><td>4</td><td>资产管理子公司</td></tr><tr><td>5</td><td>信托公司</td></tr><tr><td>6</td><td>证券公司</td></tr><tr><td>7</td><td>期货公司</td></tr><tr><td>8</td><td>风险管理子公司</td></tr><tr><td>9</td><td>保险公司</td></tr><tr><td>10</td><td>基金公司</td></tr><tr><td>11</td><td>资产管理公司</td></tr><tr><td>12</td><td>基金、保险代销公司</td></tr><tr><td>15</td><td>投资公司(未取得许可)</td></tr><tr><td>16</td><td>商业保理公司</td></tr><tr><td>17</td><td>小额贷款公司</td></tr><tr><td>18</td><td>融资租赁公司</td></tr><tr><td>19</td><td>融资担保公司</td></tr><tr><td>20</td><td>典当行</td></tr><tr><td>21</td><td>区域性股权市场</td></tr><tr><td>22</td><td>上市公司</td></tr><tr><td>23</td><td>外资或合资企业</td></tr><tr><td>24</td><td>合伙企业</td></tr><tr><td>25</td><td>个体工商户</td></tr><tr><td>26</td><td>自然人</td></tr><tr><td>27</td><td>事业单位</td></tr><tr><td>28</td><td>社会团体</td></tr><tr><td>29</td><td>工会组织</td></tr><tr><td rowspan="4">枚举_非公开发行方类型</td><td>30</td><td>公益、慈善组织</td></tr><tr><td>32</td><td>基金公司专户子公司</td></tr><tr><td>33</td><td>基金公司私募股权子公司</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_资金来源</td><td>0</td><td>空值</td></tr><tr><td>2</td><td>基金产品</td></tr><tr><td>3</td><td>理财产品</td></tr><tr><td>4</td><td>信托计划</td></tr><tr><td>5</td><td>资管计划</td></tr><tr><td>6</td><td>自有资金</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="27">枚举_企业所属行业大类</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>农业</td></tr><tr><td>2</td><td>林业</td></tr><tr><td>3</td><td>畜牧业</td></tr><tr><td>4</td><td>渔业</td></tr><tr><td>5</td><td>农、林、牧、渔专业及辅助性活动</td></tr><tr><td>6</td><td>煤炭开采和洗选业</td></tr><tr><td>7</td><td>石油和天然气开采业</td></tr><tr><td>8</td><td>黑色金属矿采选业</td></tr><tr><td>9</td><td>有色金属矿采选业</td></tr><tr><td>10</td><td>非金属矿采选业</td></tr><tr><td>11</td><td>开采专业及辅助性活动</td></tr><tr><td>12</td><td>其他采矿业</td></tr><tr><td>13</td><td>农副食品加工业</td></tr><tr><td>14</td><td>食品制造业</td></tr><tr><td>15</td><td>酒、饮料和精制茶制造业</td></tr><tr><td>16</td><td>烟草制品业</td></tr><tr><td>17</td><td>纺织业</td></tr><tr><td>18</td><td>纺织服装、服饰业</td></tr><tr><td>19</td><td>皮革、毛皮、羽毛及其制品和制鞋业</td></tr><tr><td>20</td><td>木材加工和木、竹、藤、棕、草制品业</td></tr><tr><td>21</td><td>家具制造业</td></tr><tr><td>22</td><td>造纸和纸制品业</td></tr><tr><td>23</td><td>印刷和记录媒介复制业</td></tr><tr><td>24</td><td>文教、工美、体育和娱乐用品制造业</td></tr><tr><td>25</td><td>石油、煤炭及其他燃料加工业</td></tr><tr><td>26</td><td>化学原料和化学制品制造业</td></tr><tr><td rowspan="38">枚举_企业所属行业大类</td><td>27</td><td>医药制造业</td></tr><tr><td>28</td><td>化学纤维制造业</td></tr><tr><td>29</td><td>橡胶和塑料制品业</td></tr><tr><td>30</td><td>非金属矿物制品业</td></tr><tr><td>31</td><td>黑色金属冶炼和压延加工业</td></tr><tr><td>32</td><td>有色金属冶炼和压延加工业</td></tr><tr><td>33</td><td>金属制品业</td></tr><tr><td>34</td><td>通用设备制造业</td></tr><tr><td>35</td><td>专用设备制造业</td></tr><tr><td>36</td><td>汽车制造业</td></tr><tr><td>37</td><td>铁路、船舶、航空航天和其他运输设备制造业</td></tr><tr><td>38</td><td>电气机械和器材制造业</td></tr><tr><td>39</td><td>计算机、通信和其他电子设备制造业</td></tr><tr><td>40</td><td>仪器仪表制造业</td></tr><tr><td>41</td><td>其他制造业</td></tr><tr><td>42</td><td>废弃资源综合利用业</td></tr><tr><td>43</td><td>金属制品、机械和设备修理业</td></tr><tr><td>44</td><td>电力、热力生产和供应业</td></tr><tr><td>45</td><td>燃气生产和供应业</td></tr><tr><td>46</td><td>水的生产和供应业</td></tr><tr><td>47</td><td>房屋建筑业</td></tr><tr><td>48</td><td>土木工程建筑业</td></tr><tr><td>49</td><td>建筑安装业</td></tr><tr><td>50</td><td>建筑装饰、装修和其他建筑业</td></tr><tr><td>51</td><td>批发业</td></tr><tr><td>52</td><td>零售业</td></tr><tr><td>53</td><td>铁路运输业</td></tr><tr><td>54</td><td>道路运输业</td></tr><tr><td>55</td><td>水上运输业</td></tr><tr><td>56</td><td>航空运输业</td></tr><tr><td>57</td><td>管道运输业</td></tr><tr><td>58</td><td>多式联运和运输代理业</td></tr><tr><td>59</td><td>装卸搬运和仓储业</td></tr><tr><td>60</td><td>邮政业</td></tr><tr><td>61</td><td>住宿业</td></tr><tr><td>62</td><td>餐饮业</td></tr><tr><td>63</td><td>电信、广播电视和卫星传输服务</td></tr><tr><td>64</td><td>互联网和相关服务</td></tr><tr><td rowspan="27">枚举_企业所属行业大类</td><td>65</td><td>软件和信息技术服务业</td></tr><tr><td>66</td><td>货币金融服务</td></tr><tr><td>67</td><td>资本市场服务</td></tr><tr><td>68</td><td>保险业</td></tr><tr><td>69</td><td>其他金融业</td></tr><tr><td>70</td><td>房地产业</td></tr><tr><td>71</td><td>租赁业</td></tr><tr><td>72</td><td>商务服务业</td></tr><tr><td>73</td><td>研究和试验发展</td></tr><tr><td>74</td><td>专业技术服务业</td></tr><tr><td>75</td><td>科技推广和应用服务业</td></tr><tr><td>76</td><td>水利管理业</td></tr><tr><td>77</td><td>生态保护和环境治理业</td></tr><tr><td>78</td><td>公共设施管理业</td></tr><tr><td>79</td><td>土地管理业</td></tr><tr><td>80</td><td>居民服务业</td></tr><tr><td>81</td><td>机动车、电子产品和日用产品修理业</td></tr><tr><td>82</td><td>其他服务业</td></tr><tr><td>83</td><td>教育</td></tr><tr><td>84</td><td>卫生</td></tr><tr><td>85</td><td>社会工作</td></tr><tr><td>86</td><td>新闻和出版业</td></tr><tr><td>87</td><td>广播、电视、电影和录音制作业</td></tr><tr><td>88</td><td>文化艺术业</td></tr><tr><td>89</td><td>体育</td></tr><tr><td>90</td><td>娱乐业</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="12">枚举_企业所属行业中类</td><td>0</td><td>空值</td></tr><tr><td>11</td><td>谷物种植</td></tr><tr><td>12</td><td>豆类、油料和薯类种植</td></tr><tr><td>13</td><td>棉、麻、糖、烟草种植</td></tr><tr><td>14</td><td>蔬菜、食用菌及园艺作物种植</td></tr><tr><td>15</td><td>水果种植</td></tr><tr><td>16</td><td>坚果、含油果、香料和饮料作物种植</td></tr><tr><td>17</td><td>中药材种植</td></tr><tr><td>18</td><td>草种植及割草</td></tr><tr><td>19</td><td>其他农业</td></tr><tr><td>21</td><td>林木育种和育苗</td></tr><tr><td>22</td><td>造林和更新</td></tr><tr><td rowspan="38">枚举_企业所属行业中类</td><td>23</td><td>森林经营、管护和改培</td></tr><tr><td>24</td><td>木材和竹材采运</td></tr><tr><td>25</td><td>林产品采集</td></tr><tr><td>31</td><td>牲畜饲养</td></tr><tr><td>32</td><td>家禽饲养</td></tr><tr><td>33</td><td>狩猎和捕捉动物</td></tr><tr><td>39</td><td>其他畜牧业</td></tr><tr><td>41</td><td>水产养殖</td></tr><tr><td>42</td><td>水产捕捞</td></tr><tr><td>51</td><td>农业专业及辅助性活动</td></tr><tr><td>52</td><td>林业专业及辅助性活动</td></tr><tr><td>53</td><td>畜牧专业及辅助性活动</td></tr><tr><td>54</td><td>渔业专业及辅助性活动</td></tr><tr><td>61</td><td>烟煤和无烟煤开采洗选</td></tr><tr><td>62</td><td>褐煤开采洗选</td></tr><tr><td>69</td><td>其他煤炭采选</td></tr><tr><td>71</td><td>石油开采</td></tr><tr><td>72</td><td>天然气开采</td></tr><tr><td>81</td><td>铁矿采选</td></tr><tr><td>82</td><td>锰矿、铬矿采选</td></tr><tr><td>89</td><td>其他黑色金属矿采选</td></tr><tr><td>91</td><td>常用有色金属矿采选</td></tr><tr><td>92</td><td>贵金属矿采选</td></tr><tr><td>93</td><td>稀有稀土金属矿采选</td></tr><tr><td>101</td><td>土砂石开采</td></tr><tr><td>102</td><td>化学矿开采</td></tr><tr><td>103</td><td>采盐</td></tr><tr><td>109</td><td>石棉及其他非金属矿采选</td></tr><tr><td>111</td><td>煤炭开采和洗选专业及辅助性活动</td></tr><tr><td>112</td><td>石油和天然气开采专业及辅助性活动</td></tr><tr><td>119</td><td>其他开采专业及辅助性活动</td></tr><tr><td>120</td><td>其他采矿业</td></tr><tr><td>131</td><td>谷物磨制</td></tr><tr><td>132</td><td>饲料加工</td></tr><tr><td>133</td><td>植物油加工</td></tr><tr><td>134</td><td>制糖业</td></tr><tr><td>135</td><td>屠宰及肉类加工</td></tr><tr><td>136</td><td>水产品加工</td></tr><tr><td rowspan="39">枚举_企业所属行业中类</td><td>137</td><td>蔬菜、菌类、水果和坚果加工</td></tr><tr><td>139</td><td>其他农副食品加工</td></tr><tr><td>141</td><td>焙烤食品制造</td></tr><tr><td>142</td><td>糖果、巧克力及蜜饯制造</td></tr><tr><td>143</td><td>方便食品制造</td></tr><tr><td>144</td><td>乳制品制造</td></tr><tr><td>145</td><td>罐头食品制造</td></tr><tr><td>146</td><td>调味品、发酵制品制造</td></tr><tr><td>149</td><td>其他食品制造</td></tr><tr><td>151</td><td>酒的制造</td></tr><tr><td>152</td><td>饮料制造</td></tr><tr><td>153</td><td>精制茶加工</td></tr><tr><td>161</td><td>烟叶复烤</td></tr><tr><td>162</td><td>卷烟制造</td></tr><tr><td>169</td><td>其他烟草制品制造</td></tr><tr><td>171</td><td>棉纺织及印染精加工</td></tr><tr><td>172</td><td>毛纺织及染整精加工</td></tr><tr><td>173</td><td>麻纺织及染整精加工</td></tr><tr><td>174</td><td>丝绢纺织及印染精加工</td></tr><tr><td>175</td><td>化纤织造及印染精加工</td></tr><tr><td>176</td><td>针织或钩针编织物及其制品制造</td></tr><tr><td>177</td><td>家用纺织制成品制造</td></tr><tr><td>178</td><td>产业用纺织制成品制造</td></tr><tr><td>181</td><td>机织服装制造</td></tr><tr><td>182</td><td>针织或钩针编织服装制造</td></tr><tr><td>183</td><td>服饰制造</td></tr><tr><td>191</td><td>皮革鞣制加工</td></tr><tr><td>192</td><td>皮革制品制造</td></tr><tr><td>193</td><td>毛皮鞣制及制品加工</td></tr><tr><td>194</td><td>羽毛(绒)加工及制品制造</td></tr><tr><td>195</td><td>制鞋业</td></tr><tr><td>201</td><td>木材加工</td></tr><tr><td>202</td><td>人造板制造</td></tr><tr><td>203</td><td>木质制品制造</td></tr><tr><td>204</td><td>竹、藤、棕、草等制品制造</td></tr><tr><td>211</td><td>木质家具制造</td></tr><tr><td>212</td><td>竹、藤家具制造</td></tr><tr><td>213</td><td>金属家具制造</td></tr><tr><td>214</td><td>塑料家具制造</td></tr><tr><td rowspan="39">枚举_企业所属行业中类</td><td>219</td><td>其他家具制造</td></tr><tr><td>221</td><td>纸浆制造</td></tr><tr><td>222</td><td>造纸</td></tr><tr><td>223</td><td>纸制品制造</td></tr><tr><td>231</td><td>印刷</td></tr><tr><td>232</td><td>装订及印刷相关服务</td></tr><tr><td>233</td><td>记录媒介复制</td></tr><tr><td>241</td><td>文教办公用品制造</td></tr><tr><td>242</td><td>乐器制造</td></tr><tr><td>243</td><td>工艺美术及礼仪用品制造</td></tr><tr><td>244</td><td>体育用品制造</td></tr><tr><td>245</td><td>玩具制造</td></tr><tr><td>246</td><td>游艺器材及娱乐用品制造</td></tr><tr><td>251</td><td>精炼石油产品制造</td></tr><tr><td>252</td><td>煤炭加工</td></tr><tr><td>253</td><td>核燃料加工</td></tr><tr><td>254</td><td>生物质燃料加工</td></tr><tr><td>261</td><td>基础化学原料制造</td></tr><tr><td>262</td><td>肥料制造</td></tr><tr><td>263</td><td>农药制造</td></tr><tr><td>264</td><td>涂料、油墨、颜料及类似产品制造</td></tr><tr><td>265</td><td>合成材料制造</td></tr><tr><td>266</td><td>专用化学产品制造</td></tr><tr><td>267</td><td>炸药、火工及焰火产品制造</td></tr><tr><td>268</td><td>日用化学产品制造</td></tr><tr><td>271</td><td>化学药品原料药制造</td></tr><tr><td>272</td><td>化学药品制剂制造</td></tr><tr><td>273</td><td>中药饮片加工</td></tr><tr><td>274</td><td>中成药生产</td></tr><tr><td>275</td><td>兽用药品制造</td></tr><tr><td>276</td><td>生物药品制品制造</td></tr><tr><td>277</td><td>卫生材料及医药用品制造</td></tr><tr><td>278</td><td>药用辅料及包装材料制造</td></tr><tr><td>281</td><td>纤维素纤维原料及纤维制造</td></tr><tr><td>282</td><td>合成纤维制造</td></tr><tr><td>283</td><td>生物基材料制造</td></tr><tr><td>291</td><td>橡胶制品业</td></tr><tr><td>292</td><td>塑料制品业</td></tr><tr><td>301</td><td>水泥、石灰和石膏制造</td></tr><tr><td rowspan="37">枚举_企业所属行业中类</td><td>302</td><td>石膏、水泥制品及类似制品制造</td></tr><tr><td>303</td><td>砖瓦、石材等建筑材料制造</td></tr><tr><td>304</td><td>玻璃制造</td></tr><tr><td>305</td><td>玻璃制品制造</td></tr><tr><td>306</td><td>玻璃纤维和玻璃纤维增强塑料制品制造</td></tr><tr><td>307</td><td>陶瓷制品制造</td></tr><tr><td>308</td><td>耐火材料制品制造</td></tr><tr><td>309</td><td>石墨及其他非金属矿物制品制造</td></tr><tr><td>311</td><td>炼铁</td></tr><tr><td>312</td><td>炼钢</td></tr><tr><td>313</td><td>钢压延加工</td></tr><tr><td>314</td><td>铁合金冶炼</td></tr><tr><td>321</td><td>常用有色金属冶炼</td></tr><tr><td>322</td><td>贵金属冶炼</td></tr><tr><td>323</td><td>稀有稀土金属冶炼</td></tr><tr><td>324</td><td>有色金属合金制造</td></tr><tr><td>325</td><td>有色金属压延加工</td></tr><tr><td>331</td><td>结构性金属制品制造</td></tr><tr><td>332</td><td>金属工具制造</td></tr><tr><td>333</td><td>集装箱及金属包装容器制造</td></tr><tr><td>334</td><td>金属丝绳及其制品制造</td></tr><tr><td>335</td><td>建筑、安全用金属制品制造</td></tr><tr><td>336</td><td>金属表面处理及热处理加工</td></tr><tr><td>337</td><td>搪瓷制品制造</td></tr><tr><td>338</td><td>金属制日用品制造</td></tr><tr><td>339</td><td>铸造及其他金属制品制造</td></tr><tr><td>341</td><td>锅炉及原动设备制造</td></tr><tr><td>342</td><td>金属加工机械制造</td></tr><tr><td>343</td><td>物料搬运设备制造</td></tr><tr><td>344</td><td>泵、阀门、压缩机及类似机械制造</td></tr><tr><td>345</td><td>轴承、齿轮和传动部件制造</td></tr><tr><td>346</td><td>烘炉、风机、包装等设备制造</td></tr><tr><td>347</td><td>文化、办公用机械制造</td></tr><tr><td>348</td><td>通用零部件制造</td></tr><tr><td>349</td><td>其他通用设备制造业</td></tr><tr><td>351</td><td>采矿、冶金、建筑专用设备制造</td></tr><tr><td>352</td><td>化工、木材、非金属加工专用设备制造</td></tr><tr><td rowspan="35">枚举_企业所属行业中类</td><td>353</td><td>食品、饮料、烟草及饲料生产专用设备制造</td></tr><tr><td>354</td><td>印刷、制药、日化及日用品生产专用设备制造</td></tr><tr><td>355</td><td>纺织、服装和皮革加工专用设备制造</td></tr><tr><td>356</td><td>电子和电工机械专用设备制造</td></tr><tr><td>357</td><td>农、林、牧、渔专用机械制造</td></tr><tr><td>358</td><td>医疗仪器设备及器械制造</td></tr><tr><td>359</td><td>环保、邮政、社会公共服务及其他专用设备制造</td></tr><tr><td>361</td><td>汽车整车制造</td></tr><tr><td>362</td><td>汽车用发动机制造</td></tr><tr><td>363</td><td>改装汽车制造</td></tr><tr><td>364</td><td>低速汽车制造</td></tr><tr><td>365</td><td>电车制造</td></tr><tr><td>366</td><td>汽车车身、挂车制造</td></tr><tr><td>367</td><td>汽车零部件及配件制造</td></tr><tr><td>371</td><td>铁路运输设备制造</td></tr><tr><td>372</td><td>城市轨道交通设备制造</td></tr><tr><td>373</td><td>船舶及相关装置制造</td></tr><tr><td>374</td><td>航空、航天器及设备制造</td></tr><tr><td>375</td><td>摩托车制造</td></tr><tr><td>376</td><td>自行车和残疾人座车制造</td></tr><tr><td>377</td><td>助动车制造</td></tr><tr><td>378</td><td>非公路休闲车及零配件制造</td></tr><tr><td>379</td><td>潜水救捞及其他未列明运输设备制造</td></tr><tr><td>381</td><td>电机制造</td></tr><tr><td>382</td><td>输配电及控制设备制造</td></tr><tr><td>383</td><td>电线、电缆、光缆及电工器材制造</td></tr><tr><td>384</td><td>电池制造</td></tr><tr><td>385</td><td>家用电力器具制造</td></tr><tr><td>386</td><td>非电力家用器具制造</td></tr><tr><td>387</td><td>照明器具制造</td></tr><tr><td>389</td><td>其他电气机械及器材制造</td></tr><tr><td>391</td><td>计算机制造</td></tr><tr><td>392</td><td>通信设备制造</td></tr><tr><td>393</td><td>广播电视设备制造</td></tr><tr><td>394</td><td>雷达及配套设备制造</td></tr><tr><td rowspan="38">枚举_企业所属行业中类</td><td>395</td><td>非专业视听设备制造</td></tr><tr><td>396</td><td>智能消费设备制造</td></tr><tr><td>397</td><td>电子器件制造</td></tr><tr><td>398</td><td>电子元件及电子专用材料制造</td></tr><tr><td>399</td><td>其他电子设备制造</td></tr><tr><td>401</td><td>通用仪器仪表制造</td></tr><tr><td>402</td><td>专用仪器仪表制造</td></tr><tr><td>403</td><td>钟表与计时仪器制造</td></tr><tr><td>404</td><td>光学仪器制造</td></tr><tr><td>405</td><td>衡器制造</td></tr><tr><td>409</td><td>其他仪器仪表制造业</td></tr><tr><td>411</td><td>日用杂品制造</td></tr><tr><td>412</td><td>核辐射加工</td></tr><tr><td>419</td><td>其他未列明制造业</td></tr><tr><td>421</td><td>金属废料和碎屑加工处理</td></tr><tr><td>422</td><td>非金属废料和碎屑加工处理</td></tr><tr><td>431</td><td>金属制品修理</td></tr><tr><td>432</td><td>通用设备修理</td></tr><tr><td>433</td><td>专用设备修理</td></tr><tr><td>434</td><td>铁路、船舶、航空航天等运输设备修理</td></tr><tr><td>435</td><td>电气设备修理</td></tr><tr><td>436</td><td>仪器仪表修理</td></tr><tr><td>439</td><td>其他机械和设备修理业</td></tr><tr><td>441</td><td>电力生产</td></tr><tr><td>442</td><td>电力供应</td></tr><tr><td>443</td><td>热力生产和供应</td></tr><tr><td>451</td><td>燃气生产和供应业</td></tr><tr><td>452</td><td>生物质燃气生产和供应业</td></tr><tr><td>461</td><td>自来水生产和供应</td></tr><tr><td>462</td><td>污水处理及其再生利用</td></tr><tr><td>463</td><td>海水淡化处理</td></tr><tr><td>469</td><td>其他水的处理、利用与分配</td></tr><tr><td>471</td><td>住宅房屋建筑</td></tr><tr><td>472</td><td>体育场馆建筑</td></tr><tr><td>479</td><td>其他房屋建筑业</td></tr><tr><td>481</td><td>铁路、道路、隧道和桥梁工程建筑</td></tr><tr><td>482</td><td>水利和水运工程建筑</td></tr><tr><td>483</td><td>海洋工程建筑</td></tr><tr><td rowspan="38">枚举_企业所属行业中类</td><td>484</td><td>工矿工程建筑</td></tr><tr><td>485</td><td>架线和管道工程建筑</td></tr><tr><td>486</td><td>节能环保工程施工</td></tr><tr><td>487</td><td>电力工程施工</td></tr><tr><td>489</td><td>其他土木工程建筑</td></tr><tr><td>491</td><td>电气安装</td></tr><tr><td>492</td><td>管道和设备安装</td></tr><tr><td>499</td><td>其他建筑安装业</td></tr><tr><td>501</td><td>建筑装饰和装修业</td></tr><tr><td>502</td><td>建筑物拆除和场地准备活动</td></tr><tr><td>503</td><td>提供施工设备服务</td></tr><tr><td>509</td><td>其他未列明建筑业</td></tr><tr><td>511</td><td>农、林、牧、渔产品批发</td></tr><tr><td>512</td><td>食品、饮料及烟草制品批发</td></tr><tr><td>513</td><td>纺织、服装及家庭用品批发</td></tr><tr><td>514</td><td>文化、体育用品及器材批发</td></tr><tr><td>515</td><td>医药及医疗器材批发</td></tr><tr><td>516</td><td>矿产品、建材及化工产品批发</td></tr><tr><td>517</td><td>机械设备、五金产品及电子产品批发</td></tr><tr><td>518</td><td>贸易经纪与代理</td></tr><tr><td>519</td><td>其他批发业</td></tr><tr><td>521</td><td>综合零售</td></tr><tr><td>522</td><td>食品、饮料及烟草制品专门零售</td></tr><tr><td>523</td><td>纺织、服装及日用品专门零售</td></tr><tr><td>524</td><td>文化、体育用品及器材专门零售</td></tr><tr><td>525</td><td>医药及医疗器材专门零售</td></tr><tr><td>526</td><td>汽车、摩托车、零配件和燃料及其他动力销售</td></tr><tr><td>527</td><td>家用电器及电子产品专门零售</td></tr><tr><td>528</td><td>五金、家具及室内装饰材料专门零售</td></tr><tr><td>529</td><td>货摊、无店铺及其他零售业</td></tr><tr><td>531</td><td>铁路旅客运输</td></tr><tr><td>532</td><td>铁路货物运输</td></tr><tr><td>533</td><td>铁路运输辅助活动</td></tr><tr><td>541</td><td>城市公共交通运输</td></tr><tr><td>542</td><td>公路旅客运输</td></tr><tr><td>543</td><td>道路货物运输</td></tr><tr><td>544</td><td>道路运输辅助活动</td></tr><tr><td>551</td><td>水上旅客运输</td></tr><tr><td rowspan="39">枚举_企业所属行业中类</td><td>552</td><td>水上货物运输</td></tr><tr><td>553</td><td>水上运输辅助活动</td></tr><tr><td>561</td><td>航空客货运输</td></tr><tr><td>562</td><td>通用航空服务</td></tr><tr><td>563</td><td>航空运输辅助活动</td></tr><tr><td>571</td><td>海底管道运输</td></tr><tr><td>572</td><td>陆地管道运输</td></tr><tr><td>581</td><td>多式联运</td></tr><tr><td>582</td><td>运输代理业</td></tr><tr><td>591</td><td>装卸搬运</td></tr><tr><td>592</td><td>通用仓储</td></tr><tr><td>593</td><td>低温仓储</td></tr><tr><td>594</td><td>危险品仓储</td></tr><tr><td>595</td><td>谷物、棉花等农产品仓储</td></tr><tr><td>596</td><td>中药材仓储</td></tr><tr><td>599</td><td>其他仓储业</td></tr><tr><td>601</td><td>邮政基本服务</td></tr><tr><td>602</td><td>快递服务</td></tr><tr><td>609</td><td>其他寄递服务</td></tr><tr><td>611</td><td>旅游饭店</td></tr><tr><td>612</td><td>一般旅馆</td></tr><tr><td>613</td><td>民宿服务</td></tr><tr><td>614</td><td>露营地服务</td></tr><tr><td>619</td><td>其他住宿业</td></tr><tr><td>621</td><td>正餐服务</td></tr><tr><td>622</td><td>快餐服务</td></tr><tr><td>623</td><td>饮料及冷饮服务</td></tr><tr><td>624</td><td>餐饮配送及外卖送餐服务</td></tr><tr><td>629</td><td>其他餐饮业</td></tr><tr><td>631</td><td>电信</td></tr><tr><td>632</td><td>广播电视传输服务</td></tr><tr><td>633</td><td>卫星传输服务</td></tr><tr><td>641</td><td>互联网接入及相关服务</td></tr><tr><td>642</td><td>互联网信息服务</td></tr><tr><td>643</td><td>互联网平台</td></tr><tr><td>644</td><td>互联网安全服务</td></tr><tr><td>645</td><td>互联网数据服务</td></tr><tr><td>649</td><td>其他互联网服务</td></tr><tr><td>651</td><td>软件开发</td></tr><tr><td rowspan="39">枚举_企业所属行业中类</td><td>652</td><td>集成电路设计</td></tr><tr><td>653</td><td>信息系统集成和物联网技术服务</td></tr><tr><td>654</td><td>运行维护服务</td></tr><tr><td>655</td><td>信息处理和存储支持服务</td></tr><tr><td>656</td><td>信息技术咨询服务</td></tr><tr><td>657</td><td>数字内容服务</td></tr><tr><td>659</td><td>其他信息技术服务业</td></tr><tr><td>661</td><td>中央银行服务</td></tr><tr><td>662</td><td>货币银行服务</td></tr><tr><td>663</td><td>非货币银行服务</td></tr><tr><td>664</td><td>银行理财服务</td></tr><tr><td>665</td><td>银行监管服务</td></tr><tr><td>671</td><td>证券市场服务</td></tr><tr><td>672</td><td>公开募集证券投资基金</td></tr><tr><td>673</td><td>非公开募集证券投资基金</td></tr><tr><td>674</td><td>期货市场服务</td></tr><tr><td>675</td><td>证券期货监管服务</td></tr><tr><td>676</td><td>资本投资服务</td></tr><tr><td>679</td><td>其他资本市场服务</td></tr><tr><td>681</td><td>人身保险</td></tr><tr><td>682</td><td>财产保险</td></tr><tr><td>683</td><td>再保险</td></tr><tr><td>684</td><td>商业养老金</td></tr><tr><td>685</td><td>保险中介服务</td></tr><tr><td>686</td><td>保险资产管理</td></tr><tr><td>687</td><td>保险监管服务</td></tr><tr><td>689</td><td>其他保险活动</td></tr><tr><td>691</td><td>金融信托与管理服务</td></tr><tr><td>692</td><td>控股公司服务</td></tr><tr><td>693</td><td>非金融机构支付服务</td></tr><tr><td>694</td><td>金融信息服务</td></tr><tr><td>695</td><td>金融资产管理公司</td></tr><tr><td>699</td><td>其他未列明金融业</td></tr><tr><td>701</td><td>房地产开发经营</td></tr><tr><td>702</td><td>物业管理</td></tr><tr><td>703</td><td>房地产中介服务</td></tr><tr><td>704</td><td>房地产租赁经营</td></tr><tr><td>709</td><td>其他房地产业</td></tr><tr><td>711</td><td>机械设备经营租赁</td></tr><tr><td rowspan="37">枚举_企业所属行业中类</td><td>712</td><td>文体设备和用品出租</td></tr><tr><td>713</td><td>日用品出租</td></tr><tr><td>721</td><td>组织管理服务</td></tr><tr><td>722</td><td>综合管理服务</td></tr><tr><td>723</td><td>法律服务</td></tr><tr><td>724</td><td>咨询与调查</td></tr><tr><td>725</td><td>广告业</td></tr><tr><td>726</td><td>人力资源服务</td></tr><tr><td>727</td><td>安全保护服务安全服务</td></tr><tr><td>728</td><td>会议、展览及相关服务</td></tr><tr><td>729</td><td>其他商务服务业</td></tr><tr><td>731</td><td>自然科学研究和试验发展</td></tr><tr><td>732</td><td>工程和技术研究和试验发展</td></tr><tr><td>733</td><td>农业科学研究和试验发展</td></tr><tr><td>734</td><td>医学研究和试验发展</td></tr><tr><td>735</td><td>社会人文科学研究</td></tr><tr><td>741</td><td>气象服务</td></tr><tr><td>742</td><td>地震服务</td></tr><tr><td>743</td><td>海洋服务</td></tr><tr><td>744</td><td>测绘地理信息服务</td></tr><tr><td>745</td><td>质检技术服务</td></tr><tr><td>746</td><td>环境与生态监测检测服务</td></tr><tr><td>747</td><td>地质勘查</td></tr><tr><td>748</td><td>工程技术与设计服务</td></tr><tr><td>749</td><td>工业与专业设计及其他专业技术服务</td></tr><tr><td>751</td><td>技术推广服务</td></tr><tr><td>752</td><td>知识产权服务</td></tr><tr><td>753</td><td>科技中介服务</td></tr><tr><td>754</td><td>创业空间服务</td></tr><tr><td>759</td><td>其他科技推广服务业</td></tr><tr><td>761</td><td>防洪除涝设施管理</td></tr><tr><td>762</td><td>水资源管理</td></tr><tr><td>763</td><td>天然水收集与分配</td></tr><tr><td>764</td><td>水文服务</td></tr><tr><td>769</td><td>其他水利管理业</td></tr><tr><td>771</td><td>生态保护</td></tr><tr><td>772</td><td>环境治理业</td></tr><tr><td rowspan="39">枚举_企业所属行业中类</td><td>781</td><td>市政设施管理</td></tr><tr><td>782</td><td>环境卫生管理</td></tr><tr><td>783</td><td>城乡市容管理</td></tr><tr><td>784</td><td>绿化管理</td></tr><tr><td>785</td><td>城市公园管理</td></tr><tr><td>786</td><td>游览景区管理</td></tr><tr><td>791</td><td>土地整治服务</td></tr><tr><td>792</td><td>土地调查评估服务</td></tr><tr><td>793</td><td>土地登记服务</td></tr><tr><td>794</td><td>土地登记代理服务</td></tr><tr><td>799</td><td>其他土地管理服务</td></tr><tr><td>801</td><td>家庭服务</td></tr><tr><td>802</td><td>托儿所服务</td></tr><tr><td>803</td><td>洗染服务</td></tr><tr><td>804</td><td>理发及美容服务</td></tr><tr><td>805</td><td>洗浴和保健养生服务</td></tr><tr><td>806</td><td>摄影扩印服务</td></tr><tr><td>807</td><td>婚姻服务</td></tr><tr><td>808</td><td>殡葬服务</td></tr><tr><td>809</td><td>其他居民服务业</td></tr><tr><td>811</td><td>汽车、摩托车等修理与维护</td></tr><tr><td>812</td><td>计算机和办公设备维修</td></tr><tr><td>813</td><td>家用电器修理</td></tr><tr><td>819</td><td>其他日用产品修理业</td></tr><tr><td>821</td><td>清洁服务</td></tr><tr><td>822</td><td>宠物服务</td></tr><tr><td>829</td><td>其他未列明服务业</td></tr><tr><td>831</td><td>学前教育</td></tr><tr><td>832</td><td>初等教育</td></tr><tr><td>833</td><td>中等教育</td></tr><tr><td>834</td><td>高等教育</td></tr><tr><td>835</td><td>特殊教育</td></tr><tr><td>839</td><td>技能培训、教育辅助及其他教育</td></tr><tr><td>841</td><td>医院</td></tr><tr><td>842</td><td>基层医疗卫生服务</td></tr><tr><td>843</td><td>专业公共卫生服务</td></tr><tr><td>849</td><td>其他卫生活动</td></tr><tr><td>851</td><td>提供住宿社会工作</td></tr><tr><td>852</td><td>不提供住宿社会工作</td></tr><tr><td rowspan="38">枚举_企业所属行业中类</td><td>861</td><td>新闻业</td></tr><tr><td>862</td><td>出版业</td></tr><tr><td>871</td><td>广播</td></tr><tr><td>872</td><td>电视</td></tr><tr><td>873</td><td>影视节目制作</td></tr><tr><td>874</td><td>广播电视集成播控</td></tr><tr><td>875</td><td>电影和广播电视节目发行</td></tr><tr><td>876</td><td>电影放映</td></tr><tr><td>877</td><td>录音制作</td></tr><tr><td>881</td><td>文艺创作与表演</td></tr><tr><td>882</td><td>艺术表演场馆</td></tr><tr><td>883</td><td>图书馆与档案馆</td></tr><tr><td>884</td><td>文物及非物质文化遗产保护</td></tr><tr><td>885</td><td>博物馆</td></tr><tr><td>886</td><td>烈士陵园、纪念馆</td></tr><tr><td>887</td><td>群众文体活动</td></tr><tr><td>889</td><td>其他文化艺术业</td></tr><tr><td>891</td><td>体育组织</td></tr><tr><td>892</td><td>体育场地设施管理</td></tr><tr><td>893</td><td>健身休闲活动</td></tr><tr><td>899</td><td>其他体育</td></tr><tr><td>901</td><td>室内娱乐活动</td></tr><tr><td>902</td><td>游乐园</td></tr><tr><td>903</td><td>休闲观光活动</td></tr><tr><td>904</td><td>彩票活动</td></tr><tr><td>905</td><td>文化体育娱乐活动与经纪代理服务文化活动服务</td></tr><tr><td>909</td><td>其他娱乐业</td></tr><tr><td>910</td><td>中国共产党机关</td></tr><tr><td>921</td><td>国家权力机构</td></tr><tr><td>922</td><td>国家行政机构</td></tr><tr><td>923</td><td>人民法院和人民检察院</td></tr><tr><td>929</td><td>其他国家机构</td></tr><tr><td>931</td><td>人民政协</td></tr><tr><td>932</td><td>民主党派</td></tr><tr><td>941</td><td>基本保险</td></tr><tr><td>942</td><td>补充保险</td></tr><tr><td>949</td><td>其他社会保障</td></tr><tr><td>951</td><td>群众团体</td></tr><tr><td rowspan="7">枚举_企业所属行业中类</td><td>952</td><td>社会团体</td></tr><tr><td>953</td><td>基金会</td></tr><tr><td>954</td><td>宗教组织</td></tr><tr><td>961</td><td>社区居民自治组织</td></tr><tr><td>962</td><td>村民自治组织</td></tr><tr><td>970</td><td>国际组织</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="9">枚举_股权性质标签</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>发起人股</td></tr><tr><td>2</td><td>定增股</td></tr><tr><td>3</td><td>内部职工股</td></tr><tr><td>4</td><td>高管股</td></tr><tr><td>5</td><td>认缴未出资</td></tr><tr><td>6</td><td>承诺人股</td></tr><tr><td>7</td><td>股权激励股</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_代持状态</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>代持</td></tr><tr><td>2</td><td>未代持</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="7">枚举_金融行业及相关工作经历年限</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>没有经验</td></tr><tr><td>2</td><td>少于2年</td></tr><tr><td>3</td><td>2-5年</td></tr><tr><td>4</td><td>5-10年</td></tr><tr><td>5</td><td>10年以上</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="4">枚举_汇率类型</td><td>0</td><td>空值</td></tr><tr><td>1</td><td>固定汇率</td></tr><tr><td>2</td><td>浮动汇率</td></tr><tr><td>255</td><td>其他</td></tr><tr><td rowspan="2">枚举_服务状态</td><td>1</td><td>服务中</td></tr><tr><td>2</td><td>停止服务</td></tr></table>

## A. 11 预定义类型信息

预定义类型信息包括文件对象类型、枚举类型、文件对象数组、枚举值集合，应满足表A.100的要求。

表 A. 100 预定义类型信息

<table><tr><td>预定义类型</td><td>类型中文名称</td><td>字段中文描述</td><td>字段英文名称</td><td>是否必填</td><td>说明</td></tr><tr><td rowspan="7">FILE_OBJECT</td><td rowspan="7">文件对象类型</td><td>文件编号</td><td>file_number</td><td>必填</td><td>—</td></tr><tr><td>文件名称</td><td>file_name</td><td>必填</td><td>含格式扩展名</td></tr><tr><td>文件地址</td><td>uri</td><td>必填</td><td>文件地址为ossuri</td></tr><tr><td>文件摘要算法</td><td>algorithm_type</td><td>必填</td><td>类型:枚举值number,enum value:&quot;1-MD5,2-SHA128,3-SHA256,4-SM3&quot;</td></tr><tr><td>文件hash</td><td>hash</td><td>必填</td><td>MD5 Hash</td></tr><tr><td>文件用途概述</td><td>summary</td><td>不必填</td><td>200字以内</td></tr><tr><td>文件有效期</td><td>term_of_validity</td><td>不必填</td><td>yyyy-MM-dd</td></tr><tr><td rowspan="4">ENUM</td><td rowspan="4">枚举类型</td><td>枚举值</td><td>enum_value</td><td>必填</td><td>枚举的合法值,数值型或字符型</td></tr><tr><td>枚举值属性</td><td>enum_attribute</td><td>必填</td><td>枚举值的属性,字符型</td></tr><tr><td>枚举值深度(级别)</td><td>enum_depth</td><td>不必填</td><td>枚举值序列的层(或有),例:行业</td></tr><tr><td>枚举值排序号(同级别)</td><td>enum_sequence</td><td>不必填</td><td>同层级枚举值属性的顺序(或有),例:行业</td></tr><tr><td>FILE_OBJECT_ARRAY</td><td>文件对象数组</td><td>—</td><td>—</td><td>—</td><td>由文件对象型FILE_OBJECT数据构成的集合</td></tr><tr><td>ENUM_SET</td><td>枚举值集合</td><td>—</td><td>—</td><td>—</td><td>多个枚举数据</td></tr></table>

## 参考文献

[1] JR/T 0193 区块链技术金融应用评估规则  
[2] 中国证券监督管理委员会令[2016]130号-《证券期货投资者适当性管理办法》  
[3] 中国证券监督管理委员会令[2014]105号-《私募投资基金监督管理暂行办法》