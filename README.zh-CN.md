# Hermes Life · 饮食 + Fitness 公开预览版

[English](README.md) · [简体中文](README.zh-CN.md)

记一餐，记一次运动，接着过好今天。

一个 **fork 后不用 GPT 也能运行**的本地日常记录工具。饮食和 Fitness 为核心；
**Finance 默认关闭，用户主动开启**。采用 MIT 许可证。

[在线虚构 demo](https://hermes-preview.wenyeezy.com/) ·
[下载最新版](https://github.com/Wenyeezy/hermes-personal-assistant-template/releases) ·
[安装说明](START_HERE.md) · [反馈](COMMUNITY.md)

## 开始记录

安装 Python 3.10+，下载并解压，在**解压后的项目目录**打开终端：

```sh
python3 scripts/hermes.py start --open
```

不需要 Git、GPT、Codex、API key、账户或额外 Python 依赖。
Windows 将 `python3` 换成 `py -3`。也包含 macOS 的
`Start-Hermes.command` 和 Windows 的 `Start-Hermes.bat` 便捷启动文件；
若系统阻止下载文件运行，使用上面的终端命令即可。

1. **Nutrition**：保存饮食和营养值；待复核估算不计入已确认总量。
   复核后确认同一条记录，不重复生成餐次。
2. **Fitness**：记录运动或每日活动摘要；查看运动分钟数、步数和饮食汇总。
3. **Optional modules**：需要账本时主动启用 Finance。关闭后隐藏界面、
   阻止对应 Dashboard API，但保留已有本地记录。

终端保持打开，Ctrl-C 停止；不安装后台服务。
重复启动不覆盖已有配置或数据。默认数据位于 Git 忽略的
`private/Hermes_Runtime/`，数据库**未加密**。

先试虚构数据：

```sh
python3 scripts/hermes.py start --demo --open
```

示例隔离在 `private/Hermes_Demo/`；不会混入已有真实记录。
AWS 网页是独立静态模拟，不是托管个人数据服务。

## GPT / 本地模型 / Gateway 都是可选项

默认 Echo 只是离线测试，**不是 AI**。可用自己的账户或本地服务配置
OpenAI API、Codex CLI、Ollama 或兼容聊天端点。
启用云模型后，选择发送的提示或照片可能离开本机。
当前聊天**不会自动写入饮食或运动记录**。

本地 Hermes Gateway 仅在提供所需 chat-completions 协议时可通过兼容适配器接入；
生产 MCP、跨入口记忆和写入回执桥不包含在 starter 中。
详见[模型与端点接入](docs/runtime-edition.md)。

## 能力边界

| 能力 | 当前版本 |
| --- | --- |
| 手动饮食、确认、营养值、汇总和可选目标 | 无需 AI 即可用 |
| 每日活动、运动记录和当天运动总量 | 无需穿戴设备或 iPhone |
| Finance 手动账本 | 默认关闭，主动开启 |
| Career 机会追踪 | 默认关闭的扩展 |
| 本机 SQLite 和私人 Markdown 框架 | 可用；未加密 |
| 模型适配器与可选照片估算 | 需自行配置，默认关闭 |
| iOS App、银行同步、生产记忆和网关系统 | 未包含 |

## 隐私

- 不上传 `private/`、真实照片、导出、数据库或凭据。
- 首次启动不连接模型或账户；原始聊天默认不保存。
- Dashboard 默认只监听 `127.0.0.1`，不要直接暴露到公网。
- 关闭模块不等于删除或加密数据。
- 公共网页只用虚构数据，无注册、分析跟踪或模型调用。
- 接入真实记录前阅读[隐私说明](docs/safety-and-privacy.md)。

[架构](docs/architecture.md) · [路线图](ROADMAP.md) · [贡献](CONTRIBUTING.md)

## 许可证

[MIT](LICENSE)：可 fork、修改、复用及商业使用，需遵守许可条款。
早期预览按原样提供，不构成医疗或投资建议。
