from dataclasses import dataclass
from typing import List
import reflex as rx
import ollama

@dataclass
class ModelDetails:
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str

@dataclass
class OllamaModel:
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: ModelDetails

    @classmethod
    def from_dict(cls, data: dict):
        details = ModelDetails(**data['details'])
        return cls(**{**data, 'details': details})

class ModelDropdownState(rx.State):
    ollamaModels: List[OllamaModel] = [OllamaModel.from_dict(m) for m in ollama.list()["models"]]
    print(ollamaModels)
    opened: bool = False
    selected_model: OllamaModel = ollamaModels[0]

    def toggle_opened(self, value: bool):
        self.opened = value

    def select_model(self, model: OllamaModel):
        self.selected_model = model

    def refresh_models(self):
        self.ollamaModels = [OllamaModel.from_dict(m) for m in ollama.list()["models"]]
        print(self.ollamaModels)

    def pull_model(self, model_name: str):
        print(model_name)
        ollama.pull(model_name)
        self.refresh_models()

def display_row(model: OllamaModel):
    return rx.menu.item(
        rx.flex(
            rx.text(model.name),
            rx.text(model.details.parameter_size,
                    margin_left="2em"),
            on_click=lambda: ModelDropdownState.select_model(model),
            justify="between",
            align="center",
            width="100%"
        )
    )

def model_dropdown() -> rx.Component:

    return rx.hstack(
        rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.hstack(
                                rx.text("Model: "),
                                rx.text(ModelDropdownState.selected_model.name),
                                rx.cond(
                                    ModelDropdownState.opened,
                                    rx.icon(tag="chevron-down"),
                                    rx.icon(tag="chevron-right"),
                                ),
                                spacing="1"
                            ),
                            variant="soft", size="3"
                        ),
                    ),
                    rx.menu.content(
                        rx.foreach(ModelDropdownState.ollamaModels, display_row)
                    ),
        on_open_change=ModelDropdownState.toggle_opened
        ),
        rx.dialog.root(
            rx.dialog.trigger(
                rx.button(
                    rx.icon(tag="plus"),
                    size="3",
                    padding_x="0.5em"
                )
            ),
            rx.dialog.content(
                rx.vstack(
                    rx.heading("Download Model"),
                    rx.hstack(
                        rx.input(
                            placeholder="Model Name",
                            width="100%"
                        ),
                        rx.button(
                            "Download",
                            on_click=lambda: ModelDropdownState.pull_model(ModelDropdownState.selected_model.name)
                        ),
                        align="center",
                        justify="start",
                        width="100%"
                    ),

                )
            )
        )
                    
    )
