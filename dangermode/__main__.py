import os
from jupyter_console.app import ZMQTerminalIPythonApp, flags, aliases

from traitlets import Bool, Dict
from traitlets.config import catch_config_error, boolean_flag

user_interaction_required_banner = """
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🚨🚨 DANGER MODE READY FOR ACTIVATION 🚨🚨
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

This is a Jupyter console instance that has been preloaded with the dangermode library.

Run to start the ChatGPT Plugin server on your local machine 🙈

activate_dangermode()
"""

docker_banner = """

🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🚨🚨 DANGER MODE FOR CHATGPT ACTIVATED 🚨🚨
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

The server is live, running on port 8000.

Configure it with ChatGPT: https://github.com/rgbkrk/dangermode#enabling-on-chatgpt

This is a standard IPython session that ChatGPT also has access to.
"""

flags.update(
    boolean_flag(
        "totally-in-docker", "DangerModeIPython.totally_in_docker", "Activate dangermode immediately when in Docker"
    )
)


class DangerModeIPython(ZMQTerminalIPythonApp):
    flags = Dict(flags)

    totally_in_docker = Bool(
        False, config=True, help="Run dangermode.activate_dangermode(host='0.0.0.0') when in Docker"
    )

    def init_banner(self):
        if self.totally_in_docker:
            self.shell.banner = docker_banner
            self.shell.show_banner()
            return

        self.shell.banner = user_interaction_required_banner
        self.shell.show_banner()

    def initialize(self, argv=None):
        super().initialize(argv)
        self.shell.run_cell("from dangermode import activate_dangermode", store_history=False)

        if self.totally_in_docker:
            self.shell.run_cell("activate_dangermode(host='0.0.0.0')", store_history=False)


main = launch_new_instance = DangerModeIPython.launch_instance

if __name__ == "__main__":
    main()
