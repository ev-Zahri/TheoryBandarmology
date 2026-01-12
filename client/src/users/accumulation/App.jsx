import React, { useState, useEffect } from 'react';
import AccumulationTable from '../../components/accumulation/AccumulationTable';

function App() {
    const [stocks, setStocks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [summary, setSummary] = useState(null);
    const [error, setError] = useState(null);

    const fetchAccumulationData = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:8000/v1/accumulation/stocks');
            const data = await response.json();

            if (response.ok) {
                setStocks(data.stocks || []);
            } else {
                setError(data.detail || 'Failed to fetch accumulation data');
            }
        } catch (err) {
            setError('Network error: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    const fetchSummary = async () => {
        try {
            const response = await fetch('http://localhost:8000/v1/accumulation/summary');
            const data = await response.json();

            if (response.ok) {
                setSummary(data.data);
            }
        } catch (err) {
            console.error('Error fetching summary:', err);
        }
    };

    useEffect(() => {
        fetchAccumulationData();
        fetchSummary();
    }, []);

    return (
        <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen">
            <div className="relative flex min-h-screen w-full flex-col">
                {/* Header */}
                <header className="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
                                    Stock Accumulation Detection
                                </h1>
                                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                                    Stocks appearing in 100% of transactions (Bandarmology Analysis)
                                </p>
                            </div>
                            <button
                                onClick={() => {
                                    fetchAccumulationData();
                                    fetchSummary();
                                }}
                                className="flex items-center gap-2 px-4 py-2 bg-primary hover:bg-[#3cd610] text-slate-900 font-medium rounded-lg transition-colors"
                            >
                                <span className="material-symbols-outlined text-[20px]">refresh</span>
                                Refresh
                            </button>
                        </div>
                    </div>
                </header>

                {/* Main Content */}
                <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
                    {/* Summary Cards */}
                    {summary && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm text-slate-500 dark:text-slate-400">Total Brokers</p>
                                        <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">
                                            {summary.total_brokers}
                                        </p>
                                    </div>
                                    <span className="material-symbols-outlined text-4xl text-primary">business</span>
                                </div>
                            </div>

                            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm text-slate-500 dark:text-slate-400">Accumulating Stocks</p>
                                        <p className="text-2xl font-bold text-green-600 dark:text-green-400 mt-1">
                                            {stocks.filter(s => s.net_volume > 0).length}
                                        </p>
                                    </div>
                                    <span className="material-symbols-outlined text-4xl text-green-600 dark:text-green-400">trending_up</span>
                                </div>
                            </div>

                            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="text-sm text-slate-500 dark:text-slate-400">Distributing Stocks</p>
                                        <p className="text-2xl font-bold text-red-600 dark:text-red-400 mt-1">
                                            {stocks.filter(s => s.net_volume < 0).length}
                                        </p>
                                    </div>
                                    <span className="material-symbols-outlined text-4xl text-red-600 dark:text-red-400">trending_down</span>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Info Alert */}
                    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-4 mb-6">
                        <div className="flex gap-3">
                            <span className="material-symbols-outlined text-blue-600 dark:text-blue-400 text-[24px]">info</span>
                            <div className="text-sm text-blue-700 dark:text-blue-300">
                                <p className="font-medium mb-1">About Accumulation Detection:</p>
                                <ul className="list-disc list-inside space-y-1">
                                    <li>Shows stocks appearing in <strong>100% of transactions</strong> within the same broker</li>
                                    <li><strong>Net Volume</strong> = Buy Volume - Sell Volume (positive = accumulating, negative = distributing)</li>
                                    <li>Data resets on each new upload</li>
                                    <li>Upload broker summary data to see accumulation patterns</li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    {/* Error Message */}
                    {error && (
                        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4 mb-6">
                            <div className="flex gap-3">
                                <span className="material-symbols-outlined text-red-600 dark:text-red-400">error</span>
                                <p className="text-red-700 dark:text-red-300">{error}</p>
                            </div>
                        </div>
                    )}

                    {/* Table */}
                    <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
                        <AccumulationTable stocks={stocks} loading={loading} />
                    </div>

                    {/* Last Updated */}
                    {summary && summary.last_updated && (
                        <div className="mt-4 text-center text-sm text-slate-500 dark:text-slate-400">
                            Last updated: {new Date(summary.last_updated).toLocaleString()}
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
}

export default App;
