import { useEffect, useRef, useState } from "react";

import Webcam from "react-webcam";

import axios from "axios";


import RegisterUser from "./components/RegisterUser";

function App() {

  const webcamRef = useRef(null);

  const [faces, setFaces] = useState([]);

  const [logs, setLogs] = useState([]);

  const [users, setUsers] = useState([]);


  // =========================
  // Capture Frame
  // =========================

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


  // =========================
  // Fetch Logs
  // =========================

  const fetchLogs = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/logs"
      );

      setLogs(response.data);

    } catch (err) {

      console.error(err);
    }
  };


  // =========================
  // Fetch Users
  // =========================

  const fetchUsers = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/users/list"
      );

      setUsers(response.data.users);

    } catch (err) {

      console.error(err);
    }
  };


  // =========================
  // Delete User
  // =========================

  const deleteUser = async (name) => {

    try {

      await axios.delete(
        `http://127.0.0.1:8000/users/delete/${name}`
      );

      fetchUsers();

    } catch (err) {

      console.error(err);
    }
  };


  // =========================
  // Polling Loop
  // =========================

  useEffect(() => {

    captureFrame();

    fetchLogs();

    fetchUsers();

    const interval = setInterval(() => {

      captureFrame();

      fetchLogs();

      fetchUsers();

    }, 1000);

    return () => clearInterval(interval);

  }, []);


  // =========================
  // UI
  // =========================

  return (

    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "20px",
        fontFamily: "Arial",
      }}
    >

      <h1
        style={{
          textAlign: "center",
          fontSize: "48px",
          marginBottom: "30px",
          lineHeight: "1.2",
        }}
      >
        Real-Time Face Recognition &
        <br />
        Emotion Analysis
      </h1>


      {/* Webcam */}

      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={640}
        height={480}
      />


      {/* Live Inference */}

      <div
        style={{
          width: "640px",
          marginTop: "20px",
        }}
      >

        <h2>Live Inference</h2>

        {faces.length === 0 && (
          <p>No faces detected</p>
        )}

        {faces.map((face, idx) => (

          <div
            key={idx}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "10px",
            }}
          >

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

            <p>
              <strong>Score:</strong>
              {" "}
              {face.score}
            </p>

          </div>

        ))}

      </div>

      <RegisterUser
        fetchUsers={fetchUsers}
      />

      {/* Registered Users */}

      <div
        style={{
          width: "640px",
          marginTop: "30px",
        }}
      >

        <h2>Registered Users</h2>

        {users.length === 0 && (
          <p>No registered users</p>
        )}

        {users.map((user, idx) => (

          <div
            key={idx}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "10px",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >

            <p>
              <strong>{user}</strong>
            </p>

            <button
              onClick={() => deleteUser(user)}
            >
              Delete
            </button>

          </div>

        ))}

      </div>


      {/* Inference Logs */}

      <div
        style={{
          width: "640px",
          marginTop: "30px",
        }}
      >

        <h2>Inference History</h2>

        {logs.map((log) => (

          <div
            key={log.id}
            style={{
              border: "1px solid #ccc",
              padding: "10px",
              marginBottom: "10px",
            }}
          >

            <p>
              <strong>Name:</strong>
              {" "}
              {log.name}
            </p>

            <p>
              <strong>Emotion:</strong>
              {" "}
              {log.emotion}
            </p>

            <p>
              <strong>Score:</strong>
              {" "}
              {log.score}
            </p>

            <p>
              <strong>Time:</strong>
              {" "}
              {log.created_at}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}


export default App;