from dateutil.parser import parse
from pathlib import Path
from PIL import Image
import filedate
import datetime
import pytz
import json
import re
import os

IMG_TIMEZONE = 'Europe/London'


def set_datetime(media_path: str, output_dir: str, utc_timestamp: float):
    os.makedirs(output_dir, exist_ok=True)
    os.system(f'cp "{media_path}" "{output_dir}"')
    utc_datetime = pytz.timezone(IMG_TIMEZONE).localize(
        datetime.datetime.fromtimestamp(utc_timestamp)
    )
    mediaCopy = filedate.File(f'{output_dir}/{Path(media_path).name}')
    mediaCopy.set(
        created=utc_datetime,
        modified=utc_datetime,
        accessed=utc_datetime
    )


def get_datetime(media_path: str, metadata_path: str = None):
    # Check for metadata timestamp
    try:
        with open(metadata_path if metadata_path else media_path + '.json', 'r') as f:
            photo_taken_time = json.load(f).get('photoTakenTime')
            metadata_timestamp = float(
                (photo_taken_time or {}).get('timestamp'))
            return metadata_timestamp
    except Exception as e:
        if not metadata_path:
            directory = Path(media_path).parent
            media_filename = Path(media_path).stem.replace('-edited', '')
            metadata_suffix = '.json'

            if m := re.search(r"\((\d+)\)", media_filename):
                m = m.group()
                metadata_suffix = f"{m}.json"
                media_filename = media_filename.replace(m, '')

            for random_filename in os.listdir(directory):
                if random_filename.endswith(metadata_suffix):
                    metadata_filename = Path(
                        random_filename.replace('.json', '')).stem
                    if metadata_filename == media_filename:
                        return get_datetime(media_path, f'{directory}/{random_filename}')

    # Check for exif timestamp
    try:
        if not (exif_datetime := Image.open(media_path)._getexif().get(36867)):
            raise ValueError(
                '\t🟡 no exif \'datetime_original\' data found in image')
        exif_timestamp = pytz.timezone(IMG_TIMEZONE).localize(
            datetime.datetime.strptime(
                exif_datetime, '%Y:%m:%d %H:%M:%S')
        ).astimezone(pytz.utc).timestamp()
        return exif_timestamp
    except Exception as e:
        pass

    # Check for filename timestamp
    try:
        name_timestamp = parse(
            re.search(r"\d{8}", Path(media_path).stem).group()).timestamp()
        max = datetime.datetime.now().timestamp()
        min = datetime.datetime(2010, 1, 1).timestamp()
        if name_timestamp > max or name_timestamp < min:
            raise ValueError()
        return name_timestamp
    except Exception as e:
        pass

    print(media_path)

    return None
