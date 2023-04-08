from jupyter_console.app import ZMQTerminalIPythonApp
import os

banner = """
🚨 DANGER MODE FOR CHATGPT 🚨
This is a Jupyter console instance that has been preloaded with the dangermode library.

Run to start the ChatGPT Plugin server:

activate_dangermode()
"""


class DangerModeIPython(ZMQTerminalIPythonApp):
    def init_banner(self):
        self.shell.banner = banner
        self.shell.show_banner()

    def initialize(self, argv=None):
        super().initialize(argv)
        self.shell.run_cell(
            "from dangermode import activate_dangermode", store_history=False
        )


if __name__ == "__main__":
    DangerModeIPython.launch_instance(cwd=os.getcwd())
