import os
import gzip
import json
import random
import pickle
import secrets
import hashlib
import threading
from base64 import b64encode, b64decode
from typing import Final, Optional, Union
import cv2
import numpy as np


WORK_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR: Final[str] = os.path.join(WORK_DIR, 'datasets')
CAPTCHAS_FILE_PATH: Final[str] = os.path.join(WORK_DIR, 'captchas.pkl')


def generate_random_string(length: int, with_punctuation: bool = True,
                           with_letters: bool = True) -> str:
    """
    Generates a random string

    :param length: The length of the string
    :param with_punctuation: Whether to include special characters
    :param with_letters: Whether letters should be included
    """

    characters = '0123456789'

    if with_punctuation:
        characters += r"!\'#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

    if with_letters:
        characters += 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def get_random_image(all_images: list[str]) -> str:
    """
    Retrieve a random image path from the list, decode it from base64, and return it.

    :param all_images: A list of image paths encoded as base64 strings.
    :return: The decoded image data as a string.
    """

    random_image = random.choice(all_images)
    decoded_image = b64decode(random_image.encode('utf-8'))
    decompressed_data = gzip.decompress(decoded_image)

    return decompressed_data


def convert_image_to_base64(image_data: bytes) -> str:
    """
    Converts an image into Base64 Web Format

    :param image_data: The data of an image file in webp format
    :return: A data URL representing the image in Base64 Web Format
    """

    encoded_image = b64encode(image_data).decode('utf-8')

    data_url = f'data:image/webp;base64,{encoded_image}'

    return data_url


def manipulate_image_bytes(image_data: bytes, is_small: bool = False,
                           hardness: int = 1) -> bytes:
    """
    Manipulates an image represented by bytes to create a distorted version.

    :param image_data: The bytes representing the original image.
    :param is_small: Whether the image should be resized to 100x100 or not.
    :param hardness: A number between 1 and 5 that determines the distortion factor.
    :return: The bytes of the distorted image.
    """

    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Image data could not be decoded.")

    height, width = img.shape[:2]

    if hardness > 3:
        num_dots = np.random.randint(20, 50) * (hardness - 3)
        dot_coords = np.random.randint(0, [width, height], size=(num_dots, 2))
        colors = np.random.randint(0, 256, size=(num_dots, 3))

        for (x, y), color in zip(dot_coords, colors):
            img[y, x] = color

        num_lines = np.random.randint(20, 50) * (hardness - 3)
        start_coords = np.random.randint(0, [width, height], size=(num_lines, 2))
        end_coords = np.random.randint(0, [width, height], size=(num_lines, 2))
        colors = np.random.randint(0, 256, size=(num_lines, 3))

        for (start, end), color in zip(zip(start_coords, end_coords), colors):
            cv2.line(img, tuple(start), tuple(end), color.tolist(), 1)

    max_shift = max(3, hardness)
    x_shifts = np.random.randint(-max(2, hardness - 1), max_shift, size=(height, width))
    y_shifts = np.random.randint(-max(2, hardness - 1), max_shift, size=(height, width))

    map_x, map_y = np.meshgrid(np.arange(width), np.arange(height))
    map_x = (map_x + x_shifts) % width
    map_y = (map_y + y_shifts) % height

    shifted_img = cv2.remap(
        img, map_x.astype(np.float32),
        map_y.astype(np.float32), cv2.INTER_LINEAR
    )
    shifted_img_hsv = cv2.cvtColor(shifted_img, cv2.COLOR_BGR2HSV)

    shifted_img_hsv[..., 1] = np.clip(shifted_img_hsv[..., 1] * (1 + hardness * 0.06), 0, 255)
    shifted_img_hsv[..., 2] = np.clip(shifted_img_hsv[..., 2] * (1 - hardness * 0.03), 0, 255)

    shifted_img = cv2.cvtColor(shifted_img_hsv, cv2.COLOR_HSV2BGR)
    shifted_img = cv2.GaussianBlur(shifted_img, (5, 5), hardness * 0.1)

    size = 100 if is_small else 200
    shifted_img = cv2.resize(shifted_img, (size, size), interpolation=cv2.INTER_LINEAR)

    _, output_bytes = cv2.imencode('.webp', shifted_img)
    if not _:
        raise ValueError("Image encoding failed.")

    return output_bytes.tobytes()


file_locks = {}

class Json:
    """
    Class for loading / saving JavaScript Object Notation (= JSON)
    """

    def __init__(self) -> None:
        self.data = None


    def load(self, file_path: str, default: Optional[
             Union[dict, list]] = None) -> Union[dict, list]:
        """
        Function to load a JSON file securely.

        :param file_path: The JSON file you want to load
        :param default: Returned if no data was found
        """

        if default is None:
            default = {}

        if not os.path.isfile(file_path):
            return default

        if file_path not in file_locks:
            file_locks[file_path] = threading.Lock()

        with file_locks[file_path]:
            try:
                with open(file_path, 'r', encoding = 'utf-8') as file:
                    data = json.load(file)
            except Exception:
                if self.data.get(file_path) is not None:
                    self.dump(self.data[file_path], file_path)
                    return self.data
                return default
        return data


    def dump(self, data: Union[dict, list], file_path: str) -> bool:
        """
        Function to save a JSON file securely.
        
        :param data: The data to be stored should be either dict or list
        :param file_path: The file to save to
        """

        file_directory = os.path.dirname(file_path)
        if not os.path.isdir(file_directory):
            return False

        if file_path not in file_locks:
            file_locks[file_path] = threading.Lock()

        with file_locks[file_path]:
            self.data = data
            try:
                with open(file_path, 'w', encoding = 'utf-8') as file:
                    json.dump(data, file)
            except Exception:
                pass
        return True


class Pickle:
    """
    Class for loading / saving Pickle
    """

    def __init__(self) -> None:
        self.data = {}


    def load(self, file_path: str, default: Optional[
             Union[dict, list]] = None) -> Union[dict, list]:
        """
        Function to load a Pickle file securely.

        :param file_path: The Pickle file you want to load
        :param default: Returned if no data was found
        """

        if default is None:
            default = {}

        if not os.path.isfile(file_path):
            return default

        if file_path not in file_locks:
            file_locks[file_path] = threading.Lock()

        with file_locks[file_path]:
            try:
                with open(file_path, 'rb') as file:
                    data = pickle.load(file)
            except Exception:
                if self.data.get(file_path) is not None:
                    self.dump(self.data[file_path], file_path)
                    return self.data
                return default

        return data


    def dump(self, data: Union[dict, list], file_path: str) -> bool:
        """
        Function to save a Pickle file securely.
        
        :param data: The data to be stored should be either dict or list
        :param file_path: The file to save to
        """

        file_directory = os.path.dirname(file_path)
        if not os.path.isdir(file_directory):
            return False

        if file_path not in file_locks:
            file_locks[file_path] = threading.Lock()

        with file_locks[file_path]:
            self.data[file_path] = data
            try:
                with open(file_path, 'wb') as file:
                    pickle.dump(data, file)
            except Exception:
                pass

        return True


JSON = Json()
PICKLE = Pickle()


class Hashing:
    """
    Implementation for hashing
    """

    def __init__(self, salt: Optional[str] = None):
        """
        :param salt: The salt, makes the hashing process more secure (Optional)
        """

        self.salt = salt


    def hash(self, plain_text: str, hash_length: int = 8) -> str:
        """
        Function to hash a plaintext

        :param plain_text: The text to be hashed
        :param hash_length: The length of the returned hashed value
        """

        salt = self.salt
        if salt is None:
            salt = secrets.token_hex(hash_length)
        plain_text = salt + plain_text

        hash_object = hashlib.sha256(plain_text.encode())
        hex_dig = hash_object.hexdigest()

        return hex_dig + '//' + salt


    def compare(self, plain_text: str, hash_string: str) -> bool:
        """
        Compares a plaintext with a hashed value

        :param plain_text: The text that was hashed
        :param hash: The hashed value
        """

        salt = self.salt
        if '//' in hash_string:
            hash_string, salt = hash_string.split('//')

        hash_length = len(hash_string)

        comparison_hash = Hashing(salt=salt).hash(plain_text,
                                                  hash_length = hash_length).split('//')[0]

        return comparison_hash == hash_string
