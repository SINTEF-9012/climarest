# ClimaREST Mussel Farming Demo

![Frontend Screenshot](screenshots/app.png?raw=true)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Prerequisites

```sh
$ mamba create --name climarest python=3.11
$ mamba activate climarest
$ mamba install streamlit xarray matplotlib plotly numpy pandas cartopy cmocean python-dotenv shapely
```

## Development

You can run the dashboard with

```sh
$ cd ./src
$ streamlit run app/main.py
```

If you don't want the browser to pop up, do this instead

```sh
$ cd ./src
$ streamlit run app/main.py --server.headless true
```

## Contact and Blame

- Volker Hoffmann (volker.hoffmann@sintef.no)
