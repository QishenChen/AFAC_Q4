#!/usr/bin/env python3
"""
Build a Chinese financial keyword synonym dictionary.
Sends 300+ distinct canonical terms to LLM to generate synonyms.
Output: config/financial_synonyms.json as {term: group_id, ...}
Each original term + its LLM-generated synonyms share the same group_id.
"""

import json
import os
import sys
import time
import requests

# ── 400+ DISTINCT canonical Chinese financial keyword concepts ──
# Organized by the 5 question domains
CANONICAL_TERMS = [

# =====================================================================
# 1. 保险 (Insurance) — 保险责任、身故保险金、退保金额、领取规则、条款比较
# =====================================================================
    "保险责任", "身故保险金", "退保金额", "领取规则",
    "保险条款", "免责条款", "等待期", "犹豫期", "宽限期",
    "复效", "保险费", "保险金额", "保险期间", "缴费期间",
    "投保年龄", "保险利益", "投保人", "被保险人", "受益人",
    "保险人", "承保", "核保", "保全", "理赔", "给付",
    "现金价值", "保单贷款", "保单质押", "保单红利",
    "分红保险", "万能保险", "投资连结保险", "变额年金",
    "健康保险", "医疗保险", "住院津贴", "门诊医疗",
    "重大疾病保险", "轻症保险", "特定疾病", "多次赔付",
    "人寿保险", "定期寿险", "终身寿险", "两全保险",
    "年金保险", "养老年金", "即期年金", "延期年金",
    "意外伤害保险", "意外身故", "意外伤残", "意外医疗",
    "团体保险", "个人保险", "短期保险", "长期保险",
    "保费豁免", "保证续保", "不可抗辩条款", "如实告知",
    "保险事故", "近因原则", "代位求偿", "重复保险",
    "保险凭证", "暂保单", "批单", "批注",
    "保费收入", "赔付支出", "退保率", "保单继续率",
    "新业务价值", "内含价值", "偿付能力", "责任准备金",

# =====================================================================
# 2. 法规/监管 (Regulatory) — 法规适用、合规义务、时限要求、监管处罚、条文优先级
# =====================================================================
    "适用法规", "合规义务", "时限要求", "监管处罚",
    "条文优先级", "法律依据", "授权条款", "过渡条款",
    "废止条款", "施行日期", "备案", "核准", "审批",
    "行政许可", "登记", "备案制", "注册制", "核准制",
    "监管机构", "自律组织", "行业协会", "主管机关",
    "证监会", "银保监会", "央行", "国家金融监管局",
    "行政处罚", "行政罚款", "责令改正", "市场禁入",
    "公开谴责", "通报批评", "监管谈话", "出具警示函",
    "违规行为", "违法行为", "内幕交易", "操纵市场",
    "信息披露违规", "财务造假", "虚假记载", "重大遗漏",
    "误导性陈述", "不正当披露", "延迟披露",
    "强制退市", "暂停上市", "恢复上市", "终止上市",
    "重大违法", "强制措施", "调查", "立案调查",
    "行政复议", "行政诉讼", "国家赔偿",
    "金融监管", "宏观审慎", "微观审慎", "系统性风险",
    "资本充足率", "拨备覆盖率", "流动性覆盖率", "净稳定资金比率",
    "反洗钱", "反恐融资", "客户尽职调查", "可疑交易报告",

# =====================================================================
# 3. 债券 (Bonds) — 债券条款、发行信息、评级信息、权利义务关系
# =====================================================================
    "债券条款", "发行信息", "评级信息", "权利义务",
    "发行金额", "发行规模", "发行方式", "发行对象",
    "票面利率", "发行利率", "计息方式", "付息频率",
    "发行期限", "到期日", "起息日", "兑付日",
    "主体评级", "债项评级", "评级展望", "信用等级",
    "受托管理人", "主承销商", "簿记管理人", "承销团",
    "募集说明书", "发行公告", "法律意见书", "评级报告",
    "可转换债券", "可交换债券", "分离交易可转债",
    "转股价格", "转股期", "赎回条款", "回售条款",
    "向下修正条款", "强制转股", "到期赎回", "有条件赎回",
    "增信措施", "保证担保", "抵押担保", "质押担保",
    "信用增进", "差额补足", "流动性支持",
    "违约", "交叉违约", "加速到期", "违约事件",
    "违约处置", "债券持有人会议", "受托管理协议",
    "本息兑付", "到期一次性还本", "分期还本", "提前偿还",
    "本金", "利息", "票面金额", "债券面值",
    "公司债", "企业债", "中期票据", "短期融资券",
    "超短期融资券", "定向工具", "资产支持证券",
    "债券持有人", "投资者适当性", "合格投资者",
    "回购", "质押式回购", "买断式回购", "债券借贷",

# =====================================================================
# 4. 年报/财务 (Financial Reports) — 年报指标、经营表现、现金流、研发投入、分红政策
# =====================================================================
    "年报指标", "经营表现", "现金流", "研发投入", "分红政策",
    "总资产", "净资产", "负债总额", "流动资产", "非流动资产",
    "流动负债", "非流动负债", "所有者权益", "实收资本",
    "资本公积", "盈余公积", "未分配利润", "少数股东权益",
    "货币资金", "应收账款", "应收票据", "预付款项", "存货",
    "固定资产", "在建工程", "无形资产", "商誉",
    "短期借款", "长期借款", "应付债券", "应付账款",
    "合同负债", "租赁负债", "预计负债", "递延所得税负债",
    "营业收入", "营业成本", "销售费用", "管理费用",
    "研发费用", "财务费用", "投资收益", "公允价值变动收益",
    "信用减值损失", "资产减值损失", "营业利润", "利润总额",
    "所得税费用", "净利润", "归属于母公司股东的净利润",
    "扣除非经常性损益后的净利润", "基本每股收益", "稀释每股收益",
    "经营活动产生的现金流量净额", "投资活动产生的现金流量净额",
    "筹资活动产生的现金流量净额", "现金及现金等价物净增加额",
    "自由现金流", "资本支出", "折旧摊销",
    "资产负债率", "流动比率", "速动比率", "毛利率", "净利率",
    "净资产收益率", "总资产收益率", "每股净资产",
    "市盈率", "市净率", "营业收入增长率", "净利润增长率",
    "总资产周转率", "应收账款周转率", "存货周转率",
    "利息保障倍数", "权益乘数", "债务资本比率",
    "研发投入占营业收入比例", "专利数量", "研发人员占比",
    "现金分红", "股票回购", "分红比例", "股利支付率",
    "股权激励", "员工持股计划", "股份支付",
    "限售股", "流通股", "总股本", "控股股东", "实际控制人",
    "独立董事", "董事会", "监事会", "股东大会",
    "重大资产重组", "关联交易", "信息披露",
    "停牌", "退市", "借壳上市", "定向增发", "配股",
    "交易性金融资产", "其他应收款", "一年内到期的非流动资产",
    "长期股权投资", "投资性房地产", "递延所得税资产",
    "应付票据", "应付职工薪酬", "应交税费", "其他应付款",
    "一年内到期的非流动负债", "长期应付款", "其他非流动负债",
    "预收款项", "税金及附加", "利息收入", "利息支出",
    "营业外收入", "营业外支出", "其他综合收益", "综合收益总额",
    "销售商品提供劳务收到的现金", "购买商品接受劳务支付的现金",
    "支付给职工以及为职工支付的现金",
    "购建固定资产无形资产和其他长期资产支付的现金",
    "吸收投资收到的现金", "分配股利利润或偿付利息支付的现金",

# =====================================================================
# 5. 行业/研究 (Research) — 行业趋势、公司比较、指标解读、研究结论核验
# =====================================================================
    "行业趋势", "公司比较", "指标解读", "研究结论",
    "市场规模", "市场占有率", "行业集中度", "竞争格局",
    "行业景气度", "行业周期", "朝阳行业", "夕阳行业",
    "政策红利", "政策风险", "监管趋严", "简政放权",
    "技术迭代", "国产替代", "自主可控", "卡脖子",
    "产业链", "供应链", "价值链", "上下游",
    "成本优势", "规模效应", "协同效应", "范围经济",
    "对标分析", "横向比较", "纵向比较", "同行业对比",
    "估值方法", "市盈率估值", "市净率估值", "现金流折现",
    "企业价值", "股权价值", "市值", "市盈率相对盈利增长比",
    "财务分析", "杜邦分析", "因素分析", "趋势分析",
    "收入驱动", "利润驱动", "费用控制", "成本控制",
    "盈利能力", "偿债能力", "营运能力", "成长能力",
    "核心竞争力", "护城河", "进入壁垒", "转换成本",
    "商业模式", "盈利模式", "收费模式", "订阅模式",
    "业绩预告", "业绩快报", "盈利预测", "一致预期",
    "卖方报告", "买方报告", "独立研究", "第三方评估",
    "数据来源", "数据口径", "会计处理", "指标定义",
    "可比公司", "标杆企业", "行业龙头", "新进入者",
    "行业政策", "产业规划", "五年规划", "专项政策",
    "宏观经济", "GDP增长率", "通货膨胀", "利率水平",
    "汇率变动", "货币政策", "财政政策", "产业政策",

# =====================================================================
# 6. 合同/VC/法务 (Contracts / Legal) — 保留原版合同与交易术语
# =====================================================================
    "签署", "履行", "违约金", "协议", "附件", "生效日",
    "期限", "标的", "费用", "报酬", "损失", "连带责任",
    "无追索权", "诚实信用", "重大过失", "重大不利变更",
    "稀释", "反稀释", "表决权", "否决权", "优先购买权",
    "反摊薄条款", "最惠国条款", "对赌协议", "回购权",
    "优先清算权", "反稀释保护", "领售权", "跟售权",
    "退出机制", "IPO", "并购", "尽职调查", "估值",
    "融资租赁", "经营租赁", "售后回租", "租赁负债",
    "不可抗力", "仲裁", "诉讼", "管辖",
    "合同生效", "合同终止", "保密义务", "知识产权",
    "法定代表人", "授权代表", "经办人", "联系人",
    "注册资本", "注册地址", "经营范围", "营业执照",
    "统一社会信用代码", "税务登记", "组织机构代码",
    "会计政策", "会计估计变更", "前期差错更正",
    "资产负债表日后事项", "或有事项", "承诺事项",
    "非经常性损益", "分部报告", "持续经营", "合并报表",
    "审计意见", "审计报告", "会计师事务所",
    "主营业务", "年度报告", "半年度报告", "季度报告",
]

# ── LLM helpers ──

def load_dotenv(path=".env"):
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip()
            if k and k not in os.environ:
                os.environ[k] = v

load_dotenv()

LLM_MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")
LLM_API_BASE = os.environ.get("LLM_API_BASE", "https://token-plan-cn.xiaomimimo.com/v1")
LLM_API_KEY = os.environ.get("LLM_API_KEY", os.environ.get("OPENAI_API_KEY", ""))


def call_llm(messages, max_retries=2):
    url = f"{LLM_API_BASE.rstrip('/')}/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {LLM_API_KEY}"}
    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 2048,
        "thinking": {"type": "disabled"},
    }
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=(10, 30))
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
        except Exception as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
            else:
                print(f"  LLM error: {e}")
                return None
    return None


def main():
    if not LLM_API_KEY:
        print("ERROR: No LLM_API_KEY in .env")
        sys.exit(1)

    BATCH_SIZE = 20
    all_groups = []
    n_batches = (len(CANONICAL_TERMS) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(CANONICAL_TERMS), BATCH_SIZE):
        batch = CANONICAL_TERMS[i:i + BATCH_SIZE]
        terms_str = "\n".join(f"{j+1}. {t}" for j, t in enumerate(batch))

        system_prompt = (
            "你是一位中文金融文档专家。"
            "请为下列每个术语列出其在中文财务文档中常见的同义词或近义词（用 | 分隔）。"
            "如果某个术语没有常见的同义词，就只输出该术语本身。"
            "输出格式严格为 JSON：{\"术语1\": \"同义1|同义2\", \"术语2\": \"同义1\"}。"
            "不要输出任何 JSON 以外的文字。"
        )

        print(f"Batch {i // BATCH_SIZE + 1}/{n_batches} ({len(batch)} terms)...", end=" ", flush=True)

        result = call_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": terms_str},
        ])

        if result:
            print(result)
            try:
                # Parse JSON
                m = json.loads(result)
                for term, syns_str in m.items():
                    if isinstance(syns_str, str):
                        synonyms = [s.strip() for s in syns_str.split("|") if s.strip()]
                        group = [term] + synonyms
                        all_groups.append(group)
                    elif isinstance(syns_str, list):
                        group = [term] + [s.strip() for s in syns_str if s.strip()]
                        all_groups.append(group)
                    else:
                        all_groups.append([term])
                print(f"→ {len(m)} groups parsed")
            except json.JSONDecodeError:
                print(f"→ JSON parse failed, trying manual extraction")
                # Manual extraction: find lines with "术语" or ":"
                for line in result.strip().split("\n"):
                    line = line.strip().strip("[],")
                    if "|" in line and ":" not in line:
                        terms = [t.strip().strip('"').strip("'") for t in line.split("|") if t.strip()]
                        if terms:
                            all_groups.append(terms)
        else:
            # Add batch as singletons (no LLM response)
            for t in batch:
                all_groups.append([t])
            print("→ FAILED, adding as singletons")

        time.sleep(0.5)

    # Deduplicate and assign group IDs
    synonym_map = {}
    group_id = 1

    for group in all_groups:
        if not group:
            continue
        existing_ids = {synonym_map[t] for t in group if t in synonym_map}
        if existing_ids:
            gid = min(existing_ids)
            for t in group:
                synonym_map[t] = gid
            for eid in existing_ids:
                if eid != gid:
                    for k, v in list(synonym_map.items()):
                        if v == eid:
                            synonym_map[k] = gid
        else:
            for t in group:
                synonym_map[t] = group_id
            group_id += 1

    # Add any canonical terms not covered
    for kw in CANONICAL_TERMS:
        if kw not in synonym_map:
            synonym_map[kw] = group_id
            group_id += 1

    output_path = "config/financial_synonyms.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(synonym_map, f, ensure_ascii=False, indent=2)

    total_terms = len(synonym_map)
    total_groups = len(set(synonym_map.values()))
    print(f"\nSaved {total_terms} terms across {total_groups} groups to {output_path}")

    # Print a few groups for verification
    print("\nSample groups:")
    groups_by_id = {}
    for term, gid in synonym_map.items():
        groups_by_id.setdefault(gid, []).append(term)
    for gid in sorted(groups_by_id)[:5]:
        print(f"  Group {gid}: {groups_by_id[gid]}")

if __name__ == "__main__":
    main()