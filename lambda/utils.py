from variables import targets

def find_target(score: str, darts: int) -> str:
    return targets.get(score, ['Treble Twenty']*3)[darts-1]
