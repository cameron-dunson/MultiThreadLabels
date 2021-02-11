#!/usr/bin/bash

pipenv lock -r > requirements.txt && printf "\nThis project's requirements.txt created and updated!\n"