import asyncio
import os
import time
import unicodedata

from modules.ocr import MangaPageOcr

manga_ocr = MangaPageOcr()


# This normalizes full-width Latin letters and Roman numerals but also turns every other character that isn't Japanese to half-width so...
def normalize_fullwidth_chars(text):
    return unicodedata.normalize("NFKC", text)


async def process_image(img_path):
    results = manga_ocr(img_path)
    return results


async def process_and_write(file_name, directory):
    file_path = os.path.join(directory, file_name)
    results = await process_image(file_path)
    output_folder = "text"

    output_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"## {os.path.splitext(file_name)[0]}\n")
        file.writelines(
            normalize_fullwidth_chars(line)
            .replace(".....", "……")
            .replace("...", "…")
            .replace(":・", "…")  # sometimes ocr mistakes ellipses for these
            .replace("::", "…")
            .replace("..", "…")
            .replace("!", "！")
            .replace("?", "？")
            .replace("―", "ー")
            .replace("~", "～")
            .replace("〜", "～")  # wave dash vs full-width tilde
            + "\n\n"
            for line in results
        )

    print(f"Processed {file_name}")


async def process_batch(directory, files):
    for file_name in files:
        await process_and_write(file_name, directory)


async def combine_text_files(output_folder):
    combined_file = os.path.join(output_folder, "combined_text.txt")

    with open(combined_file, "w", encoding="utf-8") as outfile:
        for filename in os.listdir(output_folder):
            if filename.endswith(".txt") and filename != "combined_text.txt":
                with open(
                    os.path.join(output_folder, filename), "r", encoding="utf-8"
                ) as infile:
                    outfile.write(infile.read())


async def main():
    start = time.time()

    directory = "images"

    files = [
        file
        for file in os.listdir(directory)
        if file.endswith((".jpg", ".png", ".jpeg"))
    ]

    batch_size = 1
    for i in range(0, len(files), batch_size):
        batch = files[i : i + batch_size]
        await process_batch(directory, batch)

    output_folder = "text"
    await combine_text_files(output_folder)

    print(f"Time taken: {time.time() - start}")


asyncio.run(main())
