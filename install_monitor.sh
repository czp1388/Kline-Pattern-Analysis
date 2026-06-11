#!/bin/bash
# 烛龙项目完整监控系统安装脚本

echo "========================================"
echo "🏛️ 灵墨指挥中心监控系统安装"
echo "========================================"

# 1. 检查Python环境
echo "1. 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装，请先安装Python3"
    exit 1
fi
echo "✅ Python3已安装: $(python3 --version)"

# 2. 安装依赖
echo "2. 安装Python依赖..."
pip3 install psutil > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ psutil安装成功"
else
    echo "⚠️ psutil安装失败，尝试继续..."
fi

# 3. 创建监控目录
echo "3. 创建监控目录..."
mkdir -p /Users/xiaoling/.hermes/monitor
mkdir -p /Users/xiaoling/.hermes/reports
mkdir -p /Users/xiaoling/.hermes/workspace

echo "✅ 目录创建完成"

# 4. 设置文件权限
echo "4. 设置文件权限..."
chmod +x /Users/xiaoling/projects/kline-pattern-analysis-system/*.py
chmod +x /Users/xiaoling/projects/kline-pattern-analysis-system/*.sh

# 5. 创建cron任务
echo "5. 创建定时监控任务..."

# 删除现有相关cron任务
(crontab -l 2>/dev/null | grep -v "kline-pattern-analysis-system" | grep -v "monitor.py" | grep -v "daily_report.py") | crontab -

# 添加新cron任务
(
    crontab -l 2>/dev/null
    echo "# ===== 灵墨指挥中心监控系统 ===== #"
    echo "# 每30分钟运行系统监控"
    echo "*/30 * * * * cd /Users/xiaoling/projects/kline-pattern-analysis-system && python3 monitor.py >> /Users/xiaoling/.hermes/monitor/system_monitor.log 2>&1"
    echo ""
    echo "# 每小时运行交易监控"
    echo "0 * * * * cd /Users/xiaoling/projects/kline-pattern-analysis-system && python3 trading_monitor.py >> /Users/xiaoling/.hermes/monitor/trading_monitor.log 2>&1"
    echo ""
    echo "# 每天8:30生成每日报告（与早报时间一致）"
    echo "30 8 * * * cd /Users/xiaoling/projects/kline-pattern-analysis-system && python3 daily_report.py >> /Users/xiaoling/.hermes/monitor/daily_report.log 2>&1"
    echo ""
    echo "# 每天23:00清理旧日志（保留7天）"
    echo "0 23 * * * find /Users/xiaoling/.hermes/monitor -name \"*.log\" -mtime +7 -delete"
) | crontab -

echo "✅ Cron任务配置完成"

# 6. 立即运行一次监控
echo "6. 运行初始监控检查..."
cd /Users/xiaoling/projects/kline-pattern-analysis-system
python3 monitor.py
echo ""
python3 trading_monitor.py

# 7. 生成今日报告
echo "7. 生成今日监控报告..."
python3 daily_report.py

echo ""
echo "========================================"
echo "🎉 监控系统安装完成！"
echo "========================================"
echo ""
echo "📊 监控配置:"
echo "  - 系统监控: 每30分钟运行"
echo "  - 交易监控: 每小时运行"
echo "  - 每日报告: 每天8:30生成"
echo ""
echo "📁 重要目录:"
echo "  - 项目目录: /Users/xiaoling/projects/kline-pattern-analysis-system"
echo "  - 监控日志: /Users/xiaoling/.hermes/monitor/"
echo "  - 每日报告: /Users/xiaoling/.hermes/reports/"
echo ""
echo "🔧 管理命令:"
echo "  - 查看cron任务: crontab -l"
echo "  - 手动运行监控: python3 monitor.py"
echo "  - 手动生成报告: python3 daily_report.py"
echo ""
echo "⚠️ 待解决问题:"
echo "  - Discord Token需要更新"
echo "  - 需要测试实际交易监控"
echo "  - 需要完善烛龙项目开发"
echo ""
echo "🏛️ 灵墨指挥中心 - 监控系统已就绪"