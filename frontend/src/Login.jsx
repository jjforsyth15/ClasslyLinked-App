import React, { useState } from "react";
import axios from "axios";
import './Login.css';
import { useNavigate } from "react-router-dom"
import { useEffect } from "react";
import { Link } from "react-router-dom";

function Login() {

  const [formData, setFormData] = useState({
    userName: "",
    password: ""
  })

  const navigate = useNavigate();

  const [loggedIn, setLoggedIn] = useState(false);
  const [firstName, setFirstName] = useState("");

  useEffect(() => {
    document.title = "Login | ClasslyLinked";
  }, []);

  useEffect(() => {
    const user = localStorage.getItem("userName");

    if(user) 
        navigate("/home");
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:5000/login", formData);
      //alert(response.data.message);
      const name = response.data.firstName;

      localStorage.setItem("firstName", name);
      localStorage.setItem("userName", formData.userName);

      setFirstName(name);
      setLoggedIn(true);
      navigate("/home");
    } catch (error) {
      alert(error.response?.data?.message || "Something went wrong");
    }
  };

  return (
    <div className="container">
      <div className="head">
        <img src="ClasslyLinked_Logo2.png" className="logo" />
        <h1 className="login_title">ClasslyLinked</h1>
      </div>
          <div className="login_main">
            <div className="ring">
            <form className="loginBox" onSubmit={handleSubmit}>
              <h2 align="center" className="sign">Log in</h2>
              <div className="userBox">
                <input
                  type="text"
                  name="userName"
                  placeholder="Username"
                  align="center"
                  value = {formData.userName}
                  onChange = {(e) => setFormData({...formData, userName: e.target.value })}
                  required
                  className="input"
                />
                <br />
              </div>
              
              <div className="userBox">
                <input 
                  type="password"
                  name="password"
                  placeholder="Password"
                  align="center"
                  value = {formData.password}
                  onChange = {(e) => setFormData({...formData, password: e.target.value })}
                  required
                  className="input"
                />
                <br />
              </div>
              <button type="submit" className="submitButton" align="center">Login</button>
            </form>
            
            <h3 className="signup_message">Don't have an account? <Link className="signup_link" to="/signup">Sign up</Link></h3>
          </div>
          </div>
    </div>
  );
}

export default Login;