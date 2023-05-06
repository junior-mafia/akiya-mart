import React, { useEffect, useRef, useState } from 'react'
import mapboxgl, { Map } from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { newMap, setupMap, filterMapByYear, filterMapByPriceYenUpper } from './createMap'

interface MapboxMapProps {
  year: number
  priceYenUpper: number
}

const MapboxMap = ({ year, priceYenUpper }: MapboxMapProps) => {
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
    filterMapByYear(year, map)
  }, [year])

  // Run when map or filter changes
  useEffect(() => {
    if (!map) return
    filterMapByPriceYenUpper(priceYenUpper, map)
  }, [priceYenUpper])

  return <div/>
}

export default MapboxMap
