document.addEventListener("DOMContentLoaded", () => {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector(".chat-input span");
  
    let userMessage = null; // Store user's message
    const inputInitHeight = chatInput.scrollHeight;
  
    const createChatLi = (message, className) => {
      const chatLi = document.createElement("li");
      chatLi.classList.add("chat", `${className}`);
      let chatContent =
        className === "outgoing"
          ? `<p></p>`
          : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
      chatLi.innerHTML = chatContent;
      chatLi.querySelector("p").textContent = message;
      return chatLi;
    };
  
    const generateResponse = async (incomingChatLi) => {
      const API_URL = "/ask";
      const payload = { question: userMessage };
  
      try {
        const response = await fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
  
        if (!response.ok) {
          throw new Error("Failed to fetch response from the server.");
        }
  
        const data = await response.json();
        incomingChatLi.querySelector("p").textContent =
          data.answer || "Error: No response.";
      } catch (error) {
        console.error("Error:", error);
        incomingChatLi.querySelector("p").textContent =
          "Something went wrong. Try again later.";
      }
    };
  
    const handleChat = () => {
      userMessage = chatInput.value.trim();
      if (!userMessage) return;
  
      chatInput.value = "";
      chatInput.style.height = `${inputInitHeight}px`;
  
      chatbox.appendChild(createChatLi(userMessage, "outgoing"));
      chatbox.scrollTo(0, chatbox.scrollHeight);
  
      setTimeout(() => {
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
      }, 600);
    };
  
    chatInput.addEventListener("input", () => {
      chatInput.style.height = `${inputInitHeight}px`;
      chatInput.style.height = `${chatInput.scrollHeight}px`;
    });
  
    chatInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleChat();
      }
    });
  
    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () =>
      document.body.classList.remove("show-chatbot")
    );
    chatbotToggler.addEventListener("click", () =>
      document.body.classList.toggle("show-chatbot")
    );
  });
  