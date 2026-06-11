#!/bin/bash
# 烛龙项目监控启动脚本

echo "启动烛龙项目监控系统..."
cd /Users/xiaoling/projects/kline-pattern-analysis-system

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装"
    exit 1
fi

# 安装依赖
echo "安装依赖..."
pip3 install psutil

# 创建监控目录
mkdir -p /Users/xiaoling/.hermes/monitor

# 启动监控
echo "启动监控脚本..."
python3 monitor.py

# 创建cron任务（可选）
echo "创建监控cron任务..."
(crontab -l 2>/dev/null; echo "*/30 * * * * cd /Users/xiaoling/projects/kline-pattern-analysis-system && python3 monitor.py >> /Users/xiaoling/.hermes/monitor/cron.log 2>&1") | crontab -

echo "✅ 监控系统启动完成"
echo "监控日志: /Users/xiaoling/.hermes/monitor.log"
echo "状态文件: /Users/xiaoling/.hermes/system_status.json"