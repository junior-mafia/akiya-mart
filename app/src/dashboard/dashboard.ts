interface DashboardData {
  email: string
  subscription_type: string
  subscription_status: string
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
