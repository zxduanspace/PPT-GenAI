from pptx import Presentation

# 加载你的模板
prs = Presentation("template.pptx")

print("🔍 开始分析模板结构...\n")

# 遍历每一个布局 (Layout)
for i, layout in enumerate(prs.slide_layouts):
    print(f"--- Layout Index [{i}]: {layout.name} ---")
    
    # 遍历该布局下的所有占位符 (Placeholder)
    for shape in layout.placeholders:
        print(f"   Placeholder idx [{shape.placeholder_format.idx}] - 类型: {shape.name}")

print("\n✅ 分析结束。请把这些 Index 记下来！")