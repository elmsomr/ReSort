// src/components/LiveData.js
import React, { useEffect, useState } from "react";

function LiveData() {
  const [wasteData, setWasteData] = useState([]);

  useEffect(() => {
    fetchWasteData();
    const interval = setInterval(fetchWasteData, 5000); // Her 5 saniyede bir güncelle
    return () => clearInterval(interval);
  }, []);

  const fetchWasteData = () => {
    fetch("http://localhost:5000/api/waste")
      .then((res) => res.json())
      .then((data) => setWasteData(data))
      .catch((err) => console.error("Veri alınamadı:", err));
  };

  return (
    <div style={{ margin: "2rem" }}>
      <h2>Canlı Atık Verileri</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Tarih ve Saat</th>
            <th style={{ border: "1px solid #ddd", padding: "8px" }}>Atık Cinsi</th>
          </tr>
        </thead>
        <tbody>
          {wasteData.length === 0 ? (
            <tr>
              <td colSpan="2" style={{ border: "1px solid #ddd", padding: "8px", textAlign: "center" }}>
                Henüz veri yok.
              </td>
            </tr>
          ) : (
            wasteData.map((item) => (
              <tr key={item.id}>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  {new Date(item.timestamp).toLocaleString()}
                </td>
                <td style={{ border: "1px solid #ddd", padding: "8px" }}>
                  {item.class}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default LiveData;
