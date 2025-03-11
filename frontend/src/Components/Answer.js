import React from "react";
import styles from "./answer.module.css";

const Answer = ({ answerData }) => {
    if (!answerData) return null;

    const { short_answer, detailed_answer, references, links } = answerData;

    const handleClick = (linkPart) => {
        var link = "";

        if (linkPart.startsWith("sg")) {
            link = "https://www.redbooks.ibm.com/redbooks/pdfs/" + linkPart;
        } else if (linkPart.startsWith("redp")) {
            link = "https://www.redbooks.ibm.com/redpapers/pdfs/" + linkPart;
        }

        if (link) {
            window.open(link, "_blank");
        }
    }

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

            {links && (<div className={styles.section}>
                <h2>References</h2>
                {links.map((link, index) => (
                    <p key={index} onClick={() => handleClick(link)} className={styles.reference}>
                        {link}
                    </p>
                ))}
            </div>)}
        </div>
    );
};

export default Answer;
