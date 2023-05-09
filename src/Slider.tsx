import React from 'react'
import { Slider } from '@mui/material'
import { useTheme } from '@mui/system'

interface RangeSliderProps {
  min: number
  max: number
  lower: number,
  upper: number,
  onLowerChange: (lower: number) => void
  onUpperChange: (upper: number) => void   
}

const RangeSlider: React.FC<RangeSliderProps> = ({ min, max, lower, upper, onLowerChange, onUpperChange }) => {
  const theme = useTheme()

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    const [_lower, _upper] = newValue as [number, number]
    onLowerChange(_lower)
    onUpperChange(_upper)
  }

  return (
      <div className="price-slider">
        <Slider
          value={[lower, upper]}
          onChange={handleSliderChange}
          valueLabelDisplay="auto"
          min={min}
          max={max}
          sx={{
            '& .MuiSlider-thumb': {
              borderColor: theme.palette.primary?.main || 'blue',
            },
            '& .MuiSlider-track': {
              background: theme.palette.primary?.main || 'blue',
            },
            '& .MuiSlider-rail': {
              opacity: 0.5,
            },
          }}
        />
      </div>
  )
}

export default RangeSlider
