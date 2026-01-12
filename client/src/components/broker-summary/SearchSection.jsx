import React, { useState } from 'react';

const SearchSection = ({ onSearch, searchResults = null, isSearching = false }) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [error, setError] = useState('');

    const validateStockCode = (code) => {
        // Stock code validation rules:
        // 1. Not empty
        // 2. Only uppercase letters, numbers, and hyphens
        // 3. Length between 2-10 characters
        if (!code || code.trim() === '') {
            return 'Stock code cannot be empty';
        }

        const trimmedCode = code.trim().toUpperCase();

        if (trimmedCode.length < 2 || trimmedCode.length > 10) {
            return 'Stock code must be between 2-10 characters';
        }

        // Allow letters, numbers, and hyphens only
        if (!/^[A-Z0-9-]+$/.test(trimmedCode)) {
            return 'Stock code can only contain letters, numbers, and hyphens';
        }

        return null;
    };

    const handleSearch = () => {
        const validationError = validateStockCode(searchQuery);

        if (validationError) {
            setError(validationError);
            return;
        }

        setError('');
        const normalizedQuery = searchQuery.trim().toUpperCase();
        onSearch(normalizedQuery);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    const handleInputChange = (e) => {
        const value = e.target.value.toUpperCase();
        setSearchQuery(value);

        // Clear error when user starts typing
        if (error) {
            setError('');
        }
    };

    const handleClear = () => {
        setSearchQuery('');
        setError('');
        onSearch(''); // Clear search results
    };

    return (
        <div className="bg-white dark:bg-card-dark rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm overflow-hidden">
            {/* Header */}
            <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800">
                <div className="flex items-center gap-3">
                    <div className="h-10 w-1 bg-primary rounded-full"></div>
                    <div>
                        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Universal Search</h2>
                        <p className="text-sm text-slate-500 dark:text-slate-400">Search for stocks across all broker summaries</p>
                    </div>
                </div>
            </div>

            {/* Search Input */}
            <div className="px-6 pb-4">
                <div className="flex gap-3 items-center justify-center">
                    <div className="flex-1">
                        <div className="flex gap-3 w-full">
                            <div className="relative flex-1">
                                <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-[20px]">
                                    search
                                </span>
                                <input
                                    type="text"
                                    placeholder="Enter stock code (e.g., BBCA, TLKM, ASII)"
                                    value={searchQuery}
                                    onChange={handleInputChange}
                                    onKeyPress={handleKeyPress}
                                    className={`w-full h-11 pl-11 pr-10 py-2.5 bg-slate-50 dark:bg-slate-900 border-2 rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-base font-mono ${error
                                        ? 'border-red-500 dark:border-red-500'
                                        : 'border-slate-200 dark:border-slate-700'
                                        }`}
                                    disabled={isSearching}
                                />
                                {searchQuery && (
                                    <button
                                        onClick={handleClear}
                                        className=""
                                    >
                                        <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 text-[20px]">close</span>
                                    </button>
                                )}
                            </div>
                            <button
                                onClick={handleSearch}
                                disabled={isSearching || !searchQuery}
                                className="h-11 px-6 bg-primary hover:bg-[#3cd610] disabled:bg-slate-300 disabled:cursor-not-allowed text-slate-900 font-bold rounded-lg transition-all flex items-center gap-2 shadow-lg hover:shadow-xl disabled:shadow-none whitespace-nowrap"
                            >
                                {isSearching ? (
                                    <>
                                        <span className="material-symbols-outlined animate-spin text-[20px]">progress_activity</span>
                                        <span className="text-sm">Searching...</span>
                                    </>
                                ) : (
                                    <>
                                        <span className="material-symbols-outlined text-[20px]">search</span>
                                        <span className="text-sm">Search</span>
                                    </>
                                )}
                            </button>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <div className="mt-4 flex items-center gap-2 text-red-500 text-sm">
                                <span className="material-symbols-outlined text-[18px]">error</span>
                                <span>{error}</span>
                            </div>
                        )}

                        {/* Helper Text */}
                        {!error && (
                            <p className="mt-4 text-xs text-slate-500 dark:text-slate-400">
                                Press <kbd className="px-2 py-1 bg-slate-200 dark:bg-slate-700 rounded text-xs font-mono">Enter</kbd> to search
                            </p>
                        )}
                    </div>

                </div>
            </div>

            {/* Search Results Summary */}
            {searchResults && (
                <div className="px-6 pb-6">
                    <div className={`p-4 rounded-lg border-2 ${searchResults.totalFound > 0
                        ? 'bg-primary/10 border-primary/30'
                        : 'bg-slate-100 dark:bg-slate-800 border-slate-300 dark:border-slate-600'
                        }`}>
                        <div className="flex items-center gap-3">
                            <span className={`material-symbols-outlined text-[32px] ${searchResults.totalFound > 0
                                ? 'text-primary'
                                : 'text-slate-400'
                                }`}>
                                {searchResults.totalFound > 0 ? 'check_circle' : 'info'}
                            </span>
                            <div>
                                <p className="font-bold text-slate-900 dark:text-white">
                                    {searchResults.totalFound > 0
                                        ? `Found in ${searchResults.totalFound} broker ${searchResults.totalFound === 1 ? 'summary' : 'summaries'}`
                                        : `No results found for "${searchResults.query}"`
                                    }
                                </p>
                                {searchResults.totalFound > 0 && (
                                    <p className="text-sm text-slate-600 dark:text-slate-400">
                                        Stock code: <span className="font-mono font-bold text-primary">{searchResults.query}</span>
                                    </p>
                                )}
                                {searchResults.totalFound === 0 && (
                                    <p className="text-sm text-slate-600 dark:text-slate-400">
                                        This stock is not present in any of the uploaded broker data
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* Broker List */}
                        {searchResults.totalFound > 0 && searchResults.brokers && (
                            <div className="mt-4 pt-4 border-t border-primary/20">
                                <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                                    Found in:
                                </p>
                                <div className="flex flex-wrap gap-2">
                                    {searchResults.brokers.map((broker, index) => (
                                        <div
                                            key={index}
                                            className="px-3 py-1 bg-white dark:bg-slate-700 border border-primary/30 rounded-lg text-sm"
                                        >
                                            <span className="font-bold text-primary">{broker.broker_code}</span>
                                            <span className="text-slate-500 dark:text-slate-400 mx-2">•</span>
                                            <span className="text-slate-600 dark:text-slate-300">{broker.date_range}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default SearchSection;
