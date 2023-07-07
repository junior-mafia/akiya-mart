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
      </Routes>
    </HashRouter>
  )
}

export default App
