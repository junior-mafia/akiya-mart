import React from "react"
import { HashRouter } from "react-router-dom"
import { Route, Routes } from "react-router-dom"
import Main from "./Main"
import Authenticator from "./auth/Authenticator"

const App = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/auth" element={<Authenticator />} />
      </Routes>
    </HashRouter>
  )
}

export default App
