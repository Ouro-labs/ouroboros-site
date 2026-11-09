# 旧中文指南的时效措辞检查

2026-11-07：检查 `site/learn/zh/` 下 13 个 HTML 页。未找到统一的确认日期或 commit，不能把历史页面的源码对照描述视为现行产品验证。保留每页链接、ID/name 锚点和原有章节内容，将无时间依据的“当前源码/README/仓库已核对”改为编写时曾对照、确认日期与 commit 未记录；将当时其他语言页面的差异、运行时指南数量和章节覆盖表述为历史观察，避免声称现状或各语言完全齐平。首页中文 README 入口的“13 个运行时”说明也改为不限定数量的产品、安装与接入介绍。未指定旧中文指南的确切版本，也未复验所有旧页的技术事实。

变更位置：`index.html` 及 `architecture`, `evaluate`, `evolve`, `execute`, `existing-project`, `glossary`, `install`, `interview`, `seed`, `troubleshooting`, `what-is-ouroboros`, `why-ouroboros` 各目录的 `index.html`。每页顶部已另加未统一标注版本的提示和中文草稿入口。仍保留的“当前阶段/版本”“最新一代”等用于指用户实际状态或示例变量，不是旧文档经最新源码验证的声明；旧操作步骤是否适用于安装版本仍需独立事实审查。

复查命令（站点仓库根目录）：

```sh
rg -n '当前源码|当前的 README|当前仓库|目前没有|目前没写|目前都没写|目前有|目前在|现在三个' site/learn/zh --glob '*.html'
python3 /path/to/ouroboros-docs/integration/site/audit-existing-urls.py --base-repository . --candidate .
```

预期第一条无匹配（`rg` 返回 1），第二条不应报告新增 URL/锚点/canonical/hreflang/sitemap 回归。构建及浏览器可见性、旧指令的完整版本事实和使用安全另行验证。
