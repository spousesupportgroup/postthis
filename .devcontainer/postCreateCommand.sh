#!/bin/bash

cat .devcontainer/bashrc.override.sh >> ~/.bashrc
poetry config virtualenvs.create false
