import React, { useState } from "react"
import RangeSlider from "./RangeSlider"
import "./styles/sidebar.css"
import "./styles/main.css"

interface SidebarProps {
  priceUsdMin: number
  priceUsdMax: number
  priceUsdLower: number
  priceUsdUpper: number
  onPriceUsdLowerChange: (priceUsdLower: number) => void
  onPriceUsdUpperChange: (priceUsdUpper: number) => void
  yearMin: number
  yearMax: number
  yearLower: number
  yearUpper: number
  onYearLowerChange: (priceUsdLower: number) => void
  onYearUpperChange: (priceUsdUpper: number) => void
  underXDaysOnMarketMin: number
  underXDaysOnMarketMax: number
  underXDaysOnMarketLower: number
  underXDaysOnMarketUpper: number
  setUnderXDaysOnMarketLower: (underXDaysOnMarketLower: number) => void
  setUnderXDaysOnMarketUpper: (underXDaysOnMarketUpper: number) => void
}

const Sidebar = ({
  priceUsdMin,
  priceUsdMax,
  priceUsdLower,
  priceUsdUpper,
  onPriceUsdLowerChange,
  onPriceUsdUpperChange,
  yearMin,
  yearMax,
  yearLower,
  yearUpper,
  onYearLowerChange,
  onYearUpperChange,
  underXDaysOnMarketMin,
  underXDaysOnMarketMax,
  underXDaysOnMarketLower,
  underXDaysOnMarketUpper,
  setUnderXDaysOnMarketLower,
  setUnderXDaysOnMarketUpper,
}: SidebarProps) => {
  const [isMinimized, setIsMinimized] = useState(true)

  const minOrMaxIt = () => {
    setIsMinimized(!isMinimized)
  }

  return (
    <div className="sidebar-container">
      <div className="sidebar-item transparent-until-hover" onClick={minOrMaxIt}>
          Filters
      </div>

      {/* {!isMinimized && (
        <>
          <div className="sidebar-filter">
            <div>Price (USD)</div>
            <RangeSlider
              min={priceUsdMin}
              max={priceUsdMax}
              lower={priceUsdLower}
              upper={priceUsdUpper}
              onLowerChange={onPriceUsdLowerChange}
              onUpperChange={onPriceUsdUpperChange}
              step={10000}
            />
          </div>
          <div className="sidebar-filter">
            <div>Year Built</div>
            <RangeSlider
              min={yearMin}
              max={yearMax}
              lower={yearLower}
              upper={yearUpper}
              onLowerChange={onYearLowerChange}
              onUpperChange={onYearUpperChange}
              step={1}
            />
          </div>
          <div className="sidebar-filter">
            <div>Days on Market</div>
            <RangeSlider
              min={underXDaysOnMarketMin}
              max={underXDaysOnMarketMax}
              lower={underXDaysOnMarketLower}
              upper={underXDaysOnMarketUpper}
              onLowerChange={setUnderXDaysOnMarketLower}
              onUpperChange={setUnderXDaysOnMarketUpper}
              step={1}
            />
          </div>
        </>
      )} */}
    </div>
  )
}

export default Sidebar
