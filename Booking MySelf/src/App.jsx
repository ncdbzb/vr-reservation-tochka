import React, { useState } from "react";
import { Button, Table, Switch } from "antd";
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
  const [bookings, setBookings] = useState({});
  const [isDarkTheme, setIsDarkTheme] = useState(false);
  const [autoConfirm, setAutoConfirm] = useState(false);
  const [emailNotification, setEmailNotification] = useState(false);

  const handleHeadsetClick = (id) => {
    setSelectedHeadset(selectedHeadset === id ? null : id);
  };

  const handleBooking = (headsetId, hour) => {
    const bookingKey = `${headsetId}-${hour}`;
    setBookings((prevBookings) => {
      const newBookings = { ...prevBookings };
      if (newBookings[bookingKey]) {
        delete newBookings[bookingKey];
      } else {
        newBookings[bookingKey] = {
          price: "1000 руб.", // Пример цены
          bookingTime: new Date().toLocaleString(),
        };
      }
      return newBookings;
    });
  };

  const handleAdminAction = (action, headsetId, hour) => {
    console.log(`Admin action: ${action} for VR Headset ${headsetId} at ${hour}:00`);
    // Здесь добавьте логику для действий администратора
  };

  const handleThemeToggle = () => {
    setIsDarkTheme(!isDarkTheme);
  };

  const handleAutoConfirmToggle = () => {
    setAutoConfirm(!autoConfirm);
  };

  const handleEmailNotificationToggle = () => {
    setEmailNotification(!emailNotification);
  };

  const columns = [
    {
      title: "Time",
      dataIndex: "time",
      key: "time",
      align: 'center',
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      align: 'center',
    },
    {
      title: "Action",
      key: "action",
      align: 'center',
      render: (text, record) => {
        const bookingKey = `${selectedHeadset}-${record.key}`;
        const isBooked = bookings[bookingKey];
        return (
          <Button
            type="primary"
            danger={isBooked}
            onClick={() => handleBooking(selectedHeadset, record.key)}
          >
            {isBooked ? "Отменить бронь" : "Забронировать"}
          </Button>
        );
      },
    },
    {
      title: "Admin Action",
      key: "adminAction",
      align: 'center',
      render: (text, record) => {
        const bookingKey = `${selectedHeadset}-${record.key}`;
        const isBooked = bookings[bookingKey];
        return isBooked ? (
          <>
            <Button
              type="primary"
              style={{ marginRight: 8 }}
              onClick={() => handleAdminAction('confirm', selectedHeadset, record.key)}
            >
              Подтвердить бронь
            </Button>
            <Button
              type="default"
              danger
              onClick={() => handleAdminAction('delete', selectedHeadset, record.key)}
            >
              Удалить бронь
            </Button>
          </>
        ) : null;
      },
    },
    {
      title: "Booking Time",
      dataIndex: "bookingTime",
      key: "bookingTime",
      align: 'center',
      render: (text, record) => {
        const bookingKey = `${selectedHeadset}-${record.key}`;
        return bookings[bookingKey]?.bookingTime || "-";
      },
    },
  ];

  const data = hours.map(hour => ({
    key: hour,
    time: `${hour}:00`,
    price: "1000 руб.", // Пример цены
    bookingTime: null,
  }));

  return (
    <div className={`app-container ${isDarkTheme ? 'dark' : 'light'}`}>
      <div className="top-right-buttons">
        <Button>
          Авторизация и вход
        </Button>
        <Button onClick={handleThemeToggle}>
          {isDarkTheme ? "Светлая тема" : "Темная тема"}
        </Button>
      </div>
      <h1>VR Headset Booking</h1>
      <div style={{ marginBottom: "20px" }}>
        <div style={{ marginBottom: "10px" }}>
          <Switch
            checked={autoConfirm}
            onChange={handleAutoConfirmToggle}
            style={{ marginRight: "10px" }}
          />
          Автоподтверждение бронирования: {autoConfirm ? "Включено" : "Выключено"}
        </div>
        <div style={{ marginBottom: "10px" }}>
          <Switch
            checked={emailNotification}
            onChange={handleEmailNotificationToggle}
            style={{ marginRight: "10px" }}
          />
          Оповещать на email о освободившихся местах
        </div>
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
