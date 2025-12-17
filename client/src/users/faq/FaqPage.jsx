import React, { useState } from 'react';
import { Header } from '../dashboard/dashboard';

const FaqPage = () => {
    const [openIndex, setOpenIndex] = useState(null);

    const faqs = [
        {
            question: "Apa itu Theory Bandarmology?",
            answer: "Theory Bandarmology adalah metode analisis saham yang mempelajari pergerakan dan akumulasi saham oleh broker-broker besar (bandar). Dengan memahami pola transaksi ini, investor dapat mengidentifikasi saham yang sedang diakumulasi atau didistribusi."
        },
        {
            question: "Bagaimana cara mendapatkan data broker dari Stockbit?",
            answer: "Untuk mendapatkan data broker: 1) Buka Stockbit dan login ke akun Anda, 2) Buka Developer Tools (F12), 3) Pergi ke tab Network, 4) Buka halaman Broker Summary pada saham yang diinginkan, 5) Copy response JSON dari request API broker activity."
        },
        {
            question: "Apa arti status PROFIT dan LOSS?",
            answer: "Status PROFIT menunjukkan bahwa harga pasar saat ini lebih tinggi dari harga rata-rata pembelian broker, yang berarti broker sedang untung. Status LOSS menunjukkan sebaliknya, harga pasar lebih rendah dari harga beli broker."
        },
        {
            question: "Bagaimana cara membaca data visualisasi?",
            answer: "Pada halaman Visualization, bar chart menunjukkan top 5 saham dengan nilai akumulasi tertinggi. Donut chart menampilkan rasio saham yang profit vs loss. Tabel activity menampilkan detail transaksi broker."
        },
        {
            question: "Seberapa akurat data yang ditampilkan?",
            answer: "Data yang ditampilkan berdasarkan informasi dari Stockbit dan harga real-time dari Yahoo Finance. Akurasi bergantung pada kelengkapan data broker dan timing pengambilan harga. Selalu gunakan data ini sebagai referensi tambahan, bukan satu-satunya dasar keputusan investasi."
        },
        {
            question: "Apakah data broker menunjukkan net buy/sell?",
            answer: "Ya, data yang dianalisis adalah NET position broker, yaitu selisih antara total pembelian dan penjualan. Nilai positif menunjukkan broker net buy, negatif menunjukkan net sell."
        },
    ];

    const toggleFaq = (index) => {
        setOpenIndex(openIndex === index ? null : index);
    };

    return (
        <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen">
            <div className="relative flex min-h-screen w-full flex-col">
                <Header />

                <div className="flex flex-1 justify-center py-8 px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col max-w-[900px] flex-1 gap-8">
                        {/* Page Heading */}
                        <div className="flex flex-col gap-2">
                            <h1 className="text-3xl md:text-4xl font-black leading-tight tracking-tight text-slate-900 dark:text-white">
                                Frequently Asked Questions
                            </h1>
                            <p className="text-slate-500 dark:text-slate-400 text-base md:text-lg font-normal">
                                Jawaban untuk pertanyaan umum tentang Theory Bandarmology
                            </p>
                        </div>

                        {/* FAQ Accordion */}
                        <div className="flex flex-col gap-4">
                            {faqs.map((faq, index) => (
                                <div
                                    key={index}
                                    className="rounded-md bg-white dark:bg-background-dark border border-slate-200 dark:border-border-dark overflow-hidden"
                                >
                                    <button
                                        className="w-full px-6 py-4 flex items-center justify-between text-left hover:bg-slate-50 dark:hover:bg-background-dark/50 transition-colors"
                                        onClick={() => toggleFaq(index)}
                                    >
                                        <span className="text-slate-900 dark:text-white font-semibold pr-4">
                                            {faq.question}
                                        </span>
                                        <span className={`material-symbols-outlined text-primary transition-transform duration-200 ${openIndex === index ? 'rotate-180' : ''}`}>
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

                        {/* Contact Section */}
                        <div className="rounded-xl bg-primary/10 border border-primary/30 p-6 text-center">
                            <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
                                Masih punya pertanyaan?
                            </h3>
                            <p className="text-slate-600 dark:text-text-muted mb-4">
                                Hubungi kami jika Anda membutuhkan bantuan lebih lanjut
                            </p>
                            <a
                                href="mailto:support@example.com"
                                className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white font-bold rounded-lg hover:bg-blue-600 transition-colors"
                            >
                                <span className="material-symbols-outlined text-[20px]">mail</span>
                                Hubungi Kami
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FaqPage;
