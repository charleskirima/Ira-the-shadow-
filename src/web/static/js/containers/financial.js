async function logFinancial(income, expenses, goals) {
    try {
        const res = await csrfFetch("/log/financial", {
            method: "POST",
            body: JSON.stringify({ income, expenses, goals })
        });

        if (!res.ok) {
            const errorData = await res.json().catch(() => ({}));
            throw new Error(errorData?.error || "Failed to log financial data.");
        }

        const data = await res.json();
        alert(data.message || "Financial data saved successfully.");
        return data;
    } catch (err) {
        console.error("Financial logging error:", err);
        alert("An error occurred while saving financial info.");
    }
}