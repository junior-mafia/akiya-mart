import React, { useState } from 'react'

interface CarouselProps {
    price_yen: number
    price_usd: number
    prefecture: string
    year: number
    url: string
    image_urls: string
    address: string
}

const usd_formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
});

const yen_formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'JPY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
});

const display_usd = (amount: number): string => usd_formatter.format(amount);
const display_yen = (amount: number): string => yen_formatter.format(amount);


const Carousel = (props: CarouselProps) => {

    const image_urls: string[] = JSON.parse(props.image_urls);
    const countImages = image_urls.length
    const [currentImageIndex, setCurrentImageIndex] = useState(0)
    // console.log(image_urls)




    const nextImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % countImages)
    }

    const prevImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex - 1 + countImages) % countImages)
    }
    const translatedUrl = `https://translate.google.com/translate?sl=ja&tl=en&u=${props.url}`
    return (
        <>
            <h1>{display_usd(props.price_usd)}</h1>
            <p className='joey'>{props.prefecture}</p>
            <p className='joey'>{props.year}</p>
            <p className='joey'>{display_yen(props.price_yen)}</p>
            <p className='joey'>{props.address}</p>
            <a target="_blank" href={translatedUrl}>Real Estate Link</a>
            <a target="_blank" href={props.url}>日本語</a>

            <img src={image_urls[currentImageIndex]} style={{ width: "400px", height: "400px", objectFit: "contain" }}></img>
            <div>{currentImageIndex + 1} / {countImages}</div>
            <button onClick={prevImage}>Previous</button>
            <button onClick={nextImage}>Next</button>
        </>
    )
}

export default Carousel
