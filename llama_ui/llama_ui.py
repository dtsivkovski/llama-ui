"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from .components.model_dropdown import model_dropdown, ModelDropdownState
from .components.chatbox import chatbox

class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.hstack(
                model_dropdown(),
                rx.button(
                    rx.color_mode.button(),
                    variant="ghost",
                    color="accent",
                    size="2",
                    as_child=True,
                    cursor="pointer"
                ),
                justify="end",
                align="end",
                width="100%",
                spacing="2"
            ),
            rx.vstack(
                chatbox(),
                spacing="5",
                direction="column",
                justify="start",
                align="center",
                min_height="75vh",
                width="100%",
                margin_top="1em"
            ),
            margin_top="2em",
            width="100%"
        )
    )

defaultTitle = "LLama UI"

app = rx.App(
    theme=rx.theme(
        has_background=True,
        radius="large",
        accent_color="grass",
    ),
    stylesheets=[
        "style.css"
    ]
)
app.add_page(index, title=defaultTitle)
