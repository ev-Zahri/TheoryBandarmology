import React, { useState } from 'react';

function AnomalyAlerts({ anomalyAnalysis }) {
    const [isExpanded, setIsExpanded] = useState(false);

    if (!anomalyAnalysis || anomalyAnalysis.total_anomalies === 0) {
        return null;
    }

    const { severity_breakdown, stock_anomalies, portfolio_risks, recommendations } = anomalyAnalysis;
    const hasHighSeverity = severity_breakdown.high > 0;

    const getSeverityColor = (severity) => {
        const colors = {
            'HIGH': 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 border-red-300 dark:border-red-800',
            'MEDIUM': 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400 border-orange-300 dark:border-orange-800',
            'LOW': 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400 border-yellow-300 dark:border-yellow-800'
        };
        return colors[severity] || colors['LOW'];
    };

    const getIconForType = (type) => {
        const icons = {
            'UNUSUAL_WEIGHT': 'scale',
            'AVERAGING_DOWN': 'trending_down',
            'UNREALIZED_PROFIT': 'attach_money',
            'OVER_CONCENTRATION': 'warning',
            'WEAK_CONVICTION_LOSS': 'sentiment_dissatisfied',
            'TRAPPED_CAPITAL': 'lock',
            'PROFIT_REVERSAL_RISK': 'swap_vert',
            'SECTOR_CONCENTRATION': 'pie_chart',
            'WIDESPREAD_LOSSES': 'crisis_alert',
            'TOP_HEAVY_PORTFOLIO': 'vertical_align_top',
            'PROFIT_CONCENTRATION': 'filter_list'
        };
        return icons[type] || 'info';
    };

    return (
        <div className={`rounded-xl border p-4 ${hasHighSeverity ? 'bg-red-50 dark:bg-red-900/10 border-red-300 dark:border-red-800' : 'bg-orange-50 dark:bg-orange-900/10 border-orange-300 dark:border-orange-800'}`}>
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
                <div className="flex items-start gap-3">
                    <span className={`material-symbols-outlined text-[28px] ${hasHighSeverity ? 'text-red-600 dark:text-red-400' : 'text-orange-600 dark:text-orange-400'}`}>
                        {hasHighSeverity ? 'error' : 'warning'}
                    </span>
                    <div>
                        <h3 className={`font-bold ${hasHighSeverity ? 'text-red-900 dark:text-red-300' : 'text-orange-900 dark:text-orange-300'}`}>
                            {hasHighSeverity ? '⚠️ Critical Anomalies Detected' : '⚡ Anomalies Detected'}
                        </h3>
                        <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                            {anomalyAnalysis.total_anomalies} issue{anomalyAnalysis.total_anomalies > 1 ? 's' : ''} found
                            {severity_breakdown.high > 0 && ` (${severity_breakdown.high} high severity)`}
                        </p>
                    </div>
                </div>
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                >
                    <span className="material-symbols-outlined">
                        {isExpanded ? 'expand_less' : 'expand_more'}
                    </span>
                </button>
            </div>

            {/* Severity Summary */}
            <div className="flex gap-3 mb-3">
                {severity_breakdown.high > 0 && (
                    <div className="flex items-center gap-1 text-xs">
                        <span className="w-2 h-2 rounded-full bg-red-500"></span>
                        <span className="text-slate-600 dark:text-slate-400">{severity_breakdown.high} High</span>
                    </div>
                )}
                {severity_breakdown.medium > 0 && (
                    <div className="flex items-center gap-1 text-xs">
                        <span className="w-2 h-2 rounded-full bg-orange-500"></span>
                        <span className="text-slate-600 dark:text-slate-400">{severity_breakdown.medium} Medium</span>
                    </div>
                )}
                {severity_breakdown.low > 0 && (
                    <div className="flex items-center gap-1 text-xs">
                        <span className="w-2 h-2 rounded-full bg-yellow-500"></span>
                        <span className="text-slate-600 dark:text-slate-400">{severity_breakdown.low} Low</span>
                    </div>
                )}
            </div>

            {/* Recommendations */}
            {recommendations.length > 0 && (
                <div className="mb-3">
                    {recommendations.map((rec, idx) => (
                        <p key={idx} className="text-sm text-slate-700 dark:text-slate-300 mb-1">
                            {rec}
                        </p>
                    ))}
                </div>
            )}

            {/* Expanded Details */}
            {isExpanded && (
                <div className="mt-4 space-y-3">
                    {/* Stock Anomalies */}
                    {stock_anomalies.length > 0 && (
                        <div>
                            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-2">Stock-Level Issues:</h4>
                            <div className="space-y-2">
                                {stock_anomalies.map((anomaly, idx) => (
                                    <div key={idx} className={`p-3 rounded-lg border ${getSeverityColor(anomaly.severity)}`}>
                                        <div className="flex items-start gap-2">
                                            <span className="material-symbols-outlined text-[20px]">
                                                {getIconForType(anomaly.type)}
                                            </span>
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <span className="font-semibold">{anomaly.stock}</span>
                                                    <span className="text-xs px-2 py-0.5 rounded-full bg-white/50 dark:bg-black/20">
                                                        {anomaly.type.replace(/_/g, ' ')}
                                                    </span>
                                                </div>
                                                <p className="text-sm mb-1">{anomaly.description}</p>
                                                {anomaly.risk && (
                                                    <p className="text-xs italic mb-1">Risk: {anomaly.risk}</p>
                                                )}
                                                <p className="text-xs font-medium">💡 {anomaly.recommendation}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Portfolio Risks */}
                    {portfolio_risks.length > 0 && (
                        <div>
                            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-2">Portfolio-Level Risks:</h4>
                            <div className="space-y-2">
                                {portfolio_risks.map((risk, idx) => (
                                    <div key={idx} className={`p-3 rounded-lg border ${getSeverityColor(risk.severity)}`}>
                                        <div className="flex items-start gap-2">
                                            <span className="material-symbols-outlined text-[20px]">
                                                {getIconForType(risk.type)}
                                            </span>
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    <span className="font-semibold">{risk.type.replace(/_/g, ' ')}</span>
                                                </div>
                                                <p className="text-sm mb-1">{risk.description}</p>
                                                <p className="text-xs font-medium">💡 {risk.recommendation}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default AnomalyAlerts;
