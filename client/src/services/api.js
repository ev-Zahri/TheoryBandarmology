const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const analyzeData = async (rawJson) => {
    let jsonData;
    try {
        jsonData = JSON.parse(rawJson);
    } catch (e) {
        throw new Error('JSON tidak valid. Pastikan format JSON benar.');
    }

    const response = await fetch(`${API_BASE_URL}/v1/analyze`, {
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

export const importRecentData = async (rawJson) => {
    let jsonData;
    try {
        jsonData = JSON.parse(rawJson);
    } catch (e) {
        throw new Error('JSON tidak valid. Pastikan format JSON benar.');
    }

    const response = await fetch(`${API_BASE_URL}/v1/import-recent-data`, {
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
