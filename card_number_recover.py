import hashlib
import multiprocessing as mp
from typing import Callable


def recover_card_num(hash: str, last_symbols: str, bin: str, cores: int = mp.cpu_count(), progress_callback: Callable[[int], None] = None) -> str:
    """Function that tries to recover the card number using hash brute force

    Args:
        hash (str):
        last_symbols (str):
        bin (str):

    Returns:
        str: if the card number cannot be found, then an empty string will be returned, otherwise the card number will be returned
    """

    args = [(hash, f"{bin}{i}{last_symbols}") for i in range(100000, 1000000)]
    with mp.Pool(processes=cores) as p:
        results = p.starmap(check_hash, args)
        for index, result in enumerate(results):
            if progress_callback:
                progress_callback(index)
            if result:
                return args[index][1]
    return ""


def check_hash(hash: str, card_number: str) -> bool:
    """ompares the true hash with the hash that was obtained by hashing the card number

    Args:
        hash (str):
        card_number (str):

    Returns:
        bool: result of comparison of two hashes
    """
    return hashlib.sha384(card_number.encode()).hexdigest() == hash
