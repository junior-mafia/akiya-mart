import React, { useState } from "react"
import MapboxMap from "./MapboxMap"
import Sidebar from "./Sidebar"
import Footer from "./Footer"
import NavBar from "./NavBar"

const Main = () => {
  const [isPaidTier, setIsPaidTier] = useState(false)

  const priceUsdMin = 0
  const priceUsdMax = 200000
  const defaultUsdPriceMin = 25000
  const defaultUsdPriceMax = 130000
  const [priceUsdLower, setPriceUsdLower] = useState<number>(defaultUsdPriceMin)
  const [priceUsdUpper, setPriceUsdUpper] = useState<number>(defaultUsdPriceMax)

  const yearMin = 1800
  const yearMax = 2023
  const defaultYearMin = 1900
  const defaultYearMax = 2000
  const [yearLower, setYearLower] = useState<number>(defaultYearMin)
  const [yearUpper, setYearUpper] = useState<number>(defaultYearMax)

  const underXDaysOnMarketMin = 0
  const underXDaysOnMarketMax = 30
  const defaultUnderXDaysOnMarketMin = 0
  const defaultUnderXDaysOnMarketMax = 30
  const [underXDaysOnMarketLower, setUnderXDaysOnMarketLower] =
    useState<number>(defaultUnderXDaysOnMarketMin)
  const [underXDaysOnMarketUpper, setUnderXDaysOnMarketUpper] =
    useState<number>(defaultUnderXDaysOnMarketMax)


  return (
    <>
    <div className="main-container">
      <NavBar />

      <Sidebar
        priceUsdMin={priceUsdMin}
        priceUsdMax={priceUsdMax}
        priceUsdLower={priceUsdLower}
        priceUsdUpper={priceUsdUpper}
        onPriceUsdLowerChange={setPriceUsdLower}
        onPriceUsdUpperChange={setPriceUsdUpper}
        yearMin={yearMin}
        yearMax={yearMax}
        yearLower={yearLower}
        yearUpper={yearUpper}
        onYearLowerChange={setYearLower}
        onYearUpperChange={setYearUpper}
        underXDaysOnMarketMin={underXDaysOnMarketMin}
        underXDaysOnMarketMax={underXDaysOnMarketMax}
        underXDaysOnMarketLower={underXDaysOnMarketLower}
        underXDaysOnMarketUpper={underXDaysOnMarketUpper}
        setUnderXDaysOnMarketLower={setUnderXDaysOnMarketLower}
        setUnderXDaysOnMarketUpper={setUnderXDaysOnMarketUpper}
      />

      {/* <Footer isPaidTier={isPaidTier} setIsPaidTier={setIsPaidTier} /> */}

      <div style={{ width: "100%", height: "70vh" }}>
        <MapboxMap
          isPaidTier={isPaidTier}
          priceUsdLower={priceUsdLower}
          priceUsdUpper={priceUsdUpper}
          yearLower={yearLower}
          yearUpper={yearUpper}
          underXDaysOnMarketLower={underXDaysOnMarketLower}
          underXDaysOnMarketUpper={underXDaysOnMarketUpper}
        />
      </div>
    </div>

    <div id="container"></div>
    </>
  )
}

export default Main
