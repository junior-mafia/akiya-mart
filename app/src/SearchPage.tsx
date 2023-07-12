import React, { useState } from "react"
import MapboxMap from "./MapboxMap"
import "./styles/search-page.css"

const SearchPage = () => {
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
        <div className="search-page-container">
            <div id="container" className="search-page-map-container">
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
            <div className="search-page-list-container">
                <div className="grid-search-results">
                    <div className="search-page-list-header">
                        <h1 className="search-title">Liked Properties</h1>
                        <div className="coming-soon">Coming soon</div>
                    </div>
                    <div className="photo-cards">
                        <div className="photo-card"></div>
                        <div className="photo-card"></div>
                        <div className="photo-card"></div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SearchPage
