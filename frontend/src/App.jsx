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

import { api } from
  "./services/api";

import.meta.env.VITE_WS_URL


function App() {

  const socketRef =
    useRef(null);

  const webcamRef =
    useRef(null);

  const [faces, setFaces] =
    useState([]);

  const [users, setUsers] =
    useState([]);

  const [
    isEnrollmentMode,
    setIsEnrollmentMode,
  ] = useState(false);


  // =========================
  // Fetch Users
  // =========================

  const fetchUsers =
    async () => {

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


  // =========================
  // Delete User
  // =========================

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


  // =========================
  // WebSocket
  // =========================

  useEffect(() => {

    socketRef.current =
      new WebSocket(
        import.meta.env.VITE_WS_URL
      );

    socketRef.current.onmessage =
      (event) => {

        const data =
          JSON.parse(event.data);

        setFaces(data.faces);
      };

    const interval =
      setInterval(() => {

        if (
          !webcamRef.current ||
          !socketRef.current ||
          socketRef.current
            .readyState !==
          WebSocket.OPEN
        ) {
          return;
        }

        const imageSrc =
          webcamRef.current
            .getScreenshot();

        if (!imageSrc) {
          return;
        }

        socketRef.current.send(
          imageSrc
        );

      }, 250);

    setTimeout(() => {
      fetchUsers();
    }, 0);

    return () => {

      clearInterval(interval);

      socketRef.current?.close();
    };

  }, []);


  // =========================
  // UI
  // =========================

  return (

    <div
      className="
        min-h-screen
        bg-slate-900
        text-white
        px-8
        py-6
      "
    >

      <div
        className="
          max-w-7xl
          mx-auto
        "
      >

        <h1
          className="
            text-5xl
            font-bold
            text-center
            mb-10
          "
        >
          Real-Time Face Recognition

          &
          Emotion Analysis
        </h1>


        <div
          className="
            grid
            grid-cols-1
            lg:grid-cols-3
            gap-6
          "
        >

          {/* LEFT */}

          <div
            className="
              lg:col-span-2
              space-y-6
            "
          >

            <div
              className="
                bg-slate-800
                rounded-2xl
                p-4
                shadow-2xl
              "
            >

              <WebcamFeed
                webcamRef={webcamRef}
                faces={faces}
                isEnrollmentMode={
                  isEnrollmentMode
                }
              />

            </div>


            {!isEnrollmentMode && (

              <div
                className="
                  bg-slate-800
                  rounded-2xl
                  p-6
                  shadow-2xl
                "
              >

                <LiveInference
                  faces={faces}
                />

              </div>

            )}

          </div>


          {/* RIGHT */}

          <div
            className="
              space-y-6
            "
          >

            <div
              className="
                bg-slate-800
                rounded-2xl
                p-6
                shadow-2xl
              "
            >

              <RegisterUser
                webcamRef={webcamRef}
                faces={faces}
                fetchUsers={fetchUsers}
                isEnrollmentMode={
                  isEnrollmentMode
                }
                setIsEnrollmentMode={
                  setIsEnrollmentMode
                }
              />

            </div>


            <div
              className="
                bg-slate-800
                rounded-2xl
                p-6
                shadow-2xl
              "
            >

              <UsersPanel
                users={users}
                deleteUser={deleteUser}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;