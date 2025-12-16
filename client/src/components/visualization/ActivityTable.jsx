import React from 'react';

const ActivityTable = ({ data = [] }) => {
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency',
            currency: 'IDR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0,
        }).format(amount);
    };

    const formatDate = (dateStr) => {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    };

    return (
        <div className="rounded-xl bg-surface-dark border border-border-dark overflow-hidden">
            <div className="p-4 border-b border-border-dark flex justify-between items-center bg-background-dark/30">
                <h3 className="text-white text-sm font-semibold uppercase tracking-wider">Recent Activity</h3>
                <button className="text-primary text-sm hover:text-blue-400 transition-colors">View All</button>
            </div>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-text-muted">
                    <thead className="bg-background-dark/50 text-xs uppercase font-medium">
                        <tr>
                            <th className="px-6 py-3">Ticker</th>
                            <th className="px-6 py-3">Type</th>
                            <th className="px-6 py-3">Date</th>
                            <th className="px-6 py-3">Amount</th>
                            <th className="px-6 py-3 text-right">Return</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-border-dark/50">
                        {data.length === 0 ? (
                            <tr>
                                <td colSpan="5" className="px-6 py-8 text-center text-text-muted">
                                    No recent activity
                                </td>
                            </tr>
                        ) : (
                            data.map((item, index) => (
                                <tr key={index} className="hover:bg-background-dark/30 transition-colors">
                                    <td className="px-6 py-4 font-medium text-white">{item.stock}</td>
                                    <td className="px-6 py-4">
                                        <span className={`${item.status === 'PROFIT' ? 'bg-success/10 text-success' : 'bg-danger/10 text-danger'} px-2 py-1 rounded text-xs font-bold`}>
                                            {item.status === 'PROFIT' ? 'BUY' : 'SELL'}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 font-mono">{item.date ? formatDate(item.date) : '-'}</td>
                                    <td className="px-6 py-4 font-mono text-white">{formatCurrency(item.value || 0)}</td>
                                    <td className={`px-6 py-4 text-right font-mono ${item.diff_pct >= 0 ? 'text-success' : 'text-danger'}`}>
                                        {item.diff_pct >= 0 ? '+' : ''}{item.diff_pct?.toFixed(1) || 0}%
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ActivityTable;
