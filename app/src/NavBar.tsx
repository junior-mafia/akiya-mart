import React, { useEffect, useState } from "react"
import "./styles/main.css"
import "./styles/navbar.css"
import { Link } from "react-router-dom"
import { isLoggedIn, logout } from "./auth/auth"
import { useNavigate } from "react-router-dom"

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
        <Link to="/">
          <div id="navbar-item-title" className="navbar-item navbar-clickable">
            AkiyaMart
          </div>
        </Link>
      </div>
      <div className="navbar-right">
        {!isSignedIn && (
          <Link to="/auth">
            <div id="navbar-item-login" className="navbar-item navbar-clickable">
              Sign in
            </div>
          </Link>
        )}
        {isSignedIn && (
          <div
            id="navbar-item-logout"
            className="navbar-item navbar-clickable"
            onClick={handleLogout}
          >
            Sign out
          </div>
        )}
      </div>
    </div>
  )
}

export default NavBar
