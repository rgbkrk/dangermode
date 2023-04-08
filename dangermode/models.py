import base64
from typing import Dict, List, Optional, Tuple

from IPython import get_ipython
from pydantic import BaseModel


class RunCellRequest(BaseModel):
    code: str


class DisplayData(BaseModel):
    data: Optional[dict] = None
    metadata: Optional[dict] = None

    @classmethod
    def from_tuple(cls, formatted: Tuple[dict, dict]):
        return cls(data=formatted[0], metadata=formatted[1])


class ImageData(BaseModel):
    data: bytes
    url: str


class ImageStore(BaseModel):
    """An in-memory store for images that have been displayed in the notebook."""

    image_store: Dict[str, ImageData] = {}

    def store_images(self, dd: DisplayData) -> DisplayData:
        """Convert all image/png data to URLs that the frontend can fetch"""

        if dd.data and "image/png" in dd.data:
            image_name = f"image-{len(self.image_store)}.png"
            image_data = base64.b64decode(dd.data["image/png"])

            self.image_store[image_name] = ImageData(
                data=image_data, url=f"http://localhost:8000/images/{image_name}"
            )
            dd.data["image/png"] = self.image_store[image_name].url

        return dd

    def get_image(self, image_name: str) -> bytes:
        return self.image_store[image_name].data

    def clear(self):
        self.image_store = {}


# Initialize the image store as a global instance
image_store = ImageStore()


class ErrorData(BaseModel):
    error: str

    @classmethod
    def from_exception(cls, e: Exception):
        return cls(error=str(e) if str(e) else type(e).__name__)


class RunCellResponse(BaseModel):
    success: bool = False
    execute_result: Optional[DisplayData] = None
    error: Optional[str] = ""
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    displays: List[DisplayData] = []

    @classmethod
    def from_result(cls, result, stdout, stderr, displays):
        ip = get_ipython()

        execute_result = DisplayData.from_tuple(ip.display_formatter.format(result))
        displays = [DisplayData(data=d.data, metadata=d.metadata) for d in displays]

        # Convert all image/png data to URLs that the frontend can fetch
        displays = [image_store.store_images(d) for d in displays]
        execute_result = image_store.store_images(execute_result)

        return cls(
            success=True,
            execute_result=execute_result,
            stdout=stdout,
            stderr=stderr,
            displays=displays,
        )

    @classmethod
    def from_error(cls, error):
        return cls(
            success=False,
            result=None,
            error=f"Error executing code: {error}",
        )
