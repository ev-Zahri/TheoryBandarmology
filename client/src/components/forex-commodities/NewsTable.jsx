import React, { useState } from 'react';

function NewsTable({ news, loading, error, onActionClick }) {
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10;

    if (loading) {
        return (
            <main className="flex-1 flex justify-center py-8 px-4 md:px-10">
                <div className="w-full max-w-[1200px] flex flex-col gap-8">
                    <section className="bg-surface-dark border border-border-dark rounded-xl overflow-hidden shadow-xl flex items-center justify-center p-12">
                        <div className="text-center">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                            <p className="text-text-secondary font-mono">Loading news...</p>
                        </div>
                    </section>
                </div>
            </main>
        );
    }

    if (error) {
        return (
            <main className="flex-1 flex justify-center py-8 px-4 md:px-10">
                <div className="w-full max-w-[1200px] flex flex-col gap-8">
                    <section className="bg-surface-dark border border-border-dark rounded-xl overflow-hidden shadow-xl p-8">
                        <div className="text-center">
                            <span className="material-symbols-outlined text-6xl text-danger mb-4">error</span>
                            <h3 className="text-xl font-bold text-white mb-2">Error Loading News</h3>
                            <p className="text-text-secondary">{error.message || 'Failed to fetch news data'}</p>
                        </div>
                    </section>
                </div>
            </main>
        );
    }

    if (!news || news.length === 0) {
        return (
            <main className="flex-1 flex justify-center py-8 px-4 md:px-10">
                <div className="w-full max-w-[1200px] flex flex-col gap-8">
                    <section className="bg-surface-dark border border-border-dark rounded-xl overflow-hidden shadow-xl p-12">
                        <div className="text-center">
                            <span className="material-symbols-outlined text-6xl text-text-secondary mb-4">inbox</span>
                            <h3 className="text-xl font-bold text-white mb-2">No News Found</h3>
                            <p className="text-text-secondary">Try refreshing or changing the symbol</p>
                        </div>
                    </section>
                </div>
            </main>
        );
    }

    // Pagination
    const totalPages = Math.ceil(news.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentNews = news.slice(startIndex, endIndex);

    const formatDate = (timestamp) => {
        const date = new Date(timestamp * 1000);
        const dateStr = date.toISOString().split('T')[0];
        const timeStr = date.toTimeString().split(' ')[0].substring(0, 5);
        return { date: dateStr, time: timeStr };
    };

    const getTypeBadge = (symbols) => {
        if (!symbols || symbols.length === 0) return { type: 'Unknown', color: 'gray' };

        const symbol = symbols[0].symbol;
        if (symbol.startsWith('FX:')) {
            return { type: 'Forex', color: 'blue' };
        } else if (symbol.startsWith('TVC:') || symbol.startsWith('COMEX:')) {
            return { type: 'Commodity', color: 'yellow' };
        }
        return { type: 'Other', color: 'gray' };
    };

    return (
        <main className="flex-1 flex justify-center py-8 px-4 md:px-10">
            <div className="w-full max-w-[1200px] flex flex-col gap-8">
                <section className="bg-surface-dark border border-border-dark rounded-xl overflow-hidden shadow-xl flex flex-col">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-[#0f1623] text-text-secondary text-xs uppercase tracking-wider border-b border-border-dark font-display">
                                    <th className="p-5 font-medium w-32">Symbol</th>
                                    <th className="p-5 font-medium w-32">Type</th>
                                    <th className="p-5 font-medium">Title</th>
                                    <th className="p-5 font-medium w-48 text-right">Published Date</th>
                                    <th className="p-5 font-medium w-16 text-center">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border-dark font-mono text-sm">
                                {currentNews.map((item, index) => {
                                    const { date, time } = formatDate(item.published);
                                    const badge = getTypeBadge(item.relatedSymbols);
                                    const symbol = item.relatedSymbols?.[0]?.symbol?.split(':')[1] || 'N/A';

                                    return (
                                        <tr key={item.id || index} className="group hover:bg-background-dark/50 transition-colors">
                                            <td className="p-5">
                                                <div className="font-bold text-white text-base">{symbol}</div>
                                            </td>
                                            <td className="p-5">
                                                <span className={`inline-flex items-center px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wide ${badge.color === 'blue'
                                                        ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                                                        : badge.color === 'yellow'
                                                            ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/20'
                                                            : 'bg-gray-500/10 text-gray-400 border border-gray-500/20'
                                                    }`}>
                                                    {badge.type}
                                                </span>
                                            </td>
                                            <td className="p-5">
                                                <span className="font-medium text-white font-display text-base block mb-1">
                                                    {item.title}
                                                </span>
                                                {item.short_description && (
                                                    <span className="text-xs text-text-secondary font-display line-clamp-1">
                                                        {item.short_description}
                                                    </span>
                                                )}
                                            </td>
                                            <td className="p-5 text-right text-text-secondary">
                                                {date} <span className="text-xs opacity-60 ml-1">{time}</span>
                                            </td>
                                            <td className="p-5 text-center">
                                                <button
                                                    onClick={() => onActionClick(item)}
                                                    className="text-text-secondary hover:text-white transition-colors p-2 rounded hover:bg-border-dark"
                                                >
                                                    <span className="material-symbols-outlined">more_vert</span>
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                    <div className="flex items-center justify-between px-6 py-4 border-t border-border-dark bg-[#0f1623]">
                        <p className="text-sm text-text-secondary font-mono">
                            Showing <span className="text-white font-bold">{startIndex + 1}-{Math.min(endIndex, news.length)}</span> of <span className="text-white font-bold">{news.length}</span> news items
                        </p>
                        <div className="flex gap-2">
                            <button
                                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                                disabled={currentPage === 1}
                                className="px-3 py-1.5 text-xs font-medium rounded border border-border-dark text-text-secondary hover:text-white hover:bg-border-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Previous
                            </button>
                            <button
                                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                                disabled={currentPage === totalPages}
                                className="px-3 py-1.5 text-xs font-medium rounded border border-border-dark text-text-secondary hover:text-white hover:bg-border-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Next
                            </button>
                        </div>
                    </div>
                </section>
            </div>
        </main>
    );
}

export default NewsTable;
