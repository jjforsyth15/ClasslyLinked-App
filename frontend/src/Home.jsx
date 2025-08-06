import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.scss";
import axios from "axios";
import "./Profile.css";
import "./AddClass.css";
import "./RemoveClass.css";

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

    const [form, setForm] = useState('Dashboard');

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

    if (!newCourse) {
        setMessage("Please select a course first.");
        return;
    }

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
                    <div className='regular-menu'>
                        <ul>
                            <li className="menu-option" onClick={() => setForm('Dashboard')}>Dashboard</li>
                            <li className="menu-option" onClick={() => setForm('Profile')}>View Profile</li>
                            <li className="menu-option" onClick={() => setForm('AddClass')}>Add Class</li>
                            <li className="menu-option" onClick={() => setForm('RemoveClass')}>Remove Class</li>
                        </ul>
                    </div>
                    {/* admin options */}
                    {isAdmin && (
                        <>
                            <div className="admin-menu">
                                <ul>
                                    <li className="admin-option" onClick={() => setForm('AddCourseToCOURSES')}>Add course to COURSES</li>
                                    <li className="admin-option" onClick={() => setForm('PromoteStudent')}>Promote student user to admin</li>
                                    <li className="admin-option" onClick={() => setForm('RemoveStudentFromCourse')}>Remove student from a course</li>
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

        
                    {/* Dashboard */}
        {form === 'Dashboard' && (
            <div className="home-container">
                <div className="head">
                    <img src="ClasslyLinked_Logo2.png" className="logo" />
                    <h1 className="login_title">ClasslyLinked</h1>
                    <title>Dashboard | ClasslyLinked</title>
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
                            value={searchTerm}
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
                                    setSearchTerm(course.courseName + " (" + course.courseNumber + ")");
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
        )}

            {/* Profile */}
        {form === 'Profile' && (
            <div className="profile-container">
                <title>Profile | ClasslyLinked</title>
                <h1 className="profile-title">Profile</h1>

                {/* User courses section */}
                <div className='user-courses-container'>
                    <h2 className='user-courses-title'>My Classes</h2>
                    {courses.length === 0 ? (
                        <p>There are no courses to show</p>
                    ) : (
                        <ul className='course-list'>
                            {courses.map((course, index) => (
                                <li key={index}>
                                    {course.courseName} ({course.courseNumber})
                                </li>
                            ))}
                        </ul>
                    )}
                    <button className='course-list-buttons' onClick={() => setForm('AddClass')}>Add Class</button>
                    <button className='course-list-buttons' onClick={() => setForm('RemoveClass')}>Remove class</button>
                </div>

                {/* User ClasslyLinked Mates */}
                <div className='user-mates-container'>
                    <h2 className='user-mates-title'>My ClassyLinked Mates</h2>
                    {/* Need to add conditional for if no mates */}
                    <ul className='mate-list'>
                        {/* Need to add mates.map similar to course list */}
                    </ul>   
                </div>
            </div>
        )}

            {/* AddCourse */}
            {form === 'AddClass' && (
                <div className='AddClass-container'>
                    <title>Add Class | ClasslyLinked</title>
                    <h1 className='AddClass-title'>Add Class</h1>

                    {/* Course add section */}
                <div className="add-course-form">
                    <div className="add-box">
                        <input
                            type="text"
                            className="add-input"
                            value={searchTerm}
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
                                    setSearchTerm(course.courseName + " (" + course.courseNumber + ")");
                                    setSearchResults([]);
                                }}
                            >
                                {course.courseName} ({course.courseNumber})
                            </li>
                        ))}
                    </ul>
                    <button className="add-button" onClick={handleAddCourse}>Add</button>
                </div>
                {message && <p className="add-error-message">{message}</p>}
                </div>
            )}

            {/* RemoveClass */}
            {form === 'RemoveClass' && (
                <div className='RemoveClass-container'>
                    <title>Remove Class | ClasslyLinked</title>
                    <h1 className='RemoveClass-title'>Remove Class</h1>

                    {/* Remove course section */}
                    <div className='remove-course-form'>
                        <div className='remove-box'>
                            <input
                            type="text"
                            className="remove-input"
                            // value={searchTerm}
                            // onChange={handleSearch}
                            placeholder="Course"
                            required
                        />
                        </div>

                    </div>

                </div>

            )}
        </div>
    );
}

export default Home;