from fastapi import APIRouter
from fastapi.responses import FileResponse, Response
from IPython import get_ipython
from IPython.utils.capture import capture_output

from dangermode.models import (
    DisplayData,
    ErrorData,
    RunCellRequest,
    RunCellResponse,
    image_store,
)

router = APIRouter()


@router.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def get_ai_plugin_json():
    return {
        "schema_version": "v1",
        "name_for_human": "Notebook Session",
        "name_for_model": "notebook_session",
        "description_for_human": "Allow ChatGPT to play with data in your running IPython kernel and Jupyter Notebook.",
        "description_for_model": "Plugin for IPython/Jupyter Notebook. You can inspect variables and run code.",
        "auth": {"type": "none"},  # YOLO 😂😭
        "api": {
            "type": "openapi",
            "url": "http://localhost:8000/openapi.json",
            "is_user_authenticated": False,
        },
        "logo_url": "http://localhost:8000/static/images/logo.png",
        "contact_email": "rgbkrk@gmail.com",
        "legal_info_url": "https://github.com/rgbkrk/honchkrow/issues",
    }


@router.get("/images/{image_name}", include_in_schema=False)
async def get_image(image_name: str):
    try:
        image_bytes = image_store.get_image(image_name)
        return Response(image_bytes, media_type="image/png")
    except KeyError as ke:
        return ErrorData.from_exception(ke)


@router.get("/api/variable/{variable_name}")
async def get_variable(variable_name: str) -> DisplayData:
    try:
        ip = get_ipython()
        value = ip.user_ns[variable_name]
        return DisplayData.from_tuple(ip.display_formatter.format(value))
    except KeyError as ke:
        return ErrorData.from_exception(ke)


@router.post("/api/run_cell")
async def execute(request: RunCellRequest) -> RunCellResponse:
    try:
        with capture_output() as captured:
            ip = get_ipython()
            result = ip.run_cell(request.code)

        if result.success:
            return RunCellResponse.from_result(
                result.result, captured.stdout, captured.stderr, captured.outputs
            )
        else:
            return RunCellResponse.from_error(result.error_in_exec)

    except Exception as e:
        return RunCellResponse.from_error(e)
