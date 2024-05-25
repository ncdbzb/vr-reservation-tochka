import React, { useState } from "react";
import { Button, Table } from "antd";
import "antd/dist/reset.css"; // Импорт стилей Ant Design
import "./App.css"; // Импорт пользовательских стилей

const vrHeadsets = [
  { id: 1, name: "VR Headset 1" },
  { id: 2, name: "VR Headset 2" },
  { id: 3, name: "VR Headset 3" },
];

const hours = Array.from({ length: 24 }, (_, i) => i); // [0, 1, 2, ..., 23]

function App() {
  const [selectedHeadset, setSelectedHeadset] = useState(null);

  const handleHeadsetClick = (id) => {
    setSelectedHeadset(selectedHeadset === id ? null : id);
  };

  const handleBooking = (headsetId, hour) => {
    console.log(`Booking VR Headset ${headsetId} for ${hour}:00`);
    // Здесь можно добавить логику бронирования
  };

  const columns = [
    {
      title: "Time",
      dataIndex: "time",
      key: "time",
      align: 'center',
    },
    {
      title: "Occupied By",
      dataIndex: "occupiedBy",
      key: "occupiedBy",
      align: 'center',
      render: (text) => (text ? text : "-"),
    },
    {
      title: "Action",
      key: "action",
      align: 'center',
      render: (text, record) => (
        <Button type="primary" onClick={() => handleBooking(selectedHeadset, record.time)}>
          Забронировать
        </Button>
      ),
    },
  ];

  const data = hours.map(hour => ({
    key: hour,
    time: `${hour}:00`,
    occupiedBy: null, // Изначальное значение "-"
  }));

  return (
    <div className="app-container">
      <h1 style={{ color: "white" }}>VR Headset Booking</h1>
      <div style={{ marginBottom: "20px" }}>
        {vrHeadsets.map((headset) => (
          <Button
            key={headset.id}
            type={selectedHeadset === headset.id ? "primary" : "default"}
            onClick={() => handleHeadsetClick(headset.id)}
            style={{ margin: "5px" }}
          >
            {headset.name}
          </Button>
        ))}
      </div>
      {selectedHeadset !== null && (
        <Table
          columns={columns}
          dataSource={data}
          pagination={false}
          bordered
          size="small"
          rowClassName={(record, index) => (index % 2 === 0 ? 'table-row-light' : 'table-row-dark')}
        />
      )}
    </div>
  );
}

export default App;
