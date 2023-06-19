import React, { useState } from "react"
import { login } from "./auth"
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleLogin = async () => {
    try {
        setLoading(true)
        setError("")
        await login(email, password)
    } catch (err) {
        setError(err.message)
    } finally {
        setLoading(false)
    }
  }

  return (
    <div className="form-container">
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
                {loading ? "Logging In..." : "Login"}
            </button>
        </div>
    </div>
  )
}

export default Login
