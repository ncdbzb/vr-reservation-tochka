import axios from "axios";
import TimeBookingCard from "./components/TimeBookingCard.jsx";
import {Card} from "antd";
import { useEffect, useState } from "react";

function App() {
  const [bookings, setBookings] = useState([])


  const fetchBookings = () => {
    axios.get("http://localhost:8000/api").then(r => {
      console.log('r', r);
    }).catch(error => {
      console.error('Ошибка при фетчинге:', error);
    });
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  return (
    <div>

    </div>
  )
}

export default App
