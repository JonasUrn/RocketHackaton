import React, { useState } from "react";
import axios from "axios";
import styles from "./searchBar.module.css";
import { FaArrowRight } from "react-icons/fa";
import Notification from "./Notification";
import LoadingSpinner from "./LoadingSpinner";

const SearchBar = ({ setAnswer }) => {
    const [query, setQuery] = useState("");
    const [notification, setNotification] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) {
            setNotification({ message: "Search query cannot be empty!", status: "error" });
            return;
        }

        setAnswer(null);
        setIsLoading(true);

        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/search?query=${query}`);
            console.log("Response:", response.data);
            if (response.data["short_answer"] === "error") {
                setNotification({ message: "Something went wrong!", status: "error" });
                setAnswer(null);
            } else {
                setAnswer(response.data);
                setNotification({ message: "Search successful!", status: "good" });
            }
        } catch (error) {
            setIsLoading(false);
            console.error("Error fetching data:", error);
            setNotification({ message: "Something went wrong!", status: "error" });
        }

        setIsLoading(false);
    };

    return (
        <>
            {isLoading ? (
                <LoadingSpinner />
            ) : (
                <div className={styles.searchBar}>
                    {notification && (
                        <Notification
                            message={notification.message}
                            status={notification.status}
                            onClose={() => setNotification(null)}
                        />
                    )}
                    <input
                        type="text"
                        placeholder="Enter your search..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className={styles.input}
                    />
                    <button onClick={handleSearch} className={styles.button}>
                        <FaArrowRight />
                    </button>
                </div>
            )}
        </>
    );
};

export default SearchBar;
