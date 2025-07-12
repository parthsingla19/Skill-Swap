import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    navigate("/");
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h2>SkillSwap</h2>
      </div>
      <div className="navbar-right">
        <Link to="/explore">Explore</Link>
        <Link to="/requests">Requests</Link>
        <button onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}

export default Navbar;

