"""Top-level package for Dangermode."""

__author__ = """Kyle Kelley"""
__email__ = "rgbkrk@gmail.com"
__version__ = "0.1.0"


def activate_dangermode(host="127.0.0.1"):
    """Activate the dangermode plugin for ChatGPT. 🚨

    Intended for use in a Jupyter console or IPython kernel, like in the
    Jupyter Notebook or JupyterLab.
    """
    import asyncio
    import atexit

    import uvicorn

    from dangermode.app import app

    config = uvicorn.Config(app, host=host)
    server = uvicorn.Server(config)
    loop = asyncio.get_event_loop()
    loop.create_task(server.serve())

    atexit.register(lambda: asyncio.run(server.shutdown()))


__all__ = ["activate_dangermode"]
