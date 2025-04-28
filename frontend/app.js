const API_URL = "http://127.0.0.1:8000/chat";

let currentForm = {};
let beklenenAlan = null;
const inputField = document.getElementById("user-input");
const sendButton = document.querySelector("button");

function setLoading(isLoading) {
  inputField.disabled = isLoading;
  sendButton.disabled = isLoading;
  sendButton.textContent = isLoading ? "…" : "Gönder";
}

async function sendMessage() {
  const message = inputField.value.trim();
  if (!message) return;

  addMessage(message, "user");
  inputField.value = "";
  setLoading(true);

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: message,
        current_form: currentForm,
        beklenen_alan: beklenenAlan
      }),
    });
    const data = await res.json();

    if (data.status === "completed") {
      addMessage(data.message, "bot");
      inputField.placeholder = "Mesajınızı yazın...";
      currentForm = {};
      beklenenAlan = null;
    }
    else if (data.status === "incomplete") {
      currentForm = data.data;
      beklenenAlan = data.beklenen_alan;
      addMessage(data.next_question, "bot");
      inputField.placeholder = data.next_question;
    }
    else {
      addMessage("Bir hata oluştu: " + data.message, "bot");
      inputField.placeholder = "Mesajınızı yazın...";
    }
  }
  catch (err) {
    addMessage("Sunucu hatası: " + err.message, "bot");
    inputField.placeholder = "Mesajınızı yazın...";
  }
  finally {
    setLoading(false);
    inputField.focus();
  }
}

function addMessage(message, sender) {
  const container = document.getElementById("messages");
  const div = document.createElement("div");
  div.classList.add("message", sender === "user" ? "user-message" : "bot-message");
  div.textContent = message;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

inputField.addEventListener("keypress", e => {
  if (e.key === "Enter") sendMessage();
});
