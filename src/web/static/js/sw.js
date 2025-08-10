self.addEventListener("push", function(event) {
    let message = "New notification from IRA Companion";

    if (event.data) {
        try {
            message = event.data.text();
        } catch (err) {
            console.warn("Push payload parse error:", err);
        }
    }

    const options = {
        body: message,
        icon: "/static/images/logo.png",
        badge: "/static/images/logo.png", // Optional: for status bar on Android
        tag: "ira-notify",
        renotify: true // Replaces older notification with same tag
    };

    event.waitUntil(
        self.registration.showNotification("IRA Companion", options)
    );
});

self.addEventListener("notificationclick", function(event) {
    event.notification.close();

    event.waitUntil(
        clients.matchAll({ type: "window", includeUncontrolled: true }).then(windowClients => {
            for (const client of windowClients) {
                if (client.url.includes("/dashboard") && "focus" in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow("/dashboard");
            }
        })
    );
});