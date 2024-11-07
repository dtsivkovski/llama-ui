import reflex as rx
import ollama
from typing import List
from dataclasses import dataclass
from .model_dropdown import ModelDropdownState, OllamaModel

@dataclass
class Message:
    role: str
    content: str

class ChatboxState(ModelDropdownState):
    currentMessage: str = ""
    messages: List[Message] = []
    allowSend: bool = True

    def handle_key_down(self, e: rx.EventHandler):
        if e == "Enter" and self.allowSend:
            message = Message(role="user", content=self.currentMessage)
            self.allowSend = False
            self.currentMessage = ""
            self.messages.append(message)
            self.handle_send()

    def handle_change(self, e: rx.EventHandler):
        self.currentMessage = e

    def handle_send(self):
        model = self.get_selected_model()

        messages_dict = [{"role": message.role, "content": message.content} for message in self.messages]

        stream = ollama.chat(
            model=model.model,
            messages=messages_dict,
            stream=True
        )

        message_content = ""

        for chunk in stream:
            message_content += chunk['message']['content']
        
        message = Message(role="assistant", content=message_content)
        self.messages.append(message)
        scroll_to_bottom()
        self.allowSend = True

def scroll_to_bottom():
    rx.script(src="scroll_to_bottom.js")

def chatbox() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.hstack(
                rx.text("Chatting with ", size="4"),
                rx.text(ModelDropdownState.selected_model.name, color=rx.color("accent", shade=10), size="4"),
                direction="row",
                justify="start",
                align="center",
                width="100%",
            ),
            rx.separator(margin_top="0.75em", margin_bottom="1.5em"),
            rx.vstack(
                rx.foreach(ChatboxState.messages, lambda message: rx.hstack(
                    rx.box(
                        rx.text(message.content),
                        background_color=rx.cond(message.role == "user", rx.color("accent", shade=5), rx.color("gray", shade=5)),
                        border_radius="0.5em 0.5em 0em 0.5em",
                        padding_y="0.5em",
                        padding_x="1em",
                        margin_bottom="0.5em"
                    ),
                    direction="row",
                    width="100%",
                    justify=rx.cond(message.role == "user", "end", "start")
                )),
                width="100%",
                height="100%",
                ),
                direction="column",
                height="100%",
                width="100%",
                overflow_y="scroll",
                id="chatbox"
            ),
            width="100%",
            height="70vh",
            overflow_y="scroll"
        ),
        rx.hstack(
            rx.input(
                placeholder="Message",
                width="100%",
                size="3",
                value=ChatboxState.currentMessage,
                on_key_down=ChatboxState.handle_key_down,
                on_change=ChatboxState.handle_change,
            ),
            rx.button(rx.icon(tag="send-horizontal", size=20), size="3"),
            direction="row",
            margin_top="1em",
            width="100%",
            justify="end",
        ),
        width="100%",
        height="100%",
        background_color=rx.color_mode_cond(light="#f5f5f5", dark="#212121"),
        border_radius="1em",
        padding="1em",
    )