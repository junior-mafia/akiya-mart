import React, { useState } from 'react'
import Button from '@mui/material/Button'

interface ListingProps {
    price_yen: number
    price_usd: number
    construction_year: number
    url: string
    image_urls: string
    address: string
    translated_address: string
    first_seen_at: number
    lat: number
    lon: number
    appendExitedUrl: (url) => void
    countListings: number
    is_geocoded: boolean
    description: string
    translated_description: string
    remarks: string
    translated_remarks: string
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


    // const description: string[] = JSON.parse(props.description)
    const image_urls: string[] = JSON.parse(props.image_urls)
    const countImages = image_urls.length
    const unix_timestamp = props.first_seen_at
    const date = new Date(unix_timestamp * 1000)
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    const formattedTime = `${year}-${month}-${day}`
    const mapsURL = `https://www.google.com/maps/search/?api=1&query=${props.lat},${props.lon}`;

    const nextImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % countImages)
    }

    const prevImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex - 1 + countImages) % countImages)
    }

    const onLeftClick = () => {
        prevImage()
    }

    const onRightClick = () => {
        nextImage()
    }

    return (
            <div key={props.url} className="listing">
                <div className="listing-header-container">
                    <div className="listing-header">{display_usd(props.price_usd)}</div>
                    
                    <div className="listing-exit-icon">
                        <button className="listing-exit-icon-button" onClick={() => props.appendExitedUrl(props.url)}>
                        {props.countListings}
                        </button>
                    </div>

                    
                </div>

                <div className="listing-subtitle">Built in { props.construction_year }</div>
                <div className="listing-subtitle">{props.translated_address}</div>

                <div className="listing-image-container">
                    <img className="listing-image" src={image_urls[currentImageIndex]}></img>
                    <div 
                        className="listing-interactive-image-div left"
                        onClick={onLeftClick}
                    ></div>
                    <div 
                        className="listing-interactive-image-div right"
                        onClick={onRightClick}
                    ></div>

                    <div className="listing-image-progress-bars">
                        { image_urls.map((_, index) => {
                            const colorClass = (index === currentImageIndex) ? "active" : "inactive"
                            return <div className={`listing-image-progress-bar ${colorClass}`} key={index} />
                        })}
                    </div>
                    

                </div>

                <div>{ props.translated_description }</div>
                <div>{ props.translated_remarks }</div>

                <Button
                    className="listing-button"
                    variant="contained"
                    color="primary"
                    onClick={() => window.open(props.url, '_blank')}
                    sx={{
                        backgroundColor: '#ffabeb',
                        fontFamily: 'YuseiMagic',
                        fontSize: '1.0rem',
                        color: '#ffffff',
                        textTransform: "none",
                        '&:hover': {
                            backgroundColor: '#fc80de',
                        },
                    }}
                >
                    See more images here
                </Button>

                <Button
                    className="listing-button"
                    variant="contained"
                    color="primary"
                    onClick={() => window.open(mapsURL, '_blank')}
                    sx={{
                        backgroundColor: '#ffabeb',
                        fontFamily: 'YuseiMagic',
                        fontSize: '1.0rem',
                        color: '#ffffff',
                        textTransform: "none",
                        '&:hover': {
                            backgroundColor: '#fc80de',
                        },
                    }}
                >
                    Google maps view { props.is_geocoded && "(approximate)" }
                </Button>

                <div className="listing-subtitle">On the market since {formattedTime}</div>

            </div> )
}

export default Listing
export { ListingProps }