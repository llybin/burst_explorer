def calc_block_reward(height: int) -> int:
    month = int(height / 10800)
    return int(pow(0.95, month) * 10000)
