"""
Bandarmology Analyzer
Advanced indicators for broker strategy analysis
"""

from typing import Dict, List, Any
import numpy as np


def calculate_accumulation_score(stock_data: Dict, portfolio_context: Dict) -> Dict[str, Any]:
    """
    Calculate accumulation/distribution score (0-10)
    
    Args:
        stock_data: Individual stock data
        portfolio_context: Portfolio-level statistics for comparison
        
    Returns:
        Accumulation score with breakdown
    """
    score = 0.0
    breakdown = {}
    
    # Extract data - use correct field names from broker_summary
    # Add None checks to prevent TypeError
    avg_price = stock_data.get('avg_price', 0) or 0
    current_price = stock_data.get('current_price', 0) or 0
    weight = stock_data.get('weight_pct', 0) or 0
    diff_pct = stock_data.get('diff_pct', 0) or 0
    
    # Factor 1: Price Position (30% weight)
    price_score = 0.0
    if diff_pct > 10:
        price_score = 3.0  # Strong profit = early accumulation
    elif diff_pct > 5:
        price_score = 2.5
    elif diff_pct > 0:
        price_score = 2.0
    elif diff_pct > -5:
        price_score = 1.0  # Near breakeven = holding
    else:
        price_score = 0.5  # Deep loss = trapped/averaging
    
    breakdown['price_position'] = price_score
    score += price_score
    
    # Factor 2: Weight Allocation (30% weight)
    weight_score = 0.0
    if weight > 15:
        weight_score = 3.0  # Very high conviction
    elif weight > 10:
        weight_score = 2.5
    elif weight > 5:
        weight_score = 2.0
    elif weight > 2:
        weight_score = 1.0
    else:
        weight_score = 0.5  # Low conviction
    
    breakdown['weight_allocation'] = weight_score
    score += weight_score
    
    # Factor 3: Relative Position (20% weight)
    # Compare with portfolio average
    avg_weight = portfolio_context.get('avg_weight', 5.0)
    relative_score = 0.0
    if weight > avg_weight * 2:
        relative_score = 2.0  # Much higher than average
    elif weight > avg_weight * 1.5:
        relative_score = 1.5
    elif weight > avg_weight:
        relative_score = 1.0
    else:
        relative_score = 0.5
    
    breakdown['relative_position'] = relative_score
    score += relative_score
    
    # Factor 4: Profit Momentum (20% weight)
    momentum_score = 0.0
    if diff_pct > 15:
        momentum_score = 2.0  # Strong momentum
    elif diff_pct > 10:
        momentum_score = 1.5
    elif diff_pct > 5:
        momentum_score = 1.0
    elif diff_pct > 0:
        momentum_score = 0.5
    else:
        momentum_score = 0.0  # No momentum
    
    breakdown['profit_momentum'] = momentum_score
    score += momentum_score
    
    # Determine interpretation
    if score >= 8.0:
        interpretation = "STRONG_ACCUMULATION"
        confidence = "HIGH"
    elif score >= 6.0:
        interpretation = "MODERATE_ACCUMULATION"
        confidence = "MEDIUM"
    elif score >= 4.0:
        interpretation = "WEAK_ACCUMULATION"
        confidence = "LOW"
    elif score >= 2.0:
        interpretation = "NEUTRAL"
        confidence = "LOW"
    else:
        interpretation = "DISTRIBUTION"
        confidence = "MEDIUM"
    
    return {
        "accumulation_score": round(score, 1),
        "score_breakdown": breakdown,
        "interpretation": interpretation,
        "confidence": confidence
    }


def classify_broker_behavior(stock_data: Dict) -> Dict[str, Any]:
    """
    Classify broker's trading strategy based on position characteristics
    
    Returns:
        Strategy classification with details
    """
    avg_price = stock_data.get('avg_price', 0) or 0
    current_price = stock_data.get('current_price', 0) or 0
    weight = stock_data.get('weight_pct', 0) or 0
    diff_pct = stock_data.get('diff_pct', 0) or 0
    
    # ACCUMULATION Pattern
    if (diff_pct > 0 and weight > 5) or (diff_pct > 5 and weight > 2):
        return {
            "strategy": "ACCUMULATION",
            "conviction": "HIGH" if weight > 10 else "MEDIUM",
            "phase": "EARLY" if diff_pct < 10 else "LATE",
            "description": "Building position with profit",
            "color": "green"
        }
    
    # TRAPPED Pattern
    if diff_pct < -10 and weight > 5:
        return {
            "strategy": "TRAPPED",
            "conviction": "FORCED_HOLD",
            "phase": "AVERAGING_DOWN" if weight > 15 else "STUCK",
            "description": "Deep loss, likely averaging down or stuck",
            "color": "red"
        }
    
    # DISTRIBUTION Pattern
    if diff_pct > 15 and weight < 5:
        return {
            "strategy": "DISTRIBUTION",
            "conviction": "LOW",
            "phase": "TAKING_PROFIT",
            "description": "Reducing position after profit",
            "color": "orange"
        }
    
    # MOMENTUM Pattern
    if diff_pct > 10 and weight > 8:
        return {
            "strategy": "MOMENTUM",
            "conviction": "HIGH",
            "phase": "RIDING_TREND",
            "description": "Strong conviction on trending stock",
            "color": "blue"
        }
    
    # SWING_TRADING Pattern
    if abs(diff_pct) < 5 and weight < 5:
        return {
            "strategy": "SWING_TRADING",
            "conviction": "LOW",
            "phase": "ACTIVE",
            "description": "Quick trading, low commitment",
            "color": "gray"
        }
    
    # DEFAULT - NEUTRAL
    return {
        "strategy": "NEUTRAL",
        "conviction": "MEDIUM",
        "phase": "MONITORING",
        "description": "No clear pattern",
        "color": "gray"
    }


def analyze_position_strength(stock_data: Dict) -> Dict[str, Any]:
    """
    Analyze overall position strength and estimate targets
    
    Returns:
        Position strength metrics
    """
    avg_price = stock_data.get('avg_price', 0) or 0
    current_price = stock_data.get('current_price', 0) or 0
    weight = stock_data.get('weight_pct', 0) or 0
    diff_pct = stock_data.get('diff_pct', 0) or 0
    
    # Overall score (0-10)
    overall_score = 0.0
    
    # Factor 1: Profit cushion
    if diff_pct > 15:
        overall_score += 3.0
    elif diff_pct > 10:
        overall_score += 2.5
    elif diff_pct > 5:
        overall_score += 2.0
    elif diff_pct > 0:
        overall_score += 1.0
    
    # Factor 2: Conviction
    if weight > 15:
        overall_score += 3.0
    elif weight > 10:
        overall_score += 2.5
    elif weight > 5:
        overall_score += 2.0
    elif weight > 2:
        overall_score += 1.0
    
    # Factor 3: Risk level (inverse of loss)
    if diff_pct >= 0:
        overall_score += 2.0
    elif diff_pct > -5:
        overall_score += 1.5
    elif diff_pct > -10:
        overall_score += 1.0
    else:
        overall_score += 0.5
    
    # Factor 4: Holding power
    if diff_pct > 0 and weight > 5:
        overall_score += 2.0
    elif diff_pct > -5:
        overall_score += 1.0
    
    # Determine levels
    if overall_score >= 8:
        conviction_level = "VERY_HIGH"
        risk_level = "LOW"
        holding_power = "VERY_STRONG"
        exit_pressure = "VERY_LOW"
    elif overall_score >= 6:
        conviction_level = "HIGH"
        risk_level = "MEDIUM"
        holding_power = "STRONG"
        exit_pressure = "LOW"
    elif overall_score >= 4:
        conviction_level = "MEDIUM"
        risk_level = "MEDIUM"
        holding_power = "MODERATE"
        exit_pressure = "MEDIUM"
    else:
        conviction_level = "LOW"
        risk_level = "HIGH"
        holding_power = "WEAK"
        exit_pressure = "HIGH"
    
    # Estimate targets
    volatility = 10.0  # Default volatility estimate (can be enhanced later)
    
    if current_price > avg_price:
        # Already in profit
        estimated_target = int(current_price * (1 + (volatility * 1.5 / 100)))
        estimated_stop = int(avg_price * 0.98)
    else:
        # In loss
        estimated_target = int(avg_price * 1.05)
        estimated_stop = int(avg_price * (1 - min(0.15, volatility * 2 / 100)))
    
    # Risk-reward ratio
    if current_price > estimated_stop:
        risk_reward = round((estimated_target - current_price) / (current_price - estimated_stop), 2)
    else:
        risk_reward = 0.0
    
    return {
        "overall_score": round(overall_score, 1),
        "conviction_level": conviction_level,
        "profit_cushion": round(diff_pct, 2),
        "risk_level": risk_level,
        "holding_power": holding_power,
        "exit_pressure": exit_pressure,
        "estimated_target": estimated_target,
        "estimated_stop": estimated_stop,
        "risk_reward_ratio": risk_reward
    }


def analyze_stock_bandarmology(stock_data: Dict, portfolio_context: Dict) -> Dict[str, Any]:
    """
    Complete bandarmology analysis for a single stock
    
    Returns:
        Comprehensive bandarmology metrics
    """
    return {
        "accumulation": calculate_accumulation_score(stock_data, portfolio_context),
        "behavior": classify_broker_behavior(stock_data),
        "position_strength": analyze_position_strength(stock_data)
    }
