import React, { useEffect, useState } from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { fetchDashboardData, DashboardData } from "./dashboard"
import { Link } from "react-router-dom"
import { checkIfIsLoggedIn, logout } from "../auth/auth"
import { useNavigate } from "react-router-dom"

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
          <div className="dashboard-item">
            <div className="dashboard-item-title">
              Email: {dashboardData?.email}
            </div>
            <div className="dashboard-item-title">
              Subscription type: {dashboardData?.subscription_type}
            </div>
            <div className="dashboard-item-title">
              Subscription status: {dashboardData?.subscription_status}
            </div>
          </div>
        </div>

        <div className="splash-item">
          <h3 className="header">Danger</h3>
          <button onClick={handleLogout}>Cancel subscription</button>
        </div>

        <button onClick={handleLogout}>Logout</button>
      </div>
    </div>
  )
}

export default Dash
