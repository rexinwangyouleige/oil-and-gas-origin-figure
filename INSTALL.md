# 安装到各类 agent 工具

这个仓库是一个 **Agent Skill**（根目录一个 `SKILL.md` + `ogfig/` 引擎 + `catalog/` 图型脚本）。凡是"能读 `SKILL.md` 并按它做事"的 agent，都能用；差别只在**放哪个目录**和**怎么触发**。

> ⚠️ 前置条件（装完也跑不了图的话先看这里）：本技能是**用 Python 驱动 Origin 出图**，要在 **Windows + Origin 2024b 及以上** 的机器上才能真出图（2026b / 10.3 实测）；另需 `python` 可 `import originpro`（`pip install originpro numpy pandas pymupdf`）。
> 没有 Origin 的机器上，它仍可作为"画图规范 + 脚本模板"参考，但跑不了出图脚本。

## 1. 放哪儿

| 工具 | 目录 | 状态 |
|---|---|---|
| **通用 / VS Code Copilot** | `~/.agents/skills/<名字>/SKILL.md` | VS Code 官方文档列出的位置之一 ✅ |
| **Claude Code** | `~/.claude/skills/<名字>/SKILL.md`（个人）或 `<项目>/.claude/skills/`（项目） | 官方文档 ✅ |
| **DeepSeek Harness (DSH)** | `~/.dsh/skills/<名字>/SKILL.md`；或 `<项目>/.dsh/skills/`、`<项目>/.agents/skills/`、`~/.agents/skills/` | 读 DSH 的 `dsh-skill-filesystem` 实现确认 ✅（**只扫一层**，必须 `<根>/<名字>/SKILL.md`） |
| Codex CLI 等 | `~/.codex/skills/<名字>/SKILL.md` | 社区惯例，未逐一验证；不认就用下面的「方法 B」 |
| 其它（Cursor / Cline / WorkBuddy / 自研 agent…） | 见方法 B | — |

## 2. 装（方法 A：复制到 skills 目录）

**Windows PowerShell**

```powershell
$repo = "https://github.com/rexinwangyouleige/oil-and-gas-origin-figure.git"
$dst  = "$env:USERPROFILE\.agents\skills\oil-and-gas-origin-figure"   # 通用位置
New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
git clone --branch v0.2.2 --depth 1 $repo $dst
```

**macOS / Linux**

```bash
git clone --branch v0.2.2 --depth 1 \
  https://github.com/rexinwangyouleige/oil-and-gas-origin-figure.git \
  ~/.agents/skills/oil-and-gas-origin-figure
```

**要用在 Claude Code / DSH 上**：把 `$dst` / `~/.agents/skills/...` 换成下面对应路径再跑一次，或者做一个目录联接复用同一份（Windows 不需要管理员权限）：

```powershell
New-Item -ItemType Junction "$env:USERPROFILE\.claude\skills\oil-and-gas-origin-figure" -Target $dst
New-Item -ItemType Junction "$env:USERPROFILE\.dsh\skills\oil-and-gas-origin-figure"    -Target $dst
```

```bash
ln -s ~/.agents/skills/oil-and-gas-origin-figure ~/.claude/skills/oil-and-gas-origin-figure
```

装完重启会话（DSH 会自动监视目录，新加的 skill 下一轮就在）。

## 3. 装（方法 B：不给 skills 目录的工具）

这类工具没有"技能"概念，两个办法：

1. **让它读**：会话里直接把路径丢给它——"先读 `~/.agents/skills/oil-and-gas-origin-figure/SKILL.md`，按里面的工作流出图"；
2. **写进项目规则**：在仓库根目录的 `AGENTS.md` / `.cursor/rules/*.mdc` / 系统提示里加一行：

   ```
   出任何 Origin 图之前，先读 ~/.agents/skills/oil-and-gas-origin-figure/SKILL.md 并遵循其规范与自检流程。
   ```

## 4. 验证

```bash
ls ~/.agents/skills/oil-and-gas-origin-figure/SKILL.md      # Windows: dir $env:USERPROFILE\.agents\skills\oil-and-gas-origin-figure\SKILL.md
head -4 ~/.agents/skills/oil-and-gas-origin-figure/SKILL.md  # 应看到 name: oil-and-gas-origin-figure
```

在会话里说一句 **"用 oil-and-gas-origin-figure 画一张产量递减图"**，看它是否按 `SKILL.md` 的工作流走（先 `ogfig.cli doctor` → 选图 → 出图 → 自检）。

## 5. 给"没有终端权限"的 AI 用的提示词

把下面整段粘给豆包 / ChatGPT / Claude 网页版等，它有终端权限就直接装，没有就会把命令原样给你：

```text
你是有终端权限的安装助手。请在这台电脑上安装一个 agent skill：
oil-and-gas-origin-figure（用 Python 驱动 Origin 出油气领域论文图的技能包）。

仓库地址：https://github.com/rexinwangyouleige/oil-and-gas-origin-figure

按以下步骤做，不要跳步：
1) 判定系统：Windows 用 PowerShell，macOS/Linux 用 bash。
2) 目标目录（不存在就创建，已存在就 git -C <目录> pull --ff-only 更新，不要覆盖）：
   - 默认装到  ~/.agents/skills/oil-and-gas-origin-figure   （Windows: %USERPROFILE%\.agents\skills\oil-and-gas-origin-figure）
   - 如果机器上存在 ~/.claude/skills 或 ~/.dsh/skills，再各做一个目录联接/软链接指向它（Windows 用
     New-Item -ItemType Junction，不需要管理员权限）。
3) 克隆（浅克隆指定版本）：
   git clone --branch v0.2.2 --depth 1 <仓库地址> <目标目录>
4) 校验：<目标目录>/SKILL.md 必须存在，且前几行含 "name: oil-and-gas-origin-figure"；
   缺少任何一个就停下并报告错误，不要继续。
5) 最后报告：
   - 装到了哪个路径；
   - 目标机器是否满足运行前提（Windows + Origin 2024b 以上 + python 能 import originpro），
     不满足就明确说"只能当规范参考，出图需要 Origin"；
   - 我该怎么在会话里触发它（一句示例话术）。

限制：
- 不要用 sudo / 管理员权限，不要改系统目录；
- 不要删除或覆盖我已有的同名文件，冲突时先备份或询问；
- 只做"安装 + 校验"，不要执行仓库里的 .py 脚本（不运行 Origin）。
```

## 6. 更新 / 卸载

```bash
git -C ~/.agents/skills/oil-and-gas-origin-figure fetch --tags
git -C ~/.agents/skills/oil-and-gas-origin-figure checkout v0.2.2   # 或 main
```

卸载就是删掉那个目录（以及你建的 junction / 软链接）。
