import React, { useState } from "react"
import { register } from "./auth"
import "./styles/authenticator.css"
import { useNavigate } from "react-router-dom";

const Register = () => {
  const navigate = useNavigate()

  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleRegister = async () => {
    try {
      setLoading(true)
      setError("")
      await register(email, password)
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
          placeholder="Create password"
        />
      </div>

      {error && <div className="auth-error-message">{error}</div>}

      <div className="auth-input-field">
        <button onClick={handleRegister} className="auth-submit-button">
          {loading ? "Registering..." : "Submit"}
        </button>
      </div>
    </>
  )
}

export default Register
