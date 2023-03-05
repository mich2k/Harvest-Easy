import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/home/Home";
import Login from "./components/user_login/Login";
import useToken from "./useToken";
import AdminGeoRecord from "./components/georecord/AdminGeorecord";
import AdminRecord from "./components/georecord/AdminRecord";
function App() {
  const { token, setToken } = useToken();

  return (
    <div className="wrapper">
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<Login />} />
        <Route path="/georecord" element={<AdminGeoRecord />} />
        <Route path="/admin_home" element={<AdminRecord />} />
      </Routes>
    </div>
  );
}

export default App;
