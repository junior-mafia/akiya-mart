import React, { useState } from 'react'

// const images = [
//   'https://img01.suumo.com/front/gazo/bukken/040/N010000/img/574/70811574/70811574_0001.jpg',
//   'https://img01.suumo.com/front/gazo/bukken/040/N010000/img/574/70811574/70811574_0019.jpg',
//   'https://img01.suumo.com/front/gazo/bukken/040/N010000/img/574/70811574/70811574_0017.jpg',
// ]

interface CarouselProps {
    price_yen: number
    price_usd: string
    prefecture: string
    year: number
    url: string
    image_urls: string[]
    address: string
}

const Carousel = (props: CarouselProps) => {

    console.log(props.image_urls)

    const [currentImageIndex, setCurrentImageIndex] = useState(0)

    const nextImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % props.image_urls.length)
    }

    const prevImage = () => {
        setCurrentImageIndex((prevIndex) => (prevIndex - 1 + props.image_urls.length) % props.image_urls.length)
    }
    const translatedUrl = `https://translate.google.com/translate?sl=ja&tl=en&u=${props.url}`
    return (
        <>
            <h1>{props.price_usd}</h1>
            <p className='joey'>{props.prefecture}</p>
            <p className='joey'>{props.year}</p>
            <p className='joey'>{props.price_yen}</p>
            <p className='joey'>{props.address}</p>
            <a target="_blank" href={translatedUrl}>English</a>
            <a target="_blank" href={props.url}>日本語</a>

            <img src={props.image_urls[currentImageIndex]} style={{ width: "250px", height: "250px", objectFit: "contain" }}></img>
            {/* <img src={images[currentImageIndex]} alt={`Carousel image ${currentImageIndex + 1}`} /> */}
            <button onClick={prevImage}>Previous</button>
            <button onClick={nextImage}>Next</button>
        </>
    )
}

export default Carousel
