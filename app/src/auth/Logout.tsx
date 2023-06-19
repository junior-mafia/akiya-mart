import React, { useState } from "react";
import { logout } from "./auth";
import './Logout.css';

interface LogoutProps {
  setLoginIsVisible: (value: boolean) => void
  setRegistrationIsVisible: (value: boolean) => void
  setLogoutIsVisible: (value: boolean) => void
}

const Logout = (props: LogoutProps) => {
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleLogout = async () => {
    try {
      setLoading(true);
      setError("");
      await logout();
      props.setRegistrationIsVisible(true)
      props.setLoginIsVisible(true)
      props.setLogoutIsVisible(false)
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="logout-container">
      <button onClick={handleLogout} className="logout-button">
        {loading ? "Logging Out..." : "Logout"}
      </button>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default Logout;
