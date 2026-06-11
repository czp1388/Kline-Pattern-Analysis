#!/usr/bin/env python3
"""
综合监控报告
整合系统监控和交易监控，生成每日报告
"""

import json
import subprocess
from datetime import datetime
import os

class ComprehensiveMonitor:
    def __init__(self):
        self.report_dir = "/Users/xiaoling/.hermes/reports"
        os.makedirs(self.report_dir, exist_ok=True)
        
    def generate_daily_report(self):
        """生成每日报告"""
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        report_file = f"{self.report_dir}/daily_report_{date_str}.md"
        
        # 运行系统监控
        system_status = self.run_system_monitor()
        
        # 运行交易监控
        trading_status = self.run_trading_monitor()
        
        # 生成Markdown报告
        report = self.create_markdown_report(date_str, system_status, trading_status)
        
        # 保存报告
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✅ 每日报告已生成: {report_file}")
        return report_file
    
    def run_system_monitor(self):
        """运行系统监控"""
        try:
            result = subprocess.run(
                ["python3", "/Users/xiaoling/projects/kline-pattern-analysis-system/monitor.py"],
                capture_output=True,
                text=True
            )
            # 解析输出
            lines = result.stdout.split('\n')
            status = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    status[key.strip()] = value.strip()
            return status
        except Exception as e:
            return {"error": str(e)}
    
    def run_trading_monitor(self):
        """运行交易监控"""
        try:
            result = subprocess.run(
                ["python3", "/Users/xiaoling/projects/kline-pattern-analysis-system/trading_monitor.py"],
                capture_output=True,
                text=True
            )
            # 解析输出
            lines = result.stdout.split('\n')
            status = {}
            current_section = None
            
            for line in lines:
                if "===" in line:
                    current_section = line.strip("= ")
                elif ":" in line and current_section:
                    key, value = line.split(":", 1)
                    status[f"{current_section}_{key.strip()}"] = value.strip()
            
            return status
        except Exception as e:
            return {"error": str(e)}
    
    def create_markdown_report(self, date_str, system_status, trading_status):
        """创建Markdown格式报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# 🏛️ 灵墨指挥中心 - 每日监控报告
**报告日期:** {date_str}  
**生成时间:** {timestamp}  
**生成者:** 小墨 (Hermes系统CEO)

---

## 📊 系统状态概览

### 🔧 基础设施
"""
        
        # 系统状态
        if "Hermes Gateway" in system_status:
            report += f"- **Hermes Gateway:** {system_status['Hermes Gateway']}\n"
        if "OpenClaw Gateway" in system_status:
            report += f"- **OpenClaw Gateway:** {system_status['OpenClaw Gateway']}\n"
        if "Discord连接" in system_status:
            report += f"- **Discord连接:** {system_status['Discord连接']}\n"
        if "烛龙项目" in system_status:
            report += f"- **烛龙项目:** {system_status['烛龙项目']}\n"
        
        report += "\n### 💻 系统资源\n"
        if "CPU使用率" in system_status:
            report += f"- **CPU使用率:** {system_status['CPU使用率']}\n"
        if "内存使用率" in system_status:
            report += f"- **内存使用率:** {system_status['内存使用率']}\n"
        if "磁盘使用率" in system_status:
            report += f"- **磁盘使用率:** {system_status['磁盘使用率']}\n"
        
        report += "\n---\n\n## 💰 交易状态\n\n### 📈 持仓情况\n"
        
        # 交易状态
        if "交易监控报告_A股总资产" in trading_status:
            report += f"- **A股总资产:** {trading_status['交易监控报告_A股总资产']}\n"
        if "交易监控报告_外汇余额" in trading_status:
            report += f"- **外汇余额:** {trading_status['交易监控报告_外汇余额']}\n"
        
        report += "\n### 🎯 交易机会\n"
        # 这里可以添加具体的交易机会
        
        report += "\n### ⚠️ 风险指标\n"
        if "交易监控报告_总资金" in trading_status:
            report += f"- **总资金:** {trading_status['交易监控报告_总资金']}\n"
        if "交易监控报告_总风险敞口" in trading_status:
            report += f"- **总风险敞口:** {trading_status['交易监控报告_总风险敞口']}\n"
        if "交易监控报告_持仓数量" in trading_status:
            report += f"- **持仓数量:** {trading_status['交易监控报告_持仓数量']}\n"
        
        report += "\n---\n\n## 🚨 告警状态\n"
        
        # 检查告警条件
        alerts = []
        
        # CPU告警
        if "CPU使用率" in system_status:
            cpu_str = system_status['CPU使用率'].replace('%', '').strip()
            try:
                cpu = float(cpu_str)
                if cpu > 80:
                    alerts.append(f"⚠️ CPU使用率过高: {cpu}%")
            except:
                pass
        
        # 内存告警
        if "内存使用率" in system_status:
            mem_str = system_status['内存使用率'].replace('%', '').strip()
            try:
                mem = float(mem_str)
                if mem > 85:
                    alerts.append(f"⚠️ 内存使用率过高: {mem}%")
            except:
                pass
        
        if alerts:
            for alert in alerts:
                report += f"- {alert}\n"
        else:
            report += "- ✅ 无告警\n"
        
        report += "\n---\n\n## 📋 今日任务\n"
        report += "- [ ] 检查Discord Token有效性\n"
        report += "- [ ] 完善烛龙项目开发环境\n"
        report += "- [ ] 测试交易监控系统\n"
        report += "- [ ] 准备早报内容\n"
        
        report += "\n---\n\n## 📈 性能趋势\n"
        report += "*注: 历史数据统计功能开发中*\n"
        
        report += "\n---\n\n**报告结束**\n\n*生成于灵墨指挥中心监控系统*"
        
        return report

def main():
    monitor = ComprehensiveMonitor()
    report_file = monitor.generate_daily_report()
    
    # 输出报告路径
    print(f"\n📄 报告文件: {report_file}")
    
    # 预览报告前20行
    with open(report_file, 'r') as f:
        lines = f.readlines()[:20]
        print("\n📋 报告预览:")
        for line in lines:
            print(line.rstrip())

if __name__ == "__main__":
    main()