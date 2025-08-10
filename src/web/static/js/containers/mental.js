async function logMental(clarity, notes) {
    clarity = Number(clarity);
    if (isNaN(clarity) || clarity < 0 || clarity > 10) {
        alert("Clarity must be a number between 0 and 10.");
        return;
    }

    try {
        const res = await csrfFetch("/log/mental", {
            method: "POST",
            body: JSON.stringify({ clarity, notes })
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData?.error || "Failed to log mental state.");
        }

        const data = await res.json();
        alert(data.message || "Mental state logged.");
        return data;
    } catch (err) {
        console.error("Mental log error:", err);
        alert("An error occurred while logging mental state.");
    }
}