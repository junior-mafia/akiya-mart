import React, { useEffect, useRef, useState } from 'react'
import mapboxgl, { Map } from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { newMap, setupMap, filterMap } from './createMap'

interface MapboxMapProps {
  priceUsdLower: number
  priceUsdUpper: number
  yearLower: number
  yearUpper: number
}

const MapboxMap = ({ 
  priceUsdLower,
  priceUsdUpper,
  yearLower,
  yearUpper,
}: MapboxMapProps) => {
  const ignore = useRef(false);
  const [map, setMap] = useState<Map | undefined>(undefined)

  // Run once - idempotent under React Strict Mode
  useEffect(() => {
    if (ignore.current) return
    setMap(setupMap(newMap()))
    ignore.current = true;
  }, [])

  // Run when map or filter changes
  useEffect(() => {
    if (!map) return
    // filterMapByYear(year, map)
    // filterMapByPriceUsdLower(priceUsdLower, map)
    filterMap(priceUsdLower, priceUsdUpper, yearLower, yearUpper, map)
  }, [priceUsdLower, priceUsdUpper, yearLower, yearUpper])

  return <div/>
}

export default MapboxMap
