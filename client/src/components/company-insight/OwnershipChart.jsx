import React from 'react';

const OwnershipChart = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <section className="bg-card-dark border border-border-dark rounded-xl p-6 h-fit">
                <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-6">
                    <span className="material-symbols-outlined text-primary">donut_small</span>
                    Ownership
                </h3>
                <p className="text-text-muted text-sm">No ownership data available</p>
            </section>
        );
    }

    // Sort by percentage descending
    const sortedData = [...data].sort((a, b) => b.percent - a.percent);
    const hasHighAccumulation = sortedData[0]?.percent > 50;

    return (
        <section className="bg-card-dark border border-border-dark rounded-md p-6 h-fit">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">donut_small</span>
                    Ownership
                </h3>
                {hasHighAccumulation && (
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-primary text-[#0B1221] uppercase tracking-wide">
                        Big Accumulation
                    </span>
                )}
            </div>

            <div className="flex flex-col gap-6">
                {/* Horizontal Stacked Bar */}
                <div className="flex h-4 w-full rounded-full overflow-hidden">
                    {sortedData.map((item, idx) => (
                        <div
                            key={idx}
                            className="h-full transition-all"
                            style={{
                                width: `${item.percent}%`,
                                backgroundColor: item.color || '#94a3b8'
                            }}
                        />
                    ))}
                </div>

                {/* Legend */}
                <div className="flex flex-col gap-4">
                    {sortedData.map((item, idx) => (
                        <div key={idx} className="flex items-start gap-3">
                            <div
                                className="mt-1 size-3 rounded-full shadow-glow"
                                style={{ backgroundColor: item.color || '#94a3b8' }}
                            />
                            <div className="flex-1">
                                <p className="text-sm font-medium text-white">{item.name}</p>
                                <p className="text-xs text-text-muted">
                                    {idx === 0 ? 'Controlling Entity' : idx === 1 ? 'Financial Institutions' : '< 5% Ownership'}
                                </p>
                            </div>
                            <p className="text-sm font-mono font-bold text-white">{item.percent.toFixed(2)}%</p>
                        </div>
                    ))}
                </div>

                {/* Insight Box */}
                <div className="mt-2 p-3 bg-[#0B1221] border border-border-dark rounded-md">
                    <p className="text-xs text-text-muted leading-relaxed">
                        <span className="text-primary font-bold">Insight:</span>{' '}
                        {hasHighAccumulation
                            ? 'Strong controlling ownership indicates stability, but lower liquidity for retail traders.'
                            : 'Diversified ownership structure provides better market liquidity.'}
                    </p>
                </div>
            </div>
        </section>
    );
};

export default OwnershipChart;
