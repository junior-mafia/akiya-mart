import React, { useEffect } from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"
import { fetchAdminDashboardData } from "./adminDashboard"

const AdminDash = () => {
  const [message, setMessage] = React.useState("")

  const handleFetchAdminDashboardData = async () => {
    const data = await fetchAdminDashboardData()
    setMessage(data.message)
  }

  useEffect(() => {
    handleFetchAdminDashboardData()
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
          <h3 className="header">Admin Dashboard</h3>
          {message}
        </div>
      </div>
    </div>
  )
}

export default AdminDash
