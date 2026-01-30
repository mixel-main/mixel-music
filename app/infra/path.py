import re
from pathlib import Path


def _find_root(start: Path | None = None) -> Path:
    p = (start or Path(__file__)).resolve()
    for d in [p, *p.parents]:
        if (d / "pyproject.toml").exists() or (d / ".git").exists(): # DEV
            return d
    return Path.cwd().resolve()

ROOT_DIR: Path = _find_root()


def get_path(*args: str | Path, rel: bool = False, create_dir: bool = False) -> Path:
    """
    Abstracts a path-like object or string path and returns it as a path-like object.
    Optionally creates the directory if it doesn't exist.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to False.
        create_dir (bool, optional): Create the directory if it doesn't exist, defaults to False.
    """
    
    home = ROOT_DIR

    if create_dir:
        for arg in args: home = home / arg
        home.parent.mkdir(parents=True, exist_ok=True)
    else:
        for arg in args: home = home / arg
    
    return home.relative_to(ROOT_DIR) if rel else home


def str_path(*args: str | Path, rel: bool = True) -> str:
    """
    Abstracts a path-like object or string path and returns it as a string.

    Args:
        *args (str | Path, optional): Directory or filename.
        rel (bool, optional): Relative path, defaults to True.
    """

    home = ROOT_DIR

    for arg in args: home = home / arg
    if rel: home = home.relative_to(ROOT_DIR)

    return home.as_posix()


def get_filename(*args: str | Path) -> tuple[str, str, str]:
    home = ROOT_DIR

    for arg in args: home = home / arg
    name, stem, suffix = home.name, home.stem, home.suffix

    if not suffix.isascii():
        stem += suffix
        suffix = ''
    elif stem.startswith('.') and suffix == '':
        stem, suffix = '', stem

    return [name, stem, suffix.lower()]


def is_supported_file(path: str) -> bool:
    from tinytag import TinyTag

    if get_path(path).suffix in TinyTag.SUPPORTED_FILE_EXTENSIONS:
        return True
    else:
        return False


def is_excluded_file(name: str) -> bool:
    """
    Check if a file should be excluded based on its name.
    """

    patterns = [
        r'.*Small.*',
        r'.*Cache.*',
        r'.*[{].*',
        r'.*cache.*',
        r'^\.',
        r'.*~$',
    ]

    for pattern in patterns:
        if re.search(pattern, name, re.IGNORECASE):
            return True
        
    return False
