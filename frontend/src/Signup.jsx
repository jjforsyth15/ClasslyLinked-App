import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./Signup.css";


function Signup() {
    // Initialize sliding submittion box
    const [step, setStep] = useState(1);

    // Initialize form to send to Flask API for signup
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        userName: "",
        password: ""
    });

    // Sets tab title
    useEffect(() => {
        document.title = "Signup | ClasslyLinked";
    }, []);

    // Handles changes to input in form for Flask API
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Allows menu to slide to next step of signup - making a username and password
    const handleNext = (e) => {
        e.preventDefault();
        setStep(2);
    }

    const navigate = useNavigate();

    // Handles submittion of user info to send to Flask API for signup
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post("http://localhost:5000/signup", formData);
            //alert(res.data.message);
            const name = formData.firstName;

            localStorage.setItem("firstName", name);
            localStorage.setItem("userName", formData.userName);
            navigate("/home");
        } catch (error) {
            alert(error.response?.data?.message || "Something went wrong");
        }
    };

    // Web page to return
    return (
        <div className="form-slider">
            <div className="container">
                {/* Head of page - name and logo */}
                <div className="head">
                    <img src="ClasslyLinked_Logo2.png" className="logo" />
                    <h1 className="login_title">ClasslyLinked</h1>
                </div>
                {/* Main signup box */}
                <div className="signup_main" style={{height: "450px"}}>
                    <form onSubmit={handleSubmit}>

                        {/* Allows menu to slide */}
                        <div className="form-container"
                            style={{ transform: step === 2? "translateX(-50%)" : "translateX(0%)" }}>

                                {/* First page of form - first and last name*/}
                            <div className="form-page">
                                <input className="input" name="firstName" onChange={handleChange} placeholder="First Name" required/>
                                <input className="input" name="lastName" onChange={handleChange} placeholder="Last Name" required/>
                                <button className="next_button" align ="center" onClick={handleNext}>Next</button>
                            </div>

                                {/* Second page of form  - username and password*/}
                            <div className="form-page">
                                <input className="input" name="userName" onChange={handleChange} placeholder="Username" required/>
                                <input className="input" name="password" type="password" onChange={handleChange} placeholder="Password" required/>
                                    
                                {/* Back  and sign up buttons */}
                                <div style={{ display: "flex", justifyContent: "space-between" }}>
                                    <button className="back_button" type="button" onClick={() => setStep(1)}>Back</button>
                                    <button className="submit_button" type="submit" align="center">Sign Up</button>
                                </div>
                            </div>
                        </div>
                    </form>
                    
                {/* Link to login if user already has an account */}
                <h1 className="login_message">Already have an account? <Link to="/login" className="login_link">Log in</Link></h1>
                </div>
            </div>
        </div>
    );
}



export default Signup;