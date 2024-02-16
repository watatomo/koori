import asyncio
import os
import time
import re

from modules.ocr import MangaPageOcr

manga_ocr = MangaPageOcr()


async def process_image(img_path):
    results = manga_ocr(img_path)
    return results


async def process_and_write(file_name, directory):
    file_path = os.path.join(directory, file_name)
    results = await process_image(file_path)

    output_file = f"output_{file_name}.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        for result in zip(results):
            result = (
                re.sub("[(',')]", "", str(result))
                .replace("．．．", "…")
                .replace("．", ".")
            )
            file.write(f"{result}\n")
            file.write("\n")

    print(f"Processed {file_name}")


async def process_batch(directory, files):
    for file_name in files:
        await process_and_write(file_name, directory)


async def main():
    start = time.time()

    directory = "images"
    # jpg or png
    files = [
        file
        for file in os.listdir(directory)
        if file.endswith(".jpg") or file.endswith(".png")
    ]

    batch_size = 1  # Adjust this to your desired batch size
    for i in range(0, len(files), batch_size):
        batch = files[i : i + batch_size]
        await process_batch(directory, batch)

    print(time.time() - start)


asyncio.run(main())
