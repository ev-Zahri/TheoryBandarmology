import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Header, Error, TechnicalCard, QuantCard, FooterCard } from './deep-analyze';
import { analyzeTechnical, analyzeQuant } from '../../services/api';

function DeepAnalyzePage() {
    const { stock } = useParams();
    const navigate = useNavigate();

    const [technicalData, setTechnicalData] = useState(null);
    const [quantData, setQuantData] = useState(null);
    const [isLoadingTechnical, setIsLoadingTechnical] = useState(true);
    const [isLoadingQuant, setIsLoadingQuant] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!stock) {
            navigate('/');
            return;
        }

        // Fetch technical analysis
        const fetchTechnical = async () => {
            try {
                setIsLoadingTechnical(true);
                const response = await analyzeTechnical(stock);
                // API returns array with single stock
                setTechnicalData(response.data?.[0] || null);
            } catch (err) {
                console.error('Technical analysis error:', err);
                setError(err.message);
            } finally {
                setIsLoadingTechnical(false);
            }
        };

        // Fetch quant analysis
        const fetchQuant = async () => {
            try {
                setIsLoadingQuant(true);
                const response = await analyzeQuant(stock);
                // API returns array with single stock
                setQuantData(response.data?.[0] || null);
            } catch (err) {
                console.error('Quant analysis error:', err);
                setError(err.message);
            } finally {
                setIsLoadingQuant(false);
            }
        };

        fetchTechnical();
        fetchQuant();
    }, [stock, navigate]);

    return (
        <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen">
            <div className="relative flex min-h-screen w-full flex-col">
                <Header />

                <div className="flex flex-1 justify-center py-8 px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col max-w-[1280px] flex-1 gap-8">
                        {/* Page Heading */}
                        <div className="flex items-center gap-4">
                            <button
                                onClick={() => navigate('/')}
                                className="flex items-center justify-center w-10 h-10 rounded-full bg-surface-dark border border-border-dark hover:bg-primary hover:border-primary text-white transition-all"
                            >
                                <span className="material-symbols-outlined text-[20px]">arrow_back</span>
                            </button>
                            <div className="flex flex-col gap-1">
                                <h1 className="text-3xl md:text-4xl font-black leading-tight tracking-tight text-slate-900 dark:text-white">
                                    Deep Analysis: <span className="text-primary">{stock}</span>
                                </h1>
                                <p className="text-slate-500 dark:text-slate-400 text-base md:text-lg font-normal">
                                    Technical & Quantitative Analysis
                                </p>
                            </div>
                        </div>

                        {/* Error Message */}
                        {error && (
                            <Error error={error} />
                        )}

                        {/* Analysis Cards Grid */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            <TechnicalCard data={technicalData} isLoading={isLoadingTechnical} />
                            <QuantCard data={quantData} isLoading={isLoadingQuant} />
                        </div>

                        <FooterCard />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default DeepAnalyzePage;
