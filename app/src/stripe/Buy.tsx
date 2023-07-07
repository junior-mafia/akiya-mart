import React, { useEffect, useState } from "react"
import "../styles/splash-page.css"
import "../styles/navbar.css"
import { Link } from "react-router-dom"
import { fetchMapPrices, Price, createCheckoutSession } from "./stripe"
import "./styles/buy.css"
import { useNavigate } from "react-router-dom"
import { checkIfIsLoggedIn } from "../auth/auth"

interface PriceCardProps extends Price {
  isSignedIn: boolean
  onNotSignedIn: () => void
}

const PriceCard = (props: PriceCardProps) => {
  const handlePurchase = async (price_id: string) => {
    try {
      if (props.isSignedIn) {
        const result = await createCheckoutSession([price_id])
        //@ts-ignore
        window.location = result.url
      } else {
        props.onNotSignedIn()
      }
    } catch (err) {
      console.log(err.message)
    }
  }

  return (
    <div className="price-card">
      {props.name === "Pro" && (
        <div className="pricing-best-value">
          <div>BEST VALUE</div>
        </div>
      )}
      <h2 className="price-name">{props.name}</h2>
      <p className="price-description">{props.description}</p>
      <div className="price-unit-amount">${props.unit_amount / 100}</div>
      <div className="price-recurring-interval">
        {props.currency.toUpperCase()} / {props.recurring_interval}
      </div>
      <button
        className="price-button"
        onClick={() => handlePurchase(props.price_id)}
      >
        Purchase
      </button>
    </div>
  )
}

const Buy = () => {
  const navigate = useNavigate()
  const [mapPrices, setMapPrices] = useState<Price[]>([])
  const [recurringInterval, setRecurringInterval] = useState<string>("month")
  const monthlyIsVisible = recurringInterval === "month"
  const yearlyIsVisible = recurringInterval === "year"
  const [isSignedIn, setIsSignedIn] = useState<boolean>(false)

  const onNotSignedIn = () => {
    navigate("/auth")
  }

  const checkIfLoggedIn = async () => {
    try {
      const isLoggedIn = await checkIfIsLoggedIn()
      setIsSignedIn(isLoggedIn)
    } catch (err) {
      console.log(err.message)
    }
  }

  const getMapPrices = async () => {
    const result = await fetchMapPrices()
    setMapPrices(result)
  }

  const payMonthlyClicked = () => {
    setRecurringInterval("month")
  }

  const payYearlyClicked = () => {
    setRecurringInterval("year")
  }

  useEffect(() => {
    getMapPrices()
    checkIfLoggedIn()
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

      {/* <div className="splash-container"> */}
      <div className="pricing-hero">
        <h1 className="pricing-header">
          <div id="pricing-header-title">Discover Japanese Properties</div>
          <div id="pricing-header-subtitle">
            Private hot springs, coastal views, and more!
          </div>
        </h1>

        <div className="pricing-interval-toggle-container">
          <div
            id="pricing-interval-toggle-monthly"
            className={`pricing-interval-toggle-item ${
              monthlyIsVisible ? "pricing-interval-toggle-item-active" : ""
            }`}
            onClick={payMonthlyClicked}
          >
            Pay monthly
          </div>
          <div
            id="pricing-interval-toggle-yearly"
            className={`pricing-interval-toggle-item ${
              yearlyIsVisible ? "pricing-interval-toggle-item-active" : ""
            }`}
            onClick={payYearlyClicked}
          >
            Pay yearly
          </div>
        </div>
      </div>

      <div className="pricing-cards-container">
        {mapPrices
          .filter((price) => price.recurring_interval === recurringInterval)
          .map((price) => (
            <PriceCard
              {...{ ...price, isSignedIn, onNotSignedIn }}
              key={price.price_id}
            />
          ))}
      </div>
    </div>
    // </div>
  )
}

export default Buy
