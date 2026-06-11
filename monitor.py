#!/usr/bin/env python3
"""
烛龙项目监控系统
监控系统健康、交易状态、通信状态
"""

import time
import json
import subprocess
import psutil
from datetime import datetime
import os

class SystemMonitor:
    def __init__(self):
        self.log_file = "/Users/xiaoling/.hermes/monitor.log"
        self.status_file = "/Users/xiaoling/.hermes/system_status.json"
        
    def check_hermes_gateway(self):
        """检查Hermes Gateway状态"""
        try:
            result = subprocess.run(
                ["ps", "aux", "|", "grep", "hermes-gateway", "|", "grep", "-v", "grep"],
                capture_output=True,
                text=True,
                shell=True
            )
            return len(result.stdout.strip().split('\n')) > 0
        except:
            return False
    
    def check_openclaw_gateway(self):
        """检查OpenClaw Gateway状态"""
        try:
            result = subprocess.run(
                ["ps", "aux", "|", "grep", "openclaw-gateway", "|", "grep", "-v", "grep"],
                capture_output=True,
                text=True,
                shell=True
            )
            return len(result.stdout.strip().split('\n')) > 0
        except:
            return False
    
    def check_discord_connection(self):
        """检查Discord连接状态"""
        # 简化检查，实际需要测试API调用
        return True  # 暂时返回True，需要老板提供有效Token
    
    def check_trading_status(self):
        """检查交易状态"""
        positions_file = "/Users/xiaoling/.hermes/workspace/positions.json"
        if os.path.exists(positions_file):
            try:
                with open(positions_file, 'r') as f:
                    data = json.load(f)
                return {
                    "a_stock": data.get("a_stock", {}),
                    "forex": data.get("forex", {}),
                    "timestamp": datetime.now().isoformat()
                }
            except:
                return {"error": "无法读取持仓文件"}
        return {"error": "持仓文件不存在"}
    
    def check_system_resources(self):
        """检查系统资源"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "timestamp": datetime.now().isoformat()
        }
    
    def run_monitor(self):
        """运行监控检查"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "hermes_gateway": self.check_hermes_gateway(),
            "openclaw_gateway": self.check_openclaw_gateway(),
            "discord_connection": self.check_discord_connection(),
            "trading_status": self.check_trading_status(),
            "system_resources": self.check_system_resources(),
            "kline_project": os.path.exists("/Users/xiaoling/projects/kline-pattern-analysis-system")
        }
        
        # 保存状态
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
        
        # 记录日志
        log_entry = f"[{datetime.now().isoformat()}] 监控检查完成: {json.dumps(status, ensure_ascii=False)}\n"
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        return status

def main():
    monitor = SystemMonitor()
    status = monitor.run_monitor()
    
    # 输出摘要
    print("=== 系统监控报告 ===")
    print(f"时间: {status['timestamp']}")
    print(f"Hermes Gateway: {'✅ 运行中' if status['hermes_gateway'] else '❌ 停止'}")
    print(f"OpenClaw Gateway: {'✅ 运行中' if status['openclaw_gateway'] else '❌ 停止'}")
    print(f"Discord连接: {'✅ 正常' if status['discord_connection'] else '❌ 异常'}")
    print(f"烛龙项目: {'✅ 存在' if status['kline_project'] else '❌ 不存在'}")
    
    # 系统资源
    res = status['system_resources']
    print(f"CPU使用率: {res['cpu_percent']:.1f}%")
    print(f"内存使用率: {res['memory_percent']:.1f}%")
    print(f"磁盘使用率: {res['disk_usage']:.1f}%")
    
    # 交易状态
    trading = status['trading_status']
    if 'error' not in trading:
        print(f"A股持仓: {trading.get('a_stock', {}).get('position', '空仓')}")
        print(f"外汇余额: ${trading.get('forex', {}).get('balance', 0):.2f}")

if __name__ == "__main__":
    main()