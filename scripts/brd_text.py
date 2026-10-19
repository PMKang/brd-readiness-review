#!/usr/bin/env python3
"""BRD 文本抽取与字数统计。

用法：
  brd_text.py extract <文档路径> <输出目录>
      抽取全文到 <输出目录>/brd.txt，打印总字数和章节字数表（带行号）。
  brd_text.py count <brd.txt> <起-止:类别> [<起-止:类别> ...]
      按行号范围归类统计字数和占比；未覆盖的行计入"未分类"。

字数只算中文、英文字母和数字，不算空格、标点和表格线。
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

CHAR_RE = re.compile(r"[一-鿿A-Za-z0-9]")
HEADING_RE = re.compile(
    r"^\s*(#{1,3}\s+\S|[一二三四五六七八九十]+[、.．]\s*\S|\d+(\.\d+){0,2}\s+\S{2,}|\*?[一二三四五六七八九十]+、)"
)
EFFECTIVE = {"痛点", "场景", "规则", "期望"}


def chars(text):
    return len(CHAR_RE.findall(text))


def to_text(src: Path) -> str:
    ext = src.suffix.lower()
    if ext in (".txt", ".md"):
        return src.read_text(encoding="utf-8", errors="ignore")
    if ext == ".pdf":
        if shutil.which("pdftotext"):
            return subprocess.run(["pdftotext", "-layout", str(src), "-"],
                                  capture_output=True, text=True, check=True).stdout
        raise SystemExit("缺少 pdftotext（brew install poppler），或改用 Read 工具直接读 PDF")
    if ext == ".docx" and shutil.which("pandoc"):
        return subprocess.run(["pandoc", str(src), "-t", "plain", "--wrap=none"],
                              capture_output=True, text=True, check=True).stdout
    if ext in (".docx", ".doc", ".rtf") and shutil.which("textutil"):
        return subprocess.run(["textutil", "-convert", "txt", "-stdout", str(src)],
                              capture_output=True, text=True, check=True).stdout
    raise SystemExit(f"不支持的格式：{ext}")


def extract(src, out_dir):
    src, out = Path(src), Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    text = to_text(src)
    (out / "brd.txt").write_text(text, encoding="utf-8")
    lines = text.split("\n")
    total = chars(text)
    print(f"已写入 {out / 'brd.txt'}（{len(lines)} 行）")
    print(f"全文字数：{total}\n")

    heads = [i for i, l in enumerate(lines) if HEADING_RE.match(l) and len(l.strip()) < 40]
    if not heads:
        print("未识别到章节标题，请直接通读全文分段。")
        return
    print("行号范围\t字数\t占比\t标题")
    bounds = [0] + heads + [len(lines)]
    for a, b in zip(bounds, bounds[1:]):
        n = chars("\n".join(lines[a:b]))
        if n == 0:
            continue
        title = lines[a].strip()[:30] if a in heads else "（开头）"
        print(f"{a + 1}-{b}\t{n}\t{n * 100 / total:.0f}%\t{title}")


def count(txt, specs):
    lines = Path(txt).read_text(encoding="utf-8").split("\n")
    label_of = ["未分类"] * len(lines)
    for spec in specs:
        rng, label = spec.split(":", 1)
        a, b = (int(x) for x in rng.split("-"))
        for i in range(max(a, 1) - 1, min(b, len(lines))):
            label_of[i] = label
    stats = {}
    for line, label in zip(lines, label_of):
        stats[label] = stats.get(label, 0) + chars(line)
    total = sum(stats.values()) or 1
    unknown = set(stats) - EFFECTIVE - {"越界", "铺垫", "重复", "未分类"}
    if unknown:
        print(f"注意：类别 {unknown} 不在标准类别里（痛点/场景/规则/期望/越界/铺垫/重复），按无效计")
    print("类别\t字数\t占比")
    for label, n in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"{label}\t{n}\t{n * 100 / total:.0f}%")
    eff = sum(n for k, n in stats.items() if k in EFFECTIVE)
    core = stats.get("痛点", 0) + stats.get("场景", 0)
    print(f"\n有效内容（痛点/场景/规则/期望）：{eff} 字，占 {eff * 100 / total:.0f}%")
    print(f"核心内容（痛点/场景）：{core} 字，占 {core * 100 / total:.0f}%")
    if stats.get("未分类"):
        print(f"提示：还有 {stats['未分类']} 字未分类")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "extract":
        extract(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 4 and sys.argv[1] == "count":
        count(sys.argv[2], sys.argv[3:])
    else:
        print(__doc__)
        sys.exit(1)
