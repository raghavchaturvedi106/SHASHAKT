const API_BASE = "https://shashakt.onrender.com/";

const CHAT_URL = `${API_BASE}/chat`;

const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const micButton = document.getElementById("micButton");

const messages = document.getElementById("messages");
const typing = document.getElementById("typing");

let conversationStarted = false;


/* =========================
   ADD MESSAGE
========================= */

function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className =
        `message ${sender === "user"
            ? "user-message"
            : "bot-message"}`;

    message.textContent = text;

    messages.appendChild(message);

    scrollToBottom();
}


/* =========================
   SCROLL
========================= */

function scrollToBottom() {

    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    });

}


/* =========================
   TYPING
========================= */

function showTyping() {

    typing.classList.remove("hidden");

}

function hideTyping() {

    typing.classList.add("hidden");

}


/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {

    const text = messageInput.value.trim();

    if (!text) {
        return;
    }


    /* Show user message */

    addMessage(text, "user");

    messageInput.value = "";

    messageInput.style.height = "auto";

    showTyping();


    try {

        const response = await fetch(
            CHAT_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: text
                })
            }
        );


        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );

        }


        const data = await response.json();


        hideTyping();


        /*
         * Support multiple possible
         * backend response formats.
         */

        const reply =
            data.response ??
            data.answer ??
            data.reply ??
            data.message ??
            data.text ??
            "Mujhe abhi response nahi mila.";


        addMessage(reply, "bot");

        conversationStarted = true;


    } catch (error) {

        console.error(
            "SHASHAKT API error:",
            error
        );

        hideTyping();


        addMessage(
            "SHASHAKT se connection nahi ho pa raha. Backend server check karo.",
            "bot"
        );

    }

}


/* =========================
   QUICK PROMPTS
========================= */

function quickMessage(text) {

    messageInput.value = text;

    sendMessage();

}


/* =========================
   SEND BUTTON
========================= */

sendButton.addEventListener(
    "click",
    sendMessage
);


/* =========================
   ENTER TO SEND
========================= */

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


/* =========================
   AUTO RESIZE TEXTAREA
========================= */

messageInput.addEventListener(
    "input",
    function() {

        this.style.height = "auto";

        this.style.height =
            Math.min(
                this.scrollHeight,
                140
            ) + "px";

    }
);


/* =========================
   VOICE INPUT
========================= */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


if (SpeechRecognition) {

    const recognition =
        new SpeechRecognition();


    recognition.lang = "hi-IN";

    recognition.continuous = false;

    recognition.interimResults = false;


    micButton.addEventListener(
        "click",
        function() {

            try {

                recognition.start();

                micButton.classList.add(
                    "recording"
                );

            } catch (error) {

                console.log(
                    "Voice recognition already running."
                );

            }

        }
    );


    recognition.onresult =
        function(event) {

            const transcript =
                event
                    .results[0][0]
                    .transcript;


            messageInput.value =
                transcript;


            messageInput.dispatchEvent(
                new Event("input")
            );


            micButton.classList.remove(
                "recording"
            );


            sendMessage();

        };


    recognition.onerror =
        function(event) {

            console.error(
                "Speech recognition error:",
                event.error
            );


            micButton.classList.remove(
                "recording"
            );

        };


    recognition.onend =
        function() {

            micButton.classList.remove(
                "recording"
            );

        };

} else {

    /*
     * Browser does not support
     * SpeechRecognition.
     */

    micButton.style.display = "none";

}


/* =========================
   INITIAL BOT MESSAGE
========================= */

setTimeout(
    function() {

        addMessage(
            "Aap apni education, skills, location ya career goal ke baare mein bata sakte hain. Main aapke liye suitable options identify karne mein help karunga.",
            "bot"
        );

    },
    500
);
