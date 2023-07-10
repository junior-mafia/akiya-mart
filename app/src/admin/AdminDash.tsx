import React from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"
import { 
  executeRundateTask, 
  executeListingsAthomeTask, 
  executeListingsNiftyTask, 
  executeListingsDetailsAthomeTask, 
  executeListingsDetailsNiftyTask 
} from "./adminDashboard"
import "./styles/admin.css"

const AdminDash = () => {
  const [message, setMessage] = React.useState("")

  const handleExecuteRundateTask = async () => {
    const data = await executeRundateTask()
    setMessage(data.message)
  }

  const handleExecuteListingsAthomeTask = async () => {
    const data = await executeListingsAthomeTask()
    setMessage(data.message)
  }

  const handleExecuteListingsNiftyTask = async () => {
    const data = await executeListingsNiftyTask()
    setMessage(data.message)
  }

  const handleExecuteListingsDetailsAthomeTask = async () => {
    const data = await executeListingsDetailsAthomeTask()
    setMessage(data.message)
  }

  const handleExecuteListingsDetailsNiftyTask = async () => {
    const data = await executeListingsDetailsNiftyTask()
    setMessage(data.message)
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
        {message}
        <div className="splash-item">
          <h3 className="header">Rundate</h3>
          <button className="dash-button safe-button" onClick={handleExecuteRundateTask}>Run</button>
          
        </div>

        <div className="splash-item">
          <h3 className="header">Listings AtHome</h3>
          <button className="dash-button safe-button" onClick={handleExecuteListingsAthomeTask}>Run</button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Nifty</h3>
          <button className="dash-button safe-button" onClick={handleExecuteListingsNiftyTask}>Run</button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Details AtHome</h3>
          <button className="dash-button safe-button" onClick={handleExecuteListingsDetailsAthomeTask}>Run</button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Details Nifty</h3>
          <button className="dash-button safe-button" onClick={handleExecuteListingsDetailsNiftyTask}>Run</button>
        </div>
      </div>
    </div>
  )
}

export default AdminDash
