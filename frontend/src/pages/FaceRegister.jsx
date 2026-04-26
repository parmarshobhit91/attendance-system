import { useRef } from "react";
import { api } from "../api";

export default function FaceRegister() {
  const videoRef = useRef(null);

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: true,
    });

    videoRef.current.srcObject = stream;
  };

  const captureAndSend = async () => {
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoRef.current, 0, 0);

    const image = canvas.toDataURL("image/jpeg");

    const email = localStorage.getItem("user");

    const res = await api.post("/auth/register-face", {
      email,
      image,
    });

    alert(res.data.msg);
  };

  return (
    <div>
      <h2>Face Registration</h2>

      <video ref={videoRef} autoPlay width="400" />

      <br />

      <button onClick={startCamera}>Start Camera</button>
      <button onClick={captureAndSend}>Register Face</button>
    </div>
  );
}