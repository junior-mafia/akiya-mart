import React from "react"
import { createRoot } from "react-dom/client"
import App from "./App"

// const appComponent = React.createElement(App)
// const strictModeComponent = React.createElement(React.StrictMode, null, appComponent)
// const rootElement = document.getElementById('root') as HTMLElement
// createRoot(rootElement).render(strictModeComponent)

const appComponent = React.createElement(App)
const rootElement = document.getElementById("root") as HTMLElement
createRoot(rootElement).render(appComponent)
