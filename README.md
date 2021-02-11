Label Generation Script
=======================
> ATTN: you will need to create a `.env` file in this project directory that has the below values filled in with your preferred entries.

> NOTE: This project uses `Python 3`

Install dependencies to get started
-----------------------------------
- Run this command to install dependencies needed for this script to run properly:
```bash
pip install -r requirements.txt
```

Run the script
--------------
- Be sure to `cd` into this project directory once you have pulled it from Git, then in your terminal or command prompt run:
```bash
python multiThreadStaticLabel.py
```
- The script will begin to log output in the terminal to update you of your labels status.

- There is a folder inside the `./labels/` directory with sub folders that correspond to each of the `15` processes that are running creating labels for you. Inside each you will find the label PDF's you need.

Housekeeping
------------
- There is an additional python file you can run to clean the subdirectories within the `labels` directory between runs. This is `optional` and provides a fast way to get rid of old label pdfs.

You can run this command to clean the `labels` directory:
```bash
python clean_labels_directory.py
```