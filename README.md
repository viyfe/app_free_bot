# 精品限免 App 后台管理与自动推送系统

## 功能
- 自动/手动抓取限免 App（少数派RSS为例）
- 筛选与入库，支持关键字过滤
- 前端展示与搜索
- Telegram 一键推送
- 支持 Docker 部署

## 使用方法

1. 修改 `config.yaml`，补全 Telegram 信息等。
2. 构建 Docker 镜像：
   ```bash
   docker build -t appfreebot .
   ```
3. 运行容器：
   ```bash
   docker run -d --name appfreebot -p 5000:5000 appfreebot
   ```
4. 访问 `http://localhost:5000` 即可管理与查看。

## FAQ

- 支持扩展抓取源和推送渠道，参考 `fetcher.py` `pusher.py`。
- 如果需要定时自动抓取，可用 Docker Compose + cron 或在 Flask 中集成 APScheduler。
