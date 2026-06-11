#!/usr/bin/env python3
"""
交易监控系统
监控持仓变化、市场机会、风险指标
"""

import json
import time
from datetime import datetime
import os

class TradingMonitor:
    def __init__(self):
        self.positions_file = "/Users/xiaoling/.hermes/workspace/positions.json"
        self.trade_history = "/Users/xiaoling/.hermes/workspace/trade_history.json"
        self.monitor_log = "/Users/xiaoling/.hermes/trading_monitor.log"
        
    def load_positions(self):
        """加载持仓数据"""
        if os.path.exists(self.positions_file):
            try:
                with open(self.positions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def load_trade_history(self):
        """加载交易历史"""
        if os.path.exists(self.trade_history):
            try:
                with open(self.trade_history, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def check_position_changes(self):
        """检查持仓变化"""
        positions = self.load_positions()
        
        # 这里可以添加持仓变化检测逻辑
        # 比如与上次检查对比
        
        return {
            "timestamp": datetime.now().isoformat(),
            "a_stock": positions.get("a_stock", {}),
            "forex": positions.get("forex", {}),
            "total_a_stock_balance": positions.get("a_stock", {}).get("balance", 0),
            "total_forex_balance": positions.get("forex", {}).get("balance", 0)
        }
    
    def check_trading_opportunities(self):
        """检查交易机会"""
        # 这里可以添加市场扫描逻辑
        # 暂时返回示例数据
        return {
            "timestamp": datetime.now().isoformat(),
            "opportunities": [
                {
                    "symbol": "BTCUSDT",
                    "type": "crypto",
                    "signal": "bullish",
                    "confidence": 0.75,
                    "reason": "4小时级别突破阻力位"
                },
                {
                    "symbol": "XAUUSD",
                    "type": "forex",
                    "signal": "neutral",
                    "confidence": 0.6,
                    "reason": "日线级别盘整，等待方向选择"
                }
            ]
        }
    
    def check_risk_metrics(self):
        """检查风险指标"""
        positions = self.load_positions()
        
        total_balance = 0
        total_risk = 0
        
        # 计算总资金和风险
        a_stock = positions.get("a_stock", {})
        forex = positions.get("forex", {})
        
        total_balance = a_stock.get("balance", 0) + forex.get("balance", 0) * 7.8  # 假设汇率
        
        # 简单风险计算（示例）
        total_risk = total_balance * 0.08  # 8%止损风险
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_balance": total_balance,
            "total_risk": total_risk,
            "risk_percentage": 8.0,  # 固定止损百分比
            "position_count": len(a_stock.get("positions", [])) + len(forex.get("positions", [])),
            "max_drawdown_allowed": total_balance * 0.02  # 2%最大回撤
        }
    
    def run_monitor(self):
        """运行交易监控"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "positions": self.check_position_changes(),
            "opportunities": self.check_trading_opportunities(),
            "risk_metrics": self.check_risk_metrics()
        }
        
        # 保存到日志
        log_entry = f"[{datetime.now().isoformat()}] 交易监控: {json.dumps(status, ensure_ascii=False)}\n"
        with open(self.monitor_log, 'a') as f:
            f.write(log_entry)
        
        return status

def main():
    monitor = TradingMonitor()
    status = monitor.run_monitor()
    
    # 输出摘要
    print("=== 交易监控报告 ===")
    print(f"时间: {status['timestamp']}")
    
    # 持仓信息
    pos = status['positions']
    print(f"\n📊 持仓状态:")
    print(f"  A股总资产: ¥{pos.get('total_a_stock_balance', 0):.2f}")
    print(f"  外汇余额: ${pos.get('total_forex_balance', 0):.2f}")
    
    # 交易机会
    opps = status['opportunities']['opportunities']
    print(f"\n🎯 交易机会 ({len(opps)}个):")
    for opp in opps:
        signal_emoji = "🟢" if opp['signal'] == 'bullish' else "🔴" if opp['signal'] == 'bearish' else "🟡"
        print(f"  {signal_emoji} {opp['symbol']}: {opp['reason']} (信心: {opp['confidence']*100:.0f}%)")
    
    # 风险指标
    risk = status['risk_metrics']
    print(f"\n⚠️ 风险指标:")
    print(f"  总资金: ¥{risk['total_balance']:.2f}")
    print(f"  总风险敞口: ¥{risk['total_risk']:.2f}")
    print(f"  持仓数量: {risk['position_count']}")
    print(f"  最大允许回撤: ¥{risk['max_drawdown_allowed']:.2f}")

if __name__ == "__main__":
    main()