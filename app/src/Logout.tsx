import React, { useState } from "react";
import { logout } from "./auth";
import './Logout.css';

const Logout = () => {
  const [error, setError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleLogout = async () => {
    try {
      setLoading(true);
      setError("");
      await logout();
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
