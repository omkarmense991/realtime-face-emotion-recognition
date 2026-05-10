import {
    useEffect,
    useRef,
} from "react";

import Webcam from "react-webcam";


function WebcamFeed({
    webcamRef,
    faces,
}) {

    const canvasRef = useRef(null);


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

            ctx.strokeStyle = "lime";

            ctx.lineWidth = 3;

            ctx.strokeRect(
                x,
                y,
                w,
                h
            );

            ctx.font = "20px Arial";

            ctx.fillStyle = "lime";

            ctx.fillText(
                `${face.name} | ${face.emotion}`,
                x,
                y - 10
            );

        });

    }, [faces]);


    return (

        <div
            style={{
                position: "relative",
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
                    position: "absolute",
                    top: 0,
                    left: 0,
                }}
            />

            <canvas
                ref={canvasRef}
                width={640}
                height={480}
                style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                }}
            />

        </div>
    );
}

export default WebcamFeed;