async function logSleep(hours) {
    hours = Number(hours);
    if (isNaN(hours) || hours < 0 || hours > 24) {
        alert("Sleep hours must be a number between 0 and 24.");
        return;
    }

    try {
        const res = await csrfFetch("/log/sleep", {
            method: "POST",
            body: JSON.stringify({ hours })
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData?.error || "Failed to log sleep.");
        }

        const data = await res.json();
        alert(data.message || "Sleep logged successfully.");
        return data;
    } catch (err) {
        console.error("Sleep logging error:", err);
        alert("An error occurred while logging sleep.");
    }
}