const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const analyzeData = async (rawJson) => {
    let jsonData;
    try {
        jsonData = JSON.parse(rawJson);
    } catch (e) {
        throw new Error('JSON tidak valid. Pastikan format JSON benar.');
    }

    const response = await fetch(`${API_BASE_URL}/v1/stock/analyze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat menganalisis data');
    }

    return response.json();
};

export const analyzeQuant = async (stock) => {
    const response = await fetch(`${API_BASE_URL}/v1/stock/analyze/quant`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stocks: [stock] }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat menganalisis kuantitatif');
    }

    return response.json();
};

export const analyzeTechnical = async (stock) => {
    const response = await fetch(`${API_BASE_URL}/v1/stock/analyze/technical`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stocks: [stock] }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat menganalisis teknikal');
    }

    return response.json();
};

export const analyzeFundamental = async (stock) => {
    const response = await fetch(`${API_BASE_URL}/v1/stock/analyze/fundamental`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stocks: [stock] }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat menganalisis fundamental');
    }

    return response.json();
}

export const analyzeNews = async (stock) => {
    const response = await fetch(`${API_BASE_URL}/v1/stock/analyze/news`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stocks: [stock] }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat menganalisis news');
    }

    return response.json();
}

export const getCompanyProfile = async (stock_code) => {
    const response = await fetch(`${API_BASE_URL}/v1/stock/company-profile/${stock_code}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    console.log("getCompanyProfile: ", response);

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat menganalisis news');
    }

    return response.json();
}

export const importRecentData = async (rawJson) => {
    let jsonData;
    try {
        jsonData = JSON.parse(rawJson);
    } catch (e) {
        throw new Error('JSON tidak valid. Pastikan format JSON benar.');
    }

    const response = await fetch(`${API_BASE_URL}/v1/stock/import-recent-data`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat mengimport data');
    }

    return response.json();
};

export const getNewsSymbol = async (symbol, limit = 20, type = "forex") => {
    const response = await fetch(`${API_BASE_URL}/v1/${symbol}/get-news?limit=${limit}&type=${type}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat mengambil data berita');
    }

    return response.json();
};

export const getSentimentSymbol = async (symbol, limit = 20, type = "forex") => {
    const response = await fetch(`${API_BASE_URL}/v1/${symbol}/news-sentiment?limit=${limit}&type=${type}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Terjadi kesalahan saat mengambil data sentimen berita');
    }

    return response.json();
};