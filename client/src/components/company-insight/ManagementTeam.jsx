import React from 'react';

const ManagementTeam = ({ data }) => {
    if (!data || data.length === 0) {
        return (
            <section className="bg-card-dark border border-border-dark rounded-xl p-6 h-fit">
                <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-6">
                    <span className="material-symbols-outlined text-primary">groups</span>
                    Management  
                </h3>
                <p className="text-text-muted text-sm">No management data available</p>
            </section>
        );
    }

    // Show max 4 members initially
    const displayedMembers = data.slice(0, 4);

    return (
        <section className="bg-card-dark border border-border-dark rounded-md p-6 h-fit">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">groups</span>
                    Management
                </h3>
            </div>

            <div className="flex flex-col gap-4">
                {displayedMembers.map((member, idx) => (
                    <div
                        key={idx}
                        className="flex items-center gap-4 p-3 rounded-lg hover:bg-[#0B1221] transition-colors border border-transparent hover:border-border-dark cursor-pointer"
                    >
                        {/* Avatar */}
                        <div
                            className="size-10 rounded-full bg-cover bg-center"
                            style={{
                                backgroundImage: `url('${member.photo_url}')`,
                                backgroundColor: '#1e293b'
                            }}
                        />

                        {/* Info */}
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-bold text-white truncate">{member.name}</p>
                            <p className="text-xs text-text-muted truncate">{member.position}</p>
                        </div>

                        {/* Chevron */}
                        <span className="material-symbols-outlined text-[20px] text-text-muted hover:text-white transition-colors">
                            chevron_right
                        </span>
                    </div>
                ))}
            </div>

            {/* View All Button */}
            {data.length > 4 && (
                <div className="mt-4 pt-4 border-t border-border-dark text-center">
                    <button className="text-xs font-medium text-text-muted hover:text-white transition-colors">
                        View All Board Members ({data.length})
                    </button>
                </div>
            )}
        </section>
    );
};

export default ManagementTeam;
