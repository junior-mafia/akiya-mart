import React, { useState } from 'react'
import RangeSlider from './Slider'
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import { createHash } from 'crypto'

const secret = '6da814e354ade364b0b167119a0922a58bf9bf479454e1cdf07af9f34676f146'

function hashSHA256(value: string): string {
    const hash = createHash('sha256');
    hash.update(value);
    return hash.digest('hex');
}

interface FiltersProps {
    setIsPaidTier: (isPaidTier: boolean) => void
    isPaidTier: boolean
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
    setIsPaidTier,
    isPaidTier,
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
    const [inputValue, setInputValue] = useState('');

    const [isMinimized, setIsMinimized] = useState(false);

    const handleClick = () => {
        setIsMinimized(!isMinimized);
    };

    const handleButtonClick = () => {
        console.log(hashSHA256(inputValue), secret)
        if (hashSHA256(inputValue) === secret) {
            setIsPaidTier(true)
        } else {
            setIsPaidTier(false)
        }
    };

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
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

            { !isPaidTier && <div className="filter-flex-item" style={hideItStyle}>
                <label htmlFor="filter" className="filter-input-label">
                Unlock to discover all 80,000+ listings!
                </label>
                <TextField
                    label="password"
                    variant="outlined"
                    value={inputValue}
                    onChange={handleInputChange}
                />
                <Button 
                    onClick={handleButtonClick} 
                    variant="contained" 
                    color="primary" 
                    className="filter-show-hide" 
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
                    unlock
                </Button>
                <div>showing 100 / 80,000+ listings</div>
            </div> }

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