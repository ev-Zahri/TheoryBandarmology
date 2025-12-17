import React from 'react';

const TechnicalCard = ({ data, isLoading }) => {
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
                <p className="text-slate-500 dark:text-slate-400">Data teknikal tidak tersedia</p>
            </div>
        );
    }

    const getIchimokuColor = (status) => {
        if (status.includes('BULLISH')) return 'text-green-500';
        if (status.includes('BEARISH')) return 'text-red-500';
        return 'text-yellow-500';
    };

    const getMomentumColor = (signal) => {
        if (signal.includes('Oversold')) return 'text-green-500';
        if (signal.includes('Overbought')) return 'text-red-500';
        return 'text-slate-400';
    };

    const getDivergenceColor = (status) => {
        if (status.includes('BULLISH')) return 'text-green-500';
        if (status.includes('BEARISH')) return 'text-red-500';
        return 'text-slate-400';
    };

    return (
        <div className="bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark overflow-hidden">
            <div className="p-4 border-b border-slate-200 dark:border-border-dark bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">candlestick_chart</span>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Technical Analysis</h3>
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Ichimoku, StochRSI, OBV</p>
            </div>

            <div className="p-6 space-y-6">
                {/* Ichimoku Cloud */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Ichimoku Cloud</span>
                        <span className="material-symbols-outlined text-[18px] text-slate-400">cloud</span>
                    </div>
                    <p className={`font-bold ${getIchimokuColor(data.ichimoku_status)}`}>
                        {data.ichimoku_status}
                    </p>
                </div>

                {/* Stochastic RSI */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Stochastic RSI</span>
                        <span className="font-mono text-lg font-bold text-slate-900 dark:text-white">
                            {(data.stoch_rsi * 100).toFixed(0)}%
                        </span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                        <div
                            className={`h-2 rounded-full transition-all ${data.stoch_rsi < 0.2 ? 'bg-green-500' :
                                    data.stoch_rsi > 0.8 ? 'bg-red-500' : 'bg-primary'
                                }`}
                            style={{ width: `${data.stoch_rsi * 100}%` }}
                        />
                    </div>
                    <p className={`text-sm ${getMomentumColor(data.momentum_signal)}`}>
                        {data.momentum_signal}
                    </p>
                </div>

                {/* OBV Divergence */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">OBV Divergence</span>
                        <span className="material-symbols-outlined text-[18px] text-slate-400">show_chart</span>
                    </div>
                    <p className={`font-bold ${getDivergenceColor(data.obv_divergence)}`}>
                        {data.obv_divergence}
                    </p>
                </div>

                {/* Current Price */}
                <div className="pt-4 border-t border-slate-200 dark:border-border-dark">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Price</span>
                        <span className="font-mono text-xl font-bold text-slate-900 dark:text-white">
                            Rp {data.price?.toLocaleString('id-ID') || 0}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TechnicalCard;
