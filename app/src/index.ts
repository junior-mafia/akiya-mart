import React from "react"
import { createRoot } from "react-dom/client"
import App from "./App"

const appComponent = React.createElement(App)
const rootElement = document.getElementById("root") as HTMLElement
createRoot(rootElement).render(appComponent)
