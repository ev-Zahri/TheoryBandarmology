import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
    return (
        <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen flex items-center justify-center">
            <div className="text-center px-6">
                {/* Error Icon */}
                <div className="mb-8">
                    <span className="material-symbols-outlined text-[120px] text-primary/50">
                        search_off
                    </span>
                </div>

                {/* Error Code */}
                <h1 className="text-8xl md:text-9xl font-black text-primary mb-4">
                    404
                </h1>

                {/* Error Message */}
                <h2 className="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white mb-4">
                    Halaman Tidak Ditemukan
                </h2>
                <p className="text-slate-500 dark:text-text-muted text-lg max-w-md mx-auto mb-8">
                    Maaf, halaman yang Anda cari tidak ada atau telah dipindahkan.
                </p>

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <Link
                        to="/"
                        className="inline-flex items-center gap-2 px-6 py-3 bg-primary text-white font-bold rounded-lg hover:bg-blue-600 transition-colors shadow-lg shadow-primary/20"
                    >
                        <span className="material-symbols-outlined text-[20px]">home</span>
                        Kembali ke Dashboard
                    </Link>
                    <button
                        onClick={() => window.history.back()}
                        className="inline-flex items-center gap-2 px-6 py-3 bg-surface-dark border border-border-dark text-white font-medium rounded-lg hover:bg-border-dark transition-colors"
                    >
                        <span className="material-symbols-outlined text-[20px]">arrow_back</span>
                        Halaman Sebelumnya
                    </button>
                </div>

                {/* Helpful Links */}
                <div className="mt-12 pt-8 border-t border-border-dark/50">
                    <p className="text-slate-500 dark:text-text-muted text-sm mb-4">
                        Atau coba halaman berikut:
                    </p>
                    <div className="flex flex-wrap items-center justify-center gap-4">
                        <Link to="/" className="text-primary hover:text-blue-400 text-sm font-medium">
                            Dashboard
                        </Link>
                        <span className="text-border-dark">•</span>
                        <Link to="/visualization" className="text-primary hover:text-blue-400 text-sm font-medium">
                            Visualization
                        </Link>
                        <span className="text-border-dark">•</span>
                        <Link to="/faq" className="text-primary hover:text-blue-400 text-sm font-medium">
                            FAQ
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NotFoundPage;
