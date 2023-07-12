import React, { useEffect, useState } from "react"
import Register from "./Register"
import Login from "./Login"
import { checkIfIsLoggedIn } from "./auth"
import "./styles/authenticator.css"
import "../styles/navbar.css"
import "../styles/splash-page.css"
import { Link } from "react-router-dom"

const Authenticator = () => {
  const [registrationIsVisible, setRegistrationIsVisible] =
    useState<boolean>(false)
  const [loginIsVisible, setLoginIsVisible] = useState<boolean>(false)

  const checkIfLoggedIn = async () => {
    try {
      const isLoggedIn = await checkIfIsLoggedIn()
      if (isLoggedIn) {
      } else {
        setLoginIsVisible(true)
        setRegistrationIsVisible(false)
      }
    } catch (err) {
      console.log(err.message)
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
    <div className="splash-page-container">

      <div className="splash-container">
        <div className="splash-item">
          <h3 className="header">Welcome to AkiyaMart</h3>

          {(loginIsVisible || registrationIsVisible) && (
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
          )}

          {loginIsVisible && <Login />}

          {registrationIsVisible && <Register />}
        </div>
      </div>
    </div>
  )
}

export default Authenticator
