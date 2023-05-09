import React, { useState } from 'react'
import MapboxMap from './MapboxMap'
import Filters from './Filters'


const strictParseInt = (input: string): number | undefined => {
    if (/^\d+$/.test(input)) {
        return parseInt(input, 10)
    }
    return undefined
}

const parseIntFromInput = (input: string): number | undefined => {
    if (input === undefined)
        return
    return strictParseInt(input)
}

const App = () => {
    const priceUsdMin = 0
    const priceUsdMax = 100000
    const [priceUsdLower, setPriceUsdLower] = useState<number>(priceUsdMin)
    const [priceUsdUpper, setPriceUsdUpper] = useState<number>(priceUsdMax)
    const yearMin = 1800
    const yearMax = 2023
    const [yearLower, setYearLower] = useState<number>(yearMin)
    const [yearUpper, setYearUpper] = useState<number>(yearMax)

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