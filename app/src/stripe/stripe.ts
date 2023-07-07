interface CreateCheckoutSessionResponse {
  url: string
}

interface Price {
  price_id: string
  currency: string
  unit_amount: number
  recurring_interval: string
  name: string
  description: string
}

const createCheckoutSession = async (
  priceIds: string[]
): Promise<CreateCheckoutSessionResponse> => {
  const response = await fetch("/stripe/create-checkout-session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ priceIds }),
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.result
  }
}

const fetchMapPrices = async (): Promise<Price[]> => {
  const response = await fetch("/stripe/products/map", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  } else {
    return data.result.items
  }
}


const cancelSubscription = async (): Promise<any> => {
  const response = await fetch("/stripe/cancel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })

  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  }

  return data
}

export { createCheckoutSession, fetchMapPrices, Price, cancelSubscription }
