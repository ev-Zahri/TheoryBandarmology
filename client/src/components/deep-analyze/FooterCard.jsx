import { useState } from "react";

const FooterCard = () => {
    const [openIndex, setOpenIndex] = useState(null);
    const faqs = [
        {
            question: "What is Technical Analysis?",
            answer: "Technical Analysis menggunakan Ichimoku Cloud untuk trend detection, Stochastic RSI untuk momentum, dan OBV Divergence untuk volume analysis."
        },
        {
            question: "What is Quantitative Analysis?",
            answer: "Quantitative Analysis menggunakan Z-Score untuk statistical pricing, ATR untuk volatility measurement, dan Pivot Points untuk support/resistance levels."
        },
        {
            question: "What is Data Source?",
            answer: "Data diambil dari Yahoo Finance dengan periode 1 tahun untuk perhitungan yang akurat."
        },
        {
            question: "What is ichimoku cloud?",
            answer: "Ichimoku Cloud adalah teknik analisis teknis yang menggunakan garis garis untuk mengidentifikasi trend, support, dan resistance."
        },
        {
            question: "What is stochastic rsi?",
            answer: "Stochastic RSI adalah teknik analisis teknis yang menggunakan garis garis untuk mengidentifikasi momentum."
        },
        {
            question: "What is obv divergence?",
            answer: "OBV Divergence adalah teknik analisis teknis yang menggunakan garis garis untuk mengidentifikasi volume analysis."
        },
        {
            question: "What is z-score?",
            answer: "Z-Score adalah teknik analisis teknis yang menggunakan garis garis untuk mengidentifikasi statistical pricing."
        },
        {
            question: "What is atr?",
            answer: "ATR adalah teknik analisis teknis yang menggunakan garis garis untuk mengidentifikasi volatility measurement."
        },
        {
            question: "What is pivot points?",
            answer: "Pivot Points adalah teknik analisis teknis yang menggunakan garis garis untuk mengidentifikasi support/resistance levels."
        }
    ]

    const toggleFaq = (index) => {
        setOpenIndex(openIndex === index ? null : index);
    }
    return (
        <div className="rounded-2xl bg-white dark:bg-background-dark border border-slate-200 dark:border-border-dark p-6">
            <div className="flex flex-col items-start">
                 <div className="flex flex-col gap-2">
                    <span className="font-semibold text-xl">
                        Frequently Asked Questions
                    </span>
                    <span className="text-sm">
                        Pertanyaan umum tentang teknikal dan quantative analysis
                    </span>
                </div>
                {/* FAQ Accordion */}
                <div className="flex flex-col gap-4 w-full mt-6">
                    {faqs.map((faq, index) => (
                        <div
                            key={index}
                            className="rounded-md bg-white dark:bg-background-dark border border-slate-200 dark:border-border-dark overflow-hidden w-full"
                        >
                            <button
                                className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 dark:hover:bg-background-dark/50 transition-colors"
                                onClick={() => toggleFaq(index)}
                            >
                                <span className="text-slate-900 dark:text-white font-semibold pr-4">
                                    {faq.question}
                                </span>
                                <span className={`material-symbols-outlined text-lg text-primary transition-transform duration-200 ${openIndex === index ? 'rotate-180' : ''}`}>
                                    expand_more
                                </span>
                            </button>
                            {openIndex === index && (
                                <div className="px-6 pb-4 text-slate-600 dark:text-text-muted dark:text-white leading-relaxed">
                                    {faq.answer}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default FooterCard;
