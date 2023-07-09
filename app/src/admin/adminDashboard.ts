interface AdminDashboardData {
  message: string
}

const fetchAdminDashboardData = async (): Promise<AdminDashboardData> => {
  const response = await fetch("/admin/fetch-admin-data", {
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
    return data.results
  }
}

export { fetchAdminDashboardData, AdminDashboardData }
