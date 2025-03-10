import React, { useEffect } from "react";
import styles from "./notification.module.css";

const Notification = ({ message, status, onClose }) => {
    useEffect(() => {
        const timer = setTimeout(() => {
            onClose();
        }, 3000);
        return () => clearTimeout(timer);
    }, [onClose]);

    return (
        <div className={`${styles.notification} ${styles[status]}`}>
            {message}
        </div>
    );
};

export default Notification;
