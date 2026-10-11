# Hermes Life · 公开预览版

[English](README.md) · [简体中文](README.zh-CN.md)

一个 local-first 的日常工作区：记录并复核饮食、活动摘要、简单账目和求职下一步。

**这是可运行的 starter，不是维护者私人 Hermes 的完整副本。** 包含 Python
Dashboard 和本地手动记录；不包含个人数据、生产网关、自动记忆采纳或已连接账户。

[浏览器演示](site/README.md) ·
[在线虚构演示](https://hermes-preview.wenyeezy.com/) ·
[下载预览版](https://github.com/Wenyeezy/hermes-personal-assistant-template/releases) ·
[详细安装](INSTALL_FOR_FRIEND.md) · [反馈](COMMUNITY.md)

## 一条命令开始

在线 demo 位于 AWS，已配置固定 HTTPS 地址。它是独立的静态模拟演示，
不是本地运行版的托管服务。

下载并解压仓库，**进入解压后的文件夹**，使用 Python 3.10 或以上运行：

```sh
python3 scripts/hermes.py start --demo --open
```

不需要 Git、Codex、API key、账户或额外 Python 依赖。它会在单独的
`private/Hermes_Demo/` 创建**虚构示例**并打开 localhost Dashboard。
终端保持打开，Ctrl-C 停止。Windows 可将 `python3` 替换为 `py -3`。

先到 Career 保存一个示例机会和下一步，再到 Nutrition 对比已确认与待复核记录。
保存回执对应本机 SQLite 写入。默认聊天是 **offline echo，不是 AI 模型**。

想开始空白的私人工作区，运行：

```sh
python3 scripts/hermes.py start --open
```

已有配置和数据不会覆盖。demo 默认与真实工作区隔离；未标为 demo 的非空数据库
会拒绝加入示例。模型连接之后单独选择，使用自己的账户或本地模型。

## 能力边界

| 能力 | 公开预览版 |
| --- | --- |
| Dashboard；手动 Nutrition、Health、Finance、Career 记录 | 可用 |
| 已确认饮食统计、目标和导出格式 | 可用；不自动写入 iPhone |
| 私人 Markdown scaffold 和本机 SQLite | 可用；starter 不提供数据库加密 |
| OpenAI、Codex CLI、Ollama、兼容接口适配器 | 已包含，默认关闭 |
| 自动记忆复核、跨入口召回、生产 MCP 网关 | 私人系统能力，未包含 |
| 银行同步、投递申请、消息与定时自动化 | starter 不启用 |
| HIIS、Crypto + RWA Research Labs | 独立研发模块，目前为研究文档 |

浏览器网页用虚构数据**模拟**复核流程，不是托管 AI 服务，不读取维护者账户。
输入不发送给模型或真实网关。真正的本地记录体验请下载运行版。

## 隐私与安全

- 配置、数据库和知识文件默认只写入 Git 忽略的 `private/`，不要上传此目录。
- 首次启动不连接云模型、银行、邮箱或消息账户；原始聊天默认不保存。
- Dashboard 默认只监听 `127.0.0.1`，**不要直接对公网开放**。
- 云模型只在你主动启用后调用；文本过滤不是完整脱敏保证。
- 先使用虚构数据。接入真实数据前阅读[隐私说明](docs/safety-and-privacy.md)。

[开始使用](START_HERE.md) · [模型接入](docs/runtime-edition.md) ·
[架构](docs/architecture.md) · [产品分区](docs/product-areas.md) ·
[路线图](ROADMAP.md) · [贡献指南](CONTRIBUTING.md)

## 授权与预期

目前未授予开源许可证。仓库公开不等于开放源代码授权；许可证确定前由所有者保留权利。
这是早期预览，不提供医疗、投资或就业结果保证。欢迎通过 issue 模板提供反馈。
