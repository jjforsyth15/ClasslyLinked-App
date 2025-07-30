import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";
import axios from "axios";

function Home() {
    const firstName = localStorage.getItem("firstName");
    const username = localStorage.getItem("userName");
    const navigate = useNavigate();
    const [courses, setCourses] = useState([]);
    const [message, setMessage] = useState("");
    const [newCourse, setNewCourse] = useState("")

    const getCourses = async () => {
        try {
            const response = await axios.get("http://localhost:5000/get_courses", {params: { userName: username }});
            setCourses(response.data.courses || []);
        } catch (err) {
            setMessage(err.response?.data?.error || "Failed to load courses");
        }
    };

    const handleLogout = () => {
    localStorage.removeItem("firstName");
    localStorage.removeItem("userName");
    navigate("/login");
  };

  const handleAddCourse = async () => {
    try {
        const response = await axios.post("http://localhost:5000/add_course", {
            userName: username,
            course: newCourse
        });

        setMessage(response.data.message)
        setNewCourse("");
        await getCourses();
    } catch (err) {
        setMessage(err.response?.data?.error || "Failed to add course");
    }
  };

  useEffect(() => {
    getCourses();
  }, [username]);

    return (
        <div className="container">
            <h1 className="title">ClasslyLinked</h1>
            <h1 className="welcome_message">Welcome, {firstName}</h1>
            <p align="center">This is your homepage.</p>
            <button className="logout_button" align="center" onClick={handleLogout}>
                Log out
            </button>

            <div className="course-list">
                <h2>Your Courses</h2>
                {courses.length === 0 ? (
                    <p>There are no courses to show</p>
                ) : (
                    <ul>
                        {courses.map((course, index) => (
                            <li key={index}>
                                {course.courseName} ({course.courseNumber})
                            </li>
                        ))}
                    </ul>
                )}
            </div>

            <div className="add-course-form">
                <h2>Add Course</h2>
                <input
                    type="text"
                    value={newCourse}
                    onChange={(e) => setNewCourse(e.target.value)}
                    placeholder="Course Number"
                    required
                />
                <button className="add-button" onClick={handleAddCourse}>Add</button>
            </div>
            {message && <p className="error-message">{message}</p>}
        </div>
    );
}

export default Home;