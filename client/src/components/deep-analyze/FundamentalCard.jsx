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

    return (
        <div className='w-full h-full bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark overflow-hidden'>
            <div className="p-4 border-b border-slate-200 dark:border-border-dark bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">functions</span>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Fundamental Analysis</h3>
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Valuation, Profitability, Solvency, Growth</p>
            </div>
            <div className="flex flex-col items-center" >
                <div className='p-6 space-y-6'>
                    <span className="material-symbols-outlined text-primary">Valuation</span>
                </div>
                <div className='p-6 space-y-6'>
                    <span className="material-symbols-outlined text-primary">Health Company</span>
                </div>
            </div>
            <div className="w-full">
                <div className='p-6 space-y-6'>
                    <span className="material-symbols-outlined text-primary">Summary</span>
                </div>
            </div>
        </div>
    );
};

export default FundamentalCard;