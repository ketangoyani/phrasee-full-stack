const NOTIFICATION_URL = "http://localhost:8000/notifications/"

const apiFetch = (url: string) => {
    return fetch(url)
        .then(res => res.json())
}

export function fetchNotifications() {
    return apiFetch(NOTIFICATION_URL).then(res => res.results)
}