
const navButtons = document.querySelectorAll(".nav-btn");
const panels = document.querySelectorAll(".panel");

navButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
        const targetId = btn.getAttribute("data-target");

        navButtons.forEach(function (b) { b.classList.remove("active"); });
        panels.forEach(function (p) { p.classList.remove("active"); });

        btn.classList.add("active");
        document.getElementById(targetId).classList.add("active");
    });
});


const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeLabel = document.getElementById("themeLabel");

themeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        themeIcon.textContent = "☀️";
        themeLabel.textContent = "Light mode";
    } else {
        themeIcon.textContent = "🌙";
        themeLabel.textContent = "Dark mode";
    }
});


function createSourceTagsHTML(sources) {
    if (!sources || sources.length === 0) {
        return "";
    }

    let tagsHTML = '<div class="source-tags">';
    tagsHTML += '<span class="status-msg">📎 Sources:</span>';
    sources.forEach(function (source) {
        tagsHTML += '<span class="source-tag">' + source + "</span>";
    });
    tagsHTML += "</div>";
    return tagsHTML;
}

function showResultCard(containerId, text, sources) {
    const container = document.getElementById(containerId);
    let html = '<div class="result-card">' + text + "</div>";
    if (sources && sources.length > 0) {
        html = '<div class="result-card">' + text + createSourceTagsHTML(sources) + "</div>";
    }
    container.innerHTML = html;
}

function showStatus(containerId, message, isError) {
    const container = document.getElementById(containerId);
    const cssClass = isError ? "status-msg error" : "status-msg";
    container.innerHTML = '<p class="' + cssClass + '">' + message + "</p>";
}

const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatLog = document.getElementById("chatLog");

chatForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const message = chatInput.value.trim();
    if (message === "") {
        return;
    }

    const userBubble = document.createElement("div");
    userBubble.className = "user-msg";
    userBubble.textContent = message;
    chatLog.appendChild(userBubble);

    chatInput.value = "";
    chatLog.scrollTop = chatLog.scrollHeight;

    const thinkingCard = document.createElement("div");
    thinkingCard.className = "boarding-pass agent-msg";
    thinkingCard.innerHTML = '<div class="bp-stub">GATE · ROUTING</div><div class="bp-body">Deciding which agent should handle this...</div>';
    chatLog.appendChild(thinkingCard);
    chatLog.scrollTop = chatLog.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        thinkingCard.remove();

        const agentName = data.agent_used || "Assistant";
        const answer = data.answer || data.message || "Sorry, something went wrong.";
        const sources = data.sources || [];

        const card = document.createElement("div");
        card.className = "boarding-pass agent-msg";

        let innerHTML = '<div class="bp-stub">GATE · ' + agentName.toUpperCase() + '</div>';
        innerHTML += '<div style="flex-grow:1;">';
        innerHTML += '<div class="bp-body">' + answer + '</div>';
        if (sources.length > 0) {
            innerHTML += '<div class="bp-sources">' + sources.map(function (s) {
                return '<span class="source-tag">📎 ' + s + '</span>';
            }).join("") + '</div>';
        }
        innerHTML += '</div>';

        card.innerHTML = innerHTML;
        chatLog.appendChild(card);
        chatLog.scrollTop = chatLog.scrollHeight;
    })
    .catch(function (error) {
        thinkingCard.remove();
        const errorCard = document.createElement("div");
        errorCard.className = "boarding-pass agent-msg";
        errorCard.innerHTML = '<div class="bp-stub">GATE · ERROR</div><div class="bp-body">Something went wrong. Please try again.</div>';
        chatLog.appendChild(errorCard);
        console.log(error);
    });
});


document.getElementById("itineraryForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const destination = document.getElementById("itDestination").value;
    const days = document.getElementById("itDays").value;
    const interests = document.getElementById("itInterests").value || "general sightseeing";
    const budgetLevel = document.getElementById("itBudget").value;

    showStatus("itineraryResult", "Planning your trip...", false);

    fetch("/itinerary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            destination: destination,
            days: days,
            interests: interests,
            budget_level: budgetLevel
        })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        showResultCard("itineraryResult", data.itinerary, data.sources);
    })
    .catch(function (error) {
        showStatus("itineraryResult", "Something went wrong. Please try again.", true);
        console.log(error);
    });
});


document.getElementById("compareForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const rawInput = document.getElementById("compareDestinations").value;
    const destinations = rawInput.split(",").map(function (d) { return d.trim(); }).filter(function (d) { return d !== ""; });

    if (destinations.length < 2) {
        showStatus("compareResult", "Please enter at least two destinations, separated by commas.", true);
        return;
    }

    showStatus("compareResult", "Comparing destinations...", false);

    fetch("/compare", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ destinations: destinations })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        showResultCard("compareResult", data.comparison, data.sources);
    })
    .catch(function (error) {
        showStatus("compareResult", "Something went wrong. Please try again.", true);
        console.log(error);
    });
});


document.getElementById("budgetForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const destination = document.getElementById("budgetDestination").value;
    const days = document.getElementById("budgetDays").value;
    const travelers = document.getElementById("budgetTravelers").value;
    const style = document.getElementById("budgetStyle").value;

    showStatus("budgetResult", "Crunching the numbers...", false);

    fetch("/budget", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            destination: destination,
            days: days,
            travelers: travelers,
            style: style
        })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        const numbers = data.numbers;

        let tableHTML = '<table class="budget-table">';
        tableHTML += "<tr><td>Accommodation</td><td class='amount'>$" + numbers.stay_total + "</td></tr>";
        tableHTML += "<tr><td>Food</td><td class='amount'>$" + numbers.food_total + "</td></tr>";
        tableHTML += "<tr><td>Local transport</td><td class='amount'>$" + numbers.transport_total + "</td></tr>";
        tableHTML += "<tr><td>Activities</td><td class='amount'>$" + numbers.activities_total + "</td></tr>";
        tableHTML += "<tr class='total'><td>Total estimate</td><td class='amount'>$" + numbers.grand_total + "</td></tr>";
        tableHTML += "</table>";

        const finalHTML = tableHTML + data.explanation;
        showResultCard("budgetResult", finalHTML, []);
    })
    .catch(function (error) {
        showStatus("budgetResult", "Something went wrong. Please try again.", true);
        console.log(error);
    });
});


const weatherIconMap = {
    "Clear sky": "☀️", "Mainly clear": "🌤️", "Partly cloudy": "⛅", "Overcast": "☁️",
    "Fog": "🌫️", "Depositing rime fog": "🌫️",
    "Light drizzle": "🌦️", "Moderate drizzle": "🌦️", "Dense drizzle": "🌧️",
    "Slight rain": "🌦️", "Moderate rain": "🌧️", "Heavy rain": "🌧️",
    "Slight snow": "🌨️", "Moderate snow": "🌨️", "Heavy snow": "❄️",
    "Rain showers": "🌦️", "Moderate rain showers": "🌧️", "Violent rain showers": "⛈️",
    "Thunderstorm": "⛈️", "Thunderstorm with hail": "⛈️", "Thunderstorm with heavy hail": "⛈️"
};

document.getElementById("weatherForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const city = document.getElementById("weatherCity").value;

    showStatus("weatherResult", "Checking the sky...", false);

    fetch("/weather", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ city: city })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        if (data.error) {
            showStatus("weatherResult", data.error, true);
            return;
        }

        const icon = weatherIconMap[data.condition] || "🌍";

        let html = '<div class="weather-card">';
        html += '<div class="weather-icon">' + icon + '</div>';
        html += '<div>';
        html += '<div class="weather-temp">' + data.temperature_celsius + '°C</div>';
        html += '<div>' + data.place + ' — ' + data.condition + '</div>';
        html += '<div class="status-msg">Wind: ' + data.windspeed_kmh + ' km/h</div>';
        html += '</div></div>';

        document.getElementById("weatherResult").innerHTML = html;
    })
    .catch(function (error) {
        showStatus("weatherResult", "Something went wrong. Please try again.", true);
        console.log(error);
    });
});


document.getElementById("attractionsForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const destination = document.getElementById("attractionsDestination").value;

    showStatus("attractionsResult", "Finding great spots...", false);

    fetch("/attractions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ destination: destination })
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        showResultCard("attractionsResult", data.attractions, data.sources);
    })
    .catch(function (error) {
        showStatus("attractionsResult", "Something went wrong. Please try again.", true);
        console.log(error);
    });
});


const uploadZone = document.getElementById("uploadZone");
const pdfInput = document.getElementById("pdfInput");
const uploadBtn = document.getElementById("uploadBtn");

uploadZone.addEventListener("click", function () {
    pdfInput.click();
});

uploadBtn.addEventListener("click", function () {
    if (pdfInput.files.length === 0) {
        showStatus("uploadResult", "Please choose at least one PDF file first.", true);
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < pdfInput.files.length; i++) {
        formData.append("pdf_files", pdfInput.files[i]);
    }

    showStatus("uploadResult", "Uploading and processing your documents...", false);
    uploadBtn.disabled = true;

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
        uploadBtn.disabled = false;
        showStatus("uploadResult", "✅ " + data.message + " (" + data.chunks_added + " chunks added)", false);
    })
    .catch(function (error) {
        uploadBtn.disabled = false;
        showStatus("uploadResult", "Something went wrong while uploading.", true);
        console.log(error);
    });
});