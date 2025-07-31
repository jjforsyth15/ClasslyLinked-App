import { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./Signup.css";


function Signup() {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        firstName: "",
        lastName: "",
        userName: "",
        password: ""
    });

    useEffect(() => {
        document.title = "Signup | ClasslyLinked";
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleNext = (e) => {
        e.preventDefault();
        setStep(2);
    }

    const navigate = useNavigate();

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

    return (
        <div className="form-slider">
            <div className="container">
                <div className="head">
                    <img src="ClasslyLinked_Logo2.png" className="logo" />
                    <h1 className="login_title">ClasslyLinked</h1>
                </div>
                <div className="signup_main" style={{height: "450px"}}>
                    <form onSubmit={handleSubmit}>
                        <div className="form-container"
                            style={{ transform: step === 2? "translateX(-50%)" : "translateX(0%)" }}>
                            <div className="form-page">
                                <input className="input" name="firstName" onChange={handleChange} placeholder="First Name" required/>
                                <input className="input" name="lastName" onChange={handleChange} placeholder="Last Name" required/>
                                <button className="next_button" align ="center" onClick={handleNext}>Next</button>
                            </div>

                            <div className="form-page">
                                <input className="input" name="userName" onChange={handleChange} placeholder="Username" required/>
                                <input className="input" name="password" type="password" onChange={handleChange} placeholder="Password" required/>

                                <div style={{ display: "flex", justifyContent: "space-between" }}>
                                    <button className="back_button" type="button" onClick={() => setStep(1)}>Back</button>
                                    <button className="submit_button" type="submit" align="center">Sign Up</button>
                                </div>
                            </div>
                        </div>
                    </form>
                
                <h1 className="login_message">Already have an account? <Link to="/login" className="login_link">Log in</Link></h1>
                </div>
            </div>
        </div>
    );
}



export default Signup;