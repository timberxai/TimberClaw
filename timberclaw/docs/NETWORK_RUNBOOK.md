# TimberClaw 网络连通性 Runbook（依赖安装 / 校验链路）

> 目标：在代理或内网环境下，快速定位 `make install-python-dependencies` / Playwright 下载失败根因，避免反复卡在同一问题。

## 1. 现象分层

### A. 检验链路失败
- 命令：`make install-pre-commit-hooks`
- 预期：应成功，不依赖完整依赖下载（轻量模式）

### B. 依赖下载失败
- 命令：`make install-python-dependencies`
- 常见报错：
  - `All attempts to connect to pypi.org failed`
  - `403 Forbidden`（代理拦截）
  - Playwright browser 下载失败

## 2. 快速诊断顺序（必须按顺序）

1. **确认镜像变量**
   - `echo $PYPI_MIRROR_URL`
   - 默认链路（按优先顺序）：  
     `PYPI_MIRROR_URL`（清华） → `PYPI_FALLBACK_MIRROR_URL`（阿里） → `PYPI_FINAL_FALLBACK_URL`（官方）

2. **检查镜像连通**
   - `curl -I -L --max-time 8 https://pypi.tuna.tsinghua.edu.cn/simple`

3. **检查代理变量**
   - `env | rg -i 'proxy|PROXY'`

4. **检查 Playwright 下载域是否可达**
   - `curl -I -L --max-time 8 https://cdn.playwright.dev`

5. **最后再跑依赖安装**
   - `make install-python-dependencies`
   - 查看最终命中的镜像：`cat cache/selected_pypi_mirror.txt`

> 如果运行在 Codex 云环境且探测被代理统一拦截，可临时使用：  
> `SKIP_PYPI_CONNECTIVITY_CHECK=1 make install-python-dependencies`

## 3. 企业网络侧需放通域名（最小集合）

### Python 依赖
- `pypi.tuna.tsinghua.edu.cn`（默认镜像）
- `pypi.org`（如不走镜像时）
- `files.pythonhosted.org`

### Playwright 浏览器
- `cdn.playwright.dev`
- `playwright.download.prss.microsoft.com`

### pre-commit hooks
- `github.com`

## 4. CI / Agent 环境建议

1. 校验阶段与依赖下载阶段分离
   - 先跑：`make install-pre-commit-hooks`
   - 再跑：`make install-python-dependencies`
2. 在 CI 中显式注入 `PYPI_MIRROR_URL`
3. 若长期内网，建议引入私有仓库代理（Nexus / Artifactory / devpi）

## 5. 失败后的标准结论模板

- 失败层级：检验链路 / 依赖链路 / 浏览器下载链路
- 是否命中代理 403
- 当前 `PYPI_MIRROR_URL`
- 需要网络团队放通的域名
- 是否可通过私有仓库代理规避
