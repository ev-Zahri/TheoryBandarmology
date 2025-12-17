const Error = ({ error }) => {
    return (
        <div className="bg-loss/10 border border-loss/30 rounded-2xl p-4 flex items-center gap-3">
            <span className="material-symbols-outlined text-loss">error</span>
            <p className="text-loss font-medium">{error}</p>
        </div>
    );
};

export default Error;