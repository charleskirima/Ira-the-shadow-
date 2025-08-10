async function logMood(emotion, note) {
    try {
        const res = await csrfFetch("/log/mood", {
            method: "POST",
            body: JSON.stringify({ emotion, note })
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData?.error || "Failed to log mood");
        }

        const data = await res.json();
        alert("Mood logged successfully.");
        return data;
    } catch (err) {
        console.error("Mood log error:", err);
        alert("An error occurred while logging your mood.");
    }
}