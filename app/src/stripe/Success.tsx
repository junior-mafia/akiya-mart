import React from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"

const Success = () => {
  return (
    <div className="splash-page-container">
      <div className="navbar-container">
        <div className="navbar-left">
          <Link to="/">
            <div
              id="navbar-item-title"
              className="navbar-item navbar-clickable"
            >
              AkiyaMart
            </div>
          </Link>
        </div>
      </div>

      <div className="splash-container">
        <div className="splash-item">
          <h3 className="header">Payment successful!</h3>
        </div>
      </div>
    </div>
  )
}

export default Success
