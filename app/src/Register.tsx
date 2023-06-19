import React, { useState } from "react"
import { register } from "./auth"
import './Register.css';

const Register = () => {
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [confirm, setConfirm] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleRegister = async () => {
    if (password !== confirm) {
        setError("Passwords do not match")
        return
    }
    try {
        setLoading(true)
        setError("")
        await register(email, password)
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

        <div className="input-field">
            <label className="label" htmlFor="confirm">Confirm Password</label>
            <input
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                type="password"
                id="confirm"
                className="input"
            />
        </div>

        {error && <div className="error-message">{error}</div>}
        
        <div className="input-field">
            <button onClick={handleRegister} className="submit-button">
                {loading ? "Registering..." : "Sign Up"}
            </button>
        </div>
    </div>
  )
}

export default Register
