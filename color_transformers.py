def precharge_state_color_transformer(precharge: str) -> str:
    if precharge == "GLV ON":
        return "blue"
    elif precharge == "TSMS ON":
        return "orange"
    elif precharge == "Precharging":
        return "yellow"
    elif precharge == "Ready":
        return "green"
    else:
        return "white"
