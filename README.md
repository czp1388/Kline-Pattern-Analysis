# K线形态分析系统 (Kline-Pattern-Analysis)

A股K线形态识别与分析系统，支持多种形态模式的自动化检测和交易信号生成。

## 功能
- 多形态识别（早晨之星、黄昏之星、头肩顶、W底、M头、三只乌鸦等）
- 每日自动扫描A股市场
- 基于历史回测的形态有效性评估
- 交易信号生成与通知推送

## 文件结构
```
├── daily_report.py      # 每日形态报告
├── monitor.py           # 形态监控
├── trading_monitor.py   # 交易信号监控
├── install_monitor.sh   # 安装脚本
├── start_monitor.sh     # 启动脚本
├── src/                 # 核心算法
├── data/                # 数据存储
├── docs/                # 文档
├── tests/               # 测试
└── requirements.txt     # 依赖
```

## 用法
```bash
# 安装依赖
pip install -r requirements.txt

# 启动监控
bash start_monitor.sh

# 生成每日形态报告
python3 daily_report.py
```

## GitHub
https://github.com/czp1388/Kline-Pattern-Analysis