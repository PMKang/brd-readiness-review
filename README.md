# brd-readiness-review

业务需求文档（BRD）就绪度评估 Skill。采用通用的 `SKILL.md` 格式，Claude Code、Codex、WorkBuddy、CodeBuddy 等支持 Skills 的 agent 都能用。

业务经常发来一两万字的需求文档，读完才发现一半是无效内容、痛点没讲清、反而写了一堆表结构。这个 Skill 帮产品经理先过一遍：打分、提炼一页摘要、生成可以直接转给业务的追问清单。

## 总原则

**业务管"为什么做、谁、什么场景、想要什么结果"，产品管"怎么做"。**

## 评分（满分 100）

| 维度 | 分值 | 看什么 |
|---|---|---|
| 痛点与背景 | 35 | 遇到什么麻烦、多严重、因果链是否合理；有数据加分，有具体案例也行 |
| 用户场景四要素 | 30 | 谁、在什么场景、遇到什么事、希望怎么样 |
| 痛点和诉求对得上 | 10 | 想要的功能能不能解决说的痛点 |
| 精简度 | 25 | 有效内容占比（脚本按章节统计） |

另有门槛项（一票退回）、越界扣分（表结构、存储模型、模块设计等产品该做的事）、红旗信号（如 AI 生成的伪 PRD）。详见 [references/rubric.md](references/rubric.md)。

## 输出

- 总分与结论（可进入评估 / 补充后评估 / 建议退回）
- 一页摘要：替你读完原文
- 各维度扣分说明，每条都引原文
- 前后矛盾清单
- 追问清单，可以直接转给业务
- 附一份给业务的[一页纸需求模板](templates/一页纸需求模板.md)

## 安装

把仓库克隆到你所用 agent 的 skills 目录：

| Agent | 目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |
| CodeBuddy | `~/.codebuddy/skills/` |
| 其他支持 Agent Skills 的工具 | `~/.agents/skills/` 或该工具文档指定的目录 |

```bash
git clone https://github.com/PMKang/brd-readiness-review ~/.claude/skills/brd-readiness-review
```

同时用多个 agent 时，克隆一份，其余目录用软链接指过去即可：

```bash
ln -s ~/.claude/skills/brd-readiness-review ~/.codex/skills/brd-readiness-review
```

依赖：Python 3；docx 需要 `pandoc`（macOS 无 pandoc 时自动用 `textutil`），pdf 需要 `pdftotext`（`brew install poppler`）。

## 使用

在 agent 里附上需求文档，说"评估一下这个需求"即可。

## 本地配置（可选）

在 skill 目录下新建 `local.md`（已加入 `.gitignore`），可以写：

- 报告输出目录
- 自己的真实校准样本：每评完一份有代表性的文档追加一条，让打分尺度越来越贴合你们公司

## 目录

```
SKILL.md                     评估流程
references/rubric.md         评分标准
references/report-template.md 报告结构
references/calibration.md    校准样本（脱敏示例）
scripts/brd_text.py          文本抽取与字数统计
templates/一页纸需求模板.md    给业务的填写模板
```
