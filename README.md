<p align="center">
  <a href="https://ingage.institute">
    <img alt="logo" src="docs/images/ingage-big.png" height="auto" width="auto" style="border-radius: 50">
  </a>
  <br><br><br>
  <a href="https://codecov.io/gh/BelinguoAG/full-power-backend">
    <img src="https://codecov.io/gh/BelinguoAG/full-power-backend/branch/master/graph/badge.svg?token=ow3IXellp0"/>
  </a>
  <a href="https://github.com/BelinguoAG/full-power-backend/workflows/Tests">
    <img alt="test" src="https://github.com/BelinguoAG/full-power-backend/workflows/Tests/badge.svg">
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
</p>

# Chatbot Backend

Backend for the ingage's health chatbot application.

## Build the docs

The documentation is generated by [Mkdocs material](https://squidfunk.github.io/mkdocs-material/). In case they are not deployed on a server, you can create a server on your machine to look at it. Execute the following commands to do it:

```shell
python -m pip install -r requirements.txt
mkdocs serve -a 127.0.0.1:80
```

After you execute this commmands, the docs will be available in <a href="http://localhost" target="_blank">localhost</a>.
The last command will keep the local server online until you press `Ctrl-C`.
