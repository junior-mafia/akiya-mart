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

function getPromotionDetails(dashboardData: any) {
  let promotionCode: string = ""
  let discount: string = ""
  let duration: string = ""

  if (dashboardData?.promotion_code) {
    promotionCode = dashboardData.promotion_code

    if (dashboardData?.percent_off) {
      const percent_off = dashboardData.percent_off
      discount = `${percent_off}% off`
    } else if (dashboardData?.amount_off) {
      const amount_off = dashboardData.amount_off
      const currency = dashboardData.coupon_currency
      discount = `${amount_off} ${currency} off`
    }

    if (dashboardData?.duration) {
      const durationType = dashboardData.duration

      switch (durationType) {
        case "forever":
          duration = "For all billing periods"
          break
        case "once":
          duration = "For one billing period"
          break
        case "repeating":
          const duration_in_months = dashboardData.duration_in_months
          duration = `For the first ${duration_in_months} billing periods`
          break
        default:
          duration = "Unknown duration"
      }
    }
  }

  return { promotionCode, discount, duration }
}

const Dash = () => {
  const navigate = useNavigate()
  const [dashboardData, setDashboardData] = useState<DashboardData | undefined>(
    undefined
  )

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

  const handleAdminDashboard = async () => {
    try {
      navigate("/admin")
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
  var isAdmin = false
  var displayProductName = ""
  var displayStatus = ""
  var displayBilling = ""
  var subscriptionIsCancelable = false
  var promotionCode: string | undefined = undefined
  var promotionCodeDiscount: string | undefined = undefined
  var promotionCodeDuration: string | undefined = undefined

  if (dashboardData) {
    if (dashboardData.subscription_id) {
      const email = dashboardData.email as string
      const product_name = dashboardData.product_name as string
      const status = dashboardData.status as string
      const unit_amount = dashboardData.unit_amount as number
      const currency = dashboardData.currency as string
      const recurring_interval = dashboardData.recurring_interval as string
      const promotionCodeDetails = getPromotionDetails(dashboardData)
      promotionCode = promotionCodeDetails.promotionCode
      promotionCodeDiscount = promotionCodeDetails.discount
      promotionCodeDuration = promotionCodeDetails.duration

      displayEmail = email
      isAdmin = dashboardData.is_admin as boolean
      displayProductName = toTitleCase(product_name)
      displayStatus = toTitleCase(status)
      displayBilling = `$${
        unit_amount / 100
      } ${currency.toUpperCase()} per ${recurring_interval}`
      subscriptionIsCancelable = status != "canceled"
    } else {
      displayEmail = dashboardData.email as string
      isAdmin = dashboardData.is_admin as boolean
      displayProductName = "Free"
      displayStatus = "Active"
      displayBilling = "N/A"
      subscriptionIsCancelable = false
      promotionCode = undefined
      promotionCodeDiscount = undefined
      promotionCodeDuration = undefined
    }
  }

  return (
    <div className="splash-page-container">

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
              {promotionCode && (
                <div className="dashboard-item">
                  <div className="dashboard-data-label">Promo code</div>
                  <div>{promotionCode}</div>
                </div>
              )}
              {promotionCodeDiscount && (
                <div className="dashboard-item">
                  <div className="dashboard-data-label">Discount</div>
                  <div>{promotionCodeDiscount}</div>
                </div>
              )}
              {promotionCodeDuration && (
                <div className="dashboard-item">
                  <div className="dashboard-data-label">Discount duration</div>
                  <div>{promotionCodeDuration}</div>
                </div>
              )}
            </div>
          )}

          <button className="dash-button safe-button" onClick={handleLogout}>
            Logout
          </button>
        </div>

        {isAdmin && (
          <div className="splash-item">
            <h3 className="header">Admin</h3>
            <button
              className="dash-button safe-button"
              onClick={handleAdminDashboard}
            >
              Admin Dashboard
            </button>
          </div>
        )}

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
