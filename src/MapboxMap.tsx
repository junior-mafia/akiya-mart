import React, { useEffect, useRef, useState } from 'react'
import { Map } from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import { newMap, setupMap, filterMap } from './createMap'
import Listing, { ListingProps } from './Listing'
import { ReactJSXElement } from '@emotion/react/types/jsx-namespace'

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
  const ignore = useRef(false)
  const [map, setMap] = useState<Map | undefined>(undefined)
  const [showListings, setShowListings] = useState(false)
  const [listings, setListings] = useState<ReactJSXElement[]>([])
  const [currentListingIndex, setCurrentListingIndex] = useState(0)

  const nextListing = () => {
    setCurrentListingIndex((prevIndex) => (prevIndex + 1) % listings.length)
  }

  const prevListing = () => {
      setCurrentListingIndex((prevIndex) => (prevIndex - 1 + listings.length) % listings.length)
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
          return <Listing key={props.url}  {...fullProps}/>
      })

    if (listings.length > 0) {
        // const firstFeature = features[0]
        // const props = firstFeature.properties as ListingProps
        // const listing = <Listing key={props.url} {...props}/>

        setListings(listings)
        setShowListings(true)
    } else {
      setListings([])
      setShowListings(false)
      setCurrentListingIndex(0)
    }
  }




  // Run once - idempotent under React Strict Mode
  useEffect(() => {
    if (ignore.current) return
    const blankMap = newMap()
    const map = setupMap(priceUsdLower, priceUsdUpper, yearLower, yearUpper, blankMap, onFeatureClick)
    setMap(map)
    ignore.current = true
  }, [])

  // Run when map or filter changes
  useEffect(() => {
    if (!map) return
    filterMap(priceUsdLower, priceUsdUpper, yearLower, yearUpper, map)
  }, [priceUsdLower, priceUsdUpper, yearLower, yearUpper])


  return (
    <>
      {showListings && (
        <div className="listings-container">
          <div>{listings[currentListingIndex]}</div>
          <button onClick={prevListing}>previous listing</button>
          <button onClick={nextListing}>next listing</button>
          <p className="listing-info">{currentListingIndex + 1} / {listings.length} listings</p>
        </div>
      )}
    </>
  )
}





export default MapboxMap
