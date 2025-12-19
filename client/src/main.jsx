import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import DashboardApp from './users/dashboard/App.jsx';
import VisualizationApp from './users/visualization/App.jsx';
import FaqPage from './users/faq/FaqPage.jsx';
import NotFoundPage from './users/errors/NotFoundPage.jsx';
import DeepAnalyzeApp from './users/deep-analyze/App.jsx';
import CompanyInsightApp from './users/company-insight/App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<DashboardApp />} />
                <Route path="/visualization" element={<VisualizationApp />} />
                <Route path="/deep-analyze/:stock" element={<DeepAnalyzeApp />} />
                <Route path="/company-profile/:stock_code" element={<CompanyInsightApp />} />
                <Route path="/faq" element={<FaqPage />} />
                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </BrowserRouter>
    </React.StrictMode>
);
