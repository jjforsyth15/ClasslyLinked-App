import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
    const firstName = localStorage.getItem("firstName");
    const navigate = useNavigate();

    const handleLogout = () => {
    localStorage.removeItem("firstName");
    localStorage.removeItem("userName");
    navigate("/login");
  };

    return (
        <div className="container">
            <h1 className="title">ClasslyLinked</h1>
            <h1 className="welcome_message">Welcome, {firstName}</h1>
            <p align="center">This is your homepage.</p>
            <button className="logout_button" align="center" onClick={handleLogout}>
                Log out
            </button>
        </div>
    );
}

export default Home;