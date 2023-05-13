import React, { useState } from 'react'
import RangeSlider from './RangeSlider'
import Button from '@mui/material/Button'
import TextField from '@mui/material/TextField'
import { createHash } from 'crypto'

const secret = 'b44fef9656c878d2b80eb43df0e3e4f874eedc659075f967e0974c324f2e523d'

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

    const minimizeIt = () => {
        setIsMinimized(!isMinimized);
    };

    const handleButtonClick = () => {
        if (hashSHA256(inputValue) === secret) {
            console.log("UNLOCKED")
            setIsPaidTier(true)
        } else {
            setIsPaidTier(false)
        }
    };

    const handlePasswordInputChange = (e) => {
        setInputValue(e.target.value);
    };


    // already a member?
    // https://akiyamart.substack.com/ */}

    return (
        <div className="sidebar-container">
            
            <div className="sidebar-item sidebar-header-container">
                <div className="sidebar-item sidebar-header">
                    <img className="sidebar-header-logo" src="dalle.png" alt="logo" />
                    <div className="sidebar-header-title">あきやマート</div>
                </div>
                <button onClick={minimizeIt} className="sidebar-header-menu">
                    <i className="bx bx-menu" />
                </button>
            </div>
            
            { !isMinimized &&
                <>
                    <div className="sidebar-item sidebar-filter">
                        <div className="sidebar-label">
                            Price (USD)
                        </div>
                        <RangeSlider
                            min={priceUsdMin}
                            max={priceUsdMax}
                            lower={priceUsdLower}
                            upper={priceUsdUpper}
                            onLowerChange={onPriceUsdLowerChange} 
                            onUpperChange={onPriceUsdUpperChange}
                        />
                    </div>
                    <div className="sidebar-item sidebar-filter">
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
                </>
            }



            { !isPaidTier && 
                <>
                    <div className="sidebar-item sidebar-unlock-message">
                        Subscribe to unlock over 100k listings!
                    </div>

                    <div className="sidebar-item sidebar-unlock-inputs">
                            <TextField
                                label="Password"
                                variant="outlined"
                                value={inputValue}
                                onChange={handlePasswordInputChange}
                                sx={{
                                    '& .MuiOutlinedInput-root': {
                                      '& fieldset': {
                                        borderColor: '#dcdbdc', // Change the border color here
                                      },
                                      '&:hover fieldset': {
                                        borderColor: '#dcdbdc', // Change the border color when hovered here
                                      },
                                      '&.Mui-focused fieldset': {
                                        borderColor: '#dcdbdc', // Change the border color when focused here
                                      },
                                    },
                                    '& .MuiInputBase-input': {
                                      color: '#dcdbdc', // Change the text color here
                                    },
                                    '& .MuiFormLabel-root': {
                                        color: '#dcdbdc', // Change the label color here
                                    },
                                    '& .MuiFormLabel-root.Mui-focused': {
                                    color: '#dcdbdc', // Change the label color when focused here
                                    },
                                  }}
                            />
                            <Button 
                                onClick={handleButtonClick} 
                                variant="contained" 
                                color="primary" 
                                className="sidebar-show-hide" 
                                sx={{
                                    backgroundColor: '#ffabeb',
                                    fontFamily: 'Fredoka',
                                    color: '#ffffff',
                                    textTransform: "none",
                                    '&:hover': {
                                        backgroundColor: '#fc80de',
                                    },
                                    padding: '16.5px 30px',
                                }}
                            >
                                Unlock
                            </Button>
                    </div>
                </>
            }

        </div>
    )
}

export default Filters