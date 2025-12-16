import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    return (
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 px-10 py-4 bg-white dark:bg-[#1e293b]">
            <div className="flex items-center gap-4">
                <Link to="/" className="flex items-center gap-4">
                    <div className="size-8 text-primary">
                        <svg className="w-full h-full fill-current" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                            <path clipRule="evenodd" d="M24 0.757355L47.2426 24L24 47.2426L0.757355 24L24 0.757355ZM21 35.7574V12.2426L9.24264 24L21 35.7574Z" fillRule="evenodd"></path>
                        </svg>
                    </div>
                    <h2 className="text-xl font-bold leading-tight tracking-[-0.015em] dark:text-white">Theory Bandarmology</h2>
                </Link>
            </div>
            <div className="flex gap-2">
                <button className="flex size-10 cursor-pointer items-center justify-center overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                    <span className="material-symbols-outlined text-[20px]">light_mode</span>
                </button>
                <div className="relative">
                    <button
                        className="flex size-10 cursor-pointer items-center justify-center overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                    >
                        <span className="material-symbols-outlined text-[20px]">settings</span>
                    </button>
                    {isDropdownOpen && (
                        <div className="absolute right-0 top-full z-10 mt-2 w-48 rounded-lg bg-white shadow-lg dark:bg-slate-800 border border-slate-200 dark:border-slate-700 overflow-hidden">
                            <div className="py-1">
                                <Link
                                    to="/visualization"
                                    className="flex items-center gap-3 w-full px-4 py-3 text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-700 transition-colors"
                                    onClick={() => setIsDropdownOpen(false)}
                                >
                                    <span className="material-symbols-outlined text-[18px]">bar_chart</span>
                                    Visualization
                                </Link>
                                <Link
                                    to="/faq"
                                    className="flex items-center gap-3 w-full px-4 py-3 text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-700 transition-colors"
                                    onClick={() => setIsDropdownOpen(false)}
                                >
                                    <span className="material-symbols-outlined text-[18px]">help</span>
                                    FAQ
                                </Link>
                            </div>
                        </div>
                    )}
                </div>
                <button className="flex size-10 cursor-pointer items-center justify-center overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                    <span className="material-symbols-outlined text-[20px]">person</span>
                </button>
            </div>
        </header>
    );
};

export default Header;
