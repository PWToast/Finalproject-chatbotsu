import { PieChart, Pie, Cell, ResponsiveContainer,Legend} from 'recharts'; 

const COLORS = ['#FF8042', '#0088FE'];

function UserSourcePieChart({data}) {
    const sourceData = [
        { title : "Web", amount : data?.web_users_count || 1 },
        { title : "Line", amount : data?.line_users_count || 1  }
    ];
    return (
        <div className="p-2 w-full h-[280px] rounded-md shadow-md bg-white">
            <p className="p-1 text-xl font-light-bold text-gray-500">{"สัดส่วนผู้ใช้"}</p>
            
            <ResponsiveContainer width="100%" height="85%">
                <PieChart>
                    <Pie 
                        data={sourceData}
                        dataKey="amount" 
                        nameKey="title"
                        innerRadius={0} 
                        outerRadius={65} 
                        labelLine={true} 
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
                    {/* <Legend // ป้าย แสดง line/web
                        layout="horizontal"
                        verticalAlign="bottom"
                    /> */}
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
};
export default UserSourcePieChart;