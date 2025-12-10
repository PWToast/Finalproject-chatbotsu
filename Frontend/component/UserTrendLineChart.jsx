import { PieChart, Pie, Cell, ResponsiveContainer,Legend} from 'recharts'; 

const COLORS = ['#FF8042', '#0088FE'];

function UserTrendLineChart() {
    const sourceData = [
        { title : "web", amount : 10 },
        { title : "Line", amount : 60 }
    ];
    

    return (
        <div className="p-2 w-full h-[300px] rounded-md shadow-md bg-white"> {/* **กำหนดความสูงให้ div ภายนอก** */}
            <p className="p-2 text-3xl font-light-bold">{"Line Chart"}</p>
            
            <ResponsiveContainer width="100%" height="80%">
                <PieChart>
                    <Pie 
                        data={sourceData}
                        dataKey="amount" // ใช้ 'amount' ตามที่คุณกำหนด
                        nameKey="title"
                        innerRadius={0} 
                        outerRadius={80} 
                        labelLine={true} // เปิดเส้นเชื่อมสำหรับ Label ด้านนอก
                        label={({ title, amount, percent }) => 
                            `${title}: ${amount.toLocaleString()} (${(percent * 100).toFixed(0)}%)`
                        }
                    >
                        {sourceData.map((entry, index) => (
                            <Cell 
                                key={`cell-${index}`} 
                                fill={COLORS[index % COLORS.length]} 
                            />
                        ))}
                    </Pie>
                    <Legend // ป้าย แสดง line/web
                        layout="horizontal"
                        verticalAlign="bottom"
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};
export default UserTrendLineChart;