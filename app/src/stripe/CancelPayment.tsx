import React from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"

const CancelPayment = () => {
  return (
    <div className="splash-page-container">

      <div className="splash-container">
        <div className="splash-item">
          <h3 className="header">Payment cancelled</h3>
        </div>
      </div>
    </div>
  )
}

export default CancelPayment
