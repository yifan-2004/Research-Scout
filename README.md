# Research Scout

**带网页界面的自主研究 Agent，用于视觉论文调研与产品竞品分析。**

A focused research workspace built on [GPT Researcher](https://github.com/assafelovic/gpt-researcher). This edition adds Chinese onboarding, ready-to-fill research workflows, and an evidence review checklist.

> 本项目基于 GPT Researcher 二次整理，保留上游源码快照、来源提交记录与许可证。Research Scout 是本仓库的展示名称；研究引擎、内部包名和大部分界面来自上游。本次新增的是工作流模板、入口文案与验证资料。

## 能做什么

- 在网页输入课题，Agent 拆解问题、检索资料并汇总带引用的报告。
- 使用轻量网页界面，或选择仓库已有的 Next.js 界面。
- 根据配置研究网页、本地文档或混合资料，导出报告。
- 首页选择「视觉论文调研」或「产品竞品尽调」模板，填写范围后再启动。

```mermaid
flowchart LR
    A[填写研究范围] --> B[规划子问题]
    B --> C[检索与采集]
    C --> D[来源汇总与报告]
    D --> E[人工核对证据]
```

自主研究引擎与报告导出由上游实现；模板不保证报告结论正确。

## 本机启动

需要 **Python 3.12+**。下载 ZIP 并解压，或克隆本仓库后进入 `Research-Scout` 目录。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Windows 激活命令为 `.venv\Scripts\activate`，复制文件可用 `copy .env.example .env`。

在 `.env` 填写你自己的 `OPENAI_API_KEY` 与 `TAVILY_API_KEY`，然后启动：

```sh
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

打开 [http://127.0.0.1:8000](http://127.0.0.1:8000)。这是上游 FastAPI 提供的真实轻量界面，无需运行前端构建。研究前先填写模板里的 `{{变量}}`，点击 Start Researching 才会发起研究任务。

**这不是免配置的免费应用。** 默认使用模型和搜索服务，研究任务会调用外部接口，可能产生费用；以所选服务的实际账单为准。本次没有安装依赖、填写密钥或运行付费研究，也没有下载模型权重。服务端可能向模型提供商发送问题与资料片段，使用本地文档时同样需要核对所选模型的数据处理方式。

如需其他模型，按 [上游模型配置说明](docs/docs/gpt-researcher/gptr/config.md) 设置 `FAST_LLM`、`SMART_LLM`、`STRATEGIC_LLM`；兼容服务可配置 `OPENAI_BASE_URL`。这里不承诺所有提供商都经过验证。

可选 Docker 部署沿用 [docker-compose.yml](docker-compose.yml)，参考 [上游 Docker 指南](docs/docs/gpt-researcher/getting-started/getting-started-with-docker.md)。默认同时启动 8000 后端与 3000 Next.js 界面；本版本没有实测容器构建。

## 两个可直接填写的工作流

| 工作流 | 具体产物 |
|---|---|
| [视觉论文调研](scout/vision-literature.md) | 方法对比、数据划分、指标定义、代码/权重许可、可复现性缺口 |
| [产品竞品尽调](scout/competitor-diligence.md) | 用户问题、同类产品、可核对的能力/价格、待验证假设与最小访谈方案 |

模板机器可读版本为 [scout-workflows.json](frontend/scout-workflows.json)。首页模板选择器只填入研究问题，不会自动调用模型。报告完成后使用 [证据核对清单](scout/evidence-review.md) 逐项检查。

### 可探索的产品方向

以下是产品构想，**不是已验证的市场机会或已经实现的功能**：

- **视觉课题雷达**：为小型研究团队定期整理低照度增强或单目 3D 检测论文，输出可复现性检查表。
- **实验室采购情报**：比较公开算力平台的配置、计费规则与文档差异，帮助团队准备采购问题。
- **专业领域竞品助手**：为特定行业整理公开产品更新、目标用户与证据链接，供人工访谈前使用。

## 验证与维护

```sh
python3 scout/verify.py
python3 scout/audit_snapshot.py
```

这个离线检查核对模板变量、报告类型、网页入口和上游快照。本次只验证新增模板、静态界面接线、配置结构与许可证保留；**尚未端到端运行上游研究引擎**。未生成示例报告，仓库中上游展示与评测不代表本仓库作者亲自复测。

继承的 6 个 GitHub Actions 工作流已改为仅手动触发，避免上传时自动执行上游部署、容器构建或大规模测试。新的 `Scout content checks` 仅做无依赖离线内容检查，不调用模型或云服务。

## 来源与许可

- 上游：[assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)
- 基础提交：[`0957c301ed06c2a5857b834358c7227c739041d4`](https://github.com/assafelovic/gpt-researcher/commit/0957c301ed06c2a5857b834358c7227c739041d4)
- [原始 README 快照](docs/UPSTREAM_README.md) · [上游贡献指南](CONTRIBUTING.md) · [许可证](LICENSE)

本仓库公开的是来源提交对应的当前源码快照与本次修改。上游旧提交含被 GitHub 检出的历史凭据，完整历史未重新发布；旧历史仅保存在本机隔离备份中，没有绕过推送保护。当前快照中的一条过期签名 URL 已移除凭据与签名字段；这只是资料清理，不代表重新评测该数据集。

保留上游 `LICENSE`（Apache-2.0）及版权信息。上游 `pyproject.toml` 的许可字段写为 MIT，与 LICENSE 文件存在差异；这里保留原文件并明确记录，未自行更改上游授权。新增模板与界面接线按仓库 LICENSE 提供。`Research Scout` 名称不表示得到上游或任何公司的官方背书。
