import { useRef, useState } from "react";
import { api } from "../api";

export default function Attendance() {
  const videoRef = useRef(null);
  const [msg, setMsg] = useState("");

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });

    videoRef.current.srcObject = stream;
  };

  const mark = async () => {
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoRef.current, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    const res = await api.post("/attendance/punch", {
      image,
    });

    setMsg(res.data.msg || res.data.error);
  };

  return (
    <div>
      <h2>Attendance</h2>

      <video ref={videoRef} autoPlay width="400" />

      <br />

      <button onClick={startCamera}>Start Camera</button>
      <button onClick={mark}>Mark Attendance</button>

      <h3>{msg}</h3>
    </div>
  );
}