import React from 'react';

const VisualizationHeader = ({ onBack }) => {
    return (
        <header className="w-full px-6 py-4 lg:px-10 border-b border-border-dark bg-background-dark/50 backdrop-blur-md sticky top-0 z-10">
            <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
                {/* Breadcrumbs & Back */}
                <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2 text-sm">
                        <a className="text-text-muted hover:text-white transition-colors" href="/">Dashboard</a>
                        <span className="text-text-muted">/</span>
                        <span className="text-white font-medium">Visualization</span>
                    </div>
                    <div className="flex items-center gap-3">
                        <button
                            onClick={onBack}
                            className="flex items-center justify-center w-8 h-8 rounded-full bg-surface-dark border border-border-dark hover:bg-primary hover:border-primary text-white transition-all group"
                        >
                            <span className="material-symbols-outlined text-[20px] group-hover:-translate-x-0.5 transition-transform">arrow_back</span>
                        </button>
                        <h1 className="text-white text-2xl font-bold tracking-tight">Stock Data Visualization</h1>
                    </div>
                </div>
                {/* Actions */}
                <div className="flex items-center gap-3">
                    <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-surface-dark border border-border-dark text-white text-sm font-medium hover:bg-border-dark transition-colors">
                        <span className="material-symbols-outlined text-[18px]">calendar_today</span>
                        <span>Last 7 Days</span>
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-bold shadow-lg shadow-primary/20 hover:bg-blue-600 transition-colors">
                        <span className="material-symbols-outlined text-[18px]">download</span>
                        <span>Export Report</span>
                    </button>
                </div>
            </div>
        </header>
    );
};

export default VisualizationHeader;
