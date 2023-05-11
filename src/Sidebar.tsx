import React, { useState } from 'react'
import RangeSlider from './Slider'
import Button from '@mui/material/Button';

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

    const containerHideItStyle = {
        padding: isMinimized ? '0px' : '2%'
    }

    const hideItStyle = {
        display: isMinimized ? 'none' : 'block'
    }

    return (
        <div className="filters-container" style={containerHideItStyle}>
            
            <div className="filter-flex-item" style={hideItStyle}>
                <p className="filters-header">あきやマート</p>
            </div>
            
            <div className="filter-flex-item" style={hideItStyle}>
                <label htmlFor="filter" className="filter-input-label">
                    price (usd)
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
                    year built
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
                <Button 
                    variant="contained" 
                    color="primary" 
                    className="filter-show-hide" 
                    onClick={handleClick}
                    size="small"
                    sx={{
                        backgroundColor: '#ffabeb',
                        fontFamily: 'Fredoka',
                        color: '#ffffff',
                        textTransform: "none",
                        '&:hover': {
                            backgroundColor: '#fc80de',
                        },
                    }}
                >
                    {isMinimized ? 'show' : 'hide'}
                </Button>
            </div>

        </div>
    )
}

export default Filters