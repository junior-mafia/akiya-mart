import React, { useEffect, useRef, useState } from "react"
import { Map } from "mapbox-gl"
import "mapbox-gl/dist/mapbox-gl.css"
import {
  createMap,
  setupMap,
  swapMapSource,
  MapSource,
  BALLOON_LAYER,
} from "./map"
import Listing, { ListingProps } from "./Listing"
import { fetchActiveSubscription } from "./stripe/stripe"

interface MapboxMapProps {
  isPaidTier: boolean
  priceUsdLower: number
  priceUsdUpper: number
  yearLower: number
  yearUpper: number
  underXDaysOnMarketLower: number
  underXDaysOnMarketUpper: number
}

interface LiteListingFeatures {
  source: string
  bukken_id: string
  price_usd: number
}

interface FullListingFeatures {
  source: string
  bukken_id: string
  price_usd: number
}

const freeMapSource: MapSource = {
  name: "listings-free",
  url: "https://akiya-mart-tasks.b-cdn.net/lite-listings-free.geojson",
}

const paidMapSource: MapSource = {
  name: "listings",
  url: "https://akiya-mart-tasks.b-cdn.net/lite-listings.geojson",
}

const fetchListingDetails = async (
  source: string,
  bukken_id: string
): Promise<FullListingFeatures> => {
  const response = await fetch(`/listings/${source}/${bukken_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })

  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  }

  return data.results
}

const handleFetchListingDetails = async (source: string, bukken_id: string) => {
  const result = await fetchListingDetails(source, bukken_id)
  console.log(result)
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
  const [map, setMap] = useState<Map | undefined>(undefined)
  const [exitedUrl, setExitedUrl] = useState<string | undefined>(undefined)
  const [listings, setListings] = useState<ListingProps[]>([])
  const [mapSource, setMapSource] = useState<MapSource>(freeMapSource)

  const appendExitedUrl = (url) => {
    setExitedUrl(url)
  }

  const onFeatureClick = (e, map) => {
    const listings = map.queryRenderedFeatures(e.point, {
      layers: [BALLOON_LAYER],
    })
    console.log(listings.length)

    listings.map((feature) => {
      const { source, bukken_id, price_usd } =
        feature.properties as LiteListingFeatures
      console.log(source, bukken_id)
      handleFetchListingDetails(source, bukken_id)

      // const { coordinates } = feature.geometry
      // const longitude = coordinates[0]
      // const latitude = coordinates[1]
      // const fullProps = { ...props, latitude, longitude }
      // return fullProps
    })
    // if (listings.length > 0) {
    //   setListings(listings)
    // } else {
    //   setListings([])
    // }
  }

  const handleFetchActiveSubscription = async (map: Map) => {
    const subscriptionId = await fetchActiveSubscription()
    const mapSource = subscriptionId ? paidMapSource : freeMapSource
    setupMap(map, mapSource, onFeatureClick)
    setMap(map)
  }

  useEffect(() => {
    const blankMap = createMap()
    blankMap.on("load", () => {
      handleFetchActiveSubscription(blankMap)
    })

    // Clean up on unmount
    return () => {
      blankMap.remove()
    }
  }, [])

  // // Run when map or filter changes
  // useEffect(() => {
  //   if (!map) return
  //   filterMap(
  //     priceUsdLower,
  //     priceUsdUpper,
  //     yearLower,
  //     yearUpper,
  //     underXDaysOnMarketLower,
  //     underXDaysOnMarketUpper,
  //     map
  //   )
  // }, [
  //   priceUsdLower,
  //   priceUsdUpper,
  //   yearLower,
  //   yearUpper,
  //   underXDaysOnMarketLower,
  //   underXDaysOnMarketUpper,
  // ])

  // useEffect(() => {
  //   if (!map) return
  //   setSource(isPaidTier, map)
  // }, [isPaidTier])

  if (exitedUrl) {
    setListings(listings.filter((listing) => listing.url !== exitedUrl))
    setExitedUrl(undefined)
  }

  const listing = listings[0]
  return (
    <>
      {listings.length > 0 && (
        <div className="listing-background" onClick={() => setListings([])}>
          <div
            className="listing-container"
            onClick={(e) => e.stopPropagation()}
          >
            <Listing
              key={listing.url}
              {...listing}
              countListings={listings.length}
              appendExitedUrl={appendExitedUrl}
            />
          </div>
        </div>
      )}
    </>
  )
}

export default MapboxMap
