async function getCSRFToken() {
    try {
        const res = await fetch("/csrf/token");
        if (!res.ok) throw new Error("Failed to fetch CSRF token.");
        const data = await res.json();
        return data.csrf_token;
    } catch (err) {
        console.error("CSRF token fetch error:", err);
        throw err;
    }
}

async function csrfFetch(url, options = {}) {
    const csrfToken = await getCSRFToken();
    const authToken = localStorage.getItem("token");

    const headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        ...(options.headers || {})
    };

    if (authToken) {
        headers["Authorization"] = `Bearer ${authToken}`;
    }

    return fetch(url, {
        ...options,
        headers
    });
}