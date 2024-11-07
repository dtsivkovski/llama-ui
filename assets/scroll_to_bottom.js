function scrollToBottom() {
    const chatbox = document.getElementById("chatbox");
    if (chatbox) {
        chatbox.scrollTop = chatbox.scrollHeight;
    }
}