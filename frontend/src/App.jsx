import { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";

function App() {

  const webcamRef = useRef(null);

  const [faces, setFaces] = useState([]);

  const captureFrame = async () => {

    if (!webcamRef.current) return;

    const imageSrc = webcamRef.current.getScreenshot();

    if (!imageSrc) return;

    const blob = await fetch(imageSrc).then(
      (res) => res.blob()
    );

    const formData = new FormData();

    formData.append(
      "file",
      blob,
      "frame.jpg"
    );

    try {

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      setFaces(response.data.faces);

    } catch (err) {

      console.error(err);
    }
  };

  useEffect(() => {

    const interval = setInterval(
      captureFrame,
      1000
    );

    return () => clearInterval(interval);

  }, []);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginTop: "20px",
      }}
    >

      <h1>
        Real-Time Face Emotion Recognition
      </h1>

      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={640}
        height={480}
      />

      <div style={{ marginTop: "20px" }}>

        {faces.map((face, idx) => (

          <div key={idx}>

            <p>
              <strong>Name:</strong>
              {" "}
              {face.name}
            </p>

            <p>
              <strong>Emotion:</strong>
              {" "}
              {face.emotion}
            </p>

            <hr />

          </div>
        ))}

      </div>

    </div>
  );
}

export default App;