import React from "react"
import { HashRouter } from "react-router-dom"
import { Route, Routes } from "react-router-dom"
import Main from "./Main"
import Authenticator from "./auth/Authenticator"
import Success from "./stripe/Success"
import Cancel from "./stripe/Cancel"

const App = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/auth" element={<Authenticator />} />
        <Route path="/success" element={<Success />} />
        <Route path="/cancel" element={<Cancel />} />
      </Routes>
    </HashRouter>
  )
}

export default App
