import React from "react"
import { HashRouter } from "react-router-dom"
import { Route, Routes } from "react-router-dom"
import Main from "./Main"
import Authenticator from "./auth/Authenticator"
import Success from "./stripe/Success"
import CancelPayment from "./stripe/CancelPayment"
import CancelSubscription from "./stripe/CancelSubscription"
import Buy from "./stripe/Buy"
import Dash from "./dashboard/Dash"
import Admin from "./admin/AdminDash"

const App = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/auth" element={<Authenticator />} />
        <Route path="/success-payment" element={<Success />} />
        <Route path="/cancel-payment" element={<CancelPayment />} />
        <Route path="/buy" element={<Buy />} />
        <Route path="/cancel-subscription" element={<CancelSubscription />} />
        <Route path="/dashboard" element={<Dash />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </HashRouter>
  )
}

export default App
