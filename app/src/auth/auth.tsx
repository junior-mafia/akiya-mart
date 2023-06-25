interface RegisterResponse {
  message: string
}

interface LoginResponse {
  message: string
}

interface LogoutResponse {
  message: string
}

interface IsLoggedInResponse {
  is_logged_in: boolean
}

interface UnlockResponse {
  message: string
}

const isLoggedIn = async (): Promise<IsLoggedInResponse> => {
  const response = await fetch("/auth/is-logged-in", {
    method: "GET",
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

const register = async (
  email: string,
  password: string
): Promise<RegisterResponse> => {
  const response = await fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  })

  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  }

  return data
}

const login = async (
  email: string,
  password: string
): Promise<LoginResponse> => {
  const response = await fetch("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  })

  const data = await response.json()
  if (!response.ok) {
    const message = `${data.message}`
    throw new Error(message)
  }

  return data
}

const logout = async (): Promise<LogoutResponse> => {
  const response = await fetch("/auth/logout", {
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

export { register, login, logout, isLoggedIn }
