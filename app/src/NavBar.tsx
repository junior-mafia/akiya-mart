import React, { useEffect, useState } from "react"
import "./styles/NavBar.css"
import { Link } from "react-router-dom"
import { isLoggedIn, logout } from "./auth/auth"
import { useNavigate } from "react-router-dom";

const NavBar = () => {
  const navigate = useNavigate()
  const [isSignedIn, setIsSignedIn] = useState<boolean>(false)

  const checkIfLoggedIn = async () => {
    try {
      const result = await isLoggedIn()
      setIsSignedIn(result.is_logged_in)
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleLogout = async () => {
    try {
      await logout()
      setIsSignedIn(false)
      navigate("/auth")
    } catch (err) {
      console.log(err.message)
    }
  }

  useEffect(() => {
    checkIfLoggedIn()
  }, [])
  
  return (
    <div className="navbar-container transparent-until-hover">
      <div className="navbar-left">
        <div id="navbar-item-title" className="navbar-item navbar-clickable">
          <Link to="/">AkiyaMart</Link>
        </div>
      </div>
      <div className="navbar-right">
        <div id="navbar-item-settings" className="navbar-item navbar-clickable">
          Filters
        </div>
        
        {!isSignedIn && 
          <div id="navbar-item-login" className="navbar-item navbar-clickable">
            <Link to="/auth">Sign in</Link>
          </div>
        }
        {isSignedIn && 
          <div id="navbar-item-logout" className="navbar-item navbar-clickable" onClick={handleLogout}>
            Sign out
          </div>
        }

      </div>
    </div>
  )
}

export default NavBar
