"""
Anomaly Detector
Identifies unusual patterns and risks in broker positions
"""

from typing import Dict, List, Any
import numpy as np


def detect_statistical_anomalies(stocks_data: List[Dict], portfolio_stats: Dict) -> List[Dict]:
    """
    Detect statistical outliers using Z-score method
    
    Args:
        stocks_data: List of stock positions
        portfolio_stats: Portfolio-level statistics
        
    Returns:
        List of detected anomalies
    """
    anomalies = []
    
    if not stocks_data:
        return anomalies
    
    # Calculate statistics
    weights = [s.get('weight_pct', 0) for s in stocks_data]
    mean_weight = np.mean(weights)
    std_weight = np.std(weights) if len(weights) > 1 else 1.0
    
    for stock in stocks_data:
        stock_code = stock.get('stock', 'UNKNOWN')
        weight = stock.get('weight_pct', 0)
        
        # Avoid division by zero
        if std_weight == 0:
            continue
        
        # Calculate Z-score
        z_score = (weight - mean_weight) / std_weight
        
        # ANOMALY 1: Unusual Weight Allocation
        if abs(z_score) > 2.5:  # >2.5 standard deviations
            severity = "HIGH" if abs(z_score) > 3 else "MEDIUM"
            
            if z_score > 0:
                description = f"{weight:.1f}% allocation (portfolio avg: {mean_weight:.1f}%)"
                recommendation = "Monitor for concentration risk - consider rebalancing"
            else:
                description = f"Underweight at {weight:.1f}% (portfolio avg: {mean_weight:.1f}%)"
                recommendation = "Low conviction position - review thesis"
            
            anomalies.append({
                "stock": stock_code,
                "type": "UNUSUAL_WEIGHT",
                "severity": severity,
                "z_score": round(z_score, 2),
                "description": description,
                "recommendation": recommendation,
                "icon": "warning"
            })
    
    return anomalies


def detect_behavioral_anomalies(stock_data: Dict, portfolio_context: Dict) -> List[Dict]:
    """
    Detect contradictory or risky behavioral patterns
    
    Returns:
        List of behavioral anomalies
    """
    anomalies = []
    
    stock_code = stock_data.get('stock_code', 'UNKNOWN')
    weight = stock_data.get('weight_pct', 0) or 0
    diff_pct = stock_data.get('diff_pct', 0) or 0
    value_bn = stock_data.get('value_bn', 0) or 0
    
    # Get bandarmology data if available (with None check)
    bandarmology = stock_data.get('bandarmology') or {}
    accumulation = bandarmology.get('accumulation') or {}
    accumulation_score = accumulation.get('accumulation_score', 5.0) or 5.0
    
    # ANOMALY 1: Averaging Down on Weak Stock
    if diff_pct < -10 and weight > 10:
        severity = "HIGH" if diff_pct < -15 else "MEDIUM"
        anomalies.append({
            "stock": stock_code,
            "type": "AVERAGING_DOWN",
            "severity": severity,
            "description": f"Heavy position ({weight:.1f}%) with {diff_pct:.1f}% loss",
            "risk": "Throwing good money after bad - capital at risk",
            "recommendation": "Review investment thesis - is this conviction or stubbornness?",
            "icon": "error"
        })
    
    # ANOMALY 2: Unrealized Profit Not Taken
    if diff_pct > 20 and weight > 8:
        severity = "MEDIUM" if diff_pct < 30 else "HIGH"
        anomalies.append({
            "stock": stock_code,
            "type": "UNREALIZED_PROFIT",
            "severity": severity,
            "description": f"{diff_pct:.1f}% profit on {weight:.1f}% position (Rp {value_bn:.2f}B)",
            "risk": "Profit can evaporate quickly in market reversal",
            "recommendation": "Consider partial profit-taking to lock in gains",
            "icon": "info"
        })
    
    # ANOMALY 3: Over-Concentration Risk
    if weight > 25:
        severity = "HIGH"
        anomalies.append({
            "stock": stock_code,
            "type": "OVER_CONCENTRATION",
            "severity": severity,
            "description": f"Single stock = {weight:.1f}% of portfolio",
            "risk": "Excessive exposure to single name - portfolio at risk",
            "recommendation": "Diversify immediately or hedge position with options",
            "icon": "error"
        })
    
    # ANOMALY 4: Weak Conviction Loss
    if diff_pct < -5 and accumulation_score < 3 and weight < 5:
        anomalies.append({
            "stock": stock_code,
            "type": "WEAK_CONVICTION_LOSS",
            "severity": "MEDIUM",
            "description": f"Losing position ({diff_pct:.1f}%) with low conviction (score: {accumulation_score:.1f})",
            "risk": "No clear thesis for holding - dead money",
            "recommendation": "Consider exit if no catalyst - free up capital",
            "icon": "warning"
        })
    
    # ANOMALY 5: Deep Loss with High Weight
    if diff_pct < -15 and weight > 15:
        anomalies.append({
            "stock": stock_code,
            "type": "TRAPPED_CAPITAL",
            "severity": "HIGH",
            "description": f"Major position ({weight:.1f}%) with severe loss ({diff_pct:.1f}%)",
            "risk": "Large portion of capital trapped - opportunity cost",
            "recommendation": "Urgent review needed - consider cutting loss to preserve capital",
            "icon": "error"
        })
    
    # ANOMALY 6: Profit Reversal Risk
    if 5 < diff_pct < 15 and weight > 12:
        anomalies.append({
            "stock": stock_code,
            "type": "PROFIT_REVERSAL_RISK",
            "severity": "LOW",
            "description": f"Moderate profit ({diff_pct:.1f}%) on large position ({weight:.1f}%)",
            "risk": "Profit not yet secured - vulnerable to reversal",
            "recommendation": "Set trailing stop or take partial profits",
            "icon": "info"
        })
    
    return anomalies


def detect_portfolio_risks(stocks_data: List[Dict], portfolio_stats: Dict) -> List[Dict]:
    """
    Detect portfolio-level risk patterns
    
    Returns:
        List of portfolio risks
    """
    risks = []
    
    if not stocks_data:
        return risks
    
    total_stocks = len(stocks_data)
    total_value = sum(s.get('value_raw', 0) for s in stocks_data)
    
    # Risk 1: Sector Concentration
    # Group by sector if available
    sector_exposure = {}
    for stock in stocks_data:
        sector = stock.get('sector', 'Unknown')
        weight = stock.get('weight_pct', 0)
        sector_exposure[sector] = sector_exposure.get(sector, 0) + weight
    
    for sector, exposure in sector_exposure.items():
        if exposure > 40 and sector != 'Unknown':
            risks.append({
                "type": "SECTOR_CONCENTRATION",
                "severity": "HIGH" if exposure > 50 else "MEDIUM",
                "sector": sector,
                "exposure": round(exposure, 1),
                "description": f"{exposure:.1f}% concentrated in {sector} sector",
                "recommendation": "Diversify across sectors to reduce systematic risk",
                "icon": "warning"
            })
    
    # Risk 2: Widespread Losses
    losing_stocks = [s for s in stocks_data if s.get('diff_pct', 0) < -5]
    loss_ratio = len(losing_stocks) / total_stocks if total_stocks > 0 else 0
    
    if loss_ratio > 0.6:
        risks.append({
            "type": "WIDESPREAD_LOSSES",
            "severity": "HIGH",
            "affected_stocks": len(losing_stocks),
            "total_stocks": total_stocks,
            "description": f"{len(losing_stocks)}/{total_stocks} stocks in loss ({loss_ratio*100:.0f}%)",
            "recommendation": "Review market conditions - possible systematic risk or poor timing",
            "icon": "error"
        })
    
    # Risk 3: Trapped Capital
    trapped_stocks = [s for s in stocks_data if s.get('diff_pct', 0) < -15]
    trapped_value = sum(s.get('value_raw', 0) for s in trapped_stocks)
    trapped_pct = (trapped_value / total_value * 100) if total_value > 0 else 0
    
    if trapped_pct > 30:
        risks.append({
            "type": "TRAPPED_CAPITAL",
            "severity": "HIGH",
            "trapped_percentage": round(trapped_pct, 1),
            "trapped_value_bn": round(trapped_value / 1_000_000_000, 2),
            "description": f"{trapped_pct:.1f}% of capital in deep losses (>15%)",
            "recommendation": "Consider cutting losses to free capital for better opportunities",
            "icon": "error"
        })
    
    # Risk 4: Top-Heavy Portfolio
    if total_stocks >= 3:
        top_3_weight = sum(sorted([s.get('weight_pct', 0) for s in stocks_data], reverse=True)[:3])
        if top_3_weight > 60:
            risks.append({
                "type": "TOP_HEAVY_PORTFOLIO",
                "severity": "MEDIUM",
                "top_3_weight": round(top_3_weight, 1),
                "description": f"Top 3 stocks = {top_3_weight:.1f}% of portfolio",
                "recommendation": "Rebalance to reduce concentration in top holdings",
                "icon": "warning"
            })
    
    # Risk 5: Profit Concentration
    profitable_stocks = [s for s in stocks_data if s.get('diff_pct', 0) > 5]
    if profitable_stocks:
        profit_value = sum(s.get('value_raw', 0) for s in profitable_stocks)
        profit_pct = (profit_value / total_value * 100) if total_value > 0 else 0
        
        if profit_pct > 70 and len(profitable_stocks) < total_stocks * 0.3:
            risks.append({
                "type": "PROFIT_CONCENTRATION",
                "severity": "MEDIUM",
                "profitable_stocks": len(profitable_stocks),
                "profit_percentage": round(profit_pct, 1),
                "description": f"Only {len(profitable_stocks)} stocks carrying {profit_pct:.1f}% of portfolio",
                "recommendation": "Diversify profit sources - too dependent on few winners",
                "icon": "info"
            })
    
    return risks


def analyze_anomalies(stocks_data: List[Dict], portfolio_stats: Dict) -> Dict[str, Any]:
    """
    Complete anomaly analysis for portfolio
    
    Returns:
        Comprehensive anomaly report
    """
    all_anomalies = []
    
    # Statistical anomalies
    statistical = detect_statistical_anomalies(stocks_data, portfolio_stats)
    all_anomalies.extend(statistical)
    
    # Behavioral anomalies (per stock)
    for stock in stocks_data:
        behavioral = detect_behavioral_anomalies(stock, portfolio_stats)
        all_anomalies.extend(behavioral)
    
    # Portfolio-level risks
    portfolio_risks = detect_portfolio_risks(stocks_data, portfolio_stats)
    
    # Count by severity
    high_severity = len([a for a in all_anomalies if a.get('severity') == 'HIGH'])
    medium_severity = len([a for a in all_anomalies if a.get('severity') == 'MEDIUM'])
    low_severity = len([a for a in all_anomalies if a.get('severity') == 'LOW'])
    
    # Generate summary recommendations
    recommendations = []
    if high_severity > 0:
        recommendations.append("⚠️ URGENT: Address high-severity anomalies immediately")
    if portfolio_risks:
        recommendations.append("📊 Review portfolio-level risks for systematic issues")
    if medium_severity > 3:
        recommendations.append("⚡ Multiple medium-severity issues detected - review positions")
    
    return {
        "total_anomalies": len(all_anomalies),
        "severity_breakdown": {
            "high": high_severity,
            "medium": medium_severity,
            "low": low_severity
        },
        "stock_anomalies": all_anomalies,
        "portfolio_risks": portfolio_risks,
        "recommendations": recommendations
    }
