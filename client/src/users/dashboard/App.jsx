import React, { useState, useMemo } from 'react';
import { Header, SummaryCard, InputSection, AnalysisTable } from './dashboard';
import { analyzeData } from '../../services/api';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Extract stocks array from result
  const stocks = useMemo(() => {
    return analysisResult?.data || [];
  }, [analysisResult]);

  // Extract broker info
  const brokerInfo = useMemo(() => {
    return analysisResult?.broker_info || null;
  }, [analysisResult]);

  // Calculate summary stats
  const summaryStats = useMemo(() => {
    if (!stocks || stocks.length === 0) {
      return {
        totalValue: 0,
        winningStocks: 0,
        losingStocks: 0,
      };
    }

    const totalValue = stocks.reduce((sum, item) => sum + (item.value_raw || 0), 0);
    const winningStocks = stocks.filter(item => item.diff_pct > 0).length;
    const losingStocks = stocks.filter(item => item.diff_pct < 0).length;

    return { totalValue, winningStocks, losingStocks };
  }, [stocks]);

  // Format currency for display
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const handleAnalyze = async ({ rawJson }) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await analyzeData(rawJson);
      // result.data now contains { broker_info, stocks, total_stocks }
      setAnalysisResult(result.data || null);
    } catch (err) {
      setError(err.message);
      setAnalysisResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen">
      <div className="relative flex min-h-screen w-full flex-col">
        <Header />

        <div className="flex flex-1 justify-center py-8 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col max-w-[1280px] flex-1 gap-8">
            {/* Page Heading */}
            <div className="flex flex-col gap-2">
              <h1 className="text-3xl md:text-4xl font-black leading-tight tracking-tight text-slate-900 dark:text-white">
                Broker Analysis Dashboard
              </h1>
              <p className="text-slate-500 dark:text-slate-400 text-base md:text-lg font-normal">
                Analyze your broker data and track performance metrics
              </p>
            </div>

            {/* Broker Info Badge */}
            {brokerInfo && (
              <div className="bg-white dark:bg-card-dark rounded-2xl p-4 border border-slate-200 dark:border-border-dark flex flex-wrap items-center gap-4">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">business</span>
                  <span className="font-bold text-slate-900 dark:text-white">{brokerInfo.broker_code}</span>
                  <span className="text-slate-500 dark:text-slate-400">- {brokerInfo.broker_name}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                  <span className="material-symbols-outlined text-[16px]">calendar_today</span>
                  {brokerInfo.date_start} → {brokerInfo.date_end}
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-loss/10 border border-loss/30 rounded-2xl p-4 flex items-center gap-3">
                <span className="material-symbols-outlined text-loss">error</span>
                <p className="text-loss font-medium">{error}</p>
              </div>
            )}

            {/* Input Section */}
            <InputSection onAnalyze={handleAnalyze} isLoading={isLoading} />

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <SummaryCard
                title="Total Transacted Value"
                value={formatCurrency(summaryStats.totalValue)}
                icon="payments"
                variant="default"
              />
              <SummaryCard
                title="Winning Stocks"
                value={summaryStats.winningStocks.toString()}
                icon="emoji_events"
                trendText="Stocks closed in profit"
                variant="profit"
              />
              <SummaryCard
                title="Losing Stocks"
                value={summaryStats.losingStocks.toString()}
                icon="trending_down"
                trendText="Stocks closed in loss"
                variant="loss"
              />
            </div>

            {/* Analysis Table */}
            <AnalysisTable data={stocks} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
