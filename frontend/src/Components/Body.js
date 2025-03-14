import React, { useState } from "react";
import SearchBar from "./SearchBar";
import Answer from "./Answer";
import styles from "./body.module.css";

const Body = () => {
    const [answer, setAnswer] = useState(null);

    return (
        <div className={styles.body}>
            <div className={styles.overlay}>
                <SearchBar setAnswer={setAnswer} />
                {answer && <Answer answerData={answer} />}
            </div>
        </div>
    );
};

export default Body;
