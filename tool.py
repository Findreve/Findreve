import hashlib
import binascii
import logging
from datetime import datetime, timezone
import os
import secrets

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

def generate_password(
    length: int = 8
    ) -> str:
    """
    生成指定长度的随机密码。
    
    :param length: 密码长度
    :type length: int
    :return: 随机密码
    :rtype: str
    """
    import secrets
    
    return secrets.token_hex(length)

def hash_password(
    password: str
    ) -> str:
    """
    生成密码的加盐哈希值。

    :param password: 需要哈希的原始密码
    :type password: str
    :return: 包含盐值和哈希值的字符串
    :rtype: str

    使用SHA-256和PBKDF2算法对密码进行加盐哈希,返回盐值和哈希值的组合。
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(
    stored_password: str, 
    provided_password: str, 
    debug: bool = False
    ) -> bool:
    """
    验证存储的密码哈希值与用户提供的密码是否匹配。

    :param stored_password: 存储的密码哈希值(包含盐值)
    :type stored_password: str
    :param provided_password: 用户提供的密码
    :type provided_password: str
    :param debug: 是否输出调试信息，将会输出原密码和哈希值
    :type debug: bool
    :return: 如果密码匹配返回True,否则返回False
    :rtype: bool

    从存储的密码哈希中提取盐值,使用相同的哈希算法验证用户提供的密码。
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    if debug:
        logging.info(f"原密码: {provided_password}, 哈希值: {pwdhash}, 存储哈希值: {stored_password}")
    return secrets.compare_digest(pwdhash, stored_password)

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