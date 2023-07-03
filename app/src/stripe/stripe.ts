interface CreateCheckoutSessionResponse {
  url: string
}

interface Products {
  price_id: string
  unit_amount: number
  name: string
  description: string
}

const createCheckoutSession = async (priceIds: string[]): Promise<CreateCheckoutSessionResponse> => {
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

const fetchProducts = async (): Promise<Products[]> => {
  const response = await fetch("/stripe/products", {
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
    return data
  }
}

export { createCheckoutSession, fetchProducts }
