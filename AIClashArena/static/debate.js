const debateContainer = document.getElementById("debate-container");
const nextTurnBtn = document.getElementById("next-turn-btn");
const roleSelect = document.getElementById("role-select");
const errorMsg = document.getElementById("error-msg");

const topic = document.getElementById('topic-input').value;
let lastResponse = "";

const API_TOKEN = "SKIBIDI TOILET"; 

function escapeHTML(str) {
  return str.replace(/[&<>"']/g, function (m) {
    return ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[m];
  });
}

function markdownToHTML(text) {
  return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
}

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.classList.add("mb-2", "p-2", "rounded");
  div.style.backgroundColor = role === "attack" ? "#f8d7da" : "#d1e7dd";
  div.style.color = role === "attack" ? "#842029" : "#0f5132";

  let safeText = escapeHTML(text);
  safeText = markdownToHTML(safeText);
  safeText = safeText.replace(/\n/g, "<br>");

  div.innerHTML = `<strong>${role.toUpperCase()}:</strong><br>${safeText}`;

  debateContainer.appendChild(div);
  debateContainer.scrollTop = debateContainer.scrollHeight;
}


async function fetchNextResponse() {
  errorMsg.style.display = "none";

  try {
    const res = await fetch("/api/get_ai_response", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${API_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        topic: topic,
        role: roleSelect.value,
        response: lastResponse,
      }),
    });

    const data = await res.json(); 

    if (!res.ok) {
      throw new Error(data.error || "Failed to fetch response");
    }

    lastResponse = data.response;

    appendMessage(roleSelect.value, lastResponse);
  } catch (e) {
    errorMsg.textContent = e.message;
    errorMsg.style.display = "block";
  }
}

nextTurnBtn.addEventListener("click", fetchNextResponse);

window.addEventListener("DOMContentLoaded", () => {
  fetchNextResponse();
});
