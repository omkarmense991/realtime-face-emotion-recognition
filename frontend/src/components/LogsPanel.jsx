function LogsPanel({
    logs,
}) {

    return (

        <div
            style={{
                width: "640px",
                marginTop: "30px",
            }}
        >

            <h2>
                Inference History
            </h2>

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
    );
}

export default LogsPanel;