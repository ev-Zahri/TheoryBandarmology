import React from 'react';

function BandarmologyIndicators({ bandarmology }) {
    if (!bandarmology) return null;

    const { accumulation, behavior, position_strength } = bandarmology;

    // Color mapping for scores
    const getScoreColor = (score) => {
        if (score >= 8) return 'text-green-600 dark:text-green-400';
        if (score >= 6) return 'text-blue-600 dark:text-blue-400';
        if (score >= 4) return 'text-yellow-600 dark:text-yellow-400';
        return 'text-red-600 dark:text-red-400';
    };

    const getStrategyColor = (strategy) => {
        const colors = {
            'ACCUMULATION': 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400',
            'TRAPPED': 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400',
            'DISTRIBUTION': 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400',
            'MOMENTUM': 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400',
            'SWING_TRADING': 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400',
            'NEUTRAL': 'bg-slate-100 text-slate-700 dark:bg-slate-900/30 dark:text-slate-400'
        };
        return colors[strategy] || colors['NEUTRAL'];
    };

    return (
        <div className="space-y-3">
            {/* Accumulation Score */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[18px] text-slate-500">analytics</span>
                    <span className="text-sm text-slate-600 dark:text-slate-400">Accumulation Score</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-24 h-2 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                        <div 
                            className={`h-full ${accumulation.accumulation_score >= 7 ? 'bg-green-500' : accumulation.accumulation_score >= 5 ? 'bg-blue-500' : 'bg-yellow-500'}`}
                            style={{ width: `${(accumulation.accumulation_score / 10) * 100}%` }}
                        />
                    </div>
                    <span className={`text-sm font-bold ${getScoreColor(accumulation.accumulation_score)}`}>
                        {accumulation.accumulation_score}/10
                    </span>
                </div>
            </div>

            {/* Strategy Badge */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[18px] text-slate-500">strategy</span>
                    <span className="text-sm text-slate-600 dark:text-slate-400">Strategy</span>
                </div>
                <span className={`px-2 py-1 rounded-md text-xs font-medium ${getStrategyColor(behavior.strategy)}`}>
                    {behavior.strategy.replace(/_/g, ' ')}
                </span>
            </div>

            {/* Conviction Level */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[18px] text-slate-500">favorite</span>
                    <span className="text-sm text-slate-600 dark:text-slate-400">Conviction</span>
                </div>
                <span className="text-sm font-medium text-slate-900 dark:text-white">
                    {behavior.conviction}
                </span>
            </div>

            {/* Position Strength */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[18px] text-slate-500">shield</span>
                    <span className="text-sm text-slate-600 dark:text-slate-400">Position Strength</span>
                </div>
                <span className={`text-sm font-bold ${getScoreColor(position_strength.overall_score)}`}>
                    {position_strength.overall_score}/10
                </span>
            </div>

            {/* Target & Stop */}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-700">
                <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                        <span className="text-slate-500 dark:text-slate-400">Target:</span>
                        <span className="ml-1 font-medium text-green-600 dark:text-green-400">
                            Rp {position_strength.estimated_target?.toLocaleString()}
                        </span>
                    </div>
                    <div>
                        <span className="text-slate-500 dark:text-slate-400">Stop:</span>
                        <span className="ml-1 font-medium text-red-600 dark:text-red-400">
                            Rp {position_strength.estimated_stop?.toLocaleString()}
                        </span>
                    </div>
                </div>
                <div className="mt-1">
                    <span className="text-slate-500 dark:text-slate-400">R:R Ratio:</span>
                    <span className="ml-1 font-medium text-slate-900 dark:text-white">
                        {position_strength.risk_reward_ratio}
                    </span>
                </div>
            </div>

            {/* Interpretation */}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-700">
                <p className="text-xs text-slate-600 dark:text-slate-400 italic">
                    {behavior.description}
                </p>
            </div>
        </div>
    );
}

export default BandarmologyIndicators;
