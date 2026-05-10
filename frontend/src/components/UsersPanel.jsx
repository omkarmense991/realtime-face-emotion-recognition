function UsersPanel({
    users,
    deleteUser,
}) {

    return (

        <div
            style={{
                width: "640px",
                marginTop: "30px",
            }}
        >

            <h2>
                Registered Users
            </h2>

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
                        justifyContent:
                            "space-between",
                        alignItems: "center",
                    }}
                >

                    <p>
                        <strong>{user}</strong>
                    </p>

                    <button
                        onClick={() =>
                            deleteUser(user)
                        }
                    >
                        Delete
                    </button>

                </div>

            ))}

        </div>
    );
}

export default UsersPanel;