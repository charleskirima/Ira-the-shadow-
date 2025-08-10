async function logSpiritual() {
    try {
        const res = await csrfFetch("/log/spiritual", {
            method: "POST",
            body: JSON.stringify({})  // placeholder if future data is needed
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData?.error || "Failed to log spiritual entry.");
        }

        const data = await res.json();
        alert(data.message || "Spiritual log recorded.");
        return data;
    } catch (err) {
        console.error("Spiritual logging error:", err);
        alert("Something went wrong while logging spirituality.");
    }
}