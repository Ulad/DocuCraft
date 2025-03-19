# DocuCraft
The project automates the process of creating Word documents and (optionally) converting them to PDF files.

The script is designed to run on Windows because it uses the COM interface of Microsoft Word. Microsoft Word must be installed. On other operating systems, the conversion takes place with formatting errors.

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
3. The `pdf_converter` module manages conversion and saving.docx to .pdf 
4. The `main` module is the entry point of the program, it connects all modules

In fact, these modules are independent and can be used separately, that is, they can only be created.docx or just convert to .pdf.

❗Sample data and Word documents are stored in `tests/`
## 🔧 Prerequisites

- Windows Operating System (обязательно для корректной конвертации в PDF)
- Python 3.13+
- Microsoft Word (installed locally)

## 🛠️ Installing

Clone the repository to any folder, for example via HTTPS:
```bash
git clone https://kwannon.ukterra.ru/analytics/test.git
cd 'your directory'
```
The project uses uv to resolve dependencies and virtual environment, if you are already using it, you can skip this step
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

The project uses separate settings file (by default, a text file is used.):
- settings.py (# TODO файл .env)
You need to specify the main variables in it.

Important! In the `loader` module, the main function `load_excel_data` loads only from named tables, I did it because I want to and it's convenient. 😊
```python
PATH_TO_EXCEL = "path/to/your/excel/file.xlsx"
TABLE_NAME_IN_EXCEL = ""
PATH_TO_DOCX_TPL = "path/to/your/template.docx"
OUTPUT_DIR_DOCX = "path/to/output/docx/"
OUTPUT_DIR_PDF = "path/to/output/pdf/"
```
Just run src/main.py:
```bash
python main.py
```

## 📝 Data requirements: (TODO describe it better)
Most of it is described in the code dict[str, dict[str, Any]].
How exactly this data gets into the main module `docx_maker` is not important, but in the test file I have made several popular data transformation cases

## Logging
To output all logs to the console, it is enough to change the file `src/helpers/log_settings.yaml`
```yaml
consoleHandler:
  level: INFO  # Change from ERROR to INFO for detailed logs
```

## Running in a test environment (environment variables?). Separation of work environments via init in settings.py

## License
This repository is licensed under the [MIT License](https://github.com/Ulad/DocuCraft/blob/main/LICENSE)
