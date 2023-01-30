
from nero_model import NeroModel
from nero_view import NeroView
from typing import Optional


class NeroController:
    def __init__(self, model: NeroModel) -> None:
        self.model = model

    def run(self) -> None:
        view = NeroView(self)
        view.mainloop()

    def check_can(self) -> None:
        self.model.check_can()

    def get_mph(self) -> Optional[int]:
        return self.model.get_mph()

    def get_kph(self) -> Optional[int]:
        return self.model.get_kph()

    def get_status(self) -> Optional[bool]:
        return self.model.get_status()
