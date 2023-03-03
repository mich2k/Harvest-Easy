import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./components/home/Home";
import Login from "./components/user_login/Login";
import useToken from "./useToken";

function App() {
  const { token, setToken } = useToken();

  return (
    <div className="wrapper">
      <h1>Application</h1>
      <Routes>
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<Login />} />
}

      </Routes>
    </div>
  );
}

export default App;
