from cx_Freeze import setup, Executable

setup(
    name = "SiteKontrol",
    version = "0.1",
    description = "This app is controlling site situation and buttons in every 30 minutes and sends an message to team channel",
    executables = [Executable("main.py")]
)
