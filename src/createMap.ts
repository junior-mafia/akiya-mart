import 'mapbox-gl/dist/mapbox-gl.css'
import mapboxgl, { LngLatLike, Map, MapMouseEvent } from 'mapbox-gl'

const DEFAULT_CENTER: LngLatLike = [-221.634321, 37.272892]

const DEFAULT_ZOOM = 6 // 4 and 5 don't work for some reason on small screens

const newMap = (): Map => {
    // Only works if the request comes from https://www.akiya-mart.com
    mapboxgl.accessToken = mapboxgl.accessToken = 'pk.eyJ1Ijoiam9lc3RveCIsImEiOiJjbGhtaDV4NnAwaWU4M3BudXQzbjRyemRoIn0.tgx3FvpKZwJjlvcq4D5igw'
    return new mapboxgl.Map({
        container: 'container',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: DEFAULT_CENTER,
        zoom: DEFAULT_ZOOM,
    })
}

const setupMap = (
    priceUsdLower: number, 
    priceUsdUpper: number,
    yearLower: number,
    yearUpper: number,
    underXDaysOnMarketLower: number,
    underXDaysOnMarketUpper: number,
    map: Map,
    onFeatureClick: (event: MapMouseEvent, map: Map) => void
): Map => {
    map.on('load', () => {

        map.addSource('listings-free', {
            type: 'geojson',
            data: 'listings_free.geojson'
        })
        
        map.loadImage('mapbox-marker-icon-20px-pink2.png', (error, image) => {
            if (image === undefined) throw error
            else 
                map.addImage('green-marker', image)
                map.addLayer({
                    id: 'markers',
                    type: 'symbol',
                    source: 'listings-free',
                    layout: {
                        'icon-image': 'green-marker',
                        'icon-size': 1,
                        'icon-allow-overlap': true,
                        'text-offset': [0, 0.9],
                        'text-anchor': 'top'
                    }
                })
                filterMap(priceUsdLower, priceUsdUpper, yearLower, yearUpper, underXDaysOnMarketLower, underXDaysOnMarketUpper, map)
        })
    })

  map.on('click', (e) => {
    onFeatureClick(e, map)
  })

  // Change the cursor to a pointer when the mouse is over the 'balloon-markers' layer
  map.on('mouseenter', 'markers', () => {
      map.getCanvas().style.cursor = 'pointer'
  })
  
  // Change the cursor back to the default when the mouse leaves the 'balloon-markers' layer
  map.on('mouseleave', 'markers', () => {
      map.getCanvas().style.cursor = ''
  })

  return map
}

const filterMap = (
    priceUsdLower: number, 
    priceUsdUpper: number,
    yearLower: number,
    yearUpper: number,
    underXDaysOnMarketLower: number,
    underXDaysOnMarketUpper: number,
    map: Map
) => {
    const timestamp = Math.floor(Date.now() / 1000)
    const oneDaySeconds = 24 * 60 * 60
    map.setFilter('markers', [
        'all',
        ['>=', ['to-number', ['get', 'price_usd']], priceUsdLower],
        ['<=', ['to-number', ['get', 'price_usd']], priceUsdUpper],
        ['>=', ['to-number', ['get', 'year']], yearLower],
        ['<=', ['to-number', ['get', 'year']], yearUpper],
        ['>=', ['to-number', ['get', 'seen_at']], timestamp - (underXDaysOnMarketUpper * oneDaySeconds)],
        ['<=', ['to-number', ['get', 'seen_at']], timestamp - (underXDaysOnMarketLower * oneDaySeconds)],
    ]);
}

const setSource = (
    isPaidTier: boolean,
    map: Map
) => {

    if (isPaidTier) {
        map.removeLayer('markers');
        map.removeSource('listings-free');

        map.addSource('listings', {
            type: 'geojson',
            data: 'listings.geojson',
        });

        map.addLayer({
            id: 'markers',
            type: 'symbol',
            source: 'listings',
            layout: {
                'icon-image': 'green-marker',
                'icon-size': 1,
                'icon-allow-overlap': true,
                'text-offset': [0, 0.9],
                'text-anchor': 'top'
            }
        })
    }
}

export {
    newMap,
    setupMap,
    filterMap,
    setSource,
}