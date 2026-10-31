# TEST & EVIDENCE GUIDE — 怎么跑、怎么留证据

> 目标：让每一条"我完成了"都有**命令 + 原始输出**，而不是一句话。

---

## 1. 三条必跑命令（每天收工前）

```bash
python scripts/check_env.py          # D0 一次即可
python tests/run_all.py              # 每天至少一次
python run_demo.py --task "..." --provider mock --script data/mock_script.json
```

**保存方式**：把命令和输出**原样**粘贴到 `EVIDENCE/D<n>/E-D<n>-xx_*.md`，不要改写、不要只写"通过"。

---

## 2. 证据目录（与课程一致）

```
EVIDENCE/
├── D0/  E-D0-01_REQUIREMENT.md   E-D0-02_BASELINE.md
├── D1/  E-D1-01_loop.md          E-D1-02_run_log.jsonl
├── D2/  E-D2-01_provider.md      E-D2-02_validation.md    E-D2-03.md
├── D3/  E-D3-01_registry.md      E-D3-02_boundary.md
├── D4/  E-D4-01_feedback.md      E-D4-02_multistep.jsonl  E-D4-03.md
├── D5/  E-D5-01_errors.jsonl     E-D5-02_inject.md
└── D6/  E-D6-01_repro.txt        E-D6-02_change.md        E-D6-03_challenge.md
```

**命名规则**：`<证据ID>_<内容>.<md|jsonl|txt>`。缺文件 = 该项无证据。

---

## 3. 每日证据模板（复制填写）

```markdown
# D<N> · <称呼> · GA7-D<N>-01

## 1. 今天做了什么（≤5 行）

## 2. 命令与原始输出（不要改写）
```
$ python tests/run_all.py
<paste the full tail here>
```

## 3. 测试状态
TOTAL __ / PASS __ / EXPECTED_RED __ / FAIL __ / 退出码 __

## 4. 失败的记录（如实）
- 现象：
- 我的排查：
- 排除了什么：
- 结论：解决 / 未解决 / 绕过（绕过必须写清）

## 5. MODEL SOURCE
本次运行是 MOCK 还是 REAL？依据（`run_demo.py` 的第一行输出）：

## 6. 我的贡献声明
- 我自己写的：
- AI 生成后我改的：
- 我参考了：
```

---

## 4. 四种结果怎么用

| 结果 | 写进证据时怎么说 |
|---|---|
`PASS` | "该测试通过"（**只能**说这一句对应的行为） |
`EXPECTED_RED` | "该任务尚未实现"（**不得**写成"部分完成"） |
`UNEXPECTED_GREEN` | "已实现，需移除 todo 标记" |
`FAIL` | "出现回归，正在定位"（**必须**附堆栈） |

---

## 5. MOCK / REAL 证据规范（硬性）

| 场景 | 允许写 | 禁止写 |
|---|---|---|
全程 Mock | "离线 Mock 下闭环通过" | "模型跑通了" |
真实模型成功 | "真实模型 <名> 在 <地址> 返回 <结果>"（附日志模型名/耗时） | "训练/微调了我的模型" |
真实模型不可用 | `ENV_BLOCKED` + 报错原文 | "环境问题不影响结论" |

**日志里必须有模型标识**：`run_demo.py` 第一行 `MODEL SOURCE: MOCK|REAL`。

---

## 6. 复现（D6）证据格式

```text
复现环境：<OS> / Python <版本>
复现目录：<一个全新的绝对路径>
复现命令：
  robocopy "<源>" "<新目录>" /E /XD logs __pycache__
  cd /d "<新目录>"
  python tests/run_all.py
实际输出（尾部 5 行）：
退出码：
```

> `xcopy /EXCLUDE:` 的参数是**包含模式的文本文件**，不是目录名；排除目录要用 `robocopy /XD`。

---

## 7. 反造假自查（交之前问自己）

1. 我的输出是**粘贴**的，还是**手打**的？
2. 有没有把 `EXPECTED_RED` 说成"完成"？
3. 有没有把 Mock 结果当成模型结果？
4. 测试是我改宽松了，还是代码真的对了？
5. 换台机器，三步还能跑通吗？
