import secrets
from loguru import logger
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ph = PasswordHasher()

class Password():

    @staticmethod
    def generate(
        length: int = 8
    ) -> str:
        """
        生成指定长度的随机密码。
        
        :param length: 密码长度
        :type length: int
        :return: 随机密码
        :rtype: str
        """
        return secrets.token_hex(length)

    @staticmethod
    def hash(
        password: str
    ) -> str:
        """
        使用 Argon2 生成密码的哈希值。

        返回的哈希字符串已经包含了所有需要验证的信息（盐、算法参数等）。

        :param password: 需要哈希的原始密码
        :return: Argon2 哈希字符串
        """
        return _ph.hash(password)

    @staticmethod
    def verify(
        stored_password: str,
        provided_password: str,
        debug: bool = False
    ) -> bool:
        """
        验证存储的 Argon2 哈希值与用户提供的密码是否匹配。

        :param stored_password: 数据库中存储的 Argon2 哈希字符串
        :param provided_password: 用户本次提供的密码
        :param debug: 是否输出调试信息
        :return: 如果密码匹配返回 True, 否则返回 False
        """
        if debug:
            logger.info(f"验证密码: (哈希) {stored_password}")

        try:
            # verify 函数会自动解析 stored_password 中的盐和参数
            _ph.verify(stored_password, provided_password)

            # 检查哈希参数是否已过时。如果返回True，
            # 意味着你应该使用新的参数重新哈希密码并更新存储。
            # 这是一个很好的实践，可以随着时间推移增强安全性。
            if _ph.check_needs_rehash(stored_password):
                logger.warning("密码哈希参数已过时，建议重新哈希并更新。")

            return True
        except VerifyMismatchError:
            # 这是预期的异常，当密码不匹配时触发。
            if debug:
                logger.info("密码不匹配")
            return False
        except Exception as e:
            # 捕获其他可能的错误
            logger.error(f"密码验证过程中发生未知错误: {e}")
            return False