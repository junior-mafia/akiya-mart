import React, { useEffect, useState } from "react"
import "./styles/main.css"
import "./styles/navbar.css"
import { Link } from "react-router-dom"
import { checkIfIsLoggedIn, logout } from "./auth/auth"
import { createCheckoutSession, fetchProducts } from "./stripe/stripe"
import { useNavigate } from "react-router-dom"

const NavBar = () => {
  const navigate = useNavigate()
  const [isSignedIn, setIsSignedIn] = useState<boolean>(false)

  const checkIfLoggedIn = async () => {
    try {
      const isLoggedIn = await checkIfIsLoggedIn()
      setIsSignedIn(isLoggedIn)
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleLogout = async () => {
    try {
      await logout()
      setIsSignedIn(false)
      navigate("/auth")
    } catch (err) {
      console.log(err.message)
    }
  }

  const handleUnlock = async () => {
    try {
      if (isSignedIn) {
        const products = await fetchProducts()      
        const selectedPriceIds = [products[0].price_id]
        const result = await createCheckoutSession(selectedPriceIds)
        //@ts-ignore
        window.location = result.url
      } else {
        navigate("/auth")
      }
    } catch (err) {
      console.log(err.message)
    }
  }

  useEffect(() => {
    checkIfLoggedIn()
  }, [])

  return (
    <div className="navbar-container transparent-until-hover">
      <div className="navbar-left">
        <Link to="/">
          <div id="navbar-item-title" className="navbar-item navbar-clickable">
            AkiyaMart
          </div>
        </Link>
      </div>
      <div className="navbar-right">
        <div
          id="navbar-item-unlock"
          className="navbar-item navbar-clickable"
          onClick={handleUnlock}
        >
          Unlock
        </div>
        {!isSignedIn && (
          <Link to="/auth">
            <div
              id="navbar-item-login"
              className="navbar-item navbar-clickable"
            >
              Sign in
            </div>
          </Link>
        )}
        {isSignedIn && (
          <div
            id="navbar-item-logout"
            className="navbar-item navbar-clickable"
            onClick={handleLogout}
          >
            Sign out
          </div>
        )}
      </div>
    </div>
  )
}

export default NavBar
