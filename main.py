from nero_model import NeroModel
from nero_controller import NeroController


if __name__ == "__main__":
    model = NeroModel()
    controller = NeroController(model)

    controller.run()
