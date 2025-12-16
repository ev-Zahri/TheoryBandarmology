import React from 'react';

const DonutChart = ({ winPercent = 64, lossPercent = 36, winTrades = 0, lossTrades = 0 }) => {
    const getLabel = (percent) => {
        if (percent >= 60) return 'Strong';
        if (percent >= 50) return 'Good';
        if (percent >= 40) return 'Moderate';
        return 'Weak';
    };

    const labelClass = winPercent >= 50 ? 'text-success bg-success/10' : 'text-danger bg-danger/10';

    return (
        <div className="rounded-xl bg-surface-dark border border-border-dark p-6 h-full flex flex-col relative shadow-xl shadow-black/20">
            <div className="mb-6">
                <h2 className="text-white text-lg font-semibold mb-1">Portfolio Ratio</h2>
                <p className="text-text-muted text-sm">Win/Loss distribution analysis</p>
            </div>

            {/* Donut Chart Container */}
            <div className="flex-1 flex items-center justify-center py-6 relative">
                {/* SVG Donut Chart */}
                <div className="relative w-64 h-64">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                        {/* Background Circle */}
                        <path
                            className="text-background-dark"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="3"
                        />
                        {/* Loss Segment (Red) */}
                        <path
                            className="text-danger"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="currentColor"
                            strokeDasharray={`${lossPercent}, 100`}
                            strokeLinecap="round"
                            strokeWidth="3"
                        />
                        {/* Win Segment (Green) - Offset by loss percent */}
                        <path
                            className="text-success drop-shadow-[0_0_8px_rgba(34,197,94,0.5)]"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="currentColor"
                            strokeDasharray={`${winPercent}, 100`}
                            strokeDashoffset={`-${lossPercent}`}
                            strokeLinecap="round"
                            strokeWidth="3.5"
                        />
                    </svg>
                    {/* Center Text */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-text-muted text-sm font-medium">Win Rate</span>
                        <span className="text-white text-4xl font-mono font-bold tracking-tighter">{winPercent}%</span>
                        <span className={`${labelClass} text-xs font-medium px-2 py-0.5 rounded-full mt-1`}>
                            {getLabel(winPercent)}
                        </span>
                    </div>
                </div>
            </div>

            {/* Legend */}
            <div className="mt-auto grid grid-cols-2 gap-4 border-t border-border-dark pt-6">
                <div className="flex items-start gap-3">
                    <div className="w-3 h-3 rounded-full bg-success mt-1.5 shadow-[0_0_8px_rgba(34,197,94,0.6)]" />
                    <div>
                        <p className="text-white text-sm font-bold">Profit</p>
                        <p className="text-text-muted text-xs mt-0.5">{winTrades.toLocaleString()} Trades</p>
                    </div>
                </div>
                <div className="flex items-start gap-3">
                    <div className="w-3 h-3 rounded-full bg-danger mt-1.5 shadow-[0_0_8px_rgba(239,68,68,0.6)]" />
                    <div>
                        <p className="text-white text-sm font-bold">Loss</p>
                        <p className="text-text-muted text-xs mt-0.5">{lossTrades.toLocaleString()} Trades</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DonutChart;
