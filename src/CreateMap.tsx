import React from 'react'
import 'mapbox-gl/dist/mapbox-gl.css'
import mapboxgl, { LngLatLike, Map } from 'mapbox-gl'
import Carousel from './Popup'
import { createRoot } from 'react-dom/client'

const DEFAULT_CENTER: LngLatLike = [-221.634321, 37.272892]

const DEFAULT_ZOOM = 4.4

const newMap = (): Map => {
    mapboxgl.accessToken = mapboxgl.accessToken = 'pk.eyJ1Ijoiam9lc3RveCIsImEiOiJjbGd6a3A0enkwazVnM3NtcGZvN2h3MWp2In0.T7zApwiAP3P0DI49LATdwA'
    return new mapboxgl.Map({
        container: 'container',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: DEFAULT_CENTER,
        zoom: DEFAULT_ZOOM,
    })
}

interface FeatureProperties {
    price_yen: number
    price_usd: number
    prefecture: string
    year: number
    url: string
    image_urls: string
    address: string
}

const setupMap = (map: Map): Map => {
    map.on('load', () => {
        map.addSource('listings', {
            type: 'geojson',
            data: 'listings.geojson'
        })
        map.loadImage('mapbox-marker-icon-20px-pink2.png', (error, image) => {
            if (image === undefined) throw error
            else 
                map.addImage('green-marker', image)
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
        })
    })

  map.on('click', (e) => {
    const features = map.queryRenderedFeatures(e.point, { layers: ['markers'] }) as GeoJSON.Feature<GeoJSON.Point>[]
    if (features.length > 0) {
        const feature = features[0]
        const popupContainer = document.createElement('div')
        popupContainer.className = 'bong';

        createRoot(popupContainer).render(<Carousel {...feature.properties as FeatureProperties}/>)
        
        const lngLat = feature.geometry.coordinates as [number, number]
        new mapboxgl.Popup({ offset: [0, -15] })
            .setLngLat(lngLat)
            .setDOMContent(popupContainer)
            .addTo(map)
    }
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
    map: Map
) => {
    map.setFilter('markers', [
        'all',
        ['>=', ['to-number', ['get', 'price_usd']], priceUsdLower],
        ['<=', ['to-number', ['get', 'price_usd']], priceUsdUpper],
        ['>=', ['to-number', ['get', 'year']], yearLower],
        ['<=', ['to-number', ['get', 'year']], yearUpper],
    ]);
}

export {
    newMap,
    setupMap,
    filterMap,
}