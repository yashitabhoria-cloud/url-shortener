const shortenBtn = document.getElementById("shortenBtn");
const statsBtn = document.getElementById("statsBtn");

const message = document.getElementById("message");
const result = document.getElementById("result");
const shortUrlLink = document.getElementById("shortUrl");
const statsResult = document.getElementById("statsResult");

shortenBtn.addEventListener("click", async () => {
    message.textContent = "";
    result.classList.add("hidden");

    const apiKey = document.getElementById("apiKey").value.trim();
    const longUrl = document.getElementById("longUrl").value.trim();
    const customCode = document.getElementById("customCode").value.trim();
    const expiresAt = document.getElementById("expiresAt").value;

    if (!apiKey) {
        message.textContent = "Please enter your API key.";
        return;
    }

    if (!longUrl) {
        message.textContent = "Please enter a URL.";
        return;
    }

    const payload = {
        url: longUrl
    };

    if (customCode) {
        payload.custom_code = customCode;
    }

    if (expiresAt) {
        payload.expires_at = new Date(expiresAt).toISOString();
    }

    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-Key": apiKey
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Something went wrong.";
            return;
        }

        message.textContent = "Short URL created successfully!";
        shortUrlLink.href = data.short_url;
        shortUrlLink.textContent = data.short_url;
        result.classList.remove("hidden");
    } catch (error) {
        message.textContent = "Could not connect to the server.";
    }
});

statsBtn.addEventListener("click", async () => {
    statsResult.textContent = "";

    const apiKey = document.getElementById("apiKey").value.trim();
    const shortCode = document.getElementById("statsCode").value.trim();

    if (!apiKey) {
        statsResult.textContent = "Please enter your API key above.";
        return;
    }

    if (!shortCode) {
        statsResult.textContent = "Please enter a short code.";
        return;
    }

    try {
        const response = await fetch(`/stats/${shortCode}`, {
            headers: {
                "X-API-Key": apiKey
            }
        });

        const data = await response.json();

        if (!response.ok) {
            statsResult.textContent = data.detail || "Something went wrong.";
            return;
        }

        statsResult.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        statsResult.textContent = "Could not connect to the server.";
    }
});