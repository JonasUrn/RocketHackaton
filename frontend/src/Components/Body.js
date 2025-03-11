import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Answer from "./Answer";
import styles from "./body.module.css";

const Body = () => {
    const [answer, setAnswer] = useState(null);

    return (
        <div className={styles.body}>
            <div className={styles.overlay}>
                <h1>Search for Something</h1>
                <SearchBar setAnswer={setAnswer} />
                {answer && <Answer answerData={answer} />}
            </div>
        </div>
    );
};

export default Body;
