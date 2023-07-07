import React, { useEffect, useState } from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { fetchDashboardData, DashboardData } from "./dashboard"
import { Link } from "react-router-dom"
import { checkIfIsLoggedIn, logout } from "../auth/auth"
import { useNavigate } from "react-router-dom"
import { cancelSubscription } from "../stripe/stripe"
import "./styles/dashboard.css"

const Dash = () => {
  const navigate = useNavigate()
  const [dashboardData, setDashboardData] = useState<DashboardData | undefined>(
    undefined
  )

  const handleLogout = async () => {
    try {
      await logout()
      navigate("/")
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleCancel = async () => {
    try {
      const result = await cancelSubscription()
      console.log(result)
      navigate("/cancel-subscription")
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleDashboard = async () => {
    const result = await fetchDashboardData()
    setDashboardData(result)
  }

  useEffect(() => {
    handleDashboard()
  }, [])

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
          <h3 className="header">Account</h3>
          <div className="dashboard-data">
            
            <div className="dashboard-item">
              <div className="dashboard-data-label">Email</div>
              <div>{dashboardData?.email}</div>
            </div>

            <div className="dashboard-item">
              <div className="dashboard-data-label">Subscription</div>
              <div>{dashboardData?.subscription_type}</div>
            </div>
            <div className="dashboard-item">
              <div className="dashboard-data-label">Subscription status</div>
              <div>{dashboardData?.subscription_status}</div>
            </div>
            
          </div>

          <button className="dash-button safe-button" onClick={handleLogout}>Logout</button>
        </div>




        {dashboardData?.subscription_status && dashboardData?.subscription_status != 'canceled' && <div className="splash-item">
          <h3 className="header">Danger Zone</h3>
          <button className="dash-button danger-button" onClick={handleCancel}>Cancel subscription</button>
        </div>}

        
      </div>
    </div>
  )
}

export default Dash
