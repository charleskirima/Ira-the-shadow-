self.addEventListener("push", function(event) {
    let data = {};
    try {
        data = event.data.json(); // Try parsing JSON for structured payloads
    } catch (e) {
        data = { body: event.data.text() }; // Fallback for plain text
    }

    const title = data.title || "IRA Companion";
    const options = {
        body: data.body || "New update from IRA.",
        icon: "/static/images/logo.png",
        badge: "/static/images/logo.png",
        data: {
            url: data.url || "/"  // Where the notification should take the user
        },
        tag: "ira-update",       // Prevent duplicate stacking
        renotify: true,          // Alert again if a similar notification shows up
        vibrate: [200, 100, 200] // Optional feedback
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener("notificationclick", function(event) {
    event.notification.close();

    event.waitUntil(
        clients.matchAll({ type: "window", includeUncontrolled: true }).then(function(clientList) {
            for (const client of clientList) {
                if (client.url === event.notification.data.url && "focus" in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(event.notification.data.url || "/");
            }
        })
    );
});