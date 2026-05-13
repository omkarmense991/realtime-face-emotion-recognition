function LiveInference({
    faces,
}) {

    return (

        <div>

            <h2
                className="
                    text-2xl
                    font-semibold
                    mb-4
                "
            >
                Live Inference
            </h2>

            {faces.length === 0 && (

                <p
                    className="
                        text-slate-400
                    "
                >
                    No faces detected
                </p>

            )}

            <div
                className="
                    space-y-4
                "
            >

                {faces.map((face, idx) => (

                    <div
                        key={idx}
                        className="
                            bg-slate-700
                            rounded-xl
                            p-4
                        "
                    >

                        <div
                            className="
                                flex
                                justify-between
                                mb-2
                            "
                        >

                            <span
                                className="
                                    font-medium
                                "
                            >
                                Name
                            </span>

                            <span>
                                {face.name}
                            </span>

                        </div>


                        <div
                            className="
                                mb-3
                            "
                        >

                            <div
                                className="
                                    flex
                                    justify-between
                                    text-sm
                                    mb-1
                                "
                            >

                                <span>
                                    Recognition
                                </span>

                                <span>
                                    {face.recognition_score}%
                                </span>

                            </div>

                            <div
                                className="
                                    w-full
                                    bg-slate-600
                                    rounded-full
                                    h-3
                                "
                            >

                                <div
                                    className="
                                        bg-green-400
                                        h-3
                                        rounded-full
                                    "
                                    style={{
                                        width:
                                            `${face.recognition_score}%`
                                    }}
                                />

                            </div>

                        </div>


                        <div
                            className="
                                flex
                                justify-between
                                mb-2
                            "
                        >

                            <span>
                                Emotion
                            </span>

                            <span
                                className="
                                    capitalize
                                "
                            >
                                {face.emotion}
                            </span>

                        </div>


                        <div>

                            <div
                                className="
                                    flex
                                    justify-between
                                    text-sm
                                    mb-1
                                "
                            >

                                <span>
                                    Emotion Confidence
                                </span>

                                <span>
                                    {face.emotion_score}%
                                </span>

                            </div>

                            <div
                                className="
                                    w-full
                                    bg-slate-600
                                    rounded-full
                                    h-3
                                "
                            >

                                <div
                                    className="
                                        bg-cyan-400
                                        h-3
                                        rounded-full
                                    "
                                    style={{
                                        width:
                                            `${face.emotion_score}%`
                                    }}
                                />

                            </div>

                        </div>

                    </div>

                ))}

            </div>

        </div>
    );
}

export default LiveInference;