import { LineChart, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Line,ResponsiveContainer } from 'recharts';


function QuestionCategoryBarChart() {
    const conversationData = [
    { month: 'Jan', count: 10 },
    { month: 'Feb', count: 2 },
    { month: 'Mar', count: 3 },
    { month: 'Apr', count: 10 },
    { month: 'May', count: 5 },
    { month: 'Jun', count: 0 },
    { month: 'Jul', count: 0 },
    { month: 'Aug', count: 0 },
    { month: 'Sep', count: 32 },
    { month: 'Oct', count: 44 },
    { month: 'Nov', count: 2},
    { month: 'Dec', count: 23 }, 
];
    const COLORS = ['#FF6B6B', '#4ECDC4', '#FFC33C', '#5B6B7C'];
    return (
        <div className="p-2 w-full h-[300px] rounded-md shadow-md bg-white"> 
            <p className="p-2 text-xl font-light-bold text-gray-500">{"จำนวนผู้ใช้ในแต่ละเดือน"}</p>
            
            <ResponsiveContainer width="100%" height="80%">
                <LineChart 
                    data={conversationData}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip />
                    <Legend />
                    <YAxis dataKey="count" type="number" name="จำนวนครั้ง"/> 
                    <XAxis dataKey="month" type="category" name="เวลา" /> 
                    <Line type="monotone" dataKey="count" name="จำนวนการสนทนา" stroke="#007A6D"/>
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};
export default QuestionCategoryBarChart;