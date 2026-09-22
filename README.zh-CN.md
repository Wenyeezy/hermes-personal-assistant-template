# Hermes 个人 AI 助手模板

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个 local-first 个人助手项目，分为两大产品区域：作为主产品的 **Hermes Life**，以及仍在开发中的 **Hermes Research Labs**。Research Labs 目前包含 HIIS 和 Crypto + RWA。

本仓库经过有意清理，只公开架构、规则、模板与可复现的示例，不包含私有配置、API 密钥、账户标识或个人记忆。

## 先从 Hermes Life 开始

Hermes Life 是项目的主要产品。它围绕可迁移记忆、隐私路由和明确的任务回执，组织个人背景、决策与日常工作流。维护者每天都在使用私有 Life 系统；它是整个项目里成熟度最高、测试最多的部分。

| 产品区域 | 当前状态 | 在本仓库可以做什么 |
| --- | --- | --- |
| **Hermes Life** | 主产品；维护者的私有系统每天测试使用 | 下载或 Fork 公共 starter，然后运行 [Easy Setup](START_HERE.md) |
| **Hermes Research Labs** | 开发中；还不是完成的公共插件 | 阅读 [HIIS](docs/hiis.md) 和 [Crypto + RWA Lab](docs/digital-assets-lab.md) |

目前可以下载的 Life 版本是经过清理的 starter package，包含架构、记忆模板、确定性的 Easy Setup 和设置测试。它不包含维护者的个人数据或完整私有 Runtime。Research Labs 是可选的独立区域，不会随 Life Easy Setup 一起安装。

[产品与分装方式](docs/product-areas.md) · [项目地图](docs/project-map.md) · [路线图](ROADMAP.md) · [社区与反馈](COMMUNITY.md) · [参与贡献](CONTRIBUTING.md)

## 安装 Hermes Life Starter

Fork 或下载本仓库，将整个文件夹作为 Codex 项目打开，然后说：

```text
Read AGENTS.md and help me start Easy Setup.
```

Codex 会读取仓库内的说明并执行确定性的脚手架流程。默认情况下，个人文件只会生成在 Git 忽略的 `private/` 目录中；该流程不会启用凭据、模型服务、消息网关、定时任务或后台服务。

等价的手动命令为：

```text
python3 scripts/easy_setup.py check
python3 scripts/easy_setup.py init
python3 scripts/easy_setup.py check
```

详见 [Start Here](START_HERE.md) 和 [Codex Easy Setup](docs/easy-setup.md)。目前操作文档以英文为主；本页提供项目的完整中文入口。

---

## Hermes Life：主要产品

Hermes Life 被设计成个人助手层，而不只是一个聊天机器人。目标包括：

- 保存稳定偏好和项目状态；
- 在写入长期记忆前，对生活、项目和决策更新进行分类；
- 使用可迁移、可人工检查的 Markdown 保存长期记忆；
- 私密任务优先使用本地模型；
- 对适合云端处理的任务使用高质量云模型；
- 通过由所有者控制的微信、Telegram 等消息入口使用助手；
- 将私有实现日志与经过清理的公共说明分开；
- 对健康、财务、职业与研究等工作流保留明确边界和验证证据。

```text
微信 / Telegram / Dashboard
  -> 单一 Hermes Gateway 服务
      -> 平台适配器 + 平台独立会话
  -> Hermes Agent
  -> 隐私路由 + 记忆路由 + 模型路由
      -> 本地模型：私密或简单任务
      -> 云端模型：非敏感或高质量任务
      -> 工具：网页、文件、任务、健康、财务、研究
  -> 可迁移的 Markdown 长期记忆层
```

## 核心设计

最重要的设计选择，是将 **Agent 运行时记忆** 与 **可迁移长期记忆** 分开：

```text
Agent 内部记忆
  只保存简短、稳定、非敏感的索引事实

Markdown 长期记忆层
  保存详细偏好、项目状态、决策记录和工作流

禁止保存区
  随机聊天片段、敏感原始数据和临时上下文
```

研究证据也与个人资料记忆分开。一篇文章中的观点不会因为被收集，就自动成为已验证事实或用户偏好。

## 建议的记忆结构

```text
AI_Knowledge_Base/
├── START_HERE.md
├── Profile/
│   ├── user_core_profile.md
│   └── response_preferences.md
├── Current_State/
│   └── current_state.md
├── Decision_Logs/
│   └── decision_log_index.md
├── Projects/
│   └── local_ai_system.md
├── Workflows/
│   ├── personal_memory_policy.md
│   └── personal_memory_triage.md
├── Life_Updates/
│   ├── daily_logs/
│   └── weekly_reviews/
└── Index/
    └── master_index.md
```

用户只需要记住一个入口文件：`START_HERE.md`。新的助手应先阅读该文件。

## 快速设置顺序

1. 将仓库作为 Codex 项目打开并启动 Easy Setup。
2. 创建私有 Markdown 脚手架，暂时不要添加凭据。
3. 填写回复偏好、当前状态和一个项目。
4. 在公共 Git 跟踪目录之外配置一个模型服务商。
5. 先用简单、非敏感的任务测试。
6. 定义仅限本地、经过脱敏聚合以及可使用云端的内容范围。
7. 核心设置稳定后，再添加消息网关。
8. 最后添加有明确上限、由所有者授权的自动化。

如果接入多个聊天平台，建议由一个长期运行的 Gateway 服务承载多个隔离的平台适配器。隐私、记忆、模型、工具与文件访问策略可以共享，但会话、媒体传输、回执、速率限制和所有者白名单应按平台隔离。

模型路由建议逐步推进：

```text
单一服务商 -> 手动切换 -> 基于规则切换 -> 自动化
```

不要静默切换到聚合服务商或更昂贵的模型。隐式回退可能在用户不知情的情况下发送上下文并产生费用。

## Research Labs：HIIS + Crypto/RWA

Research Labs 是第二个产品区域，由两个相互连接的模块组成：

- **HIIS（Hermes Investment Intelligence System）**：以证据为中心的投资研究系统，让研究结论能够追溯到来源、时间、反证和后续复盘；
- **Crypto + RWA Lab**：HIIS 的早期应用，研究 stablecoin 证据、数字资产运行状态和代币化现实世界资产的披露。

这两个模块仍在开发和测试。本仓库目前公开研究范围和[虚构证据案例](examples/digital-assets-evidence-demo.md)，尚未提供完成的安装包或实时金融服务。

计划采用模块化分装：

```text
Hermes 基础层
  ├── Hermes Life starter       现在可用
  └── Research Labs package     计划中
        ├── HIIS
        └── Crypto + RWA Lab
```

用户可以只安装 Life，以后单独安装 Research Labs，也可以把两者接到同一个 Hermes 基础层。即使组合安装，个人记忆和研究证据仍然属于两个独立的数据域。详见[产品区域与分装方式](docs/product-areas.md)。

### 研究方法

HIIS 关注的不是生成更多摘要，而是保留研究结论与原始证据之间的连接：

```text
收集来源
  -> 记录发布时间、观察时间、范围和权利信息
  -> 提取主张，但不自动判定为真
  -> 关联支持证据和冲突证据
  -> 写出不确定性与失效条件
  -> 在新证据出现后复盘
```

Digital Assets Lab 将这套方法用于 stablecoin 与 RWA 研究。例如，两条供应量记录只有在资产、链、时间范围和统计口径相容时才可以比较；产品文件没有说明的准入或转让限制应保持为未知，而不是由模型补全。

当前公共仓库提供方法说明和虚构数据案例。私有开发中已有更多实现工作，但尚未作为可安装的公共插件发布。详见 [HIIS](docs/hiis.md)、[Crypto + RWA Lab](docs/digital-assets-lab.md) 和[虚构证据案例](examples/digital-assets-evidence-demo.md)。

## 隐私与安全边界

请勿提交：

- `.env` 文件；
- API 密钥和模型服务 token；
- 微信、iLink 或其他账户标识；
- 个人记忆文件；
- 原始日志；
- 私人截图或文档；
- 包含个人细节的真实 `~/.hermes/config.yaml`。

请把本仓库当作模板和公共说明层，不要把真实助手运行环境直接复制进来。

## 文档入口

- [项目地图](docs/project-map.md)
- [产品区域与分装方式](docs/product-areas.md)
- [路线图](ROADMAP.md)
- [社区与反馈](COMMUNITY.md)
- [Codex Easy Setup](docs/easy-setup.md)
- [系统架构](docs/architecture.md)
- [HIIS 研究流程](docs/hiis.md)
- [Digital Assets Lab](docs/digital-assets-lab.md)
- [当前状态日志](docs/current-state-log.md)
- [模型服务策略](docs/provider-strategy.md)
- [隐私与安全](docs/safety-and-privacy.md)
- [维护流程](docs/maintenance-routine.md)

## 当前边界

- Hermes Life Easy Setup 是目前公开且可运行的主要入口；
- HIIS 与 Digital Assets Lab 的公共材料目前以设计说明和虚构案例为主；
- 本仓库不提供交易执行、钱包操作、实时投资建议或经过验证的投资业绩；
- 私有测试记录不能替代别人可以独立复现的公共发布；
- 路线图中的目标是计划，不代表已经完成或已有用户规模。

## 许可证与权利

本项目尚未授予开源许可证。在许可证和知识产权策略完成评审前，版权及相关权利归仓库所有者保留。重新分发或商业使用前，请先联系仓库所有者。
