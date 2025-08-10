async function subscribeToPush() {
    try {
        const reg = await navigator.serviceWorker.ready;

        const subscription = await reg.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
        });

        const csrfToken = await getCSRFToken();
        const token = localStorage.getItem("token");

        const res = await fetch("/push/subscribe", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ subscription })
        });

        if (!res.ok) throw new Error("Failed to send subscription to server.");

        console.log("[✔] Push subscription successful.");
    } catch (err) {
        console.error("[✖] Push subscription error:", err);
        alert("Failed to subscribe to notifications.");
    }
}

// Register service worker and subscribe to push
if ("serviceWorker" in navigator && "PushManager" in window) {
    navigator.serviceWorker.register("/sw.js")
        .then(() => {
            console.log("[✔] Service worker registered.");
            subscribeToPush();  // Automatically attempt subscription
        })
        .catch(err => {
            console.error("[✖] Service worker registration failed:", err);
            alert("Could not register service worker.");
        });
} else {
    console.warn("Push messaging not supported in this browser.");
}