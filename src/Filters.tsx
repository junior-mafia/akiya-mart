import React, { useState } from 'react'
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


    const [isMinimized, setIsMinimized] = useState(false);

    const handleClick = () => {
        setIsMinimized(!isMinimized);
    };

    const containerStyle = {
        width: isMinimized ? '100px' : 'auto',
        height: isMinimized ? '50px' : 'auto',
        transition: 'width 0.3s ease-out, height 0.3s ease-out',
    }

    const hideItStyle = {
        display: isMinimized ? 'none' : 'block'
    }

    return (
        <div className="filters-container" style={containerStyle}>
            
            <div className="filter-flex-item" style={hideItStyle}>
                <p className="filters-header">あきやマート</p>
            </div>
            
            <div className="filter-flex-item" style={hideItStyle}>
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

            <div className="filter-flex-item" style={hideItStyle}>
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

            <div className="filter-flex-item">
                <button className="filter-show-hide" onClick={handleClick}>{isMinimized ? 'Show Filters' : 'Hide Filters'}</button>
            </div>

        </div>
    )
}

export default Filters