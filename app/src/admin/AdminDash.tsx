import React from "react"
import "../styles/splash-page.css"
import "./styles/admin.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"
import {
  executeRundateTask,
  executeListingsAthomeTask,
  executeListingsNiftyTask,
  executeListingsDetailsAthomeTask,
  executeListingsDetailsNiftyTask,
  executeListingsDetailsTranslateTask,
  executeGenerateGeojsonTask,
  executeRunAllTask,
} from "./adminDashboard"


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

  const handleEexecuteListingsDetailsTranslateTask = async () => {
    const data = await executeListingsDetailsTranslateTask()
    setMessage(data.message)
  }

  const handleExecuteGenerateGeojsonTask = async () => {
    const data = await executeGenerateGeojsonTask()
    setMessage(data.message)
  }

  const handleExecuteRunAllTask = async () => {
    const data = await executeRunAllTask()
    setMessage(data.message)
  }

  return (
    <div className="splash-page-container">

      <div className="splash-container">
        {message}
        <div className="splash-item">
          <h3 className="header">Run All</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteRunAllTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Rundate</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteRundateTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings AtHome</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteListingsAthomeTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Nifty</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteListingsNiftyTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Details AtHome</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteListingsDetailsAthomeTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Details Nifty</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteListingsDetailsNiftyTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Listings Details Translate</h3>
          <button
            className="dash-button danger-button"
            onClick={handleEexecuteListingsDetailsTranslateTask}
          >
            Run
          </button>
        </div>

        <div className="splash-item">
          <h3 className="header">Generate Geojson</h3>
          <button
            className="dash-button danger-button"
            onClick={handleExecuteGenerateGeojsonTask}
          >
            Run
          </button>
        </div>
      </div>
    </div>
  )
}

export default AdminDash
