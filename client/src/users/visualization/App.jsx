import React, { useMemo } from 'react';
import {
    VisualizationHeader,
    AccumulationBarChart,
    StatCard,
    DonutChart,
    ActivityTable
} from "./visualization";

const VisualizationApp = ({ analysisData = null, onBack }) => {
    // Extract stocks data
    const stocks = useMemo(() => {
        return analysisData?.stocks || [];
    }, [analysisData]);

    // Calculate statistics
    const stats = useMemo(() => {
        if (!stocks.length) {
            return {
                totalValue: 0,
                totalTrades: 0,
                winTrades: 0,
                lossTrades: 0,
                winPercent: 0,
                lossPercent: 0,
                changePercent: 0,
            };
        }

        const totalValue = stocks.reduce((sum, s) => sum + (s.value || 0), 0);
        const totalTrades = stocks.length;
        const winTrades = stocks.filter(s => s.diff_pct > 0).length;
        const lossTrades = stocks.filter(s => s.diff_pct < 0).length;
        const winPercent = totalTrades > 0 ? Math.round((winTrades / totalTrades) * 100) : 0;
        const lossPercent = 100 - winPercent;

        // Average change percent
        const avgChange = stocks.reduce((sum, s) => sum + (s.diff_pct || 0), 0) / totalTrades;

        return {
            totalValue,
            totalTrades,
            winTrades,
            lossTrades,
            winPercent,
            lossPercent,
            changePercent: avgChange,
        };
    }, [stocks]);

    // Top 5 stocks by value for bar chart
    const topStocks = useMemo(() => {
        return [...stocks]
            .sort((a, b) => b.value - a.value)
            .slice(0, 5);
    }, [stocks]);

    return (
        <div className="dark bg-background-light dark:bg-background-dark font-display min-h-screen">
            <div className="layout-container flex h-full grow flex-col">
                <VisualizationHeader onBack={onBack} />

                {/* Main Content */}
                <main className="flex-1 px-6 py-8 lg:px-10 w-full max-w-7xl mx-auto">
                    {/* Grid Layout */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        {/* Left Column: Large Bar Chart (Span 2) */}
                        <div className="lg:col-span-2 flex flex-col gap-6">
                            {/* Chart Card */}
                            <AccumulationBarChart
                                data={topStocks}
                                totalValue={stats.totalValue}
                                changePercent={stats.changePercent}
                            />

                            {/* Stats Row */}
                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                                <StatCard
                                    icon="swap_horiz"
                                    title="Total Trades"
                                    value={stats.totalTrades.toLocaleString()}
                                    change={5.2}
                                />
                                <StatCard
                                    icon="verified"
                                    title="Avg Win %"
                                    value={`${stats.winPercent}%`}
                                    change={1.8}
                                />
                                <StatCard
                                    icon="warning"
                                    title="Avg Loss %"
                                    value={`${stats.lossPercent}%`}
                                    change={-0.5}
                                />
                            </div>
                        </div>

                        {/* Right Column: Donut Chart (Span 1) */}
                        <div className="lg:col-span-1 flex flex-col h-full">
                            <DonutChart
                                winPercent={stats.winPercent}
                                lossPercent={stats.lossPercent}
                                winTrades={stats.winTrades}
                                lossTrades={stats.lossTrades}
                            />
                        </div>
                    </div>

                    {/* Bottom Table Section */}
                    <div className="mt-6">
                        <ActivityTable data={stocks.slice(0, 10)} />
                    </div>
                </main>
            </div>
        </div>
    );
};

export default VisualizationApp;
