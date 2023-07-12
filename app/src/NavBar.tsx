import React, { useEffect, useState } from "react"
import "./styles/main.css"
import "./styles/navbar.css"
import { Link } from "react-router-dom"
import { checkIfIsLoggedIn } from "./auth/auth"
import { useNavigate } from "react-router-dom"

const NavBar = () => {
  const navigate = useNavigate()
  const [isSignedIn, setIsSignedIn] = useState<boolean>(false)

  const checkIfLoggedIn = async () => {
    try {
      const isLoggedIn = await checkIfIsLoggedIn()
      setIsSignedIn(isLoggedIn)
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleDashboard = async () => {
    try {
      navigate("/dashboard")
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleUnlock = async () => {
    navigate("/buy")
  }

  useEffect(() => {
    checkIfLoggedIn()
  }, [])

  return (
    <div className="navbar-container">
      <div className="navbar-left">
        <Link to="/">
          <div className="navbar-item navbar-clickable">
            Map
          </div>
        </Link>
      </div>

      <div className="navbar-center">
        <div id="navbar-item-title" className="navbar-item">
          AkiyaMart
        </div>
      </div>

      <div className="navbar-right">
        <div
          id="navbar-item-unlock"
          className="navbar-item navbar-clickable"
          onClick={handleUnlock}
        >
          Buy
        </div>
        {!isSignedIn && (
          <Link to="/auth">
            <div
              id="navbar-item-login"
              className="navbar-item navbar-clickable"
            >
              Sign in
            </div>
          </Link>
        )}
        {isSignedIn && (
          <div
            id="navbar-item-logout"
            className="navbar-item navbar-clickable"
            onClick={handleDashboard}
          >
            Account
          </div>
        )}
      </div>
    </div>
  )
}

export default NavBar

// {isSignedIn && (
//   <div
//     id="navbar-item-logout"
//     className="navbar-item navbar-clickable"
//     onClick={handleLogout}
//   >
//     Sign out
//   </div>
// )}
