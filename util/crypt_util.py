#!/usr/bin/env python
# -*- coding:utf8 -*-
import hashlib


class Crypt(object):
    @staticmethod
    def generate_password_hash(password):
        """
            256Hash加密
        :param password:
        :return:
        """
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        res = sha256.hexdigest()
        return res

    @staticmethod
    def check_password_hash(password_hash, password):
        """
            验证密码Hash
        :param password_hash:
        :param password:
        :return:
        """
        return password_hash == Crypt.generate_password_hash(password)


if __name__ == '__main__':
    pwd_hash = Crypt.generate_password_hash('12345678')
    print(pwd_hash)
