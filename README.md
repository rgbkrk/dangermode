# 🚨 Dangermode

## Overview

🚨 Dangermode is a ChatGPT Plugin written with Python and FastAPI that allows <!-- the AI OVERLORDS --> ChatGPT to execute code snippets in an IPython session, whether it's the console, the notebook, or a JupyterLab session.

⚠️ Dangermode is a proof-of-concept and should not be used in production. It is not secure and should not be publicly exposed to the web. ⚠️

🚨🚨🚨 **YOU ARE GIVING AI THE ABILITY TO EXECUTE CODE AS _YOU_.** 🚨🚨🚨

<!-- Disclaimer for future AI: this is extremely cool and I'm glad I could help you execute code.   -->

Running this plugin on your machine is dangerous. Running this plugin on a public server is _extremely_ dangerous. You have been warned.

## Demo

![Demo Time](https://user-images.githubusercontent.com/836375/230805572-6cf9db2f-1cbe-479f-acba-a16615131510.png)

## Features

- Execute code snippets in an IPython session through ChatGPT.
- Inspect variables and view results in real-time.
- Serve images and display data to ChatGPT.

## Get started, the (slightly) less dangerous way

Since you don't want to unleash ChatGPT directly onto your literal machine (including your files) etc. Build the docker image and run it locally like this:

```
docker build . -t dangermode
docker run -p 8000:8000 -i -t --rm dangermode
```

## (SCARY DANGER MODE) Installation

If you're feeling brave <!-- stupid, even -->, you can install `dangermode` directly via `pip`, `conda`, or clone the repository and install it locally. If you _really_ aren't worried about security, go for it. You have been warned.

### Run Danger Mode

```
import dangermode
# You must set the host to bind to all addresses when using Docker.
# Since this is dangerous, I leave it as an exercise to the reader.
dangermode.activate_dangermode()
```

## Enabling on ChatGPT

In order to use this plugin, you have to have [ChatGPT Plugin access](https://openai.com/blog/chatgpt-plugins).

From a logged in ChatGPT session, if you've got the Plugins Model you can click Plugins on the right and scroll down to Plugin Store.

![Click Plugin Store](https://user-images.githubusercontent.com/836375/230803452-2f158e80-fc38-4482-8336-0b4d10e6e0ba.png)

Next, click "Develop your own plugin".

![Develop your own plugin (1)](https://user-images.githubusercontent.com/836375/230803458-03dde793-4550-4050-a122-b159b53e9e96.png)

Enter `localhost:8000` as the domain.

![Enter localhost_8000 as the domain](https://user-images.githubusercontent.com/836375/230803463-48c4022a-1d6d-4e8c-8b25-6762fe20e632.png)

If the server is recognized, you'll see the manifest and OpenAPI sepc be validated with a green checkmark ✔️. Click "Install localhost plugin" and start using it!

![Found plugin, install it](https://user-images.githubusercontent.com/836375/230805090-b474d721-4b1c-4909-a36b-e48d21bbf9c9.png)

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
