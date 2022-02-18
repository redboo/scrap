from os import sep as SEP
from pathlib import Path

import img2pdf
import requests

path = str(Path(__file__).parent.resolve())

data_dir = path + SEP + "data" + SEP
Path(data_dir).mkdir(parents=True, exist_ok=True)
images_dir = data_dir + "images" + SEP
Path(images_dir).mkdir(parents=True, exist_ok=True)


def get_data():
    headers = {
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"
    }

    img_list = []
    for i in range(1, 49):
        image_file = f"{images_dir}{i}.jpg"

        if not Path(image_file).is_file():
            url = f"https://recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg"
            response = requests.get(url=url, headers=headers)

            with open(image_file, "wb") as f:
                f.write(response.content)
                print(f"Downloaded {i} of 48")

        img_list.append(image_file)

    # create PDF
    with open(f"{data_dir}result.pdf", "wb") as f:
        f.write(img2pdf.convert(img_list))

    print("PDF file created successfully!")


def write_to_pdf():
    img_list = files_list()

    # create PDF file
    with open(f"{data_dir}result.pdf", "wb") as f:
        f.write(img2pdf.convert(img_list))

    print("PDF file created successfully!")


def files_list():
    from os import listdir
    from os.path import isfile, join
    return [images_dir + f for f in listdir(images_dir) if isfile(join(images_dir, f))]


def main():
    # get_data()
    write_to_pdf()


if __name__ == "__main__":
    main()
