import React, { useState, useMemo } from 'react';
import { Header, SummaryCard, InputSection, AnalysisTable } from './broker-summary';
import { uploadBrokerSummary } from '../../services/api';

function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async ({ file }) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await uploadBrokerSummary(file);
      setAnalysisResult(result.data || null);
    } catch (err) {
      setError(err.message);
      setAnalysisResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Get broker summaries array
  const brokerSummaries = useMemo(() => {
    return analysisResult?.broker_summaries || [];
  }, [analysisResult]);

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
                Analyze broker data from XHR intercepted responses
              </p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-loss/10 border border-loss/30 rounded-2xl p-4 flex items-center gap-3">
                <span className="material-symbols-outlined text-loss">error</span>
                <p className="text-loss font-medium">{error}</p>
              </div>
            )}

            {/* Input Section */}
            <InputSection onAnalyze={handleAnalyze} isLoading={isLoading} />

            {/* Display multiple broker summaries */}
            {brokerSummaries.length > 0 && (
              <div className="flex flex-col gap-8">
                {brokerSummaries.map((summary, index) => (
                  <BrokerSummarySection
                    key={index}
                    summary={summary}
                    index={index}
                    isLoading={isLoading}
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Component for each broker summary section
function BrokerSummarySection({ summary, index, isLoading }) {
  const { broker_info, stocks, summary: summaryStats } = summary;

  // Format currency for display
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  // Calculate winning and losing stocks
  const winningStocks = stocks.filter(item => item.diff_pct > 0).length;
  const losingStocks = stocks.filter(item => item.diff_pct < 0).length;

  return (
    <div className="flex flex-col gap-6">
      {/* Section Header */}
      <div className="flex items-center gap-3">
        <div className="h-10 w-1 bg-primary rounded-full"></div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">
          Broker Summary #{index + 1}
        </h2>
      </div>

      {/* Broker Info Badge */}
      {broker_info && (
        <div className="bg-white dark:bg-card-dark rounded-2xl p-4 border border-slate-200 dark:border-border-dark flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-primary">business</span>
            <span className="font-bold text-slate-900 dark:text-white">{broker_info.broker_code}</span>
            <span className="text-slate-500 dark:text-slate-400">- {broker_info.broker_name}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
            <span className="material-symbols-outlined text-[16px]">calendar_today</span>
            {broker_info.date_start} → {broker_info.date_end}
          </div>
          {broker_info.timestamp && (
            <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
              <span className="material-symbols-outlined text-[16px]">schedule</span>
              {new Date(broker_info.timestamp).toLocaleString('id-ID')}
            </div>
          )}
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <SummaryCard
          title="Net Position Value"
          value={summaryStats?.net_value_formatted || 'Rp 0'}
          icon="payments"
          variant={summaryStats?.position === 'NET BUY' ? 'profit' : summaryStats?.position === 'NET SELL' ? 'loss' : 'default'}
          trendText={summaryStats?.position || 'NEUTRAL'}
        />
        <SummaryCard
          title="Total Buy Value"
          value={summaryStats?.total_buy_value_formatted || 'Rp 0'}
          icon="trending_up"
          trendText={`${stocks.filter(s => s.buy_value > 0).length} stocks`}
          variant="profit"
        />
        <SummaryCard
          title="Total Sell Value"
          value={summaryStats?.total_sell_value_formatted || 'Rp 0'}
          icon="trending_down"
          trendText={`${stocks.filter(s => s.sell_value > 0).length} stocks`}
          variant="loss"
        />
      </div>

      {/* Analysis Table */}
      <AnalysisTable
        data={stocks}
        isLoading={isLoading}
        totalValue={summaryStats?.total_buy_value + summaryStats?.total_sell_value || 0}
      />
    </div>
  );
}

export default App;
