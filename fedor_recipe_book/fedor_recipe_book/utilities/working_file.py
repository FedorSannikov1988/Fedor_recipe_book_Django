"""
This module is responsible for working with files inside the application.
"""
from pathlib import Path


class WorkingWithFiles:
    """
    Class for working with files.

    Attributes:
    - path_to_file: Path - the path to the file

    Methods:
    - __init__(self, path_to_file: Path) - constructor method to initialize the path to the file
    - delete_file(self) -> None - method to delete the file
    - generating_path_file_in_folder__user_photos(name_file: str) -> Path - static method to generate
    the path to a file in the 'user_photos' folder
    Example usage:
    file = WorkingWithFiles(Path('path/to/file.txt'))
    file.delete_file()
    path = WorkingWithFiles.generating_path_file_in_folder__user_photos('photo.jpg')
    """
    def __init__(self, path_to_file: Path | str):
        self.__path_to_file = path_to_file

    def delete_file(self) -> None:
        """
        Method to delete the file.

        Parameters:
        - None

        Returns:
        - None

        Description:
        This method checks if the file exists and deletes it if it does.
        """
        file_path = Path(self.__path_to_file)

        if file_path.exists():
            file_path.unlink()
