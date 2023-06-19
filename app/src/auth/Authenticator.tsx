import React, { useEffect, useState } from "react"
import Register from "./Register"
import Login from "./Login"
import Logout from "./Logout"
import { isLoggedIn } from "./auth"

const Authenticator = () => {
    const [registrationIsVisible, setRegistrationIsVisible] = useState<boolean>(false)
    const [loginIsVisible, setLoginIsVisible] = useState<boolean>(false)
    const [logoutIsVisible, setLogoutIsVisible] = useState<boolean>(false)
    
    const handleLogin = async () => {
        try {
            // setLoading(true)
            // setError("")
            const result = await isLoggedIn()
            if (result.is_logged_in) {
                setLoginIsVisible(false)
                setRegistrationIsVisible(false)
                setLogoutIsVisible(true)
            } else {
                setLoginIsVisible(true)
                setRegistrationIsVisible(true)
                setLogoutIsVisible(false)
            }
        } catch (err) {
            // setError(err.message)
        } finally {
            // setLoading(false)
        }
    }

    useEffect(() => {
        handleLogin()
    }, [])
    
    
    return (
        <>
            <h1 className="header">Welcome to AkiyaMart</h1>

            {registrationIsVisible && <Register 
                setLoginIsVisible={setLoginIsVisible}
                setRegistrationIsVisible={setRegistrationIsVisible}
                setLogoutIsVisible={setLogoutIsVisible}
            />}
            {loginIsVisible && <Login 
                setLoginIsVisible={setLoginIsVisible}
                setRegistrationIsVisible={setRegistrationIsVisible}
                setLogoutIsVisible={setLogoutIsVisible}
            />}
            {logoutIsVisible && <Logout 
                setLoginIsVisible={setLoginIsVisible}
                setRegistrationIsVisible={setRegistrationIsVisible}
                setLogoutIsVisible={setLogoutIsVisible}
            />}
        </>
    )
}

export default Authenticator
