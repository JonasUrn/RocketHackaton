import React, { useState } from "react";
import axios from "axios";
import styles from "./searchBar.module.css";
import { FaArrowRight } from "react-icons/fa";
import Notification from "./Notification";

const SearchBar = () => {
    const [query, setQuery] = useState("");
    const [notification, setNotification] = useState(null);

    const handleSearch = async () => {
        if (!query.trim()) {
            setNotification({ message: "Search query cannot be empty!", status: "error" });
            return;
        }

        try {
            const response = await axios.get(`http://127.0.0.1:5000/api/search?query=${query}`);
            console.log("Response:", response.data);
            setNotification({ message: "Search successful!", status: "good" });
        } catch (error) {
            console.error("Error fetching data:", error);
            setNotification({ message: "Something went wrong!", status: "error" });
        }
    };

    return (
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
    );
};

export default SearchBar;
