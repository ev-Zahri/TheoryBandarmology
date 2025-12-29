import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import DashboardApp from './users/dashboard/App';
import VisualizationApp from './users/visualization/App';
import DeepAnalyzeApp from './users/deep-analyze/App';
import FaqPage from './users/faq/FaqPage';
import ForexCommoditiesApp from './users/forex-commodities/App';
import NotFoundPage from './users/errors/NotFoundPage';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardApp />} />
        <Route path="/visualization" element={<VisualizationApp />} />
        <Route path='/deep-analyze' element={<DeepAnalyzeApp />} />
        <Route path="/faq" element={<FaqPage />} />
        <Route path='/forex-commodities' element={<ForexCommoditiesApp />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

reportWebVitals();
