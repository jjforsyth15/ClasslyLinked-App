import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.scss";
import axios from "axios";

function Home() {

    // Assigns login data via localStorage
    const firstName = localStorage.getItem("firstName");
    const username = localStorage.getItem("userName");
    const isAdmin = localStorage.getItem("isAdmin") === "true";

    const navigate = useNavigate();

    // Sets useState functions
    const [courses, setCourses] = useState([]);
    const [message, setMessage] = useState("");
    const [newCourse, setNewCourse] = useState("")
    const [searchTerm, setSearchTerm] = useState("");
    const [searchResults, setSearchResults] = useState([]);

    // Function to get courses from Flask API backend
    const getCourses = async () => {
        try {
            const response = await axios.get("http://localhost:5000/get_courses", {params: { userName: username }});
            setCourses(response.data.courses || []);
        } catch (err) {
            setMessage(err.response?.data?.error || "Failed to load courses");
        }
    };

    // Function to handle Logout process
    const handleLogout = () => {
    localStorage.removeItem("firstName");
    localStorage.removeItem("userName");
    localStorage.removeItem("isAdmin");
    navigate("/login");
  };

//   Allows user to add course 
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
        setNewCourse("");
    }
  };

// useEffect functions

//   Sets tab title
  useEffect(() => {
    document.title = "Home | ClasslyLinked"
  }, []);

// Gets courses list based on username
  useEffect(() => {
    getCourses();
  }, [username]);
  
//   Runs rain background effect
  useEffect(() => {
    rainBackground();
  }, []);

//   Allows user to search courses to add
const handleSearch = async (e) => {
    const value = e.target.value;
    setSearchTerm(value);

    if(value.trim() === "") {
        setSearchResults([]);
        return
    }

    try {
        const response = await axios.get("http://localhost:5000/search_courses", {
            params: { q: value }
        });
        setSearchResults(response.data.courses || []);
    } catch {
        setSearchResults([]);
    }
}

// Rain background
const rainBackground = () => {
    const rain = document.querySelector(".rain");
    for (let i = 0; i < 500; i++) {
        const drop = document.createElement("div");
        drop.className = "drop";
        rain.appendChild(drop);
    }
}

    // Webpage to return
    return (
        <div className="entire-page">
        <div className="rain"></div>
        {/* menu */}
        <div className="menu-hover-wrapper">
            <div className="hover-zone"></div>
            <div className="sliding-menu">
                <div className="menu-lists"
                    style={{marginLeft: isAdmin ? "36%" : "43.5%"}}>
                    <ul>
                        <li className="menu-option">View Profile</li>
                        <li className="menu-option">Add Class</li>
                        <li className="menu-option">Remove Class</li>
                    </ul>
                    {/* admin options */}
                    {isAdmin && (
                        <>
                            <div className="admin-menu">
                                <ul>
                                    <li className="admin-option">Add course to COURSES</li>
                                    <li className="admin-option">Promote student user to admin</li>
                                    <li className="admin-option">Remove student from a course</li>
                                </ul>
                            </div>
                        </>
                    )}
                </div>
                {/* Logout button */}
                <button className="logout_button" onClick={handleLogout}>
                    Log out
                </button>
                <h3 className="menu">Menu</h3>
            </div>
        </div>
                    {/* Main page container */}
        <div className="home-container">
            <div className="head">
                <img src="ClasslyLinked_Logo2.png" className="logo" />
                <h1 className="login_title">ClasslyLinked</h1>
            </div>
            <h1 className="welcome_message">Welcome, {firstName}</h1>
            <p align="center">This is your homepage.</p>

                    {/* User course list */}
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
                {/* Course add section */}
            <div className="add-course-form">
                <h2>Add Course</h2>
                <div className="add-box">
                    <input
                        type="text"
                        className="add-input"
                        value={searchTerm || newCourse}
                        onChange={handleSearch}
                        placeholder="Course"
                        required
                    />
                </div>
                {/* Dropdown list of courses from course search */}
                <ul className="search-dropdown">
                    {searchResults.map((course, index) => (
                        <li
                            key={index}
                            onClick={() => {
                                setNewCourse(course.courseNumber);
                                setSearchTerm("");
                                setSearchResults([]);
                            }}
                        >
                            {course.courseName} ({course.courseNumber})
                        </li>
                    ))}
                </ul>
                <button className="add-button" onClick={handleAddCourse}>Add</button>
            </div>
            {message && <p className="error-message">{message}</p>}
        
        </div>
        </div>
    );
}

export default Home;