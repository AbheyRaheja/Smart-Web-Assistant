document.addEventListener("DOMContentLoaded", () => {
  const chat = document.getElementById("chat");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");

  let pageContent = "";
  let initialized = false;

  // Append message to chat
  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.innerHTML = text.replace(/\n/g, "<br>");
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  // Send request to get greeting when extension opens
  function initializeChat() {
    if (!pageContent || initialized) return;

    initialized = true;

    fetch("http://127.0.0.1:8000/summary-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        content: pageContent,
        question: "",  
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.response) {
          addMessage(data.response, "bot");
        }
      })
      .catch((err) => {
        console.error("Init request failed", err);
        addMessage("⚠️ Failed to connect to assistant.", "bot");
      });
  }

  // Handle user input
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";

    try {
      const res = await fetch("http://127.0.0.1:8000/summary-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          content: pageContent,
          question,
        }),
      });

      const data = await res.json();
      addMessage(data.response || "No response", "bot");
    } catch (err) {
      console.error("Request failed", err);
      addMessage("⚠️ Failed to connect to assistant.", "bot");
    }
  });

  // Ask script to fetch page text
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { type: "GET_PAGE_CONTENT" },
      (response) => {
        if (response && response.content) {
          pageContent = response.content;
        } else {
          pageContent = "No content retrieved from page.";
        }
        initializeChat();
      }
    );
  });
});
