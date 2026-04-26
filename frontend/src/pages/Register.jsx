import { useState } from "react";
import { api } from "../api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const register = async () => {
    try {
      const res = await api.post("/auth/signup", {
        email,
        password,
      });

      alert(res.data.msg || "Registered");
    } catch (err) {
      alert("Error registering user");
    }
  };

  return (
    <div>
      <h2>User Registration</h2>

      <input
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />

      <button onClick={register}>Register</button>
    </div>
  );
}