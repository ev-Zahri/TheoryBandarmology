import React, { useState } from 'react';

const CompanyHeader = ({ data, stockCode }) => {
    const [isDescriptionExpanded, setIsDescriptionExpanded] = useState(false);
    if (!data) return null;

    const { identity } = data;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Main Info Card */}
            <div className="lg:col-span-8 bg-card-dark border border-border-dark rounded-md p-6 relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -mr-16 -mt-16 pointer-events-none"></div>

                <div className="flex flex-col sm:flex-row gap-6 relative z-10">
                    {/* Logo Placeholder */}
                    <div className="size-24 rounded-xl bg-white p-2 flex-shrink-0 flex items-center justify-center border border-border-dark">
                        <div className="w-full h-full flex items-center justify-center text-4xl font-bold text-primary">
                            {stockCode.charAt(0)}
                        </div>
                    </div>

                    {/* Company Info */}
                    <div className="flex flex-col justify-between flex-1">
                        <div className='h-full'>
                            <div className="flex items-center gap-3 mb-1">
                                <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">{stockCode}</h1>
                                <span className="px-2 py-0.5 rounded text-xs font-mono font-medium bg-white/10 text-white border border-white/10">
                                    IDX:{stockCode}
                                </span>
                            </div>
                            <h2 className="text-lg text-text-muted font-medium mb-3">{identity?.name || stockCode}</h2>

                            {/* Description with expand/collapse */}
                            <div>
                                <p className={`text-sm text-text-muted leading-relaxed max-w-2xl transition-all ${isDescriptionExpanded ? '' : 'line-clamp-3'}`}>
                                    {identity?.description || 'No description available'}
                                </p>
                                {identity?.description && identity.description.length > 200 && (
                                    <button
                                        onClick={() => setIsDescriptionExpanded(!isDescriptionExpanded)}
                                        className="text-xs text-primary hover:underline mt-1 font-medium"
                                    >
                                        {isDescriptionExpanded ? 'Read less' : 'Read more'}
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* Tags */}
                        <div className="flex items-center gap-4 mt-4 flex-wrap">
                            {identity?.sector && (
                                <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                    {identity.sector}
                                </span>
                            )}
                            {identity?.industry && (
                                <span className="px-3 py-1 rounded-full text-xs font-medium bg-purple-500/10 text-purple-400 border border-purple-500/20">
                                    {identity.industry}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Info Card */}
            <div className="lg:col-span-4 bg-card-dark border border-border-dark rounded-md p-6 flex flex-col justify-center relative">
                <p className="text-sm text-text-muted font-medium mb-1">Company Info</p>
                <div className="grid grid-cols-2 gap-4 border-t border-border-dark pt-4 mt-4">
                    <div>
                        <p className="text-xs text-text-muted mb-1">Sector</p>
                        <p className="text-sm font-mono font-medium text-white truncate">{identity?.sector || '-'}</p>
                    </div>
                    <div>
                        <p className="text-xs text-text-muted mb-1">Industry</p>
                        <p className="text-sm font-mono font-medium text-white truncate">{identity?.industry || '-'}</p>
                    </div>
                    <div>
                        <p className="text-xs text-text-muted mb-1">Employees</p>
                        <p className="text-sm font-mono font-medium text-white">{identity?.employees?.toLocaleString() || '-'}</p>
                    </div>
                    <div>
                        <p className="text-xs text-text-muted mb-1">Website</p>
                        {identity?.website && identity?.website !== '#' ? (
                            <a href={identity.website} target="_blank" rel="noopener noreferrer" className="text-sm font-mono font-medium text-primary hover:underline truncate block">
                                Visit
                            </a>
                        ) : (
                            <p className="text-sm font-mono font-medium text-white">-</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CompanyHeader;
