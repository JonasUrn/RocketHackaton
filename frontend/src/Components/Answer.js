import React from "react";
import styles from "./answer.module.css";

const Answer = ({ answerData }) => {
    if (!answerData) return null;

    const { short_answer, detailed_answer, references } = answerData;

    return (
        <div className={styles.answerBox}>
            {short_answer && (
                <div className={styles.section}>
                    <h2>Short Answer</h2>
                    <p dangerouslySetInnerHTML={{ __html: short_answer.replace("**1. Short Answer:**", "") }} />
                </div>
            )}

            {detailed_answer && (
                <div className={styles.section}>
                    <h2>Detailed Answer</h2>
                    <p dangerouslySetInnerHTML={{ __html: detailed_answer.replace("**2. Detailed Answer:**", "") }} />
                </div>
            )}

            {references && (
                <div className={styles.section}>
                    <h2>References</h2>
                    <p>{references}</p>
                </div>
            )}
        </div>
    );
};

export default Answer;
