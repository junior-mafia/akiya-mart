import "mapbox-gl/dist/mapbox-gl.css"
import mapboxgl, { LngLatLike, Map, MapMouseEvent } from "mapbox-gl"

const DEFAULT_CENTER: LngLatLike = [-221.634321, 37.272892]

const DEFAULT_ZOOM = 6 // 4 and 5 don't work for some reason on small screens

interface MapSource {
  name: string
  url: string
}

const BALLOON_LAYER = "balloons"
const DOM_MAP_CONTAINER_ID = "container"
const MAP_STYLE = "mapbox://styles/mapbox/streets-v12"

const createMap = (): Map => {
  // Only works if the request comes from https://www.akiya-mart.com
  mapboxgl.accessToken = mapboxgl.accessToken =
    "pk.eyJ1Ijoiam9lc3RveCIsImEiOiJjbGhtaDV4NnAwaWU4M3BudXQzbjRyemRoIn0.tgx3FvpKZwJjlvcq4D5igw"
  return new mapboxgl.Map({
    container: DOM_MAP_CONTAINER_ID,
    style: MAP_STYLE,
    center: DEFAULT_CENTER,
    zoom: DEFAULT_ZOOM,
  })
}

const addMapSource = (map: Map, mapSource: MapSource) => {
  const now = new Date()
  now.setHours(Math.floor(now.getHours() / 3) * 3, 0, 0, 0) // Round to 3 hour intervals
  const timestamp = now.getTime()
  map.addSource(mapSource.name, {
    type: "geojson",
    data: `${mapSource.url}?v=${timestamp}`,
  })
}

const addBalloons = (map: Map, mapSource: MapSource) => {
  map.loadImage("mapbox-marker-icon-20px-pink2.png", (error, image) => {
    if (image === undefined) throw error
    else map.addImage("green-marker", image)
    map.addLayer({
      id: BALLOON_LAYER,
      type: "symbol",
      source: mapSource.name,
      layout: {
        "icon-image": "green-marker",
        "icon-size": 1,
        "icon-allow-overlap": true,
        "text-offset": [0, 0.9],
        "text-anchor": "top",
      },
    })
    // filterMap(
    //   priceUsdLower,
    //   priceUsdUpper,
    //   yearLower,
    //   yearUpper,
    //   underXDaysOnMarketLower,
    //   underXDaysOnMarketUpper,
    //   map
    // )
  })
}

const swapMapSource = (
  map: Map,
  previousMapSource: MapSource,
  mapSource: MapSource
) => {
  map.removeLayer(BALLOON_LAYER)
  map.removeSource(previousMapSource.name)
  addMapSource(map, mapSource)
  addBalloons(map, mapSource)
}

const addMouseEvents = (
  map: Map,
  onFeatureClick: (event: MapMouseEvent, map: Map) => void
) => {
  map.on("click", (e) => {
    onFeatureClick(e, map)
  })

  // Change the cursor to a pointer when the mouse is over the BALLOON_LAYER layer
  map.on("mouseenter", BALLOON_LAYER, () => {
    map.getCanvas().style.cursor = "pointer"
  })

  // Change the cursor back to the default when the mouse leaves the BALLOON_LAYER layer
  map.on("mouseleave", BALLOON_LAYER, () => {
    map.getCanvas().style.cursor = ""
  })
}

const setupMap = (
  // priceUsdLower: number,
  // priceUsdUpper: number,
  // yearLower: number,
  // yearUpper: number,
  // underXDaysOnMarketLower: number,
  // underXDaysOnMarketUpper: number,
  map: Map,
  mapSource: MapSource,
  onBalloonMarkerClick: (event: MapMouseEvent, map: Map) => void
): Map => {
  addMapSource(map, mapSource)
  addBalloons(map, mapSource)
  addMouseEvents(map, onBalloonMarkerClick)
  return map
}

// const filterMap = (
//   priceUsdLower: number,
//   priceUsdUpper: number,
//   yearLower: number,
//   yearUpper: number,
//   underXDaysOnMarketLower: number,
//   underXDaysOnMarketUpper: number,
//   map: Map
// ) => {
//   // const now = Math.floor(Date.now() / 1000)
//   // const oneDaySeconds = 24 * 60 * 60
//   // map.setFilter(BALLOON_LAYER, [
//   //   "all",
//   //   [">=", ["to-number", ["get", "price_usd"]], priceUsdLower],
//   //   ["<=", ["to-number", ["get", "price_usd"]], priceUsdUpper],
//   //   [">=", ["to-number", ["get", "construction_year"]], yearLower],
//   //   ["<=", ["to-number", ["get", "construction_year"]], yearUpper],
//   //   [
//   //     ">=",
//   //     ["to-number", ["get", "first_seen_at"]],
//   //     now - underXDaysOnMarketUpper * oneDaySeconds,
//   //   ],
//   //   [
//   //     "<=",
//   //     ["to-number", ["get", "first_seen_at"]],
//   //     now - underXDaysOnMarketLower * oneDaySeconds,
//   //   ],
//   // ])
// }

export { createMap, setupMap, swapMapSource, MapSource, BALLOON_LAYER }
