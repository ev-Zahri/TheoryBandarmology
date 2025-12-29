
import React, { useState, useEffect, useCallback } from "react";
import { Header, NewsTable, SentimentModal, SearchBar } from "./forex-commodities";
import { getNewsSymbol, getSentimentSymbol } from "../../services/api";

function ForexCommoditiesApp() {
    const [news, setNews] = useState([]);
    const [sentimentData, setSentimentData] = useState(null);
    const [selectedNews, setSelectedNews] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [modalOpen, setModalOpen] = useState(false);
    const [modalLoading, setModalLoading] = useState(false);
    const [symbol, setSymbol] = useState("XAUUSD");
    const [symbolType, setSymbolType] = useState("forex");
    const [limit] = useState(20);

    const fetchNews = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await getNewsSymbol(symbol, limit, symbolType);
            setNews(response.data || []);
        } catch (err) {
            setError(err);
            console.error("Error fetching news:", err);
        } finally {
            setLoading(false);
        }
    }, [symbol, limit, symbolType]);

    useEffect(() => {
        fetchNews();
    }, [fetchNews]);

    const handleActionClick = async (newsItem) => {
        setSelectedNews(newsItem);
        setModalOpen(true);
        setModalLoading(true);
        setSentimentData(null);

        try {
            // Use the SAME symbol and type as the news fetch to ensure cache HIT
            // This avoids fetching news again since we already have it cached
            const response = await getSentimentSymbol(symbol, limit, symbolType);
            setSentimentData(response);
        } catch (err) {
            console.error("Error fetching sentiment:", err);
            setError(err);
        } finally {
            setModalLoading(false);
        }
    };

    const handleCloseModal = () => {
        setModalOpen(false);
        setSelectedNews(null);
        setSentimentData(null);
    };

    const handleSearch = (searchTerm) => {
        // For now, just update the symbol
        if (searchTerm) {
            setSymbol(searchTerm.toUpperCase());
        }
    };

    const handleRefresh = () => {
        fetchNews();
    };

    const handleFilterChange = (type) => {
        setSymbolType(type);
    };

    return (
        <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen">
            <div className="relative flex min-h-screen w-full flex-col">
                <Header />
                <SearchBar
                    onSearch={handleSearch}
                    onRefresh={handleRefresh}
                    onFilterChange={handleFilterChange}
                />
                <NewsTable
                    news={news}
                    loading={loading}
                    error={error}
                    onActionClick={handleActionClick}
                />
                <SentimentModal
                    isOpen={modalOpen}
                    onClose={handleCloseModal}
                    sentimentData={sentimentData}
                    newsItem={selectedNews}
                    loading={modalLoading}
                />
            </div>
        </div>
    );
}

export default ForexCommoditiesApp;