import {
    useState,
} from "react";

import { api } from
    "../services/api";


function RegisterUser({

    webcamRef,
    faces,
    fetchUsers,

    isEnrollmentMode,
    setIsEnrollmentMode,

}) {

    const [name, setName] =
        useState("");

    const [message, setMessage] =
        useState("");

    const [
        isRegistering,
        setIsRegistering,
    ] = useState(false);

    const [progress,
        setProgress] =
        useState(0);

    const [
        currentInstruction,
        setCurrentInstruction,
    ] = useState("");


    const TOTAL_SAMPLES = 10;


    const instructions = [

        "Look straight",

        "Look slightly left",

        "Look slightly right",

        "Move slightly closer",

        "Move slightly back",

        "Smile slightly",

        "Neutral face",

        "Tilt head left",

        "Tilt head right",

        "Look straight",
    ];


    const sleep = (ms) =>

        new Promise(
            (resolve) =>
                setTimeout(
                    resolve,
                    ms
                )
        );


    // =========================
    // Validation
    // =========================

    const hasNoFace =
        faces.length === 0;

    const hasMultipleFaces =
        faces.length > 1;

    const isFaceValid =
        faces.length === 1;


    // =========================
    // Capture
    // =========================

    const handleRegister =
        async () => {

            if (
                !name.trim()
            ) {
                return;
            }

            if (
                !isFaceValid
            ) {
                return;
            }

            setIsRegistering(true);

            setMessage("");

            setProgress(0);

            try {

                const formData =
                    new FormData();

                formData.append(
                    "name",
                    name
                );

                let captured = 0;

                while (
                    captured <
                    TOTAL_SAMPLES
                ) {

                    // Face validation
                    if (
                        faces.length !== 1
                    ) {

                        await sleep(300);

                        continue;
                    }

                    // Show instruction
                    setCurrentInstruction(
                        instructions[
                            captured
                        ]
                    );

                    // Give user time to move
                    await sleep(1500);

                    const imageSrc =
                        webcamRef.current
                            .getScreenshot();

                    if (!imageSrc) {
                        continue;
                    }

                    const blob =
                        await fetch(
                            imageSrc
                        ).then(
                            (res) =>
                                res.blob()
                        );

                    formData.append(
                        "files",
                        blob,
                        `sample_${captured}.jpg`
                    );

                    captured++;

                    setProgress(
                        captured
                    );
                }


                const response =
                    await api.post(
                        "/users/register",
                        formData,
                    );

                setMessage(
                    response.data.message
                );

                setName("");

                fetchUsers();

            } catch (err) {

                console.error(err);

                setMessage(
                    "Registration failed"
                );

            } finally {

                setCurrentInstruction("");

                setIsRegistering(false);

                setIsEnrollmentMode(false);
            }
        };


    // =========================
    // UI
    // =========================

    return (

        <div>

            {!isEnrollmentMode && (

                <button
                    onClick={() =>
                        setIsEnrollmentMode(
                            true
                        )
                    }
                    className="
                        w-full
                        bg-cyan-500
                        hover:bg-cyan-600
                        transition
                        py-3
                        rounded-xl
                        font-semibold
                    "
                >
                    + Enroll User
                </button>

            )}


            {isEnrollmentMode && (

                <div
                    className="
                        space-y-4
                    "
                >

                    <h2
                        className="
                            text-2xl
                            font-semibold
                        "
                    >
                        Live Enrollment
                    </h2>


                    <input
                        type="text"
                        placeholder="Enter name"
                        value={name}
                        onChange={(e) =>
                            setName(
                                e.target.value
                            )
                        }
                        disabled={
                            isRegistering
                        }
                        className="
                            w-full
                            bg-slate-700
                            border
                            border-slate-600
                            rounded-xl
                            px-4
                            py-3
                            text-white
                            outline-none
                        "
                    />


                    {/* Validation */}

                    {hasNoFace && (

                        <p
                            className="
                                text-red-400
                                text-sm
                            "
                        >
                            No face detected
                        </p>

                    )}


                    {hasMultipleFaces && (

                        <p
                            className="
                                text-orange-400
                                text-sm
                            "
                        >
                            Only one face allowed
                        </p>

                    )}


                    {isFaceValid && !isRegistering && (

                        <p
                            className="
                                text-cyan-400
                                text-sm
                            "
                        >
                            Face detected ✓
                        </p>

                    )}


                    {!isRegistering && (

                        <button
                            onClick={
                                handleRegister
                            }
                            disabled={
                                !name.trim() ||
                                !isFaceValid
                            }
                            className={`
                                w-full
                                py-3
                                rounded-xl
                                font-semibold
                                transition

                                ${
                                    !name.trim() ||
                                    !isFaceValid

                                    ? "bg-slate-600 cursor-not-allowed"

                                    : "bg-cyan-500 hover:bg-cyan-600"
                                }
                            `}
                        >
                            Begin Capture
                        </button>

                    )}


                    {isRegistering && (

                        <div
                            className="
                                space-y-4
                            "
                        >

                            <div
                                className="
                                    text-center
                                    space-y-2
                                "
                            >

                                <p
                                    className="
                                        text-sm
                                        text-slate-400
                                    "
                                >
                                    Follow the instruction
                                </p>

                                <p
                                    className="
                                        text-cyan-400
                                        text-xl
                                        font-semibold
                                    "
                                >
                                    {currentInstruction}
                                </p>

                            </div>


                            <div
                                className="
                                    w-full
                                    bg-slate-700
                                    rounded-full
                                    h-4
                                "
                            >

                                <div
                                    className="
                                        bg-cyan-400
                                        h-4
                                        rounded-full
                                        transition-all
                                    "
                                    style={{
                                        width:
                                            `${(progress / TOTAL_SAMPLES) * 100}%`
                                    }}
                                />

                            </div>


                            <p
                                className="
                                    text-center
                                    text-sm
                                "
                            >
                                {progress}
                                /
                                {TOTAL_SAMPLES}
                                samples captured
                            </p>

                        </div>

                    )}


                    <button
                        onClick={() => {

                            setIsEnrollmentMode(
                                false
                            );

                            setName("");

                            setMessage("");

                            setCurrentInstruction("");
                        }}
                        className="
                            w-full
                            bg-slate-700
                            hover:bg-slate-600
                            transition
                            py-3
                            rounded-xl
                        "
                    >
                        Cancel
                    </button>


                    {message && (

                        <p
                            className="
                                text-green-400
                                text-sm
                            "
                        >
                            {message}
                        </p>

                    )}

                </div>

            )}

        </div>
    );
}

export default RegisterUser;