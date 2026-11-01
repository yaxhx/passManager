import secrets
from constants import(
    DEFAULT_GENERATED_PASSWORD_LEN,
    DIGITS,
    LOWERCASE_LETTERS,
    MINIMUN_GENERATED_PASSWORD_LEN,
    SAFE_SYMBOLS,
    UPPERCASE_LETTERS
)


class passwordTooShortError(ValueError):
    ()
    
def generate_pass(
    length: int = DEFAULT_GENERATED_PASSWORD_LEN,
    *,
    use_lowercase: bool = True,
    user_uppercase: bool = True,
    use_digits: bool = True,
    use_syms: bool = True,
) -> str:
    if length < MINIMUN_GENERATED_PASSWORD_LEN:
        raise passwordTooShortError(
            f"Password length must be >= "
            f"{MINIMUN_GENERATED_PASSWORD_LEN}, got {len}"
        )
        
    enabled_pools = {
        "lower": LOWERCASE_LETTERS if use_lowercase else "",
        "upper": UPPERCASE_LETTERS if user_uppercase else "",
        "digit": DIGITS if use_digits else "",
        "symbol": SAFE_SYMBOLS if use_syms else "",
    }
    
    enabled_pools = {k: v for k, v in enabled_pools.items() if v}
    
    if not enabled_pools:
        raise ValueError("At least one character pool must be enabled")
    
    if length < len(enabled_pools):
        raise passwordTooShortError(
            f"length={length} is too small to include one character "
            f"from each of {len(enabled_pools)} enabled pools" 
        )
        
    alphabet = "".join(enabled_pools.values())
    
    
    required = [secrets.choice(pool) for pool in enabled_pools.values()]
    
    fill_count = length - len(required)
    fill = [secrets.choice(alphabet) for _ in range(fill_count)]
    
    chars = required + fill
    _secure_shuffle(chars)
    
    
    return "".join(chars)


def _secure_shuffle(items: list[str]) -> None:
    for i in range(len(items) - 1,0,-1):
        j = secrets.randbelow(i+1)
        items[i], items[j] = items[j], items[i]
        