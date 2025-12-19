import React from 'react';

// Placeholder competitor data
const PLACEHOLDER_COMPETITORS = [
    { symbol: 'BMRI', name: 'Bank Mandiri', logo: 'https://ui-avatars.com/api/?name=BM&background=3b82f6&color=fff&size=128' },
    { symbol: 'BBRI', name: 'Bank BRI', logo: 'https://ui-avatars.com/api/?name=BR&background=22c55e&color=fff&size=128' },
    { symbol: 'BBNI', name: 'Bank BNI', logo: 'https://ui-avatars.com/api/?name=BN&background=f59e0b&color=fff&size=128' },
    { symbol: 'BBTN', name: 'Bank BTN', logo: 'https://ui-avatars.com/api/?name=BT&background=8b5cf6&color=fff&size=128' }
];

const CompetitorLandscape = () => {
    return (
        <section className="bg-card-dark border border-border-dark rounded-md p-6">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">hub</span>
                    Competitor Landscape
                </h3>
                <span className="text-xs text-text-muted italic">Placeholder Data</span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {PLACEHOLDER_COMPETITORS.map((competitor, idx) => (
                    <div
                        key={idx}
                        className="flex flex-col items-center justify-center p-6 bg-[#0B1221] border border-border-dark rounded-md group hover:border-primary/50 transition-all cursor-pointer"
                    >
                        <div className="size-12 bg-white rounded-full flex items-center justify-center mb-3 grayscale group-hover:grayscale-0 transition-all overflow-hidden">
                            <img
                                alt={`${competitor.name} Logo`}
                                className="w-full h-full object-cover"
                                src={competitor.logo}
                            />
                        </div>
                        <span className="text-sm font-bold text-white">{competitor.symbol}</span>
                        <span className="text-xs text-text-muted mt-1 font-mono truncate w-full text-center">
                            {competitor.name}
                        </span>
                    </div>
                ))}
            </div>

            <div className="mt-4 p-3 bg-[#0B1221] border border-border-dark rounded-lg">
                <p className="text-xs text-text-muted">
                    <span className="text-primary font-bold">Note:</span> Competitor data not available from API. This is placeholder data for UI demonstration.
                </p>
            </div>
        </section>
    );
};

export default CompetitorLandscape;
