from datetime import datetime, timezone

def format_phone(
    phone: str, 
    groups: list[int] | None = None, 
    separator: str = " ", 
    private: bool = False
    ) -> str:
    """
    格式化中国大陆的11位手机号

    :param phone: 手机号
    :param groups: 分组长度列表
    :param separator: 分隔符
    :param private: 是否隐藏前七位

    :return: 格式化后的手机号
    """
    if groups is None:
        groups = [3, 4, 4]
        
    result = []
    start = 0
    for i, length in enumerate(groups):
        segment = phone[start:start + length]
        # 如果是private模式，将前两组（前7位）替换为星号
        if private and i < 2:
            segment = "*" * length
        result.append(segment)
        start += length
        
    return separator.join(result)

def format_time_diff(
    target_time: datetime | str
    ) -> str:
    """
    计算目标时间与当前时间的差值，返回易读的中文描述
    
    Args:
        target_time: 目标时间，可以是datetime对象或时间字符串
        
    Returns:
        str: 格式化的时间差描述，如"一年前"、"3个月前"等
    """
    # 如果输入是字符串，先转换为datetime对象
    if isinstance(target_time, str):
        try:
            target_time = datetime.fromisoformat(target_time)
        except ValueError:
            return "时间格式错误"
    
    now = datetime.now(timezone.utc)
    target_time = target_time.astimezone(timezone.utc)
    diff = now - target_time
    
    # 如果是未来时间
    if diff.total_seconds() < 0:
        diff = -diff
        suffix = "后"
    else:
        suffix = "前"
        
    seconds = diff.total_seconds()
    
    # 定义时间间隔
    intervals = [
        (31536000, " 年"),
        (2592000, " 个月"),
        (86400, " 天"),
        (3600, " 小时"),
        (60, " 分钟"),
        (1, " 秒")
    ]
    
    # 计算最适合的时间单位
    for seconds_in_unit, unit in intervals:
        if seconds >= seconds_in_unit:
            value = int(seconds / seconds_in_unit)
            if unit == "个月" and value >= 12:  # 超过12个月显示为年
                continue
            return f"{value}{unit}{suffix}"
            
    return f"刚刚"

if __name__ == "__main__":
    print(format_phone("18888888888", private=True))
    print(format_phone("18888888888", private=False))