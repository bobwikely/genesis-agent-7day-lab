# GA7 Agent 起步包 v0.2.0

七天 Agent 实战的代码骨架。你从零把核心逻辑写出来，这个包负责给你：
能跑的环境检查、能跑的测试框架、能读的日志、能提交的证据结构。

> **这不是一个做好的 Agent。** 九个核心任务故意留空，等你自己实现。

---

## 1. 这个包是干什么的

七天里你只做**一个** Agent。每天加一层能力，到第 6 天它要能真的跑、能被别人复现、你能解释。

这个包提供的是**脚手架**，不是答案：
- 已经给好：配置、日志、Provider 接口、离线 Mock、测试运行器、环境自检
- 要你写：决策校验、工具注册与边界、主循环、异常处理、真实模型接入

## 2. 适合谁

- 会用命令行，能读 Python
- 愿意按测试的失败信息一步步改代码
- 不要求你之前写过 Agent

**不需要**：GPU、API Key、付费账户、外部数据库。

## 3. 环境要求

| 项 | 要求 |
|---|---|
Python | **3.9 或更高**（`python -V` 查看） |
第三方包 | **一个都不需要**，不用 `pip install` |
网络 | 基础闭环**不需要联网**；只有接本机 Ollama 时才连 `127.0.0.1` |
磁盘 | 约 1 MB |

## 4. 安装与启动

```bash
# 进入包目录后
python -V                     # 确认 >= 3.9
python scripts/check_env.py   # 环境自检，退出码 0 表示可用
python tests/run_all.py       # 看当前进度（会有很多 EXPECTED_RED）
```

跑一次 Agent（核心逻辑还没写时返回 `NOT_IMPLEMENTED`，这是**正常**的）：

```bash
python run_demo.py --task "读取 notes.txt 并说出 total_lines" \
                   --provider mock --script data/mock_script.json
```

## 5. 目录结构

```
.
├── README.md                    本文件
├── TEST_AND_EVIDENCE_GUIDE.md   测试与证据规范
├── TEST_REPORT.md               本次实际测试结果
├── STARTER_KIT_MANIFEST.json    文件清单 + SHA-256（完整性校验）
├── run_demo.py                  命令行入口
├── .env.example                 环境变量示例（不含任何密钥）
├── agent/
│   ├── config.py                配置（已给）
│   ├── runlog.py                结构化日志（已给）+ 日志目录边界校验（已给）
│   ├── providers.py             Provider 协议 + 离线 Mock（已给）／Ollama（留空）
│   ├── decision.py              决策校验（留空）
│   ├── tools.py                 工具注册表与边界（留空）
│   └── loop.py                  主循环（留空）
├── scripts/check_env.py         Day0 环境自检
├── tests/                       55 项测试（含分类器自测与边界测试）
├── data/                        示例输入
└── evidence/                    你的证据放这里
```

## 6. 七天怎么用这个包

每一天的任务文字在课程主手册 **《GENESIS AGENT 7-DAY ENGINEERING CHALLENGE V1.0》** 的对应章节里（任务编号 `GA7-D0-01` … `GA7-D6-01`）。这个包只提供**代码落点**。

| 天 | 任务编号 | 你要改的代码 | 验收看什么 |
|---|---|---|---|
D0 | GA7-D0-01 / D0-02 | 无代码；跑 `scripts/check_env.py` | 需求卡可判定 + 环境记录 |
D1 | GA7-D1-01 / D1-02 | `agent/loop.py` | 五环节可指行号；有 `max_steps` 终止记录 |
D2 | GA7-D2-01 / D2-02 | `agent/providers.py`、`agent/decision.py` | 非法决策被拒且**无工具执行** |
D3 | GA7-D3-01 / D3-02 | `agent/tools.py` | 恰好 2 个工具；越界被拒 |
D4 | GA7-D4-01 / D4-02 | `agent/loop.py` | 第 2 步输入含第 1 步结果 |
D5 | GA7-D5-01 | `agent/loop.py` | 三类故障各有状态、不崩溃 |
D6 | GA7-D6-01 / D6-02 | 全包 | 干净目录跑通 + 旧测试全绿 |

**建议顺序**：D0 → D3-01 → D3-02 → D2-02 → D1-01 → D1-02 → D4 → D5 → D2-01。
先让工具能用，再让决策合法，最后才跑循环。

每天收工前跑一次 `python tests/run_all.py`，把命令和原始输出存进 `evidence/D<N>/`。

## 7. 注意事项

**关于测试**
- 红色不等于你做错了。`EXPECTED_RED` 的意思是"这项还等你实现"，详见 `TEST_AND_EVIDENCE_GUIDE.md`。
- 只有全部变绿才是 D6 的"全绿"，中途退出码是 2（进行中），不是失败。

**关于模型**
- 默认 `GA7_PROVIDER=mock`，**完全离线**，不需要任何 Key。
- **Mock 不是模型**。用 Mock 跑通只能说"逻辑通了"，不能说"模型验证过了"。
- 要接真实模型，需自己在本机装 Ollama；装不上就如实记 `ENV_BLOCKED`，不扣分。

**安全红线（写代码时必须守住）**
- 工具**白名单**：不得出现 shell / exec / 任意网络
- 禁止 `eval()`，算术走 AST 白名单
- `read_file` 只能读工作区内；拒绝 `..`、绝对路径、`C:foo`、UNC
- 必须有步数上限与工具错误次数上限
- 异常必须进日志，不许 `except: pass`
- **不要提交任何真实密钥**；`.env` 不进版本库

**关于你的成果**
- 你写的代码归你
- 包内材料未设开源许可：可以读、可以改，不要对外转发
