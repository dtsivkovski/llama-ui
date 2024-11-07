import reflex as rx


def chatbox(current_model: str) -> rx.Component:
    return rx.box(
        rx.flex(
            rx.hstack(
                rx.text("Chatting with ", size="4"),
                rx.text(current_model, color=rx.color("accent", shade=10), size="4"),
                direction="row",
                justify="start",
                align="center",
                width="100%",
            ),
            rx.separator(margin_top="0.75em", margin_bottom="1.5em"),
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.text("Hello, World!"),
                        background_color=rx.color("accent", shade=5),
                        border_radius="0.5em 0.5em 0em 0.5em",
                        padding_y="0.5em",
                        padding_x="1em"
                    ),
                    direction="row",
                    width="100%",
                    justify="end"
                ),
                rx.hstack(
                    rx.box(
                        rx.text("Hello, World!"),
                        background_color=rx.color("gray", shade=5),
                        border_radius="0 0.5em 0.5em 0.5em",
                        padding_y="0.5em",
                        padding_x="1em"
                    ),
                    direction="row",
                    width="100%",
                    justify="start"
                ),
                width="100%",
                height="100%"
            ),
            direction="column",
            height="100%",
            width="100%",
            flex_grow=1
        ),
        background_color=rx.color_mode_cond(light="#f5f5f5", dark="#212121"),
        border_radius="1em",
        padding="1em",
        min_height="70vh",
        width="100%",
        height="100%"
    )
