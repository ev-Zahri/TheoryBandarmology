import React, { useState, useEffect } from 'react';

function AccumulationTable({ stocks, loading }) {
    const [sortConfig, setSortConfig] = useState({ key: 'net_volume', direction: 'desc' });
    const [filterBroker, setFilterBroker] = useState('all');
    const [filterSector, setFilterSector] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');

    // Get unique brokers and sectors
    const brokers = ['all', ...new Set(stocks.map(s => s.broker_code))];
    const sectors = ['all', ...new Set(stocks.map(s => s.sector).filter(Boolean))];

    // Filter and sort stocks
    const filteredStocks = stocks
        .filter(stock => {
            const matchesBroker = filterBroker === 'all' || stock.broker_code === filterBroker;
            const matchesSector = filterSector === 'all' || stock.sector === filterSector;
            const matchesSearch = stock.stock_code.toLowerCase().includes(searchQuery.toLowerCase());
            return matchesBroker && matchesSector && matchesSearch;
        })
        .sort((a, b) => {
            const aValue = a[sortConfig.key];
            const bValue = b[sortConfig.key];

            if (sortConfig.direction === 'asc') {
                return aValue > bValue ? 1 : -1;
            }
            return aValue < bValue ? 1 : -1;
        });

    const handleSort = (key) => {
        setSortConfig({
            key,
            direction: sortConfig.key === key && sortConfig.direction === 'desc' ? 'asc' : 'desc'
        });
    };

    const formatNumber = (num) => {
        if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
        if (num >= 1_000) return `${(num / 1_000).toFixed(1)}K`;
        return num.toLocaleString();
    };

    const formatCurrency = (num) => {
        if (num >= 1_000_000_000) return `Rp ${(num / 1_000_000_000).toFixed(1)}B`;
        if (num >= 1_000_000) return `Rp ${(num / 1_000_000).toFixed(1)}M`;
        return `Rp ${num.toLocaleString()}`;
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center py-12">
                <span className="material-symbols-outlined animate-spin text-4xl text-primary">progress_activity</span>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {/* Filters */}
            <div className="flex gap-4 items-center">
                <div className="flex-1">
                    <input
                        type="text"
                        placeholder="Search stock code..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full px-4 py-2 bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                </div>
                <select
                    value={filterBroker}
                    onChange={(e) => setFilterBroker(e.target.value)}
                    className="px-4 py-2 bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                >
                    {brokers.map(broker => (
                        <option key={broker} value={broker}>
                            {broker === 'all' ? 'All Brokers' : broker}
                        </option>
                    ))}
                </select>
                <select
                    value={filterSector}
                    onChange={(e) => setFilterSector(e.target.value)}
                    className="px-4 py-2 bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                >
                    {sectors.map(sector => (
                        <option key={sector} value={sector}>
                            {sector === 'all' ? 'All Sectors' : sector}
                        </option>
                    ))}
                </select>
            </div>

            {/* Table */}
            <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-700">
                <table className="w-full">
                    <thead className="bg-slate-100 dark:bg-slate-800">
                        <tr>
                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700 dark:text-slate-300 cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-700"
                                onClick={() => handleSort('stock_code')}>
                                Stock Code {sortConfig.key === 'stock_code' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700 dark:text-slate-300">
                                Broker
                            </th>
                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700 dark:text-slate-300 cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-700"
                                onClick={() => handleSort('sector')}>
                                Sector {sortConfig.key === 'sector' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-left text-sm font-semibold text-slate-700 dark:text-slate-300 cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-700"
                                onClick={() => handleSort('industry')}>
                                Industry {sortConfig.key === 'industry' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-center text-sm font-semibold text-slate-700 dark:text-slate-300">
                                Rate
                            </th>
                            <th className="px-4 py-3 text-right text-sm font-semibold text-slate-700 dark:text-slate-300 cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-700"
                                onClick={() => handleSort('net_volume')}>
                                Net Volume {sortConfig.key === 'net_volume' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-right text-sm font-semibold text-slate-700 dark:text-slate-300 cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-700"
                                onClick={() => handleSort('avg_price')}>
                                Avg Price {sortConfig.key === 'avg_price' && (sortConfig.direction === 'asc' ? '↑' : '↓')}
                            </th>
                            <th className="px-4 py-3 text-right text-sm font-semibold text-slate-700 dark:text-slate-300">
                                Net Value
                            </th>
                            <th className="px-4 py-3 text-center text-sm font-semibold text-slate-700 dark:text-slate-300">
                                Transactions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                        {filteredStocks.length === 0 ? (
                            <tr>
                                <td colSpan="9" className="px-4 py-8 text-center text-slate-500 dark:text-slate-400">
                                    No accumulating stocks found
                                </td>
                            </tr>
                        ) : (
                            filteredStocks.map((stock, index) => (
                                <tr key={index} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                                    <td className="px-4 py-3 text-sm font-semibold text-slate-900 dark:text-white">
                                        {stock.stock_code}
                                    </td>
                                    <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400">
                                        {stock.broker_code}
                                    </td>
                                    <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400">
                                        <span className="inline-flex items-center px-2 py-1 rounded-md text-xs bg-slate-100 dark:bg-slate-700">
                                            {stock.sector || 'Unknown'}
                                        </span>
                                    </td>
                                    <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400 max-w-[200px] truncate" title={stock.industry}>
                                        {stock.industry || 'Unknown'}
                                    </td>
                                    <td className="px-4 py-3 text-center">
                                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
                                            {stock.appearance_rate.toFixed(0)}%
                                        </span>
                                    </td>
                                    <td className={`px-4 py-3 text-sm text-right font-medium ${stock.net_volume >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                                        {stock.net_volume >= 0 ? '+' : ''}{formatNumber(stock.net_volume)}
                                    </td>
                                    <td className="px-4 py-3 text-sm text-right text-slate-600 dark:text-slate-400">
                                        Rp {stock.avg_price.toLocaleString()}
                                    </td>
                                    <td className={`px-4 py-3 text-sm text-right font-medium ${stock.net_value >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                                        {stock.net_value >= 0 ? '+' : ''}{formatCurrency(stock.net_value)}
                                    </td>
                                    <td className="px-4 py-3 text-sm text-center text-slate-600 dark:text-slate-400">
                                        {stock.appearances}/{stock.total_transactions}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Summary */}
            <div className="flex justify-between items-center text-sm text-slate-600 dark:text-slate-400">
                <span>Showing {filteredStocks.length} of {stocks.length} stocks</span>
                <span>{filteredStocks.filter(s => s.net_volume > 0).length} accumulating, {filteredStocks.filter(s => s.net_volume < 0).length} distributing</span>
            </div>
        </div>
    );
}

export default AccumulationTable;
