function sendMessage() {
    const input = document.getElementById("userMessage");
    const msg = input.value.trim();

    if (!msg) {
        alert("Please type a message.");
        return;
    }

    csrfFetch("/chat/respond", {
        method: "POST",
        body: JSON.stringify({ message: msg })
    })
    .then(res => {
        if (res.status === 401) {
            alert("Session expired. Please log in again.");
            window.location.href = "/auth/login";
            return null;
        }
        return res.json();
    })
    .then(data => {
        if (!data || !data.response) return;

        const chatBox = document.getElementById("chatResponses");

        const userMessage = document.createElement("p");
        userMessage.textContent = "You: " + msg;
        userMessage.classList.add("user-message");

        const botMessage = document.createElement("p");
        botMessage.textContent = "IRA: " + data.response;
        botMessage.classList.add("bot-response");

        chatBox.appendChild(userMessage);
        chatBox.appendChild(botMessage);
        input.value = "";
        input.focus();
    })
    .catch(err => {
        console.error("Chat fetch error:", err);
        alert("Failed to contact IRA. Please try again.");
    });
}