from modules.upscaler import Upscaler, UpscalerData
from waifu2x.main import processImageWithSplitter, getModel, getCarnV2Model


class Waifu2xFields():
    def __init__(self, style: str, noise: int):
        self.style = style
        self.noise = noise

    def getName(self):
        noiseStr = ['none', 'low', 'medium', 'hight'][self.noise]
        return f'Waifu2x {self.style.lower()} denoise {self.noise} ({noiseStr})'


data = [
    Waifu2xFields('Anime', 0),
    Waifu2xFields('Anime', 1),
    Waifu2xFields('Anime', 2),
    Waifu2xFields('Anime', 3),
    Waifu2xFields('Photo', 0),
    Waifu2xFields('Photo', 1),
    Waifu2xFields('Photo', 2),
    Waifu2xFields('Photo', 3),
]


class BaseClass(Upscaler):
    def __init__(self, dirname, waifu2xFields: Waifu2xFields = None):
        if waifu2xFields is None:
            self.scalers = []
            return

        self.waifu2xFields = waifu2xFields
        self.name = "Waifu2x"
        self.scalers = [UpscalerData(self.waifu2xFields.getName(), None, self, 2)]
        super().__init__()

    def do_upscale(self, img, selected_model):
        model = getModel(self.waifu2xFields.noise, self.waifu2xFields.style)
        return processImageWithSplitter(model, img)


class Class0(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[0])


class Class1(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[1])


class Class2(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[2])


class Class3(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[3])


class Class4(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[4])


class Class5(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[5])


class Class6(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[6])


class Class7(BaseClass, Upscaler):
    def __init__(self, dirname):
        super().__init__(dirname, data[7])


class CarnV2Upscaler(Upscaler):
    def __init__(self, dirname):
        self.name = "Waifu2x"
        self.scalers = [UpscalerData("Waifu2x+ model CarnV2", None, self, 2)]
        super().__init__()

    def do_upscale(self, img, selected_model):
        model = getCarnV2Model()
        return processImageWithSplitter(model, img)


# -------------------------------------------------------------------------
# Forge Classic compatibility patch
# -------------------------------------------------------------------------
# sd-webui-forge-classic may not automatically collect external upscalers
# from extension scripts. This manually appends the Waifu2x upscalers to
# shared.sd_upscalers after the WebUI has initialized enough modules.
# -------------------------------------------------------------------------

def _register_waifu2x_upscalers_for_forge_classic(*args, **kwargs):
    try:
        from modules import shared

        if not hasattr(shared, "sd_upscalers"):
            print("[Waifu2x] shared.sd_upscalers not found; skipping manual registration.")
            return

        upscaler_classes = [
            Class0,
            Class1,
            Class2,
            Class3,
            Class4,
            Class5,
            Class6,
            Class7,
            CarnV2Upscaler,
        ]

        added = 0
        existing_names = {getattr(x, "name", "") for x in shared.sd_upscalers}

        for cls in upscaler_classes:
            upscaler = cls(None)

            for scaler in getattr(upscaler, "scalers", []):
                scaler_name = getattr(scaler, "name", "")

                if scaler_name and scaler_name not in existing_names:
                    shared.sd_upscalers.append(scaler)
                    existing_names.add(scaler_name)
                    added += 1

        try:
            shared.sd_upscalers = sorted(
                shared.sd_upscalers,
                key=lambda x: getattr(x, "name", "").lower()
            )
        except Exception:
            pass

        if added > 0:
            print(f"[Waifu2x] Registered {added} upscalers for Forge Classic.")
        else:
            print("[Waifu2x] Upscalers already registered; nothing added.")

    except Exception as e:
        print(f"[Waifu2x] Failed to register upscalers for Forge Classic: {e}")


try:
    from modules import script_callbacks

    script_callbacks.on_before_ui(_register_waifu2x_upscalers_for_forge_classic)
    script_callbacks.on_app_started(_register_waifu2x_upscalers_for_forge_classic)
except Exception as e:
    print(f"[Waifu2x] Could not attach Forge Classic callbacks: {e}")
