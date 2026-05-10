import { useState } from "react";

import axios from "axios";


function RegisterUser({ fetchUsers }) {

    const [name, setName] = useState("");

    const [files, setFiles] = useState([]);

    const [message, setMessage] =
        useState("");


    const handleRegister = async () => {

        if (!name || files.length === 0) {
            return;
        }

        const formData = new FormData();

        formData.append("name", name);

        for (let i = 0; i < files.length; i++) {

            formData.append(
                "files",
                files[i]
            );
        }

        try {

            const response = await axios.post(
                "http://127.0.0.1:8000/users/register",
                formData,
                {
                    headers: {
                        "Content-Type":
                            "multipart/form-data",
                    },
                }
            );

            setMessage(
                response.data.message
            );

            setName("");

            setFiles([]);

            fetchUsers();

        } catch (err) {

            console.error(err);

            setMessage(
                "Registration failed"
            );
        }
    };


    return (

        <div
            style={{
                width: "640px",
                marginTop: "30px",
                border: "1px solid #ccc",
                padding: "20px",
            }}
        >

            <h2>Register User</h2>

            <input
                type="text"
                placeholder="Enter name"
                value={name}
                onChange={(e) =>
                    setName(e.target.value)
                }
                style={{
                    width: "100%",
                    padding: "10px",
                    marginBottom: "10px",
                }}
            />

            <input
                type="file"
                multiple
                accept="image/*"
                onChange={(e) =>
                    setFiles(e.target.files)
                }
                style={{
                    marginBottom: "10px",
                }}
            />

            <br />

            <button onClick={handleRegister}>
                Register
            </button>

            {message && (
                <p>{message}</p>
            )}

        </div>
    );
}


export default RegisterUser;