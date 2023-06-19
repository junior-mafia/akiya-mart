import React, { useState } from "react"
import { register } from "./auth"
import './Register.css';

interface RegisterProps {
    setLoginIsVisible: (value: boolean) => void
    setRegistrationIsVisible: (value: boolean) => void
    setLogoutIsVisible: (value: boolean) => void
}

const Register = (props: RegisterProps) => {
  const [email, setEmail] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [error, setError] = useState<string>("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleRegister = async () => {
    try {
        setLoading(true)
        setError("")
        await register(email, password)
        props.setLoginIsVisible(true)
        props.setRegistrationIsVisible(false)
    } catch (err) {
        setError(err.message)
    } finally {
        setLoading(false)
    }
  }

  return (
    <div className="form-container">
        <h1 className="header">New Account</h1>

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
            <button onClick={handleRegister} className="submit-button">
                {loading ? "Registering..." : "Submit"}
            </button>
        </div>
    </div>
  )
}

export default Register
