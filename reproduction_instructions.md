# Instructions for reproducing the pipeline
If you want to run the pipeline and get the results for yourself, and you're using linux, here are the instructions. I don't know if this works the same on other operating systems.

1. Copy the repository. Click the green 'Code'-button and download the zip. Unzip it.
2. In the ´code´-folder, run the command line command `poetry install`. This install the needed dependencies.
3. Copy the first url in ´data/example_query.txt´ into your browser, wait for the page to load, and press Ctrl+s to save the page in the ´data/count_all´ folder with the name `all.json`.
4. Use the command `poetry run python3` + the name of the file you want to run. You'll want to run `get_concordances.py` first, for reference it took ~20 minutes to complete on my machine. The API it accesses is free to be accessed.
