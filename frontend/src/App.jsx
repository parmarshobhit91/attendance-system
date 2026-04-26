import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import FaceRegister from "./pages/FaceRegister";
import Attendance from "./pages/Attendance";

function App() {
  const [page, setPage] = useState("login");

  return (
    <div style={{ textAlign: "center" }}>
      <h1>🔥 Face Attendance System</h1>

      <div>
        <button onClick={() => setPage("login")}>Login</button>
        <button onClick={() => setPage("register")}>Register</button>
        <button onClick={() => setPage("face")}>Face Register</button>
        <button onClick={() => setPage("attendance")}>Attendance</button>
      </div>

      <hr />

      {page === "login" && <Login />}
      {page === "register" && <Register />}
      {page === "face" && <FaceRegister />}
      {page === "attendance" && <Attendance />}
    </div>
  );
}

export default App;