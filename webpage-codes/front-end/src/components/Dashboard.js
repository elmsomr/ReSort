import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [wasteData, setWasteData] = useState([]);

  // PostgreSQL'den verileri çek
  useEffect(() => {
    axios.get("http://localhost:5000/api/waste")
      .then((response) => {
        setWasteData(response.data);
      })
      .catch((error) => console.error("Veri çekme hatası:", error));
  }, []);

  return (
    <div>
      <h2>Atık Verileri</h2>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ağırlık (kg)</th>
            <th>Enerji Tasarrufu (kWh)</th>
            <th>Kurtarılan Ağaç</th>
            <th>Zaman</th>
          </tr>
        </thead>
        <tbody>
          {wasteData.map((data) => (
            <tr key={data.id}>
              <td>{data.id}</td>
              <td>{data.weight} kg</td>
              <td>{data.energy_saved} kWh</td>
              <td>{data.trees_saved} ağaç</td>
              <td>{new Date(data.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
