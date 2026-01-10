import React from 'react';

const SummaryCard = ({ title, value, icon, trend, trendText, variant = 'default' }) => {
    const getVariantClasses = () => {
        switch (variant) {
            case 'profit':
                return 'group-hover:text-primary';
            case 'loss':
                return 'group-hover:text-loss';
            default:
                return 'group-hover:text-primary';
        }
    };

    const getValueColor = () => {
        switch (variant) {
            case 'profit':
                return 'text-primary';
            case 'loss':
                return 'text-loss';
            default:
                return 'text-slate-900 dark:text-white';
        }
    };

    const getBorderHover = () => {
        switch (variant) {
            case 'loss':
                return 'hover:border-loss/50';
            default:
                return 'hover:border-primary/50';
        }
    };

    return (
        <div className={`bg-white dark:bg-card-dark rounded-3xl p-6 border border-slate-200 dark:border-border-dark flex flex-col gap-2 shadow-sm group ${getBorderHover()} transition-colors`}>
            <div className="flex items-center justify-between">
                <span className="text-slate-500 dark:text-slate-400 text-sm font-medium">{title}&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;&nbsp;&nbsp;&nbsp;{trendText}</span>
                <span className={`material-symbols-outlined text-slate-300 dark:text-slate-600 ${getVariantClasses()} transition-colors`}>
                    {icon}
                </span>
            </div>
            <p className={`text-3xl font-bold font-mono ${getValueColor()}`}>{value}</p>
            {(trend || trendText) && (
                <div className="text-xs text-slate-400 mt-2 flex items-center gap-1">
                    {trend && (
                        <span className="text-primary flex items-center">
                            <span className="material-symbols-outlined text-[14px]">trending_up</span> {trend}
                        </span>
                    )}
                </div>
            )}
        </div>
    );
};

export default SummaryCard;
