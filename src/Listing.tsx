import React, { useState } from 'react'

interface ListingProps {
    price_yen: number
    price_usd: number
    prefecture: string
    year: number
    url: string
    image_urls: string
    address: string
    seen_at: number
    latitude: number
    longitude: number
}

const usd_formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
  
  const yen_formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'JPY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  })
  
  const display_usd = (amount: number): string => usd_formatter.format(amount)
  const display_yen = (amount: number): string => yen_formatter.format(amount)

const Listing = (props: ListingProps) => {
    const [currentImageIndex, setCurrentImageIndex] = useState(0)
    
    const image_urls: string[] = JSON.parse(props.image_urls)
    const countImages = image_urls.length
    const translatedUrl = `https://translate.google.com/translate?sl=ja&tl=en&u=${props.url}`
    const unix_timestamp = props.seen_at
    const date = new Date(unix_timestamp * 1000)
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    const formattedTime = `${year}-${month}-${day}`
    const mapsURL = `https://www.google.com/maps/search/?api=1&query=${props.latitude},${props.longitude}`;
    const streetViewURL = `https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${props.latitude},${props.longitude}`;


    const nextImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % countImages)
    }

    const prevImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex - 1 + countImages) % countImages)
    }

    return (
        <div key={props.url} className="listing">
            <div className="listing-info">
                <div className="listing-header">{display_usd(props.price_usd)}</div>
                <div className="listing-header-subscript">{display_yen(props.price_yen)}</div>
            </div>
            <div className="listing-image-container">
                <img className="listing-image" src={image_urls[currentImageIndex]}></img>
            </div>
            <p className="listing-info">{}</p>
            <a className="listing-info" target="_blank" href={translatedUrl}>see more images here</a>
            <p className="listing-info">on the market since at least {formattedTime}</p>
            <a className="listing-info" target="_blank" href={mapsURL}>google maps view</a>
            <a className="listing-info" target="_blank" href={streetViewURL}>google street view</a>



            <button onClick={prevImage}>previous image</button>
            <button onClick={nextImage}>next image</button>
            <p className="listing-info">{currentImageIndex + 1} / {countImages} images</p>
        </div>
    )
}

export default Listing
export { ListingProps }