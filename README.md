# Koori

A fork of [Yuki](https://github.com/c-sig/yuki) which is in turn a fork of [Mokuro](https://github.com/kha-white/mokuro). Automatically OCRs manga pages and outputs the results to a TXT file.

Requires Python 3.10.

## Usage

1. Clone the repository by using git or [downloading the zip](https://github.com/watatomo/koori/archive/refs/heads/master.zip)
2. Install the required packages with `pip install -r requirements.txt`
3. Place pages in the `images` folder
4. Run `main.py` with `python main.py`
   put images in images directory

The outputs will have the same name as the pages and will be exported in the `text` folder. There is also a file named `combined_text.txt` that combines all the outputs into one with page headers.

> [!NOTE]
> Remember that the OCR is not 100% accurate and you will still need to manually correct mistakes. This simply exists to speed up the process.

## To-do

-   [x] Combine all the outputs into a single file, with headers signifying which sections are from
-   [ ] Have the OCR follow the text in "reading order" (This is probably complicated as hell to do, so it's just here as an "idea" of sorts.)
