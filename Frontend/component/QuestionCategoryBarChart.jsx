import { BarChart, Legend, XAxis, YAxis, CartesianGrid, 
    Tooltip, Bar, ResponsiveContainer,Cell } from 'recharts';

function QuestionCategoryBarChart() {
    const categoryData = [
        { category : "กองบริหารวิชาการ", amount : 10 },
        { category : "สำนักดิจิทัล", amount : 20 },
        { category : "กองกิจการนักศึกษา", amount : 5 },
        { category : "อื่นๆ", amount : 1 }
    ];
    const COLORS = ['#FF6B6B', '#4ECDC4', '#FFC33C', '#5B6B7C'];
    return (
        <div className="p-2 w-full h-[300px] rounded-md shadow-md bg-white"> 
            <p className="p-2 text-3xl font-light-bold">{"Bar Chart"}</p>
            
            <ResponsiveContainer width="100%" height="80%">
                <BarChart 
                    layout="horizontal" 
                    data={categoryData}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <Tooltip />
                    <YAxis type="number" /> 
                    <XAxis dataKey="category" type="category" /> 
                    <Bar dataKey="amount" name="จำนวนคำถามที่พบ" fill="#007A6D">
                        {
                            categoryData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))
                        }
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};
export default QuestionCategoryBarChart;