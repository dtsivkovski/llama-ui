import reflex as rx
import ollama
from typing import List
from dataclasses import dataclass
from .model_dropdown import ModelDropdownState, OllamaModel
import asyncio

@dataclass
class Message:
    role: str
    content: str

class ChatboxState(ModelDropdownState):
    currentMessage: str = ""
    messages: List[Message] = []
    allowSend: bool = True
    isTyping: bool = False
    typingMessage: str = ""
    lastUsedModelName : str = ""

    @rx.background
    async def handle_send(self):
        model_name = self.get_selected_model_name()

        messages_dict = [{"role": message.role, "content": message.content} for message in self.messages]

        stream = ollama.chat(
            model=model_name,
            messages=messages_dict,
            stream=True
        )

        async with self:
            self.isTyping = True

        for chunk in stream:
            async with self:
                self.typingMessage += chunk['message']['content']
            await asyncio.sleep(0)  
        
        message = Message(role="assistant", content=self.typingMessage)
        async with self:
            self.isTyping = False
            self.typingMessage = ""
            self.messages.append(message)
            self.allowSend = True
            self.lastUsedModelName = model_name
    
    def handle_key_down(self, e: rx.EventHandler):
        if e == "Enter" and self.allowSend and self.currentMessage != "":
            if self.lastUsedModelName != self.get_selected_model_name():
                self.lastUsedModelName = self.get_selected_model_name()
                self.handle_clear()
            
            message = Message(role="user", content=self.currentMessage)
            self.allowSend = False
            self.currentMessage = ""
            self.messages.append(message)
            scroll_to_bottom()
            return ChatboxState.handle_send
        
    def handle_button_send(self):
        if self.allowSend and self.currentMessage != "":
            if self.lastUsedModelName != self.get_selected_model_name():
                self.lastUsedModelName = self.get_selected_model_name()
                self.handle_clear()
            
            message = Message(role="user", content=self.currentMessage)
            self.allowSend = False
            self.currentMessage = ""
            self.messages.append(message)
            scroll_to_bottom()
            return ChatboxState.handle_send


    def handle_change(self, e: rx.EventHandler):
        self.currentMessage = e

    def handle_clear(self):
        self.messages = []


def scroll_to_bottom():
    rx.script(src="scroll_to_bottom.js") 
    rx.script("scrollToBottom()")  

def chatbox() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.hstack(
                    rx.hstack(
                        rx.text("Chatting with ", size="4"),
                        rx.text(ModelDropdownState.selected_model.name, color=rx.color("accent", shade=10), size="4"),
                    ),
                    rx.button(rx.icon(tag="trash", size=20), size="3", on_click=ChatboxState.handle_clear, background_color=rx.color("red", shade=9), cursor="pointer"),
                    direction="row",
                    justify="between",
                    align="center",
                    width="100%",
                ),
            rx.separator(margin_top="0.75em", margin_bottom="0em"),
            rx.flex(
                rx.flex(
                rx.foreach(ChatboxState.messages, lambda message: rx.hstack(
                    rx.box(
                        rx.markdown(message.content),
                        background_color=rx.cond(message.role == "user", rx.color("accent", shade=5), rx.color("gray", shade=5)),
                        border_radius=rx.cond(message.role == "user", "0.5em 0.5em 0em 0.5em", "0.5em 0.5em 0.5em 0em"),
                        padding_x="2em",
                        max_width="80%",
                        margin_bottom="0.5em"
                    ),
                    direction="row",
                    width="100%",
                    justify=rx.cond(message.role == "user", "end", "start")
                )),
                rx.cond(
                    ChatboxState.isTyping,
                    rx.hstack(
                        rx.box(
                            rx.markdown(ChatboxState.typingMessage),
                            background_color=rx.color("gray", shade=5),
                            border_radius="0.5em 0.5em 0.5em 0em",
                            padding_x="2em",
                            margin_bottom="0.5em",
                            max_width="80%"
                        ),
                        direction="row",
                        width="100%",
                        justify="start",
                        align="start"
                    )
                ),
                margin_top="0.75em",
                direction="column"
                ),
                direction="column-reverse",
                overflow_y="scroll",
                id="chatbox"
                ),
                direction="column",
                height="100%",
                width="100%",
            ),
            width="100%",
            height="70vh"
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
            rx.cond(
                ChatboxState.allowSend,
                rx.button(rx.icon(tag="send-horizontal", size=20), size="3", on_click=ChatboxState.handle_button_send, cursor="pointer"),
                rx.button(rx.icon(tag="loader-circle", 
                                  size=20,
                                  animation="spin 1s linear infinite",
                                  ), size="3", disabled=True),
            ),
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