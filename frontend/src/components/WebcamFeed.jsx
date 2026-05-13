import {
    useEffect,
    useRef,
} from "react";

import Webcam from
    "react-webcam";


function WebcamFeed({

    webcamRef,
    faces,
    isEnrollmentMode,

}) {

    const canvasRef =
        useRef(null);


    useEffect(() => {

        const canvas =
            canvasRef.current;

        const ctx =
            canvas.getContext("2d");

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        faces.forEach((face) => {

            const [
                x,
                y,
                w,
                h,
            ] = face.bbox;


            ctx.strokeStyle =
                isEnrollmentMode
                    ? "#22d3ee"
                    : "#00ff00";

            ctx.lineWidth = 3;

            ctx.strokeRect(
                x,
                y,
                w,
                h
            );


            if (
                !isEnrollmentMode
            ) {

                ctx.font =
                    "20px Arial";

                ctx.fillStyle =
                    "#00ff00";

                ctx.fillText(
                    `${face.track_id} | ${face.name} | ${face.emotion}`,
                    x,
                    y - 10
                );
            }

        });

    }, [
        faces,
        isEnrollmentMode,
    ]);


    return (

        <div
            style={{
                position:
                    "relative",

                width: "640px",

                height: "480px",
            }}
        >

            <Webcam
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width={640}
                height={480}
                style={{
                    position:
                        "absolute",

                    top: 0,

                    left: 0,

                    borderRadius:
                        "16px",
                }}
            />

            <canvas
                ref={canvasRef}
                width={640}
                height={480}
                style={{
                    position:
                        "absolute",

                    top: 0,

                    left: 0,
                }}
            />

        </div>
    );
}

export default WebcamFeed;