import React from 'react';
import Error from '../common/Error';

const FundamentalCard = ({ data, isLoading }) => {
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
            <Error error="Data fundamental tidak tersedia" />
        );
    }

    const getHealthColor = (status) => {
        if (status.includes('HEALTHY') || status.includes('STRONG')) return 'text-green-500';
        if (status.includes('RISKY') || status.includes('WEAK')) return 'text-red-500';
        return 'text-yellow-500';
    };

    return (
        <div className='w-full bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark overflow-hidden'>
            <div className="p-4 border-b border-slate-200 dark:border-border-dark bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">monitoring</span>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Fundamental Analysis</h3>
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Valuation, Profitability, Solvency</p>
            </div>

            <div className='p-6 space-y-6'>
                {/* Market Cap */}
                <div className="space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Market Cap</span>
                        <span className="material-symbols-outlined text-[18px] text-slate-400">paid</span>
                    </div>
                    <p className="font-mono text-2xl font-bold text-slate-900 dark:text-white">
                        Rp {data.market_cap_t?.toLocaleString('id-ID')} T
                    </p>
                </div>

                {/* Valuation Metrics */}
                <div className="space-y-3">
                    <h4 className="text-sm font-bold text-slate-700 dark:text-slate-300">📊 Valuation</h4>
                    <div className="grid grid-cols-3 gap-3">
                        <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">
                            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">PER</p>
                            <p className="font-mono text-lg font-bold text-slate-900 dark:text-white">
                                {data.valuation?.per || 0}x
                            </p>
                        </div>
                        <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">
                            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">PBV</p>
                            <p className="font-mono text-lg font-bold text-slate-900 dark:text-white">
                                {data.valuation?.pbv || 0}x
                            </p>
                        </div>
                        <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">
                            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Div Yield</p>
                            <p className="font-mono text-lg font-bold text-slate-900 dark:text-white">
                                {data.valuation?.div_yield || 0}%
                            </p>
                        </div>
                    </div>
                </div>

                {/* Health Metrics */}
                <div className="space-y-3">
                    <h4 className="text-sm font-bold text-slate-700 dark:text-slate-300">💪 Company Health</h4>
                    <div className="grid grid-cols-2 gap-3">
                        <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-3">
                            <p className="text-xs text-green-600 dark:text-green-400 font-medium mb-1">ROE</p>
                            <p className="font-mono text-lg font-bold text-green-700 dark:text-green-300">
                                {data.health?.roe || 0}%
                            </p>
                        </div>
                        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3">
                            <p className="text-xs text-blue-600 dark:text-blue-400 font-medium mb-1">NPM</p>
                            <p className="font-mono text-lg font-bold text-blue-700 dark:text-blue-300">
                                {data.health?.npm || 0}%
                            </p>
                        </div>
                        <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                            <p className="text-xs text-red-600 dark:text-red-400 font-medium mb-1">DER</p>
                            <p className="font-mono text-lg font-bold text-red-700 dark:text-red-300">
                                {data.health?.der || 0}%
                            </p>
                        </div>
                        <div className="bg-purple-500/10 border border-purple-500/20 rounded-lg p-3">
                            <p className="text-xs text-purple-600 dark:text-purple-400 font-medium mb-1">Rev Growth</p>
                            <p className="font-mono text-lg font-bold text-purple-700 dark:text-purple-300">
                                {data.health?.rev_growth || 0}%
                            </p>
                        </div>
                    </div>
                </div>

                {/* Summary */}
                <div className="pt-4 border-t border-slate-200 dark:border-border-dark space-y-2">
                    <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400">Health Status</span>
                        <span className={`font-bold text-lg ${getHealthColor(data.summary?.status)}`}>
                            {data.summary?.status || 'N/A'}
                        </span>
                    </div>
                    {data.summary?.flags && data.summary.flags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3">
                            {data.summary.flags.map((flag, idx) => (
                                <span key={idx} className="text-xs px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded-full">
                                    {flag}
                                </span>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default FundamentalCard;