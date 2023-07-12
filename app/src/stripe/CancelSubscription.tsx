import React from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"

const CancelSubscription = () => {
  return (
    <div className="splash-page-container">

      <div className="splash-container">
        <div className="splash-item">
          <h3 className="header">Subscription cancelled</h3>
        </div>
      </div>
    </div>
  )
}

export default CancelSubscription
