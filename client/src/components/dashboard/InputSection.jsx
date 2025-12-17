import React, { useState } from 'react';

const InputSection = ({ onAnalyze, isLoading }) => {
    const [brokerCode, setBrokerCode] = useState('');
    const [transactionDate, setTransactionDate] = useState(new Date().toISOString().split('T')[0]);
    const [rawJson, setRawJson] = useState('');

    const handleSubmit = () => {
        onAnalyze({
            brokerCode,
            transactionDate,
            rawJson,
        });
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 bg-white dark:bg-card-dark p-6 rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm">
            {/* Left Inputs */}
            <div className="lg:col-span-8 flex flex-col gap-6">
                {/* <div className="flex flex-wrap gap-4">
                    <label className="flex flex-col min-w-[200px] flex-1">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-2">Broker Code</span>
                        <input
                            className="form-input w-full rounded-full border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900/50 text-slate-900 dark:text-white px-5 h-12 focus:ring-2 focus:ring-primary focus:border-transparent transition-all placeholder:text-slate-400"
                            placeholder="e.g. YP, ZP, CS"
                            type="text"
                            value={brokerCode}
                            onChange={(e) => setBrokerCode(e.target.value)}
                        />
                    </label>
                    <label className="flex flex-col min-w-[200px] flex-1">
                        <span className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-2">Transaction Date</span>
                        <div className="relative">
                            <input
                                className="form-input w-full rounded-full border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900/50 text-slate-900 dark:text-white px-5 h-12 focus:ring-2 focus:ring-primary focus:border-transparent transition-all placeholder:text-slate-400"
                                type="date"
                                value={transactionDate}
                                onChange={(e) => setTransactionDate(e.target.value)}
                            />
                        </div>
                    </label>
                </div> */}
                <label className="flex flex-col flex-1 h-full">
                    <span className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-2">Raw Data (JSON)</span>
                    <textarea
                        className="form-textarea w-full rounded-3xl border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900/50 text-slate-900 dark:text-white p-5 min-h-[140px] focus:ring-2 focus:ring-primary focus:border-transparent transition-all font-mono text-sm leading-relaxed resize-none overflow-y-scroll scrollbar-hide"
                        placeholder="Paste your broker JSON export here..."
                        value={rawJson}
                        onChange={(e) => setRawJson(e.target.value)}
                    />
                </label>
            </div>
            {/* Right Action */}
            <div className="lg:col-span-4 flex flex-col justify-end gap-4 h-full">
                <div className="bg-slate-100 dark:bg-slate-800/50 rounded-3xl p-6 flex-1 flex flex-col justify-center items-center text-center border border-dashed border-slate-300 dark:border-slate-700">
                    <div className="mb-3 text-slate-400 dark:text-slate-500">
                        <span className="material-symbols-outlined text-4xl">upload_file</span>
                    </div>
                    <p className="text-sm text-slate-500 dark:text-slate-400">Drag & drop file or paste text</p>
                </div>
                <button
                    className="w-full cursor-pointer flex items-center justify-center gap-3 rounded-full h-14 bg-primary hover:bg-[#3cd610] text-slate-900 text-lg font-bold transition-transform active:scale-[0.98] shadow-lg shadow-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
                    onClick={handleSubmit}
                    disabled={isLoading || !rawJson.trim()}
                >
                    {isLoading ? (
                        <>
                            <span className="material-symbols-outlined animate-spin">progress_activity</span>
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <span className="material-symbols-outlined">analytics</span>
                            Analyze Broker
                        </>
                    )}
                </button>
            </div>
        </div>
    );
};

export default InputSection;
