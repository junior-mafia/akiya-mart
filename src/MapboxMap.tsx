import React, { useEffect, useRef, useState } from 'react'
import { Map } from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { newMap, setupMap, filterMap, setSource } from './createMap'
import Listing, { ListingProps } from './Listing'

interface MapboxMapProps {
  isPaidTier: boolean
  priceUsdLower: number
  priceUsdUpper: number
  yearLower: number
  yearUpper: number
  underXDaysOnMarketLower: number
  underXDaysOnMarketUpper: number
}

const MapboxMap = ({
  isPaidTier,
  priceUsdLower,
  priceUsdUpper,
  yearLower,
  yearUpper,
  underXDaysOnMarketLower,
  underXDaysOnMarketUpper,
}: MapboxMapProps) => {
  const ignore = useRef(false) // Used with React Strict Mode
  const [map, setMap] = useState<Map | undefined>(undefined)
  const [exitedUrl, setExitedUrl] = useState<string | undefined>(undefined)
  const [listings, setListings] = useState<ListingProps[]>([])

  const appendExitedUrl = (url) => {
    setExitedUrl(url)
  }

  const onFeatureClick = (e, map) =>  {
    const listings = map
      .queryRenderedFeatures(e.point, { layers: ['markers'] })
      .map(feature => {
          const props = feature.properties as ListingProps
          const { coordinates } = feature.geometry;
          const longitude = coordinates[0];
          const latitude = coordinates[1];
          const fullProps = {...props, latitude, longitude}
          return fullProps
      })
    if (listings.length > 0) {
        setListings(listings)
    } else {
      setListings([])
    }
  }

  // Run once - idempotent under React Strict Mode
  useEffect(() => {
    if (ignore.current) return
    const blankMap = newMap()
    const map = setupMap(priceUsdLower, priceUsdUpper, yearLower, yearUpper, underXDaysOnMarketLower, underXDaysOnMarketUpper, blankMap, onFeatureClick)
    setMap(map)
    ignore.current = true
  }, [])

  // Run when map or filter changes
  useEffect(() => {
    if (!map) return
    filterMap(priceUsdLower, priceUsdUpper, yearLower, yearUpper, underXDaysOnMarketLower, underXDaysOnMarketUpper, map)
  }, [priceUsdLower, priceUsdUpper, yearLower, yearUpper, underXDaysOnMarketLower, underXDaysOnMarketUpper])

  useEffect(() => {
    if (!map) return
    setSource(isPaidTier, map)
  }, [isPaidTier])

  if (exitedUrl) {
    setListings(listings.filter(listing => listing.url !== exitedUrl))
    setExitedUrl(undefined)
  }

  const listing = listings[0]
  return (<>
    { (listings.length > 0) && 
      <div className="listing-background" onClick={() => setListings([])}>
        <div className="listing-container" onClick={e => e.stopPropagation()}>
          <Listing key={listing.url} {...listing} countListings={listings.length} appendExitedUrl={appendExitedUrl} />
        </div>
      </div>
    }
  </>)
}





export default MapboxMap
