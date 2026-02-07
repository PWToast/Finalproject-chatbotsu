import axios from "axios";
import { useState, useEffect } from "react";
import {
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Line,
  ResponsiveContainer,
} from "recharts";

function UserTrendLineChart() {
  const [data, setData] = useState([]);
  const [timeRange, setTimeRange] = useState("7days");
  useEffect(() => {
    const token = localStorage.getItem("token"); //auth
    axios
      .get(`http://localhost:8000/admin/user-trend?range=${timeRange}`, {
        headers: {
          //auth
          Authorization: `Bearer ${token}`, // แนบไปตามกติกา oauth2_scheme ของหลังบ้าน
        },
      })
      .then((res) => setData(res.data.data))
      .catch((err) => console.error(err));
    console.log(data);
  }, [timeRange]);

  return (
    <div className="p-2 w-full h-[280px] rounded-md shadow-md bg-white">
      <div className="flex justify-between items-center mb-4">
        <p className="p-1 text-xl font-light-bold text-gray-500">
          {"จำนวนการสนทนาในแต่ละช่วงเวลา"}
        </p>
        <div className="flex flex-wrap gap-2">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="text-sm border-1 border-gray-500 rounded p-1"
          >
            <option value="7days">7 วันล่าสุด</option>
            <option value="30days">30 วันล่าสุด</option>
            <option value="year">ปีนี้</option>
          </select>
        </div>
      </div>
      <ResponsiveContainer width="100%" height="80%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Legend />
          <YAxis />
          {/* แกน x ใส่ dataKey ตามที่filterเลือก  */}
          <XAxis dataKey="label" type="category" name="เวลา" />
          <Line
            type="monotone"
            dataKey="web_count"
            name="เว็บไซต์"
            stroke="#FF8042"
          />
          <Line
            type="monotone"
            dataKey="line_count"
            name="ไลน์"
            stroke="#0088FE"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
export default UserTrendLineChart;
