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
    const [year, setYear] = useState<number>(2023)
    const [priceYenUpper, setPriceYenUpper] = useState<number>(10000)

    const onYearChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
        const year = parseIntFromInput(e.target.value)
        if (year === undefined)
            return
        setYear(year)
    }

    const onPriceYenUpperChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
        const priceYenUpper = parseIntFromInput(e.target.value)
        if (priceYenUpper === undefined)
            return
        setPriceYenUpper(priceYenUpper)
    }

    return (
        <div>
            <Filters
                onYearChange={onYearChange}
                onPriceYenUpperChange={onPriceYenUpperChange} 
            />
            <div style={{ width: '100%', height: '70vh' }}>
                <MapboxMap year={year} priceYenUpper={priceYenUpper} />
            </div>
        </div>
    )
}

export default App