import asyncio
import os
import time

from modules.ocr import MangaPageOcr
from modules.translate import translate
from modules.define import process_word, get_romaji
from concurrent.futures import ThreadPoolExecutor
from fugashi import Tagger

manga_ocr = MangaPageOcr()
tagger = Tagger('-Owakati')

async def process_image(img_path):
    results = manga_ocr(img_path)
    tasks = [translate(result) for result in results]
    translated_results = await asyncio.gather(*tasks)
    return translated_results, results

async def process_text_async(text):
    tagger.parse(text)
    with ThreadPoolExecutor(max_workers=None) as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, process_word, word) for word in tagger(text)]
        return await asyncio.gather(*futures)
    
def process_text(text):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(process_text_async(text))
    return [result for result in results if result is not None]

async def process_and_write(file_name, directory):
    file_path = os.path.join(directory, file_name)
    translated_results, results = await process_image(file_path)

    coroutines = [process_text_async(result) for result in results]
    processed_texts = await asyncio.gather(*coroutines)

    output_file = f'output_{file_name}.txt'
    with open(output_file, 'w') as file:
        for result, translated_result, processed_text in zip(results, translated_results, processed_texts):
            file.write(f"{result}\n")
            file.write(f"{await get_romaji(result)}\n")
            file.write(f"{translated_result}\n")
            for item in processed_text:
                if item is not None:
                    text, definitions = item
                    file.write(text + ": " + str(definitions) + "\n")
                else:
                    file.write("None\n")
            file.write("\n")

    print(f'Processed {file_name}')

async def process_batch(directory, files):
    for file_name in files:
        await process_and_write(file_name, directory)

async def main():
    start = time.time()

    directory = "images"
    #jpg or png
    files = [file for file in os.listdir(directory) if file.endswith('.jpg') or file.endswith('.png')]

    batch_size = 1  # Adjust this to your desired batch size
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        await process_batch(directory, batch)

    print(time.time() - start)
    
asyncio.run(main())