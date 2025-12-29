import React, { useState } from 'react';

function SearchBar({ onSearch, onRefresh, onFilterChange }) {
    const [searchTerm, setSearchTerm] = useState('');
    const [symbolType, setSymbolType] = useState('forex');

    const handleSearch = (e) => {
        e.preventDefault();
        if (onSearch) {
            onSearch(searchTerm);
        }
    };

    const handleRefresh = () => {
        if (onRefresh) {
            onRefresh();
        }
    };

    const handleTypeChange = (type) => {
        setSymbolType(type);
        if (onFilterChange) {
            onFilterChange(type);
        }
    };

    return (
        <div className="w-full max-w-[1200px] mx-auto px-4 md:px-10 pt-8">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white font-display mb-2">Forex & Commodities News</h1>
                    <p className="text-text-secondary">Real-time market intelligence and sentiment analysis.</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="relative group">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <span className="material-symbols-outlined text-text-secondary text-sm">search</span>
                        </div>
                        <form onSubmit={handleSearch}>
                            <input
                                className="h-10 bg-surface-dark border border-border-dark rounded-lg pl-9 pr-4 text-sm font-mono text-white placeholder-text-secondary focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all w-64 shadow-lg"
                                placeholder="Search symbol or keyword..."
                                type="text"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </form>
                    </div>
                    <div className="relative">
                        <select
                            value={symbolType}
                            onChange={(e) => handleTypeChange(e.target.value)}
                            className="h-10 px-4 bg-surface-dark border border-border-dark text-white font-medium rounded-lg hover:bg-border-dark transition-colors flex items-center gap-2 text-sm shadow-lg appearance-none pr-10 cursor-pointer"
                        >
                            <option value="forex">Forex</option>
                            <option value="commodity">Commodity</option>
                        </select>
                        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                            <span className="material-symbols-outlined text-text-secondary text-lg">expand_more</span>
                        </div>
                    </div>
                    <button
                        onClick={handleRefresh}
                        className="h-10 px-4 bg-primary text-background-dark font-bold rounded-lg hover:bg-green-400 transition-colors flex items-center gap-2 text-sm shadow-lg shadow-primary/10"
                    >
                        <span className="material-symbols-outlined text-lg">refresh</span>
                        Refresh
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SearchBar;
