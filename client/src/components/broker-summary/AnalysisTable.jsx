import React, { useState, useMemo } from 'react';
import StockTableRow from './StockTableRow';

const AnalysisTable = ({ data = [], isLoading, totalValue = 0 }) => {
    const [currentPage, setCurrentPage] = useState(1);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [activeDropdown, setActiveDropdown] = useState(null);

    // Filter & Search states
    const [showFilters, setShowFilters] = useState(false);
    const [showSearch, setShowSearch] = useState(false);
    const [searchQuery, setSearchQuery] = useState('');
    const [filters, setFilters] = useState({
        position: 'all', // all, NET BUY, NET SELL
        minValue: '',
        maxValue: '',
        minPnL: '',
        maxPnL: '',
    });

    // Sorting state
    const [sortConfig, setSortConfig] = useState({
        key: null, // 'current_price', 'weight_pct', 'value_bn', etc.
        direction: 'asc' // 'asc' or 'desc'
    });

    // Calculate weight % for each stock based on total value
    const dataWithWeight = useMemo(() => {
        if (!totalValue || totalValue === 0) return data;
        return data.map(item => ({
            ...item,
            weight_pct: (Math.abs(item.value_raw) / totalValue) * 100
        }));
    }, [data, totalValue]);

    // Apply filters and search
    const filteredData = useMemo(() => {
        let result = dataWithWeight;

        // Apply search
        if (searchQuery.trim()) {
            result = result.filter(item =>
                item.stock_code?.toLowerCase().includes(searchQuery.toLowerCase())
            );
        }

        // Apply position filter
        if (filters.position !== 'all') {
            result = result.filter(item => item.position === filters.position);
        }

        // Apply value range filter
        if (filters.minValue) {
            const minVal = parseFloat(filters.minValue) * 1_000_000_000; // Convert to raw value
            result = result.filter(item => Math.abs(item.value_raw) >= minVal);
        }
        if (filters.maxValue) {
            const maxVal = parseFloat(filters.maxValue) * 1_000_000_000;
            result = result.filter(item => Math.abs(item.value_raw) <= maxVal);
        }

        // Apply PnL range filter
        if (filters.minPnL) {
            const minPnL = parseFloat(filters.minPnL);
            result = result.filter(item => item.value_raw >= minPnL);
        }
        if (filters.maxPnL) {
            const maxPnL = parseFloat(filters.maxPnL);
            result = result.filter(item => item.value_raw <= maxPnL);
        }

        return result;
    }, [dataWithWeight, searchQuery, filters]);

    // Apply sorting
    const sortedData = useMemo(() => {
        if (!sortConfig.key) return filteredData;

        return [...filteredData].sort((a, b) => {
            let aValue, bValue;

            switch (sortConfig.key) {
                case 'current_price':
                    aValue = a.current_price || a.sell_avg_price || a.buy_avg_price || 0;
                    bValue = b.current_price || b.sell_avg_price || b.buy_avg_price || 0;
                    break;
                case 'weight_pct':
                    aValue = a.weight_pct || 0;
                    bValue = b.weight_pct || 0;
                    break;
                case 'value_bn':
                    aValue = Math.abs(a.value_raw) / 1_000_000_000;
                    bValue = Math.abs(b.value_raw) / 1_000_000_000;
                    break;
                default:
                    return 0;
            }

            if (sortConfig.direction === 'asc') {
                return aValue - bValue;
            } else {
                return bValue - aValue;
            }
        });
    }, [filteredData, sortConfig]);

    // Calculate pagination
    const totalRows = sortedData.length;
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const paginatedData = sortedData.slice(startIndex, endIndex);

    // Reset to page 1 when filters/search changes
    React.useEffect(() => {
        setCurrentPage(1);
    }, [searchQuery, filters, data.length, sortConfig]);

    const handlePageChange = (page) => {
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
        }
    };

    const handleRowsPerPageChange = (newRowsPerPage) => {
        setRowsPerPage(newRowsPerPage);
        setCurrentPage(1);
    };

    const handleFilterChange = (key, value) => {
        setFilters(prev => ({ ...prev, [key]: value }));
    };

    const clearFilters = () => {
        setFilters({
            position: 'all',
            minValue: '',
            maxValue: '',
            minPnL: '',
            maxPnL: '',
        });
        setSearchQuery('');
        setSortConfig({ key: null, direction: 'asc' });
    };

    const handleSort = (key) => {
        setSortConfig(prev => ({
            key,
            direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
        }));
    };

    const getSortIcon = (key) => {
        if (sortConfig.key !== key) {
            return <span className="material-symbols-outlined text-[16px] text-slate-400">unfold_more</span>;
        }
        return sortConfig.direction === 'asc'
            ? <span className="material-symbols-outlined text-[16px] text-primary">arrow_upward</span>
            : <span className="material-symbols-outlined text-[16px] text-primary">arrow_downward</span>;
    };

    const activeFiltersCount = useMemo(() => {
        let count = 0;
        if (filters.position !== 'all') count++;
        if (filters.minValue || filters.maxValue) count++;
        if (filters.minPnL || filters.maxPnL) count++;
        if (searchQuery.trim()) count++;
        return count;
    }, [filters, searchQuery]);

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
                        <p className="text-slate-500 dark:text-slate-400">No data available. Upload JSON file to analyze.</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-card-dark rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm overflow-hidden flex flex-col">
            {/* Header with Filter & Search buttons */}
            <div className="p-6 border-b border-slate-200 dark:border-slate-800 flex justify-between items-center">
                <div className="flex items-center gap-3">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">Analysis Results</h3>
                    {activeFiltersCount > 0 && (
                        <span className="px-2 py-1 bg-primary/20 text-primary text-xs font-bold rounded-full">
                            {activeFiltersCount} active
                        </span>
                    )}
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={() => setShowFilters(!showFilters)}
                        className={`p-2 rounded-full transition-colors ${showFilters
                            ? 'bg-primary text-white'
                            : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
                            }`}
                    >
                        <span className="material-symbols-outlined text-[20px]">filter_list</span>
                    </button>
                </div>
            </div>

            {/* Combined Filters & Search Panel */}
            {showFilters && (
                <div className="p-4 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/30">
                    <div className="space-y-4">

                        <div className="flex items-center gap-2 justify-between w-full">
                            {/* Search */}
                            <div className="w-[40%]">
                                <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-2">
                                    Search Stock
                                </label>
                                <div className="relative">
                                    <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-[20px]">
                                        search
                                    </span>
                                    <input
                                        type="text"
                                        placeholder="Search by stock code..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        className="w-full pl-10 pr-10 py-2 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 focus:ring-2 focus:ring-primary focus:border-transparent"
                                    />
                                    {searchQuery && (
                                        <button
                                            onClick={() => setSearchQuery('')}
                                            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 transition-colors"
                                        >
                                            <span className="material-symbols-outlined text-[20px]">close</span>
                                        </button>
                                    )}
                                </div>
                            </div>
                            {/* Position Filter */}
                            <div className="w-[40%]">
                                <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-2">
                                    Position
                                </label>
                                <select
                                    value={filters.position}
                                    onChange={(e) => handleFilterChange('position', e.target.value)}
                                    className="w-full px-3 py-2 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-lg text-sm text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                                >
                                    <option value="all">All Positions</option>
                                    <option value="NET BUY">NET BUY</option>
                                    <option value="NET SELL">NET SELL</option>
                                </select>
                            </div>

                            {/* Clear All Button */}
                            <button
                                onClick={clearFilters}
                                className="w-[20%] mt-6 px-4 py-2 bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-900 dark:text-white rounded-lg transition-colors flex items-center justify-center gap-2 text-sm font-medium"
                            >
                                <span className="material-symbols-outlined text-[20px]">clear_all</span>
                                Clear All Filters
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Table */}
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-slate-200 text-center dark:border-slate-700/50 text-xs uppercase tracking-wider text-slate-500 dark:text-white font-semibold bg-slate-50 dark:bg-slate-800/30">
                            <th className="px-6 py-4 font-bold">Stock Ticker</th>
                            <th className="px-6 py-4 font-bold">Avg Price</th>
                            <th
                                className="px-6 py-4 font-bold cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors"
                                onClick={() => handleSort('current_price')}
                            >
                                <div className="flex items-center justify-center gap-1">
                                    Current Price
                                    {getSortIcon('current_price')}
                                </div>
                            </th>
                            <th
                                className="px-6 py-4 font-bold cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors"
                                onClick={() => handleSort('value_bn')}
                            >
                                <div className="flex items-center justify-center gap-1">
                                    Total Value (Bn)
                                    {getSortIcon('value_bn')}
                                </div>
                            </th>
                            <th
                                className="px-6 py-4 font-bold cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-700/50 transition-colors"
                                onClick={() => handleSort('weight_pct')}
                            >
                                <div className="flex items-center justify-center gap-1">
                                    Weight %
                                    {getSortIcon('weight_pct')}
                                </div>
                            </th>
                            <th className="px-6 py-4 font-bold">Floating PnL</th>
                            <th className="px-6 py-4 font-bold">Status</th>
                            <th className="px-6 py-4 font-bold">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200 dark:divide-slate-700/50">
                        {paginatedData.map((item, index) => {
                            const rowId = startIndex + index;
                            return (
                                <StockTableRow
                                    key={rowId}
                                    rowId={rowId}
                                    stock={item.stock_code}
                                    brokerAvg={item.buy_avg_price || item.sell_avg_price || 0}
                                    currentPrice={item.current_price || item.sell_avg_price || item.buy_avg_price || 0}
                                    value_bn={(Math.abs(item.value_raw) / 1_000_000_000) || 0}
                                    diffPct={item.diff_pct ?? 0}
                                    status={item.position}
                                    weight_pct={item.weight_pct ?? 0}
                                    floating_pnl={item.value_raw ?? 0}
                                    isDropdownOpen={activeDropdown === rowId}
                                    onToggleDropdown={(id) => setActiveDropdown(activeDropdown === id ? null : id)}
                                />
                            );
                        })}
                    </tbody>
                </table>
            </div>

            {/* No Results Message */}
            {filteredData.length === 0 && (
                <div className="p-12 flex items-center justify-center">
                    <div className="flex flex-col items-center gap-4">
                        <span className="material-symbols-outlined text-4xl text-slate-400">search_off</span>
                        <p className="text-slate-500 dark:text-slate-400">No stocks match your filters</p>
                        <button
                            onClick={clearFilters}
                            className="px-4 py-2 bg-primary hover:bg-[#3cd610] text-slate-900 rounded-lg text-sm font-medium transition-colors"
                        >
                            Clear Filters
                        </button>
                    </div>
                </div>
            )}

            {/* Pagination Footer */}
            {filteredData.length > 0 && (
                <div className="p-4 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-4">
                    {/* Left: Row count info */}
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-slate-500 dark:text-slate-400">
                            Showing <span className="font-bold text-slate-900 dark:text-white">{startIndex + 1}-{Math.min(endIndex, totalRows)}</span> of <span className="font-bold text-slate-900 dark:text-white">{totalRows}</span> rows
                        </span>

                        {/* Rows per page selector */}
                        <div className="flex items-center gap-2">
                            <span className="text-sm text-slate-500 dark:text-slate-400">Rows:</span>
                            <select
                                value={rowsPerPage}
                                onChange={(e) => handleRowsPerPageChange(Number(e.target.value))}
                                className="bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-lg px-2 py-1 text-sm text-slate-900 dark:text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                            >
                                <option value={10}>10</option>
                                <option value={20}>20</option>
                                <option value={30}>30</option>
                                <option value={50}>50</option>
                            </select>
                        </div>
                    </div>

                    {/* Right: Page navigation */}
                    <div className="flex items-center gap-2">
                        {/* Previous button */}
                        <button
                            onClick={() => handlePageChange(currentPage - 1)}
                            disabled={currentPage === 1}
                            className={`p-2 rounded-lg transition-colors ${currentPage === 1
                                ? 'text-slate-300 dark:text-slate-600 cursor-not-allowed'
                                : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                                }`}
                        >
                            <span className="material-symbols-outlined text-[20px]">chevron_left</span>
                        </button>

                        {/* Page numbers */}
                        {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                            let pageNum;
                            if (totalPages <= 5) {
                                pageNum = i + 1;
                            } else if (currentPage <= 3) {
                                pageNum = i + 1;
                            } else if (currentPage >= totalPages - 2) {
                                pageNum = totalPages - 4 + i;
                            } else {
                                pageNum = currentPage - 2 + i;
                            }

                            return (
                                <button
                                    key={pageNum}
                                    onClick={() => handlePageChange(pageNum)}
                                    className={`w-8 h-8 rounded-lg text-sm font-medium transition-colors ${pageNum === currentPage
                                        ? 'bg-primary text-white'
                                        : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                                        }`}
                                >
                                    {pageNum}
                                </button>
                            );
                        })}

                        {/* Next button */}
                        <button
                            onClick={() => handlePageChange(currentPage + 1)}
                            disabled={currentPage === totalPages}
                            className={`p-2 rounded-lg transition-colors ${currentPage === totalPages
                                ? 'text-slate-300 dark:text-slate-600 cursor-not-allowed'
                                : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                                }`}
                        >
                            <span className="material-symbols-outlined text-[20px]">chevron_right</span>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default AnalysisTable;
