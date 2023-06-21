import React, { useEffect, useState } from "react"
import Register from "./Register"
import Login from "./Login"
import { isLoggedIn } from "./auth"
import "./styles/authenticator.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"

const Authenticator = () => {
  const [registrationIsVisible, setRegistrationIsVisible] =
    useState<boolean>(false)
  const [loginIsVisible, setLoginIsVisible] = useState<boolean>(false)

  const checkIfLoggedIn = async () => {
    try {
      // setLoading(true)
      // setError("")
      const result = await isLoggedIn()
      if (result.is_logged_in) {
        // setLoginIsVisible(false)
        // setRegistrationIsVisible(false)
        // setLogoutIsVisible(true)
        console.log("LOGGED IN")
      } else {
        setLoginIsVisible(true)
        setRegistrationIsVisible(false)
      }
    } catch (err) {
      // setError(err.message)
    } finally {
      // setLoading(false)
    }
  }

  const loginClicked = () => {
    setLoginIsVisible(true)
    setRegistrationIsVisible(false)
  }

  const registerClicked = () => {
    setLoginIsVisible(false)
    setRegistrationIsVisible(true)
  }

  useEffect(() => {
    checkIfLoggedIn()
  }, [])

  return (
    <>
      <div className="auth-page-container">
        <div className="navbar-container">
          <div className="navbar-left">
            <div
              id="navbar-item-title"
              className="navbar-item navbar-clickable"
            >
              <Link to="/">AkiyaMart</Link>
            </div>
          </div>
        </div>

        <div className="auth-item">
          <h3 className="header">Welcome to AkiyaMart</h3>

          <div className="auth-toggle-container">
            <div
              id="auth-toggle-login"
              className={`auth-toggle-item ${
                loginIsVisible ? "auth-toggle-item-active" : ""
              }`}
              onClick={loginClicked}
            >
              Sign in
            </div>
            <div
              id="auth-toggle-register"
              className={`auth-toggle-item ${
                registrationIsVisible ? "auth-toggle-item-active" : ""
              }`}
              onClick={registerClicked}
            >
              New account
            </div>
          </div>

          {loginIsVisible && <Login />}

          {registrationIsVisible && <Register />}
        </div>
      </div>
    </>
  )
}

export default Authenticator
