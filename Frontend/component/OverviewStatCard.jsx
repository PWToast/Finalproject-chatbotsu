function OverviewStatCard({ title, value, fontColor }) {
    const numberColor = fontColor;
    return (
        <div className="p-3 m-1 bg-white rounded-md border border-0 border-black-500">
            <p className="text-lg font-medium text-gray-500 ">
                {title}
            </p>
            <p className={`mt-1 text-4xl font-bold text-center ${numberColor}`}>
                {value}
            </p>
        </div>
    );
};
export default OverviewStatCard;