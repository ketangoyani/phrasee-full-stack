import React, { useState, useEffect } from 'react';
import './notification.css';
import { BsBell } from 'react-icons/bs';
import DefaultAvatar from "../images/portrait.png";
import { fetchNotifications } from '../utils/apifetch';

// Helper function to format the display names in the notification
const formatUsersList = (users) => {
    // Extract the first two names
    const firstTwoNames = users.slice(0, 2).map(item => item.name);

    // Calculate the count of remaining names
    const remainingCount = Math.max(0, users.length - 2);
    const plural = remainingCount > 1 ? "s" : "";
    // Create the dynamic string
    const dynamicString = `${firstTwoNames.join(', ')}${remainingCount > 0 ? ` and ${remainingCount} other${plural}` : ''}`;

    return dynamicString;
}

// Individual Notification component
const Notification = ({ notification }) => {
    // Extract user avatar URLs from the notification
    const userDisplayImage = notification.users.filter(item => item.avatar_url);

    // Get verb for notification based on the type
    const getVerb = () => {
        let verb = "";
        if (notification.type === "Like") {
            verb = notification.users.length === 1 ? "likes" : "liked";
        }
        else {
            verb = "commented";
        }
        return verb;
    }

    const getNotificationLength = () => {
        let len = formatUsersList(notification.users).length + 1;
        len += getVerb().length + 1;
        len += "your post: ".length;
        return len
    }

    const textCurtail = 82-getNotificationLength();
    return (
        <div className="notification-item">
            <div className="d-flex align-items-center">
                <div className="flex-shrink-0">
                    {/* Display user avatar or default avatar if not available */}
                    {userDisplayImage.length > 0 ? <img className="img-fluid avatar rounded" src={userDisplayImage[0].avatar_url} alt="User Avatar"></img> : <img className="img-fluid avatar rounded" src={DefaultAvatar} alt="Default Avatar"></img>}
                </div>
                <div className="flex-grow-0 ms-3 text-secondary">
                    {/* Display formatted user names, notification verb, and post title */}
                    <span className="text-primary"><b>{formatUsersList(notification.users)}</b></span>&nbsp;
                    {getVerb()}&nbsp;
                    <b>your post: </b>
                    "<span>{notification.post.title.slice(0, textCurtail)}{textCurtail > 0 ?"...":""}</span>"
                </div>
            </div>
        </div>
    );
}

// Notifications component that fetches and displays notifications
const Notifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [showNotifications, setShowNotifications] = useState(true);

    // Fetch notifications on component mount
    useEffect(() => {
        fetchNotifications().then(data => {
            setNotifications(data);
        })
    }, [])

    return (
        <div className="notification-container">
            {/* Notification bell icon in the navbar */}
            <nav className="navbar navbar-expand-lg bg-body-tertiary bg-linear-gradient-orange-pink">
                <div className="container-fluid">
                    <div></div>
                    <button type="button"
                        className="btn btn-primary position-relative me-4 bg-transparent border border-0"
                        onClick={() => { setShowNotifications(!showNotifications) }}
                    >
                        <BsBell />
                        {/* Display notification count if there are notifications */}
                        {notifications.length > 0 && (
                            <span className="position-absolute top-0 start-50 translate-middle badge rounded-pill bg-primary">
                                {notifications.length}</span>
                        )}
                    </button>
                </div>
            </nav>

            {/* Display notifications if showNotifications state is true */}
            {showNotifications && <div>
                {notifications.length > 0 && (
                    <div className="notification-dropdown me-2">
                        {/* Map through notifications and render individual Notification components */}
                        {notifications.map((notification, index) => (
                            <Notification key={index} notification={notification} />
                        ))}
                    </div>
                )}
            </div>}
        </div>
    );
};

export default Notifications;
