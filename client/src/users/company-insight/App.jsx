import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CompanyHeader, OwnershipChart, ManagementTeam, RevenueSegments, CompetitorLandscape, Header, Error } from "./company-insight";
import { getCompanyProfile } from "../../services/api";

function CompanyInsightPage() {
    const { stock_code } = useParams();
    const navigate = useNavigate();

    const [profileData, setProfileData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!stock_code) {
            navigate('/');
            return;
        }

        const fetchProfile = async () => {
            try {
                setIsLoading(true);
                setError(null);
                console.log("stock_code: ", stock_code);
                const response = await getCompanyProfile(stock_code);
                console.log("response: ", response);
                setProfileData(response.data);
            } catch (err) {
                console.error('Company profile error:', err);
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };

        fetchProfile();
    }, [stock_code, navigate]);

    return (
        <div className="dark bg-background-light dark:bg-background-dark text-slate-900 dark:text-white font-display min-h-screen">
            <div className="relative flex min-h-screen w-full flex-col">
                <Header />

                <main className="flex-grow py-8 px-4 sm:px-6 lg:px-8 max-w-[1400px] mx-auto w-full">
                    {/* Breadcrumb */}
                    <div className="flex items-center gap-2 text-sm text-text-muted mb-6">
                        <a className="hover:text-primary transition-colors cursor-pointer" onClick={() => navigate('/')}>Stocks</a>
                        <span className="material-symbols-outlined text-[16px]">chevron_right</span>
                        {profileData && (
                            <>
                                <a className="hover:text-primary transition-colors">{profileData.identity?.sector || 'Unknown'}</a>
                                <span className="material-symbols-outlined text-[16px]">chevron_right</span>
                            </>
                        )}
                        <span className="text-white font-medium">{stock_code}</span>
                    </div>

                    {/* Error State */}
                    {error && (
                        <Error error={error} />
                    )}

                    {/* Loading State */}
                    {isLoading && (
                        <div className="flex items-center justify-center py-20">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                        </div>
                    )}

                    {/* Main Content */}
                    {!isLoading && !error && profileData && (
                        <>
                            {/* Company Header */}
                            <CompanyHeader data={profileData} stockCode={stock_code} />

                            {/* Main Grid */}
                            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
                                {/* Left Column */}
                                <div className="lg:col-span-8 flex flex-col gap-6">
                                    <RevenueSegments />
                                    <CompetitorLandscape />
                                </div>

                                {/* Right Column */}
                                <div className="lg:col-span-4 flex flex-col gap-6">
                                    <OwnershipChart data={profileData.shareholders} />
                                    <ManagementTeam data={profileData.management} />
                                </div>
                            </div>
                        </>
                    )}
                </main>
            </div>
        </div>
    );
}

export default CompanyInsightPage;