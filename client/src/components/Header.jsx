import React from 'react';

const Header = () => {
    return (
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 px-10 py-4 bg-white dark:bg-[#1e293b]">
            <div className="flex items-center gap-4">
                <div className="size-8 text-primary">
                    <svg className="w-full h-full fill-current" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <path clipRule="evenodd" d="M24 0.757355L47.2426 24L24 47.2426L0.757355 24L24 0.757355ZM21 35.7574V12.2426L9.24264 24L21 35.7574Z" fillRule="evenodd"></path>
                    </svg>
                </div>
                <h2 className="text-xl font-bold leading-tight tracking-[-0.015em] dark:text-white">StockDash</h2>
            </div>
            <div className="flex gap-2">
                <button className="flex size-10 cursor-pointer items-center justify-center overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                    <span className="material-symbols-outlined text-[20px]">notifications</span>
                </button>
                <button className="flex size-10 cursor-pointer items-center justify-center overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                    <span className="material-symbols-outlined text-[20px]">settings</span>
                </button>
                <button className="flex size-10 cursor-pointer items-center justify-center overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors">
                    <span className="material-symbols-outlined text-[20px]">person</span>
                </button>
            </div>
        </header>
    );
};

export default Header;
