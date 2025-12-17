import React from 'react';

const QuantCard = ({ data, isLoading }) => {
    if (isLoading) {
        return (
            <div className="bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark p-6 animate-pulse">
                <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-1/3 mb-4"></div>
                <div className="space-y-3">
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-full"></div>
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3"></div>
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <div className="bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark p-6">
                <p className="text-slate-500 dark:text-slate-400">Data kuantitatif tidak tersedia</p>
            </div>
        );
    }

    const getZScoreColor = (status) => {
        if (status.includes('Cheap')) return 'text-green-500';
        if (status.includes('Expensive')) return 'text-red-500';
        return 'text-slate-400';
    };

    const getBiasColor = (bias) => {
        if (bias.includes('Breakout')) return 'text-green-500';
        if (bias.includes('Breakdown')) return 'text-red-500';
        return 'text-slate-400';
    };

    return (
        <div className="bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark overflow-hidden">
            <div className="p-4 border-b border-slate-200 dark:border-border-dark bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">functions</span>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Quantitative Analysis</h3>
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Z-Score, ATR, Pivot Points</p>
            </div>

            <div className="p-6 space-y-6">
                {/* Z-Score */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Z-Score</span>
                        <span className="font-mono text-lg font-bold text-slate-900 dark:text-white">
                            {data.z_score?.toFixed(2) || 0}
                        </span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 relative">
                        <div
                            className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-0.5 h-4 bg-slate-400"
                        />
                        <div
                            className={`h-2 rounded-full transition-all ${data.z_score < -1 ? 'bg-green-500' :
                                    data.z_score > 1 ? 'bg-red-500' : 'bg-primary'
                                }`}
                            style={{
                                width: `${Math.min(Math.max((data.z_score + 3) / 6 * 100, 0), 100)}%`
                            }}
                        />
                    </div>
                    <div className="flex justify-between text-xs text-slate-500">
                        <span>-3σ</span>
                        <span>0</span>
                        <span>+3σ</span>
                    </div>
                    <p className={`text-sm font-medium ${getZScoreColor(data.z_status)}`}>
                        {data.z_status}
                    </p>
                </div>

                {/* Volatility (ATR) */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Volatility (ATR)</span>
                        <span className="material-symbols-outlined text-[18px] text-slate-400">timeline</span>
                    </div>
                    <p className="font-mono text-2xl font-bold text-slate-900 dark:text-white">
                        Rp {data.volatility_atr?.toLocaleString('id-ID') || 0}
                    </p>
                    <p className="text-xs text-slate-500 dark:text-slate-400">Average True Range (14-day)</p>
                </div>

                {/* Support & Resistance */}
                <div className="space-y-3">
                    <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-[18px] text-slate-400">show_chart</span>
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Pivot Points</span>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                        <div className="bg-green-500/10 border border-green-500/20 rounded-md p-3">
                            <p className="text-xs text-green-600 dark:text-green-400 font-medium mb-1">Support (S1)</p>
                            <p className="font-mono text-lg font-bold text-green-700 dark:text-green-300">
                                Rp {data.algo_support_s1?.toLocaleString('id-ID') || 0}
                            </p>
                        </div>

                        <div className="bg-red-500/10 border border-red-500/20 rounded-md p-3">
                            <p className="text-xs text-red-600 dark:text-red-400 font-medium mb-1">Resistance (R1)</p>
                            <p className="font-mono text-lg font-bold text-red-700 dark:text-red-300">
                                Rp {data.algo_resistance_r1?.toLocaleString('id-ID') || 0}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Technical Bias */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Technical Bias</span>
                        <span className="material-symbols-outlined text-[18px] text-slate-400">insights</span>
                    </div>
                    <p className={`font-bold ${getBiasColor(data.technical_bias)}`}>
                        {data.technical_bias}
                    </p>
                </div>

                {/* Current Price */}
                <div className="pt-4 border-t border-slate-200 dark:border-border-dark">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Price</span>
                        <span className="font-mono text-xl font-bold text-slate-900 dark:text-white">
                            Rp {data.last_price?.toLocaleString('id-ID') || 0}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QuantCard;
