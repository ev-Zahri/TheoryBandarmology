import React from 'react';

function SentimentModal({ isOpen, onClose, sentimentData, newsItem, loading }) {
    if (!isOpen) return null;

    const getSentimentColor = (sentiment) => {
        switch (sentiment?.toUpperCase()) {
            case 'BULLISH':
                return 'text-primary';
            case 'BEARISH':
                return 'text-danger';
            default:
                return 'text-yellow-400';
        }
    };

    const getSentimentIcon = (sentiment) => {
        switch (sentiment?.toUpperCase()) {
            case 'BULLISH':
                return 'trending_up';
            case 'BEARISH':
                return 'trending_down';
            default:
                return 'trending_flat';
        }
    };

    const getUrgencyBadge = (urgency) => {
        if (urgency === 1) {
            return (
                <span className="px-2 py-1 rounded bg-red-500/10 text-red-400 border border-red-500/20 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1">
                    <span className="material-symbols-outlined text-sm">bolt</span>
                    Urgency: Immediate
                </span>
            );
        } else if (urgency === 2) {
            return (
                <span className="px-2 py-1 rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1">
                    <span className="material-symbols-outlined text-sm">priority_high</span>
                    Normal Priority
                </span>
            );
        }
        return null;
    };

    const formatDate = (timestamp) => {
        const date = new Date(timestamp * 1000);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const getSymbolType = (symbols) => {
        if (!symbols || symbols.length === 0) return 'Unknown';
        const symbol = symbols[0].symbol;
        if (symbol.startsWith('FX:')) return 'Forex';
        if (symbol.startsWith('TVC:') || symbol.startsWith('COMEX:')) return 'Commodity';
        return 'Other';
    };

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
            <div className="absolute inset-0 bg-black/70 backdrop-blur-md" onClick={onClose}></div>

            <div className="relative w-full max-w-2xl bg-[#0B1221] border border-border-dark rounded-2xl shadow-2xl flex flex-col max-h-[90vh] animate-in fade-in zoom-in-95 duration-200">
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-border-dark bg-surface-dark/50">
                    <div className="flex items-center gap-3">
                        <div className="flex items-center justify-center size-8 rounded bg-primary/10 border border-primary/20 text-primary">
                            <span className="material-symbols-outlined text-lg">newspaper</span>
                        </div>
                        <div>
                            <h3 className="text-white font-bold text-sm tracking-wide font-display">NEWS DETAIL</h3>
                            <p className="text-[10px] text-text-secondary font-mono uppercase">
                                ID: {newsItem?.id?.substring(0, 20) || 'N/A'}
                            </p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="size-8 flex items-center justify-center rounded-lg text-text-secondary hover:text-white hover:bg-white/5 transition-colors"
                    >
                        <span className="material-symbols-outlined">close</span>
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
                    {loading ? (
                        <div className="flex items-center justify-center py-12">
                            <div className="text-center">
                                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                                <p className="text-text-secondary font-mono">Loading sentiment analysis...</p>
                            </div>
                        </div>
                    ) : sentimentData ? (
                        <>
                            {/* Symbol & Sentiment Header */}
                            <div className="mb-8 relative overflow-hidden rounded-xl border border-primary/30 bg-surface-dark group">
                                <div className="absolute top-0 right-0 w-64 h-full bg-gradient-to-l from-primary/10 to-transparent pointer-events-none"></div>
                                <div className="p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative z-10">
                                    <div className="flex items-center gap-4">
                                        <div className="size-12 rounded-lg bg-background-dark border border-border-dark flex items-center justify-center shadow-lg">
                                            <span className="material-symbols-outlined text-primary text-2xl">currency_exchange</span>
                                        </div>
                                        <div>
                                            <div className="flex items-center gap-2 mb-1">
                                                <span className="font-bold text-xl text-white font-display">
                                                    {newsItem?.relatedSymbols?.[0]?.symbol || 'N/A'}
                                                </span>
                                                <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-border-dark text-text-secondary uppercase border border-border-dark tracking-wider">
                                                    {getSymbolType(newsItem?.relatedSymbols)}
                                                </span>
                                            </div>
                                            <div className="text-xs text-text-secondary font-medium uppercase tracking-wider">Market Sentiment</div>
                                        </div>
                                    </div>
                                    <div className="flex flex-col items-end">
                                        <div className={`flex items-center gap-2 mb-1 ${getSentimentColor(sentimentData.market_sentiment?.overall_sentiment)}`}>
                                            <span className="material-symbols-outlined text-xl fill-1" style={{ fontVariationSettings: "'FILL' 1" }}>
                                                {getSentimentIcon(sentimentData.market_sentiment?.overall_sentiment)}
                                            </span>
                                            <span className="text-2xl font-bold font-mono tracking-tight">
                                                {sentimentData.market_sentiment?.overall_sentiment || 'NEUTRAL'}
                                            </span>
                                        </div>
                                        <div className="flex items-center gap-1.5">
                                            <span className="text-[10px] text-primary/80 font-mono font-medium">
                                                Score: {sentimentData.market_sentiment?.weighted_score || 0}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* News Details */}
                            <div className="flex flex-col gap-5 mb-8">
                                <div className="flex flex-wrap items-center gap-2">
                                    {getUrgencyBadge(newsItem?.urgency)}
                                    {newsItem?.is_high_priority && (
                                        <span className="px-2 py-1 rounded bg-orange-500/10 text-orange-400 border border-orange-500/20 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1">
                                            <span className="material-symbols-outlined text-sm">priority_high</span>
                                            High Priority
                                        </span>
                                    )}
                                    <span className={`px-2 py-1 rounded border text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 ${sentimentData.market_sentiment?.overall_sentiment === 'BULLISH'
                                            ? 'bg-primary/10 text-primary border-primary/20'
                                            : sentimentData.market_sentiment?.overall_sentiment === 'BEARISH'
                                                ? 'bg-danger/10 text-danger border-danger/20'
                                                : 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20'
                                        }`}>
                                        <span className="material-symbols-outlined text-sm">thumb_up</span>
                                        {sentimentData.market_sentiment?.overall_sentiment || 'Neutral'}
                                    </span>
                                </div>
                                <h1 className="text-2xl md:text-3xl font-bold text-white leading-tight font-display">
                                    {newsItem?.title || 'No title available'}
                                </h1>
                                <div className="flex flex-wrap items-center gap-y-2 gap-x-6 text-sm text-text-secondary font-mono border-b border-border-dark pb-6">
                                    <div className="flex items-center gap-2">
                                        <span className="material-symbols-outlined text-lg text-primary">feed</span>
                                        <span className="text-white">{newsItem?.provider?.name || 'Unknown'}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="material-symbols-outlined text-lg">calendar_today</span>
                                        <span>{formatDate(newsItem?.published)}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Sentiment Metrics */}
                            {sentimentData.top_news && sentimentData.top_news.length > 0 && (
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                                    <div className="bg-surface-dark border border-border-dark rounded-lg p-4 flex flex-col items-center justify-center text-center">
                                        <span className="text-[10px] text-text-secondary uppercase tracking-wider mb-3 font-bold">Sentiment Score</span>
                                        <div className="text-3xl font-bold text-white font-mono mb-2">
                                            {sentimentData.top_news[0]?.sentiment_score?.toFixed(2) || '0.00'}
                                        </div>
                                        <span className={`text-xs font-bold ${getSentimentColor(sentimentData.top_news[0]?.sentiment)}`}>
                                            {sentimentData.top_news[0]?.sentiment || 'Neutral'}
                                        </span>
                                    </div>
                                    <div className="bg-surface-dark border border-border-dark rounded-lg p-4 flex flex-col items-center justify-center text-center">
                                        <span className="text-[10px] text-text-secondary uppercase tracking-wider mb-3 font-bold">AI Confidence</span>
                                        <div className="flex items-end gap-1 mb-2">
                                            <span className="text-3xl font-bold text-white font-mono leading-none">
                                                {Math.round((sentimentData.top_news[0]?.sentiment_confidence || 0) * 100)}
                                            </span>
                                            <span className="text-sm text-text-secondary font-mono mb-0.5">%</span>
                                        </div>
                                        <div className="w-24 bg-background-dark h-1.5 rounded-full overflow-hidden mb-1">
                                            <div className="bg-blue-400 h-full rounded-full" style={{ width: `${(sentimentData.top_news[0]?.sentiment_confidence || 0) * 100}%` }}></div>
                                        </div>
                                        <span className="text-xs text-blue-400 font-bold">High Reliability</span>
                                    </div>
                                    <div className="bg-surface-dark border border-border-dark rounded-lg p-4 flex flex-col items-center justify-center text-center">
                                        <span className="text-[10px] text-text-secondary uppercase tracking-wider mb-3 font-bold">Importance Score</span>
                                        <div className="flex items-end gap-1 mb-2">
                                            <span className="text-3xl font-bold text-white font-mono leading-none">
                                                {Math.round((sentimentData.top_news[0]?.importance_score || 0) * 100)}
                                            </span>
                                            <span className="text-sm text-text-secondary font-mono mb-0.5">/100</span>
                                        </div>
                                        <span className="text-xs text-danger font-bold">Market Impact</span>
                                    </div>
                                </div>
                            )}

                            {/* Market Summary */}
                            <div className="bg-surface-dark/50 border border-border-dark rounded-lg p-5">
                                <h4 className="text-xs font-bold text-white uppercase tracking-wider mb-3 flex items-center gap-2">
                                    <span className="material-symbols-outlined text-primary text-sm">auto_awesome</span>
                                    Market Summary
                                </h4>
                                <div className="text-text-secondary leading-relaxed text-sm space-y-2">
                                    <p>
                                        <strong className="text-white">Total News Analyzed:</strong> {sentimentData.market_sentiment?.news_count || 0}
                                    </p>
                                    <p>
                                        <strong className="text-white">Breakdown:</strong> {sentimentData.market_sentiment?.breakdown?.bullish || 0} Bullish, {sentimentData.market_sentiment?.breakdown?.bearish || 0} Bearish, {sentimentData.market_sentiment?.breakdown?.neutral || 0} Neutral
                                    </p>
                                    <p>
                                        <strong className="text-white">Overall Sentiment:</strong> {sentimentData.market_sentiment?.overall_sentiment || 'NEUTRAL'} with weighted score of {sentimentData.market_sentiment?.weighted_score || 0}
                                    </p>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="text-center py-12">
                            <span className="material-symbols-outlined text-6xl text-text-secondary mb-4">info</span>
                            <p className="text-text-secondary">No sentiment data available</p>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-border-dark bg-surface-dark/50 flex justify-end gap-3 rounded-b-2xl">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 rounded-lg border border-border-dark text-text-secondary hover:text-white hover:bg-surface-dark transition-colors text-sm font-medium"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
}

export default SentimentModal;
