import { useState } from "react";
import { api } from "../api";

export default function Login() {
  const [email, setEmail] = useState("");

  const login = async () => {
    try {
      const res = await api.post("/auth/login", {
        email,
      });

      localStorage.setItem("user", email);

      alert("Login successful");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />

      <br />
      <button onClick={login}>Login</button>
    </div>
  );
}