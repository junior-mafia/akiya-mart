interface DashboardData {
  email: string
  subscription_id: string | undefined
  product_name: string | undefined
  status: string | undefined
  currency: string | undefined
  unit_amount: number | undefined
  recurring_interval: string | undefined
}

const fetchDashboardData = async (): Promise<DashboardData> => {
  const response = await fetch("/user/dashboard", {
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
    return data.result
  }
}

export { fetchDashboardData, DashboardData }
