import React from 'react';

// Placeholder data since backend doesn't provide this
const PLACEHOLDER_SEGMENTS = [
    { name: 'Product A', percent: 45.5, description: 'Main revenue contributor' },
    { name: 'Product B', percent: 28.3, description: 'Growing market segment' },
    { name: 'Product C', percent: 15.8, description: 'Stable revenue stream' },
    { name: 'Services', percent: 10.4, description: 'Support and maintenance' }
];

const RevenueSegments = () => {
    return (
        <section className="bg-card-dark border border-border-dark rounded-md p-6">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">pie_chart</span>
                    Revenue Segments
                </h3>
                <span className="text-xs text-text-muted italic">Placeholder Data</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {PLACEHOLDER_SEGMENTS.map((segment, idx) => (
                    <div
                        key={idx}
                        className="bg-[#0B1221] border border-border-dark rounded-md p-4 hover:border-primary/30 transition-colors"
                    >
                        <div className="flex justify-between items-end mb-2">
                            <span className="text-sm font-medium text-white">{segment.name}</span>
                            <span className="text-lg font-mono font-bold text-primary">{segment.percent}%</span>
                        </div>
                        <div className="w-full bg-gray-800 rounded-full h-2 mb-2">
                            <div
                                className="bg-primary h-2 rounded-full transition-all"
                                style={{ width: `${segment.percent}%` }}
                            />
                        </div>
                        <p className="text-xs text-text-muted">{segment.description}</p>
                    </div>
                ))}
            </div>

            <div className="mt-4 p-3 bg-[#0B1221] border border-border-dark rounded-lg">
                <p className="text-xs text-text-muted">
                    <span className="text-primary font-bold">Note:</span> Revenue segment data not available from API. This is placeholder data for UI demonstration.
                </p>
            </div>
        </section>
    );
};

export default RevenueSegments;
