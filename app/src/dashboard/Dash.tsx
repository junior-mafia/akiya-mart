import React, { useEffect, useState } from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { fetchDashboardData, DashboardData } from "./dashboard"
import { Link } from "react-router-dom"
import { checkIfIsLoggedIn, logout } from "../auth/auth"
import { useNavigate } from "react-router-dom"
import { cancelSubscription } from "../stripe/stripe"
import "./styles/dashboard.css"

const toTitleCase = (str: string): string => {
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.slice(1).toLowerCase()
  })
}

const Dash = () => {
  const navigate = useNavigate()
  const [dashboardData, setDashboardData] = useState<DashboardData | undefined>(
    undefined
  )
  const [isSignedIn, setIsSignedIn] = useState<boolean>(false)

  const checkIfLoggedIn = async () => {
    try {
      const isLoggedIn = await checkIfIsLoggedIn()
      if (!isLoggedIn) {
        navigate("/auth")
      }
    } catch (err) {
      console.log(err.message)
    }
  }

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
      await cancelSubscription()
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
    checkIfLoggedIn()
    handleDashboard()
  }, [])

  var displayEmail = ""
  var displayProductName = ""
  var displayStatus = ""
  var displayBilling = ""
  var subscriptionIsCancelable = false
  if (dashboardData) {
    if (dashboardData.subscription_id) {
      const email = dashboardData.email as string
      const product_name = dashboardData.product_name as string
      const status = dashboardData.status as string
      const unit_amount = dashboardData.unit_amount as number
      const currency = dashboardData.currency as string
      const recurring_interval = dashboardData.recurring_interval as string
      displayEmail = email
      displayProductName = toTitleCase(product_name)
      displayStatus = toTitleCase(status)
      displayBilling = `$${
        unit_amount / 100
      } ${currency.toUpperCase()} per ${recurring_interval}`
      subscriptionIsCancelable = status != "canceled"
    } else {
      displayEmail = dashboardData.email as string
      displayProductName = "Free"
      displayStatus = "Active"
      displayBilling = "N/A"
      subscriptionIsCancelable = false
    }
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
          <h3 className="header">Account</h3>

          {dashboardData && (
            <div className="dashboard-data">
              <div className="dashboard-item">
                <div className="dashboard-data-label">Email</div>
                <div>{displayEmail}</div>
              </div>
              <div className="dashboard-item">
                <div className="dashboard-data-label">Subscription</div>
                <div>{displayProductName}</div>
              </div>
              <div className="dashboard-item">
                <div className="dashboard-data-label">Subscription status</div>
                <div>{displayStatus}</div>
              </div>
              <div className="dashboard-item">
                <div className="dashboard-data-label">Billing</div>
                <div>{displayBilling}</div>
              </div>
            </div>
          )}

          <button className="dash-button safe-button" onClick={handleLogout}>
            Logout
          </button>
        </div>

        {dashboardData && subscriptionIsCancelable && (
          <div className="splash-item">
            <h3 className="header">Danger Zone</h3>
            <button
              className="dash-button danger-button"
              onClick={handleCancel}
            >
              Cancel subscription
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default Dash
