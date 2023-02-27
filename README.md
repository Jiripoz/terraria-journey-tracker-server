# Terraria Journey Tracker - Server

The main purpose of this project is to track your progress when playing Terraria Journey mode. This repository is the backend part of the project and has the following features:
- Decrypt the player file, read it and update the frontend whenever a change is made.
- Has methods that can be run to get new items added to the the game when it is updated. This is made through the use of the MediaWiki API of [terraria.wiki.gg//api.php](https://terraria.wiki.gg//api.php) and [https://terraria.fandom.com/wiki/Terraria_Wiki]

## Requirements
To run this project you will need to install [OpenSSL](https://www.openssl.org/)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements file.

```bash
pip install -r requirements
```
It's also necessary to create a copy of `.env.example` named `.env` and fill the appropriate environment variables.

## Usage

```sh
py start.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
