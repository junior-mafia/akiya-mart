import React, { useState } from 'react'

interface FiltersProps {
    onYearChange: (event: React.ChangeEvent<HTMLInputElement>) => void
    onPriceYenUpperChange: (event: React.ChangeEvent<HTMLInputElement>) => void
}

const Filters = ({ onYearChange, onPriceYenUpperChange }: FiltersProps) => {
    return (
        <div className="filters-container">
            <div className="filter-flex-item">
                <label htmlFor="filter" className="filter-input-label">
                    Year
                </label>
                <input
                    id="filter"
                    type="text"
                    onChange={onYearChange}
                    className="input-field"
                />
            </div>
            <div className="filter-flex-item">
                <label htmlFor="filter" className="filter-input-label">
                    Price (JPY)
                </label>
                <input
                    id="filter"
                    type="text"
                    onChange={onPriceYenUpperChange}
                    className="input-field"
                />
            </div>
        </div>
    )
}

export default Filters