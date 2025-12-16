import React from 'react';

const AccumulationBarChart = ({ data = [], totalValue = 0, changePercent = 0 }) => {
    // Calculate max value for percentage calculation
    const maxValue = Math.max(...data.map(item => item.value), 1);

    // Format currency
    const formatValue = (value) => {
        if (value >= 1e12) return `Rp ${(value / 1e12).toFixed(1)}T`;
        if (value >= 1e9) return `Rp ${(value / 1e9).toFixed(1)}B`;
        if (value >= 1e6) return `Rp ${(value / 1e6).toFixed(1)}M`;
        return `Rp ${value.toLocaleString('id-ID')}`;
    };

    return (
        <div className="rounded-xl bg-surface-dark border border-border-dark p-6 shadow-xl shadow-black/20 flex flex-col h-full">
            <div className="flex items-start justify-between mb-6">
                <div>
                    <h2 className="text-white text-lg font-semibold mb-1">Top Accumulation by Value</h2>
                    <p className="text-text-muted text-sm">Real-time market accumulation across top tickers</p>
                </div>
                <div className="text-right">
                    <p className="text-white font-mono text-2xl font-bold tracking-tight">{formatValue(totalValue)}</p>
                    <div className={`flex items-center justify-end gap-1 ${changePercent >= 0 ? 'text-success' : 'text-danger'} text-sm font-medium`}>
                        <span className="material-symbols-outlined text-[16px]">
                            {changePercent >= 0 ? 'trending_up' : 'trending_down'}
                        </span>
                        <span>{changePercent >= 0 ? '+' : ''}{changePercent.toFixed(1)}%</span>
                    </div>
                </div>
            </div>

            {/* Bar Chart Visualization */}
            <div className="flex-1 flex flex-col justify-center gap-6 py-2">
                {data.slice(0, 5).map((item, index) => {
                    const widthPercent = Math.min((item.value / maxValue) * 100, 100);
                    return (
                        <div key={item.stock || index} className="group">
                            <div className="flex justify-between items-end mb-2">
                                <span className="text-white font-bold text-sm tracking-wide">{item.stock}</span>
                                <span className="text-text-muted font-mono text-xs opacity-0 group-hover:opacity-100 transition-opacity">
                                    {formatValue(item.value)}
                                </span>
                            </div>
                            <div className="relative w-full h-3 bg-background-dark rounded-full overflow-hidden">
                                <div
                                    className="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-900 to-primary rounded-full group-hover:shadow-[0_0_12px_rgba(59,130,246,0.6)] transition-all duration-300"
                                    style={{ width: `${widthPercent}%` }}
                                />
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* X Axis Labels */}
            <div className="flex justify-between text-text-muted text-xs font-mono mt-4 pt-4 border-t border-border-dark/50">
                <span>Rp 0</span>
                <span>{formatValue(maxValue * 0.25)}</span>
                <span>{formatValue(maxValue * 0.5)}</span>
                <span>{formatValue(maxValue * 0.75)}</span>
                <span>{formatValue(maxValue)}</span>
            </div>
        </div>
    );
};

export default AccumulationBarChart;
