import React from 'react';
import Error from '../common/Error';

const NewsCard = ({ data, isLoading }) => {
    if (isLoading) {
        return (
            <div className="bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark p-6 animate-pulse">
                <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded w-1/3 mb-4"></div>
                <div className="space-y-3">
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-full"></div>
                    <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3"></div>
                </div>
            </div>
        );
    }

    if (!data) {
        return (
            <Error error="Data news tidak tersedia" />
        );
    }

    const getMoodColor = (mood) => {
        if (mood.includes('Bullish')) return 'text-green-500';
        if (mood.includes('Bearish')) return 'text-red-500';
        return 'text-slate-400';
    };

    const getSentimentBadge = (sentiment) => {
        if (sentiment === 'Positive') return 'bg-green-500/10 border-green-500/20 text-green-700 dark:text-green-300';
        if (sentiment === 'Negative') return 'bg-red-500/10 border-red-500/20 text-red-700 dark:text-red-300';
        return 'bg-slate-500/10 border-slate-500/20 text-slate-700 dark:text-slate-300';
    };

    return (
        <div className='w-full bg-white dark:bg-card-dark rounded-2xl border border-slate-200 dark:border-border-dark overflow-hidden'>
            <div className="p-4 border-b border-slate-200 dark:border-border-dark bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">newspaper</span>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white">News & Sentiment</h3>
                </div>
                <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Recent news (7 days) from Google News Indonesia</p>
            </div>

            <div className='p-6 space-y-6'>
                {/* News Summary */}
                <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-lg">
                    <div>
                        <p className="text-sm text-slate-500 dark:text-slate-400">News Found</p>
                        <p className="text-2xl font-bold text-slate-900 dark:text-white">{data.news_count || 0}</p>
                    </div>
                    <div className="text-right">
                        <p className="text-sm text-slate-500 dark:text-slate-400">Narrative Mood</p>
                        <p className={`text-lg font-bold ${getMoodColor(data.narrative_mood)}`}>
                            {data.narrative_mood || 'Neutral'}
                        </p>
                    </div>
                </div>

                {/* News List */}
                {data.headlines && data.headlines.length > 0 ? (
                    <div className="space-y-3">
                        <h4 className="text-sm font-bold text-slate-700 dark:text-slate-300">📰 Headlines</h4>
                        {data.headlines.map((news, idx) => (
                            <>
                                <div className="flex items-start gap-3 block p-4 bg-slate-50 dark:bg-slate-800 rounded-md hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
                                    <span className="material-symbols-outlined text-primary mt-1">article</span>
                                    <div className="flex-1">
                                        <p className="font-medium text-slate-900 dark:text-white mb-2 line-clamp-2">
                                            {news.title}
                                        </p>
                                        <div className="flex items-center gap-2 flex-wrap">
                                            <span className="text-xs text-slate-500 dark:text-slate-400">
                                                {news.date}
                                            </span>
                                            <span className={`text-xs px-2 py-0.5 rounded-full border ${getSentimentBadge(news.sentiment)}`}>
                                                {news.sentiment}
                                            </span>
                                            {news.category && news.category !== 'General' && (
                                                <span className="text-xs px-2 py-0.5 bg-primary/10 border border-primary/20 text-primary rounded-full">
                                                    {news.category}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <a
                                        key={idx}
                                        href={news.link}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <span className="material-symbols-outlined text-[24px] text-slate-400">open_in_new</span>
                                    </a>
                                </div>
                            </>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-8">
                        <span className="material-symbols-outlined text-[48px] text-slate-300 dark:text-slate-600 mb-2">newspaper</span>
                        <p className="text-slate-500 dark:text-slate-400">No recent news found for this stock</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default NewsCard;