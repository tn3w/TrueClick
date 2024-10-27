"""
common.py

This module provides a collection of utility functions and classes for various 
operations related to file handling, image processing, and data caching. 
Key features include random string generation, image manipulation, file read/write 
capabilities with locking, and hashing functionalities.

Additionally, the module supports operations for checking file permissions and 
directory status, as well as providing an interface for cached file access.

License:
Made available under the GPL-3.0 license.
"""

import os
import gzip
import json
import random
import pickle
import secrets
import hashlib
from threading import Lock
from base64 import b64encode
from typing import Final, Optional, Any
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np


WORK_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR: Final[str] = os.path.join(WORK_DIR, 'datasets')
CAPTCHAS_FILE_PATH: Final[str] = os.path.join(WORK_DIR, 'captchas.pkl')


def generate_random_string(length: int, with_punctuation: bool = True,
                           with_letters: bool = True) -> str:
    """
    Generates a random string.

    Args:
        length (int): The length of the string.
        with_punctuation (bool): Whether to include special characters. Default is True.
        with_letters (bool): Whether letters should be included. Default is True.

    Returns:
        str: A randomly generated string.
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

    Args:
        all_images (List[str]): A list of image paths encoded as base64 strings.

    Returns:
        bytes: The decoded image data.
    """

    random_image = random.choice(all_images)
    decompressed_data = gzip.decompress(random_image)

    return decompressed_data


def convert_image_to_base64(image_data: bytes) -> str:
    """
    Converts an image into Base64 Web Format.

    Args:
        image_data (bytes): The data of an image file in webp format.

    Returns:
        str: A data URL representing the image in Base64 Web Format.
    """

    encoded_image = b64encode(image_data).decode('utf-8')
    data_url = f'data:image/webp;base64,{encoded_image}'

    return data_url


def manipulate_image_bytes(image_data: bytes, is_small: bool = False,
                           hardness: int = 1) -> bytes:
    """
    Manipulates an image represented by bytes to create a distorted version.

    Args:
        image_data (bytes): The bytes representing the original image.
        is_small (bool): Whether the image should be resized to 100x100 or not. Default is False.
        hardness (int): A number between 1 and 5 that determines the distortion factor.

    Returns:
        bytes: The bytes of the distorted image.
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


def is_directory_empty(directory_path: str) -> bool:
    """
    Checks if a directory has any subdirectories.

    Args:
        directory_path (str): The path to the directory to check.

    Returns:
        bool: True if the directory has any subdirectories, False otherwise.
    """

    if not os.path.isdir(directory_path):
        return True

    for entry in os.listdir(directory_path):
        full_path = os.path.join(directory_path, entry)
        if os.path.exists(full_path):
            return False

    return True


def read(file_path: str, as_bytes: bool = False, default: Any = None) -> Any:
    """
    Reads a file.
    
    Args:
        file_path (str): The path to the file to read.
        default (Any, optional): The default value to return if the file
                                 does not exist. Defaults to None.
        as_bytes (bool, optional): Whether to return the file as bytes. Defaults to False.

    Returns:
        Any: The contents of the file, or the default value if the file does not exist.
    """

    try:
        with open(file_path, "r" + ("b" if as_bytes else ""),
                  encoding = None if as_bytes else "utf-8") as file:
            return file.read()

    except (FileNotFoundError, IsADirectoryError, IOError,
            PermissionError, ValueError, UnicodeDecodeError,
            TypeError, OSError):
        pass

    return default


def write(file_path: str, content: Any) -> bool:
    """
    Writes a file.

    Args:
        file_path (str): The path to the file to write to.
        content (Any): The content to write to the file.

    Returns:
        bool: True if the file was written successfully, False otherwise.
    """

    try:
        with open(file_path, "w" + ("b" if isinstance(content, bytes) else "")) as file:
            file.write(content)

        return True

    except (FileNotFoundError, IsADirectoryError, IOError,
            PermissionError, ValueError, TypeError, OSError):
        pass

    return False


file_locks: dict = {}
WRITE_EXECUTOR = ThreadPoolExecutor()


class CachedFile:
    """
    A interface for an file type with caching.
    """


    def __init__(self) -> None:
        self._data = {}


    def _get_cache(self, file_path: str) -> Any:
        """
        Gets the cached value for the given file path.

        Args:
            file_path (str): The path to the file to get the cached value for.

        Returns:
            Any: The cached value for the given file path.
        """

        return self._data.get(file_path)


    def _set_cache(self, file_path: str, value: Any) -> None:
        """
        Sets the cached value for the given file path.

        Args:
            file_path (str): The path to the file to set the cached value for.
            value (Any): The value to set the cached value to.
        
        Returns:
            None
        """

        self._data[file_path] = value


    def _load(self, file_path: str) -> Any:
        """
        Loads the file.

        Args:
            file_path (str): The path to the file to load.

        Returns:
            Any: The loaded file.
        """

        return read(file_path)


    def _dump(self, data: Any, file_path: str) -> bool:
        """
        Writes the data to the file.

        Args:
            data (Any): The data to write to the file.
            file_path (str): The path to the file to write to.

        Returns:
            bool: True if the file was written successfully, False otherwise.
        """

        return write(file_path, data)


    def load(self, file_path: str,
             default: Any = None) -> Any:
        """
        Loads the file.

        Args:
            file_path (str): The path to the file to load.
            default (Any, optional): The default value to return if the file
                                     does not exist. Defaults to None.

        Returns:
            Any: The loaded file.
        """

        file_data = self._get_cache(file_path)

        if file_data is None:
            if file_path not in file_locks:
                file_locks[file_path] = Lock()

            with file_locks[file_path]:
                try:
                    data = self._load(file_path)
                except (FileNotFoundError, IsADirectoryError, IOError,
                        PermissionError, ValueError, json.JSONDecodeError,
                        pickle.UnpicklingError, UnicodeDecodeError):
                    pass
                else:

                    self._set_cache(file_path, data)
                    return data

            return default

        return file_data


    def dump(self, file_path: str, data: Any, as_thread: bool = False) -> bool:
        """
        Dumps the data to the file.

        Args:
            file_path (str): The path to the file to dump the data to.
            data (Any): The data to dump to the file.
            as_thread (bool, optional): Whether to dump the data as a thread. Defaults to False.
        
        Returns:
            bool: True if the data was dumped successfully, False otherwise.
        """

        if file_path not in file_locks:
            file_locks[file_path] = Lock()

        self._set_cache(file_path, data)

        try:
            if as_thread:
                WRITE_EXECUTOR.submit(self._dump, data, file_path)
            else:
                self._dump(data, file_path)
        except (FileNotFoundError, IsADirectoryError, IOError,
                PermissionError, ValueError, TypeError,
                pickle.PicklingError, OSError, RuntimeError):
            pass

        return True


class PICKLEFile(CachedFile):
    """
    A pickle file type with caching.
    """


    def _load(self, file_path: str) -> Any:
        """
        Loads the file.

        Args:
            file_path (str): The path to the file to load.

        Returns:
            Any: The loaded file.
        """

        with open(file_path, 'rb') as file:
            return pickle.load(file)


    def _dump(self, data: Any, file_path: str) -> None:
        """
        Writes the data to the file.

        Args:
            data (Any): The data to write to the file.
        
        Returns:
            bool: True if the file was written successfully, False otherwise.
        """

        with file_locks[file_path]:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)


PICKLE = PICKLEFile()


class Hashing:
    """
    Implementation for hashing
    """


    def __init__(self, salt: Optional[bytes] = None):
        """
        Args:
            salt (Optional[bytes]): The salt, makes the hashing process more secure. Default is None.
        """

        self.salt = salt


    def hash(self, plain_text: str, hash_length: int = 8) -> str:
        """
        Function to hash a plaintext.

        Args:
            plain_text (str): The text to be hashed.
            hash_length (int): The length of the returned hashed value. Default is 8.

        Returns:
            str: The hashed value along with the salt.
        """

        salt = self.salt
        if salt is None:
            salt = secrets.token_bytes(hash_length)

        hash_object = hashlib.sha256(salt + plain_text.encode()).digest()
        return hash_object + b'00' + salt


    def compare(self, plain_text: str, hash_string: str) -> bool:
        """
        Compares a plaintext with a hashed value.

        Args:
            plain_text (str): The text that was hashed.
            hash_string (str): The hashed value.

        Returns:
            bool: True if they match, False otherwise.
        """

        salt = self.salt
        if b'00' in hash_string:
            hash_string, salt = hash_string.split(b'00')

        hash_length = len(hash_string)

        comparison_hash = Hashing(salt=salt).hash(
            plain_text, hash_length=hash_length
        ).split(b'00')[0]

        return comparison_hash == hash_string


if __name__ == "__main__":
    print("common.py: This file is not designed to be executed.")
