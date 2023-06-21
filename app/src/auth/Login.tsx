import React, { useState } from "react"
import { login } from "./auth"
import "./styles/authenticator.css"
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate()

  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleLogin = async () => {
    try {
      setLoading(true)
      setError("")
      await login(email, password)
      navigate("/")
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="auth-input-field">
        <label className="auth-input-label" htmlFor="email">
          Email
        </label>
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
          id="email"
          className="auth-input"
          placeholder="Enter email"
        />
      </div>

      <div className="auth-input-field">
        <label className="auth-input-label" htmlFor="password">
          Password
        </label>
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          id="password"
          className="auth-input"
          placeholder="Enter password"
        />
      </div>

      {error && <div className="auth-error-message">{error}</div>}

      <div className="auth-input-field">
        <button onClick={handleLogin} className="auth-submit-button">
          {loading ? "Logging In..." : "Sign In"}
        </button>
      </div>
    </>
  )
}

export default Login
