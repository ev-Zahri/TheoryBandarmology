import React from 'react';
import StockTableRow from './StockTableRow';

const AnalysisTable = ({ data = [], isLoading }) => {
    if (isLoading) {
        return (
            <div className="bg-white dark:bg-card-dark rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm overflow-hidden flex flex-col">
                <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Analysis Results</h3>
                </div>
                <div className="p-12 flex items-center justify-center">
                    <div className="flex flex-col items-center gap-4">
                        <span className="material-symbols-outlined text-4xl text-primary animate-spin">progress_activity</span>
                        <p className="text-slate-500 dark:text-slate-400">Analyzing broker data...</p>
                    </div>
                </div>
            </div>
        );
    }

    if (data.length === 0) {
        return (
            <div className="bg-white dark:bg-card-dark rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm overflow-hidden flex flex-col">
                <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Analysis Results</h3>
                </div>
                <div className="p-12 flex items-center justify-center">
                    <div className="flex flex-col items-center gap-4">
                        <span className="material-symbols-outlined text-4xl text-slate-400">table_chart</span>
                        <p className="text-slate-500 dark:text-slate-400">No data available. Paste JSON and click Analyze.</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-card-dark rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm overflow-hidden flex flex-col">
            <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">Analysis Results</h3>
                <div className="flex gap-2">
                    <button className="text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                        <span className="material-symbols-outlined text-[20px]">filter_list</span>
                    </button>
                    <button className="text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                        <span className="material-symbols-outlined text-[20px]">download</span>
                    </button>
                </div>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-slate-200 dark:border-slate-700/50 text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 font-semibold bg-slate-50 dark:bg-slate-800/30">
                            <th className="px-6 py-4">Stock Ticker</th>
                            <th className="px-6 py-4 text-right">Avg Price</th>
                            <th className="px-6 py-4 text-right">CMP</th>
                            <th className="px-6 py-4 text-right">Total Value</th>
                            <th className="px-6 py-4 text-center">Status</th>
                            <th className="px-6 py-4 text-right">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 dark:divide-slate-700/50">
                        {data.map((item, index) => (
                            <StockTableRow
                                key={index}
                                stock={item.stock}
                                brokerAvg={item.broker_avg}
                                currentPrice={item.current_price}
                                value={item.value}
                                diffPct={item.diff_pct}
                                status={item.status}
                            />
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="p-4 border-t border-slate-200 dark:border-slate-800 flex justify-center">
                <button className="text-sm font-bold text-primary hover:text-[#3cd610] flex items-center gap-1 transition-colors">
                    View All Transactions <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
                </button>
            </div>
        </div>
    );
};

export default AnalysisTable;
