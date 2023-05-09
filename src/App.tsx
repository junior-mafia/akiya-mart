import React, { useState } from 'react'
import MapboxMap from './MapboxMap'
import Filters from './Filters'

const App = () => {
    const priceUsdMin = 0
    const priceUsdMax = 100000
    const defaultUsdPriceMin = 0
    const defaultUsdPriceMax = 15000
    const [priceUsdLower, setPriceUsdLower] = useState<number>(defaultUsdPriceMin)
    const [priceUsdUpper, setPriceUsdUpper] = useState<number>(defaultUsdPriceMax)
    const yearMin = 1800
    const yearMax = 2023
    const defaultYearMin = 1988
    const defaultYearMax = yearMax
    const [yearLower, setYearLower] = useState<number>(defaultYearMin)
    const [yearUpper, setYearUpper] = useState<number>(defaultYearMax)

    return (
        <div>
            <Filters
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
            
            <div style={{ width: '100%', height: '70vh' }}>
                <MapboxMap 
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