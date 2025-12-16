import React from 'react';

const StockTableRow = ({ stock, brokerAvg, currentPrice, value, diffPct, status }) => {
    const getStatusBadge = () => {
        switch (status) {
            case 'BUY':
            case 'PROFIT':
                return (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-primary/20 text-primary border border-primary/20">
                        {status}
                    </span>
                );
            case 'SELL':
            case 'LOSS':
                return (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-loss/20 text-loss border border-loss/20">
                        {status}
                    </span>
                );
            default:
                return (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-slate-200 dark:bg-slate-700 text-slate-500 dark:text-slate-300 border border-slate-300 dark:border-slate-600">
                        NEUTRAL
                    </span>
                );
        }
    };

    // Get stock initials for avatar
    const getInitials = (ticker) => {
        return ticker.substring(0, 2).toUpperCase();
    };

    // Format currency
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        }).format(amount);
    };

    return (
        <tr className="group hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4">
                <div className="flex items-center gap-3">
                    <div className="size-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-xs font-bold text-slate-600 dark:text-slate-300">
                        {getInitials(stock)}
                    </div>
                    <div>
                        <div className="font-bold text-slate-900 dark:text-white">{stock}</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">
                            {diffPct > 0 ? '+' : ''}{diffPct}%
                        </div>
                    </div>
                </div>
            </td>
            <td className="px-6 py-4 text-right font-mono text-sm text-slate-600 dark:text-slate-300">
                {formatCurrency(brokerAvg)}
            </td>
            <td className="px-6 py-4 text-right font-mono text-sm text-slate-900 dark:text-white font-medium">
                {formatCurrency(currentPrice)}
            </td>
            <td className="px-6 py-4 text-right font-mono text-sm text-slate-900 dark:text-white font-bold">
                {formatCurrency(value)}
            </td>
            <td className="px-6 py-4 text-center">
                {getStatusBadge()}
            </td>
            <td className="px-6 py-4 text-right">
                <button className="text-slate-400 hover:text-white transition-colors">
                    <span className="material-symbols-outlined text-[20px]">more_vert</span>
                </button>
            </td>
        </tr>
    );
};

export default StockTableRow;
