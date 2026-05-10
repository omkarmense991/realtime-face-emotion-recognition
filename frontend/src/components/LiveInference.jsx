function LiveInference({
    faces,
}) {

    return (

        <div
            style={{
                width: "640px",
                marginTop: "20px",
            }}
        >

            <h2>
                Live Inference
            </h2>

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
    );
}

export default LiveInference;