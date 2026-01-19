import { BarChart, Legend, XAxis, YAxis, CartesianGrid, 
    Tooltip, Bar, ResponsiveContainer,Cell } from 'recharts';

function QuestionCategoryBarChart({data}) {
    const categoryData = [
        { category : "กองบริหารวิชาการ", amount : data?.total_agencies["กองบริหารวิชาการ"] || 0 },
        { category : "สำนักดิจิทัล", amount : data?.total_agencies["สำนักดิจิทัลเทคโนโลยี"] || 0 },
        { category : "กองกิจการนักศึกษา", amount : data?.total_agencies["กองกิจการนักศึกษา"] || 0 },
        { category : "อื่นๆ", amount : data?.total_agencies["อื่นๆ"] || 0 }
    ];
    const COLORS = ['#FF6B6B', '#4ECDC4', '#FFC33C', '#5B6B7C'];
    return (
        <div className="p-2 w-full h-[280px] rounded-md shadow-md bg-white"> 
            <p className="p-1 text-xl font-light-bold text-gray-500">{"ความถี่ของคำถามแต่ละหมวด"}
                <p className="text-sm font-light-bold text-gray-500">{"( โมเดลที่ใช้คัดแยกหมวดยังคงมีความคลาดเคลื่อนในบางกรณี )"}</p>
            </p>
            
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