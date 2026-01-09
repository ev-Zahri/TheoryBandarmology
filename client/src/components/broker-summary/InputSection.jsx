import React, { useState, useRef } from 'react';

const InputSection = ({ onAnalyze, isLoading }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef(null);

    const handleFileSelect = (file) => {
        // Validate file type
        if (!file.name.endsWith('.json')) {
            alert('File harus berformat JSON (.json)');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('Ukuran file terlalu besar. Maksimal 10MB');
            return;
        }

        setSelectedFile(file);
    };

    const handleFileInputChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileSelect(file);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileSelect(file);
        }
    };

    const handleSubmit = () => {
        if (selectedFile) {
            return onAnalyze({ file: selectedFile });
        }
    };

    const handleRemoveFile = () => {
        setSelectedFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 bg-white dark:bg-card-dark p-6 rounded-3xl border border-slate-200 dark:border-border-dark shadow-sm">
            {/* Left Upload Area */}
            <div className="lg:col-span-8 flex flex-col gap-6">
                <div className="flex flex-col flex-1 h-full">
                    <span className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-2">
                        Upload Broker Summary File (JSON)
                    </span>

                    {/* File Upload Drop Zone */}
                    <div
                        className={`flex-1 rounded-3xl border-2 border-dashed transition-all ${isDragging
                                ? 'border-primary bg-primary/5 dark:bg-primary/10'
                                : 'border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-900/50'
                            } p-8 flex flex-col items-center justify-center text-center min-h-[200px] cursor-pointer`}
                        onDragOver={handleDragOver}
                        onDragLeave={handleDragLeave}
                        onDrop={handleDrop}
                        onClick={() => fileInputRef.current?.click()}
                    >
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept=".json"
                            onChange={handleFileInputChange}
                            className="hidden"
                        />

                        {selectedFile ? (
                            <div className="flex flex-col items-center gap-4 w-full">
                                <div className="bg-primary/10 dark:bg-primary/20 rounded-2xl p-4">
                                    <span className="material-symbols-outlined text-5xl text-primary">
                                        description
                                    </span>
                                </div>
                                <div className="flex flex-col gap-1">
                                    <p className="text-lg font-bold text-slate-900 dark:text-white">
                                        {selectedFile.name}
                                    </p>
                                    <p className="text-sm text-slate-500 dark:text-slate-400">
                                        {formatFileSize(selectedFile.size)}
                                    </p>
                                </div>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        handleRemoveFile();
                                    }}
                                    className="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-300 text-sm font-medium transition-colors"
                                >
                                    <span className="material-symbols-outlined text-[18px]">close</span>
                                    Remove File
                                </button>
                            </div>
                        ) : (
                            <>
                                <div className="mb-4 text-slate-400 dark:text-slate-500">
                                    <span className="material-symbols-outlined text-6xl">
                                        upload_file
                                    </span>
                                </div>
                                <p className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
                                    Drop your JSON file here
                                </p>
                                <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
                                    or click to browse
                                </p>
                                <div className="flex items-center gap-2 text-xs text-slate-400 dark:text-slate-500">
                                    <span className="material-symbols-outlined text-[16px]">info</span>
                                    <span>Supported format: .json (max 10MB)</span>
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>

            {/* Right Action */}
            <div className="lg:col-span-4 flex flex-col justify-end gap-4 h-full">
                <div className="bg-gradient-to-br from-primary/10 to-primary/5 dark:from-primary/20 dark:to-primary/10 rounded-3xl p-6 flex-1 flex flex-col justify-center items-center text-center border border-primary/20">
                    <div className="mb-3 text-primary">
                        <span className="material-symbols-outlined text-5xl">analytics</span>
                    </div>
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
                        Broker Summary Analysis
                    </h3>
                    <p className="text-sm text-slate-600 dark:text-slate-400">
                        Upload XHR intercepted data from Stockbit broker summary
                    </p>
                </div>

                <button
                    className="w-full cursor-pointer flex items-center justify-center gap-3 rounded-full h-14 bg-primary hover:bg-[#3cd610] text-slate-900 text-lg font-bold transition-transform active:scale-[0.98] shadow-lg shadow-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
                    onClick={handleSubmit}
                    disabled={isLoading || !selectedFile}
                >
                    {isLoading ? (
                        <>
                            <span className="material-symbols-outlined animate-spin">progress_activity</span>
                            Processing...
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
