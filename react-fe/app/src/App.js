import React from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./components/home/Home";
import Login from "./components/user_login/Login";
import AdminGeoRecord from "./components/georecord/AdminGeorecord";
import AdminRecord from "./components/georecord/AdminRecord";
function App() {
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
