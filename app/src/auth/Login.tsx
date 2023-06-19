import React, { useState } from "react"
import { login } from "./auth"
import './Login.css';

interface LoginProps {
    setLoginIsVisible: (value: boolean) => void
    setRegistrationIsVisible: (value: boolean) => void
    setLogoutIsVisible: (value: boolean) => void
}

const Login = (props: LoginProps) => {
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleLogin = async () => {
    try {
        setLoading(true)
        setError("")
        await login(email, password)
        props.setRegistrationIsVisible(false)
        props.setLoginIsVisible(false)
        props.setLogoutIsVisible(true)
    } catch (err) {
        setError(err.message)
    } finally {
        setLoading(false)
    }
  }

  return (
    <div className="form-container">
        <h1 className="header">Sign In</h1>

        <div className="input-field">
            <label className="label" htmlFor="email">Email</label>
            <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                type="email" 
                id="email"
                className="input"
            />
        </div>

        <div className="input-field">
            <label className="label" htmlFor="password">Password</label>
            <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                id="password"
                className="input"
            />
        </div>

        {error && <div className="error-message">{error}</div>}
        
        <div className="input-field">
            <button onClick={handleLogin} className="submit-button">
                {loading ? "Logging In..." : "Sign In"}
            </button>
        </div>
    </div>
  )
}

export default Login
