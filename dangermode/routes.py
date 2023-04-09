from typing import Union
from fastapi import APIRouter, HTTPException
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

from dangermode.suggestions import RUN_CELL_PARSE_FAIL

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
async def get_image(image_name: str) -> Response:
    try:
        image_bytes = image_store.get_image(image_name)
        return Response(image_bytes, media_type="image/png")
    except KeyError as ke:
        raise HTTPException(status_code=404, detail="Image not found")


@router.get("/api/variable/{variable_name}")
async def get_variable(variable_name: str) -> Union[DisplayData, ErrorData]:
    '''Get a variable if it exists'''
    try:
        ip = get_ipython()
        value = ip.user_ns[variable_name]
        return DisplayData.from_tuple(ip.display_formatter.format(value))
    except KeyError as ke:
        raise HTTPException(status_code=404, detail=f"Variable {variable_name} not defined")


@router.post("/api/run_cell")
async def execute(request: RunCellRequest) -> RunCellResponse:
    '''Execute a cell and return the result

    The execution format is

    ```json
    {
        "code": "print('hello world')"
    }
    ```

    '''
    code = request.code

    if code is None or code == "":
        raise HTTPException(
            status_code=400,
            detail=RUN_CELL_PARSE_FAIL,
        )

    try:
        with capture_output() as captured:
            ip = get_ipython()
            result = ip.run_cell(code)

        if result.success:
            return RunCellResponse.from_result(result.result, captured.stdout, captured.stderr, captured.outputs)
        else:
            return RunCellResponse.from_error(result.error_in_exec)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing code: {e}")
