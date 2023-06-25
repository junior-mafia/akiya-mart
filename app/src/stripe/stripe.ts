interface UnlockResponse {
  message: string
  url: string
}

const unlock = async (productId: string): Promise<UnlockResponse> => {
  const response = await fetch("/stripe/create-checkout-session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ productId }),
  })
  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message} ${data.details}`
    throw new Error(message)
  }

  return data
}

export { unlock }
