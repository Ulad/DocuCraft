# DocuCraft
The project automates the process of creating Word documents.

Main library: [docxtpl](https://docxtpl.readthedocs.io/en/latest/)  
>The idea is to begin to create an example of the document you want to generate with Microsoft Word, it can be as complex as you want : pictures, index tables, footer, header, variables, anything you can do with word. Then, as you are still editing the document with microsoft word, you insert jinja2-like tags directly in the document. You save the document as a .docx file (xml format) : it will be your .docx template file.
> 
>Now you can use python-docx-template to generate as many word documents you want from this .docx template and context variables you will associate.

The script was created for GitLab, so here is this file `.gitlab-ci.yaml`

## The scheme of the script
![Схема работы скрипта](assets/Схема.png)
The main modules are located in the `src` directory, everything else just imports them with different settings.
1. The `loader` module manages data loading
2. The `docx_maker` module manages the creation and saving of reports
3. The `main` module is the entry point of the program, it connects all modules

❗Sample data and Word documents are stored in `tests/`

## 🛠️ Installing

Clone the repository to any folder, for example via HTTPS:
```bash
git clone https://github.com/Ulad/DocuCraft.git
cd 'your directory'
```
The project uses [UV](https://docs.astral.sh/uv/) to resolve dependencies and virtual environment, if you are already using it, you can skip this step
```bash
pip install uv
```
After installation:
```bash
uv sync
```
All dependencies are specified in the `pyproject.toml` file.

UPD: For backward compatibility, it was added `requirements.txt` in pre-commit, installation via pip (Not recommended!):
```bash
pip install -r requirements.txt --require-hashes
```

## ⚙️ Configuration and Usage

The project uses separate settings file with `pydantic_settings` library:

- `settings.py`

By default, variables for local development are specified there. In the production environment, you need to create environment variables with the same names or create an `.env` file in which you can also specify these variables. There is an example in the `.env.example` file.

Important! In the `loader` module, the main function `load_excel_data` loads only from Excel's named tables, I did it because I want to and it's convenient. 😊
```python
PATH_TO_EXCEL = "path/to/your/excel/file.xlsx"
TABLE_NAME_IN_EXCEL = "table_name"
PATH_TO_DOCX_TPL = "path/to/your/template.docx"
OUTPUT_DIR_DOCX = "path/to/output/docx/"
```
Just run `docucraft/main.py`:
```bash
python main.py
```

## Known issues
Some transformations have been done in the `main` so far, I don't know how to do it in a separate module yet, since the transformations are different in each case.

## Logging
To output all logs to the console, it is enough to change the file `src/helpers/log_settings.yaml`
```yaml
consoleHandler:
  level: INFO  # Change from ERROR to INFO for detailed logs
```

## License
This repository is licensed under the [MIT License](https://github.com/Ulad/DocuCraft/blob/main/LICENSE)
