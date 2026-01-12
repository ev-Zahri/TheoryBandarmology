import React, { useState } from 'react';
import { reloadTechnicalData, reloadFundamentalData, getMasterDataStats } from '../services/api';

function MasterDataReload() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState({ technical: false, fundamental: false });
    const [showPanel, setShowPanel] = useState(false);

    const fetchStats = async () => {
        try {
            const response = await getMasterDataStats();
            setStats(response.data);
        } catch (error) {
            console.error('Error fetching stats:', error);
        }
    };

    const handleReloadTechnical = async () => {
        if (!confirm('Reload technical data? This will take approximately 15-20 minutes.')) return;

        setLoading({ ...loading, technical: true });
        try {
            const response = await reloadTechnicalData();
            alert(`Technical data reload started! Estimated time: ${response.data.estimated_time_minutes} minutes`);
            // Refresh stats after a delay
            setTimeout(fetchStats, 2000);
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            setLoading({ ...loading, technical: false });
        }
    };

    const handleReloadFundamental = async () => {
        if (!confirm('Reload fundamental data? This will take approximately 15-20 minutes.')) return;

        setLoading({ ...loading, fundamental: true });
        try {
            const response = await reloadFundamentalData();
            alert(`Fundamental data reload started! Estimated time: ${response.data.estimated_time_minutes} minutes`);
            // Refresh stats after a delay
            setTimeout(fetchStats, 2000);
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            setLoading({ ...loading, fundamental: false });
        }
    };

    React.useEffect(() => {
        if (showPanel) {
            fetchStats();
        }
    }, [showPanel]);

    return (
        <div className="relative">
            {/* Toggle Button */}
            <button
                onClick={() => setShowPanel(!showPanel)}
                className="flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition-colors text-slate-700 dark:text-slate-300 text-sm font-medium"
            >
                <span className="material-symbols-outlined text-[20px]">database</span>
                Master Data
                <span className={`material-symbols-outlined text-[18px] transition-transform ${showPanel ? 'rotate-180' : ''}`}>
                    expand_more
                </span>
            </button>

            {/* Panel */}
            {showPanel && (
                <div className="absolute right-0 mt-2 w-[400px] bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 shadow-xl z-50">
                    <div className="p-4">
                        <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-4">
                            Master Data Management
                        </h3>

                        {/* Stats */}
                        {stats && (
                            <div className="space-y-3 mb-4">
                                {/* Technical Data Stats */}
                                <div className="p-3 bg-slate-50 dark:bg-slate-900 rounded-lg">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Technical Data
                                        </span>
                                        <span className={`text-xs px-2 py-1 rounded ${stats.technical.is_stale ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'}`}>
                                            {stats.technical.is_stale ? 'Stale' : 'Fresh'}
                                        </span>
                                    </div>
                                    <div className="text-xs text-slate-500 dark:text-slate-400">
                                        <div>Stocks: {stats.technical.total_stocks}</div>
                                        <div>Updated: {stats.technical.age || 'Never'}</div>
                                    </div>
                                </div>

                                {/* Fundamental Data Stats */}
                                <div className="p-3 bg-slate-50 dark:bg-slate-900 rounded-lg">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                                            Fundamental Data
                                        </span>
                                        <span className={`text-xs px-2 py-1 rounded ${stats.fundamental.is_stale ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' : 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'}`}>
                                            {stats.fundamental.is_stale ? 'Stale' : 'Fresh'}
                                        </span>
                                    </div>
                                    <div className="text-xs text-slate-500 dark:text-slate-400">
                                        <div>Stocks: {stats.fundamental.total_stocks}</div>
                                        <div>Updated: {stats.fundamental.age || 'Never'}</div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Reload Buttons */}
                        <div className="space-y-2">
                            <button
                                onClick={handleReloadTechnical}
                                disabled={loading.technical}
                                className="w-full px-4 py-2.5 bg-primary hover:bg-[#3cd610] disabled:bg-slate-300 disabled:cursor-not-allowed text-slate-900 font-medium rounded-lg transition-all flex items-center justify-center gap-2"
                            >
                                {loading.technical ? (
                                    <>
                                        <span className="material-symbols-outlined animate-spin text-[20px]">progress_activity</span>
                                        Reloading Technical...
                                    </>
                                ) : (
                                    <>
                                        <span className="material-symbols-outlined text-[20px]">refresh</span>
                                        Reload Technical Data
                                    </>
                                )}
                            </button>

                            <button
                                onClick={handleReloadFundamental}
                                disabled={loading.fundamental}
                                className="w-full px-4 py-2.5 bg-blue-500 hover:bg-blue-600 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2"
                            >
                                {loading.fundamental ? (
                                    <>
                                        <span className="material-symbols-outlined animate-spin text-[20px]">progress_activity</span>
                                        Reloading Fundamental...
                                    </>
                                ) : (
                                    <>
                                        <span className="material-symbols-outlined text-[20px]">refresh</span>
                                        Reload Fundamental Data
                                    </>
                                )}
                            </button>
                        </div>

                        {/* Info */}
                        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                            <div className="flex gap-2">
                                <span className="material-symbols-outlined text-blue-600 dark:text-blue-400 text-[20px]">info</span>
                                <div className="text-xs text-blue-700 dark:text-blue-300">
                                    <p className="font-medium mb-1">About Reload:</p>
                                    <ul className="list-disc list-inside space-y-1">
                                        <li>Fetches latest data from yfinance</li>
                                        <li>Takes 15-20 minutes (~900 stocks)</li>
                                        <li>Runs in background</li>
                                        <li>Anti-rate-limiting enabled</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default MasterDataReload;
