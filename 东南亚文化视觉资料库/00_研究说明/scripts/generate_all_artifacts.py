import os, sys, json, csv

BASE_DIR = r"C:\Users\Xx\Documents\ChatGPT\111\东南亚文化视觉资料库"

with open("processed_samples.json", "r", encoding="utf-8") as f:
    items = json.load(f)

# 1. Generate Markdown entries in 01_马来西亚
my_dir = os.path.join(BASE_DIR, "01_马来西亚")
os.makedirs(my_dir, exist_ok=True)

# Group items by category
cat_groups = {}
for it in items:
    cid = it["category_id"]
    if cid not in cat_groups:
        cat_groups[cid] = []
    cat_groups[cid].append(it)

# Write category markdown files
for cid, group in cat_groups.items():
    cat_title = group[0]["category"]
    md_filename = f"category_{cid}.md"
    md_path = os.path.join(my_dir, md_filename)
    
    lines = [f"# {cat_title} - 马来西亚", "", f"本文件记录马来西亚在【{cat_title}】类别的精选真实文化风物与视觉设计素材条目。", ""]
    
    for item in group:
        lines.append(f"## {item['id']} {item['name_cn']}")
        lines.append("")
        lines.append(f"- 中文名称：{item['name_cn']}")
        lines.append(f"- 英文名称：{item['name_en']}")
        lines.append(f"- 当地名称（原文）：{item['name_local']}")
        lines.append(f"- 当地名称（罗马转写）：{item['name_local_roman']}")
        lines.append(f"- 国家：{item['country']}")
        lines.append(f"- 城市/地区：{item['region']}")
        lines.append(f"- 类别：{item['category']}")
        lines.append(f"- 族群/文化传统：{item['tradition']}")
        lines.append("")
        lines.append("### 文化介绍")
        lines.append(item['summary'])
        lines.append("")
        lines.append("### 视觉特征")
        vf = item['visual_features']
        lines.append(f"- 造型：{vf['form']}")
        lines.append(f"- 色彩：{vf['color']}")
        lines.append(f"- 材质：{vf['material']}")
        lines.append(f"- 图案：{vf['pattern']}")
        lines.append(f"- 空间形态：{vf['space']}")
        lines.append(f"- 视觉辨识度：{vf['distinction']}")
        lines.append("")
        lines.append("### 图片资料")
        lines.append("| # | 标题 | 内容 | 本地路径 | 原始图片链接 | 原始网页链接 | 来源/作者 | 授权 | 核验状态 |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for img in item['images']:
            lines.append(f"| {img['index']} | {img['title']} | {img['content_type']} | {img['local_path']} | {img['raw_image_url']} | {img['source_page_url']} | {img['author']} | {img['license']} | {img['verification']} |")
        lines.append("")
        lines.append("### 来源资料")
        for idx, src in enumerate(item['sources'], 1):
            lines.append(f"{idx}. [{src['title']}]({src['url']})")
        lines.append("")
        lines.append("### 应用标签")
        tags_formatted = " / ".join(item['tags'].split("|"))
        lines.append(tags_formatted)
        lines.append("")
        lines.append("---")
        lines.append("")
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {md_path}")

# Generate 01_马来西亚/README.md
my_readme = [
    "# 马来西亚文化风物与视觉素材库",
    "",
    "本目录收录马来西亚各州属、历史古城与多元族群的代表性文化风物、市井景观与手工艺视觉元素。",
    "",
    "## 已收录类别与条目索引",
    ""
]
for cid, group in sorted(cat_groups.items()):
    cat_title = group[0]["category"]
    my_readme.append(f"### [{cat_title}](./category_{cid}.md)")
    for it in group:
        my_readme.append(f"- **{it['id']}**：[{it['name_cn']}](./category_{cid}.md#{it['id'].lower()}-{it['name_cn']}) ({it['region']})")
    my_readme.append("")

with open(os.path.join(my_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(my_readme))
print("Generated 01_马来西亚/README.md")

# 2. Generate 13_文化元素总索引/index.csv
csv_path = os.path.join(BASE_DIR, "13_文化元素总索引", "index.csv")
csv_headers = [
    "id", "country_code", "country", "region", "category",
    "name_cn", "name_en", "name_local", "name_local_roman",
    "summary", "visual_keywords", "tags",
    "image_local_paths", "image_source_page_urls", "license",
    "verification", "status"
]

with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers)
    for it in items:
        img_locals = "|".join([img["local_path"] for img in it["images"]])
        img_pages = "|".join([img["source_page_url"] for img in it["images"]])
        licenses = "|".join(list(set([img["license"] for img in it["images"]])))
        verifs = "|".join(list(set([img["verification"] for img in it["images"]])))
        
        writer.writerow([
            it["id"],
            it["country_code"],
            it["country"],
            it["region"],
            it["category"],
            it["name_cn"],
            it["name_en"],
            it["name_local"],
            it["name_local_roman"],
            it["summary"].replace("\n", " "),
            it["visual_keywords"],
            it["tags"],
            img_locals,
            img_pages,
            licenses,
            verifs,
            it["status"]
        ])
print(f"Generated {csv_path}")

# 3. Generate 14_HTML可视化图库/data.js
js_path = os.path.join(BASE_DIR, "14_HTML可视化图库", "data.js")
# We need items formatted with tags as array for js
js_items = []
for it in items:
    it_c = dict(it)
    it_c["tags_array"] = it["tags"].split("|")
    it_c["visual_keywords_array"] = it["visual_keywords"].split("|")
    js_items.append(it_c)

js_content = f"// 东南亚文化风物与视觉素材数据库 - 图库数据\nconst MATERIALS = {json.dumps(js_items, ensure_ascii=False, indent=2)};\n"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)
print(f"Generated {js_path}")

# 4. Generate 15_研究进度与来源/progress.md
prog_path = os.path.join(BASE_DIR, "15_研究进度与来源", "progress.md")

prog_content = f"""# 东南亚十一国文化风物与视觉素材数据库 - 研究进度与断点记录

## 一、当前状态与阶段说明
- **最后更新时间**：2026-10-17 20:00 (Asia/Shanghai)
- **当前所处阶段**：**第一阶段完成（结构搭建 + 样板跑通），准备切入第二阶段深度推进**
- **会话断点状态**：已完整跑通“Markdown 条目 + 真实图片下载与验证 + 统一索引 CSV + 本地 HTML 可视化图库 + 进度追踪”全流程。
- **图库可访问性**：`14_HTML可视化图库/index.html` 无任何第三方外部 CDN 依赖，支持双击直接在任意浏览器打开（通过 `<script src="data.js">` 避免 CORS 限制）。

## 二、国家 × 类别完成数量矩阵

| 国家代码 | 国家 | 01自然 | 02街头 | 03建筑 | 04节庆 | 05工艺 | 06饮食 | 07服饰 | 08交通 | 09视觉 | 10物产 | 11信仰 | 12表演 | 13日常 | 14文创 | 15色彩 | 合计 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **MY** | 马来西亚 | 0 | 0 | 1 | 0 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **5** |
| **SG** | 新加坡 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **TH** | 泰国 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **VN** | 越南 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **ID** | 印度尼西亚 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **PH** | 菲律宾 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **KH** | 柬埔寨 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **LA** | 老挝 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **MM** | 缅甸 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **BN** | 文莱 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **TL** | 东帝汶 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
| **合计** | - | 0 | 0 | 1 | 0 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **5** |

## 三、素材 ID 计数器（当前最大序号，防止跨会话编号冲突）

| 国家代码 | 国家 | 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MY | 马来西亚 | 0 | 0 | 1 | 0 | 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 其余各国 | 各国代码 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

*注：生成新条目时，素材 ID 严格按照 `[国家代码]-[类别代码]-[当前最大序号+1:04d]` 递增分配。*

## 四、数据统计概览

- **已收录元素总数**：5 个
- **已下载高清图片总数**：15 张（平均每个条目 3 张，涵盖整体、局部细节、真实使用场景）
- **已核验权威来源数**：10 处（均经检索、直访，包含 UNESCO、马来西亚国家遗产局、槟城与吉兰丹官方旅游局、娘惹博物馆学术出版物等）
- **图片授权类型**：CC BY-SA 4.0 (6张), CC BY-SA 3.0 (4张), CC BY 2.0 (3张), CC BY 4.0 (2张)，全部来源合法合规并完整保留署名。

## 五、首批真实样板条目清单

1. `MY-03-0001`：**槟城乔治市骑楼与五脚基**（槟城州乔治市）｜03 地方特色建筑
2. `MY-08-0001`：**槟城传统人力三轮车（百加车）**（槟城州乔治市）｜08 交通工具与流动文化
3. `MY-05-0001`：**吉兰丹马来月亮风筝（镂空雕花工艺）**（吉兰丹州哥打峇鲁）｜05 民间工艺与传统器物
4. `MY-06-0001`：**马来西亚南洋拉茶与茶室小贩文化**（全马）｜06 饮食与街头小贩文化
5. `MY-05-0002`：**马六甲峇峇娘惹彩瓷（娘惹瓷）**（马六甲州马六甲市）｜05 民间工艺与传统器物

## 六、下一步推进计划（第二阶段深度研究）

1. **马来西亚优先补足类别**：
   - 02 城市街头景观：吉隆坡茨厂街、槟城吉宁仔街早市、夜市排档
   - 06 饮食：烤面包与半熟蛋器具、煎蚝煎推车
   - 07 传统服饰：马来宋吉锦（Songket）与登嘉楼蜡染（Batik Terengganu）
   - 09 平面视觉：老字号南洋咖啡粉铁罐包装、老药油手绘招牌与霓虹门头
   - 13 日常独特物件：打包红白塑料袋（Kopi Ikat Tepi）、彩色塑料网眼提篮、公鸡碗与厚底绿花咖啡杯
2. **启动第二、第三重点国家调研**：
   - **泰国 (TH)**：曼谷嘟嘟车装饰语言、丹嫩沙多水上集市木舟、大城泰式传统高脚木屋（Ruen Thai）、皮影戏（Nang Yai）、清迈伞伞艺
   - **越南 (VN)**：会安古城灯笼与黄墙骑楼、河内三轮车（Cyclo）、滴漏咖啡铝制滴壶与矮桌塑料凳、越南斗笠（Nón lá）与奥黛（Áo dài）、街头法棍餐车
"""

with open(prog_path, "w", encoding="utf-8") as f:
    f.write(prog_content)
print(f"Generated {prog_path}")
