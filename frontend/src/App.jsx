import {
  useEffect,
  useRef,
  useState,
} from "react";

import WebcamFeed from
  "./components/WebcamFeed";

import LiveInference from
  "./components/LiveInference";

import RegisterUser from
  "./components/RegisterUser";

import UsersPanel from
  "./components/UsersPanel";

import LogsPanel from
  "./components/LogsPanel";

import { api } from
  "./services/api";


function App() {

  const webcamRef = useRef(null);

  const [faces, setFaces] =
    useState([]);

  const [logs, setLogs] =
    useState([]);

  const [users, setUsers] =
    useState([]);


  const captureFrame = async () => {

    if (!webcamRef.current) return;

    const imageSrc =
      webcamRef.current.getScreenshot();

    if (!imageSrc) return;

    const blob = await fetch(
      imageSrc
    ).then((res) => res.blob());

    const formData = new FormData();

    formData.append(
      "file",
      blob,
      "frame.jpg"
    );

    try {

      const response =
        await api.post(
          "/analyze",
          formData,
          {
            headers: {
              "Content-Type":
                "multipart/form-data",
            },
          }
        );

      setFaces(
        response.data.faces
      );

    } catch (err) {

      console.error(err);
    }
  };


  const fetchLogs = async () => {

    try {

      const response =
        await api.get("/logs");

      setLogs(response.data);

    } catch (err) {

      console.error(err);
    }
  };


  const fetchUsers = async () => {

    try {

      const response =
        await api.get(
          "/users/list"
        );

      setUsers(
        response.data.users
      );

    } catch (err) {

      console.error(err);
    }
  };


  const deleteUser =
    async (name) => {

      try {

        await api.delete(
          `/users/delete/${name}`
        );

        fetchUsers();

      } catch (err) {

        console.error(err);
      }
    };


  useEffect(() => {

    captureFrame();

    fetchLogs();

    fetchUsers();

    const interval =
      setInterval(() => {

        captureFrame();

        fetchLogs();

      }, 1000);

    return () =>
      clearInterval(interval);

  }, []);


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
        Real-Time Face Recognition
        & Emotion Analysis
      </h1>

      <WebcamFeed
        webcamRef={webcamRef}
        faces={faces}
      />

      <LiveInference
        faces={faces}
      />

      <RegisterUser
        fetchUsers={fetchUsers}
      />

      <UsersPanel
        users={users}
        deleteUser={deleteUser}
      />

      <LogsPanel
        logs={logs}
      />

    </div>
  );
}

export default App;