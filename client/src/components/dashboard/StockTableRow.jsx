import React from 'react';
import { Link } from 'react-router-dom';

const StockTableRow = ({
    rowId,
    stock,
    brokerAvg,
    currentPrice,
    value_bn,
    diffPct,
    status,
    weight_pct,
    floating_pnl,
    isDropdownOpen,
    onToggleDropdown
}) => {

    const getStatusBadge = () => {
        switch (status) {
            case 'BUY':
            case 'PROFIT':
                return (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-primary/20 text-primary border border-primary/20">
                        {status}
                    </span>
                );
            case 'BIG PROFIT':
                return (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-green-500/20 text-green-500 border border-green-500/20">
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
            case 'DEEP LOSS':
                return (
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-red-600/20 text-red-500 border border-red-500/20">
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
        amount = parseInt(amount)
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
                        <div className="font-mono font-bold text-sm text-slate-600 dark:text-slate-300">{stock}</div>
                        <div className="font-mono text-sm text-slate-600 dark:text-slate-300">
                            {diffPct > 0 ? '+' : ''}{diffPct}%
                        </div>
                    </div>
                </div>
            </td>
            <td className="px-6 py-4 text-center font-mono text-sm text-slate-600 dark:text-slate-300">
                {formatCurrency(brokerAvg)}
            </td>
            <td className="px-6 py-4 text-center font-mono text-sm text-slate-900 dark:text-slate-300">
                {formatCurrency(currentPrice)}
            </td>
            <td className="px-6 py-4 text-center font-mono text-sm text-slate-900 dark:text-slate-300">
                Rp {value_bn?.toFixed(2) || 0} B
            </td>
            <td className="px-6 py-4 text-center font-mono text-sm text-slate-900 dark:text-slate-300">
                {weight_pct?.toFixed(1) || 0}%
            </td>
            <td className="px-6 py-4 text-center font-mono text-sm text-slate-900 dark:text-slate-300">
                {formatCurrency(floating_pnl || 0)}
            </td>
            <td className="px-6 py-4 text-center">
                {getStatusBadge()}
            </td>
            <td className="px-6 py-4 text-center relative">
                <button
                    className="text-slate-400 hover:text-white transition-colors"
                    onClick={() => onToggleDropdown(rowId)}
                >
                    <span className="material-symbols-outlined text-[20px]">more_vert</span>
                </button>
                {isDropdownOpen && (
                    <div className="absolute right-6 top-12 z-20 w-44 text-left bg-white dark:bg-card-dark border rounded-md border-slate-200 dark:border-border-dark shadow-lg overflow-hidden">
                        <button className="w-full py-2.5 px-3 text-left hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-2">
                            <span className="material-symbols-outlined text-[16px] text-primary">analytics</span>
                            <Link to={`/deep-analyze/${stock}`}><span className="text-sm dark:text-white">Deep Analysis</span></Link>
                        </button>
                        <button className="w-full py-2.5 px-3 text-left hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-2">
                            <span className="material-symbols-outlined text-[16px] text-primary">lightbulb</span>
                            <Link to={`/insight/${stock}`}><span className="text-sm dark:text-white">Get Insight</span></Link>
                        </button>
                    </div>
                )}
            </td>
        </tr>
    );
};

export default StockTableRow;

