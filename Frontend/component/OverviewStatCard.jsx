function OverviewStatCard({ title, value, fontColor }) {
    const numberColor = fontColor;
    return (
        <div className="px-2 py-2 bg-white shadow-md rounded-md border border-0 border-black-500">
            <p className="text-lg font-light-bold text-gray-500 ">
                {title}
            </p>
            <p className={`m-2 text-4xl font-bold text-center ${numberColor}`}>
                {value}
            </p>
        </div>
    );
};
export default OverviewStatCard;