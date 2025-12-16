import React from 'react';

const StatCard = ({ icon, title, value, change, changeLabel = 'vs last week' }) => {
    const isPositive = change >= 0;

    return (
        <div className="rounded-xl bg-surface-dark border border-border-dark p-5 flex flex-col gap-3 hover:border-primary/50 transition-colors">
            <div className="flex items-center gap-2 text-text-muted">
                <span className="material-symbols-outlined text-[20px]">{icon}</span>
                <span className="text-sm font-medium">{title}</span>
            </div>
            <div>
                <p className="text-white font-mono text-2xl font-bold">{value}</p>
                <p className={`${isPositive ? 'text-success' : 'text-danger'} text-sm font-medium mt-1`}>
                    {isPositive ? '+' : ''}{change}%
                    <span className="text-text-muted text-xs font-normal ml-1">{changeLabel}</span>
                </p>
            </div>
        </div>
    );
};

export default StatCard;
