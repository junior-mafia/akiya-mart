import React from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { useNavigate,  Link } from "react-router-dom"

const Success = () => {
  const navigate = useNavigate()

  const message = `
  Thank you for your subscription!
  You will gain access to all 100k+ listings once we receive confirmation of your payment.
  This generally only takes a few seconds.
  `

  const handleViewMap = () => {
    navigate("/")
  }

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
          <h3 className="header">{message}</h3>
          <div className="splash-input-field">
            <button onClick={handleViewMap} className="splash-submit-button">
              View map
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Success
