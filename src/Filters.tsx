import React from 'react'
import RangeSlider from './Slider'

interface FiltersProps {
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
}

const Filters = ({
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
}: FiltersProps) => {
    return (
        <div className="filters-container">

            <div className="filter-flex-item">
                <label htmlFor="filter" className="filter-input-label">
                    Price (USD)
                </label>
                <RangeSlider
                    min={priceUsdMin}
                    max={priceUsdMax}
                    lower={priceUsdLower}
                    upper={priceUsdUpper}
                    onLowerChange={onPriceUsdLowerChange} 
                    onUpperChange={onPriceUsdUpperChange}
                />
            </div>

            <div className="filter-flex-item">
                <label htmlFor="filter" className="filter-input-label">
                    Year Built
                </label>
                <RangeSlider
                    min={yearMin}
                    max={yearMax}
                    lower={yearLower}
                    upper={yearUpper}
                    onLowerChange={onYearLowerChange} 
                    onUpperChange={onYearUpperChange}
                />
            </div>

        </div>
    )
}

export default Filters