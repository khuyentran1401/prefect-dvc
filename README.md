[![](https://img.shields.io/badge/DagsHub-Link%20to%20DagsHub-red)](https://dagshub.com/khuyentran1401/dagshub-demo)
# End-to-end Customer Segmentation Project

## Tools Used in This Project
* [hydra](https://hydra.cc/): Manage configuration files
* [DVC](https://dvc.org/): Data version control
* [DagsHub](http://dagshub.com/): GitHub-like platform for data scientists and machine learning engineers
## Project Structure
* `src`: consists of Python scripts
* `config`: consists of configuration files
* `data`: consists of data
* `notebook`: consists of Jupyter Notebooks
* `tests`: consists of test files

## Set Up the Project
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
make setup
make install_all
```

## Run the Project
To run all flows, type:
```bash
python src/main.py
```



