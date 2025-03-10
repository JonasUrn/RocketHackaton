import React from "react";
import SearchBar from "./SearchBar";
import styles from "./body.module.css";

const Body = () => {
    return (
        <div className={styles.body}>
            <div className={styles.overlay}>
                <h1>Search for Something</h1>
                <SearchBar />
            </div>
        </div>
    );
};

export default Body;
