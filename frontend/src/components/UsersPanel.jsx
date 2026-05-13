function UsersPanel({
    users,
    deleteUser,
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
                Registered Users
            </h2>

            <div
                className="
                    space-y-3
                "
            >

                {users.map((user, idx) => (

                    <div
                        key={idx}
                        className="
                            bg-slate-700
                            rounded-xl
                            p-4
                            flex
                            justify-between
                            items-center
                        "
                    >

                        <span>
                            {user}
                        </span>

                        <button
                            onClick={() =>
                                deleteUser(user)
                            }
                            className="
                                bg-red-500
                                hover:bg-red-600
                                transition
                                px-4
                                py-2
                                rounded-lg
                                text-sm
                            "
                        >
                            Delete
                        </button>

                    </div>

                ))}

            </div>

        </div>
    );
}

export default UsersPanel;