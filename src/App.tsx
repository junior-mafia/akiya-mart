import React, { useState } from 'react'
import MapboxMap from './MapboxMap'
import Sidebar from './Sidebar'
import Footer from './Footer'

const App = () => {
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
    

    return (
        <div>
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
            />

            <Footer
                isPaidTier={isPaidTier}
                setIsPaidTier={setIsPaidTier}
            />
            
            <div style={{ width: '100%', height: '70vh' }}>
                <MapboxMap 
                    isPaidTier={isPaidTier}
                    priceUsdLower={priceUsdLower} 
                    priceUsdUpper={priceUsdUpper} 
                    yearLower={yearLower}
                    yearUpper={yearUpper}
                />
            </div>
        </div>
    )
}

export default App