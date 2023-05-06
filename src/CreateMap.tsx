import 'mapbox-gl/dist/mapbox-gl.css'
import mapboxgl, { LngLatLike, Map } from 'mapbox-gl'
import ReactDOM from 'react-dom'
import Carousel from './Carousel'
import { createRoot } from 'react-dom/client'

const DEFAULT_CENTER: LngLatLike = [-221.634321, 37.272892]

const DEFAULT_ZOOM = 4.4


const newMap = (): Map => {
    mapboxgl.accessToken = mapboxgl.accessToken = 'pk.eyJ1Ijoiam9lc3RveCIsImEiOiJjbGd6a3A0enkwazVnM3NtcGZvN2h3MWp2In0.T7zApwiAP3P0DI49LATdwA'
    return new mapboxgl.Map({
        container: 'container',
        style: 'mapbox://styles/mapbox/dark-v11',
        center: DEFAULT_CENTER,
        zoom: DEFAULT_ZOOM,
    })
}

const setupMap = (map: Map): Map => {
    map.on('load', () => {
        map.addSource('listings', {
            type: 'geojson',
            data: 'listings.geojson'
        })
        map.loadImage('mapbox-marker-icon-20px-green.png', (error, image) => {
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

//   const popupHtml = ({properties: props}) => {
//     // const popupContent = ReactDOMServer.renderToString(Carousel())
//     // console.log(popupContent)
//     // return popupContent
    
//     const translatedUrl = `https://translate.google.com/translate?sl=ja&tl=en&u=${props.url}`
//     return (`
//         <h1>${props.price_usd_display}</h1>
//         <p class='joey'>${props.prefecture}</p>
//         <p class='joey'>${props.year}</p>
//         <p class='joey'>${props.price_yen_display}</p>

        // <a href=${translatedUrl}>English</a>
        // <a href=${props.url}>日本語</a>
//     `)
//   }

  map.on('click', (e) => {
    const features = map.queryRenderedFeatures(e.point, { layers: ['markers'] })
    if (features.length > 0) {
        const feature = features[0]
        
        const popupContainer = document.createElement('div')
        popupContainer.className = 'bong';
        // ReactDOM.eateRoot i(<Carousel />, popupContainer)


        console.log(feature.properties)
        createRoot(popupContainer).render(<Carousel {...feature.properties}/>)
        
        
        const popup = new mapboxgl.Popup({ offset: [0, -15] })
            .setLngLat(feature.geometry.coordinates)
            // .setHTML(popupHtml(feature))
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

const filterMapByYear = (
    year: number, 
    map: Map
) => {
    map.setFilter('markers', ['<=', ['to-number', ['get', 'year']], year])
}

const filterMapByPriceYenUpper = (
    priceYenUpper: number, 
    map: Map
) => {
    map.setFilter('markers', ['<=', ['to-number', ['get', 'price_yen']], priceYenUpper])
}

export {
    newMap,
    setupMap,
    filterMapByYear,
    filterMapByPriceYenUpper,
}