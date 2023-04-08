# 🚨 Dangermode

## Overview

🚨 Dangermode is a ChatGPT Plugin written with Python and FastAPI that allows users to execute code snippets in an IPython session.

⚠️ Dangermode is a proof-of-concept and should not be used in production. It is not secure and should not be used to execute code on a remote server. ⚠️

## Features

- Execute code snippets in an IPython session through ChatGPT.
- Inspect variables and view results in real-time.
- Serve images and display data to ChatGPT.

## Installation

To install the Dangermode package, use the following command:

```bash
pip install dangermode
```

## Usage

🚨🚨🚨 YOU ARE GIVING AN AI ACCESS TO YOUR ENTIRE COMPUTER. 🚨🚨🚨

After installing the package, you can use the Dangermode plugin in your IPython session. Here's how to get started:

1. Import the `dangermode` package in your IPython session.

```python
import dangermode
```

2. Activate the Dangermode plugin.

```python
dangermode.activate_dangermode()
```

3. Use ChatGPT to run code snippets and interact with your IPython session.

## API Endpoints

- `GET /openapi.json`: Retrieve the OpenAPI JSON configuration.
- `GET /.well-known/ai-plugin.json`: Retrieve the AI plugin JSON configuration.
- `GET /images/{image_name}`: Retrieve an image by its name.
- `GET /api/variable/{variable_name}`: Retrieve the value of a variable by its name.
- `POST /api/run_cell`: Execute a code cell and return the result.

## Contributing

Please do. I can't let Large Language Models write all of it.

Please fork the repository, make your changes, and submit a pull request.

## License

Dangermode is released under the BSD 3-Clause License. See [LICENSE](LICENSE) for more information.

## Contact

If you have any questions or feedback, please feel free to reach out to the author, Kyle Kelley, on Twitter at [@KyleRayKelley](https://twitter.com/KyleRayKelley) or just open an issue on the repository.
