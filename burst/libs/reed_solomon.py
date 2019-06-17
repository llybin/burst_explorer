""" Reed Solomon Encoding and Decoding for Burst
Ported from BRS by Lev Lybin
Licensed under GPLv3 ported from
https://github.com/burst-apps-team/burstcoin/blob/master/src/brs/crypto/ReedSolomon.java
"""

gf_exp = (1, 2, 4, 8, 16, 5, 10, 20, 13, 26, 17, 7, 14, 28, 29, 31, 27,
          19, 3, 6, 12, 24, 21, 15, 30, 25, 23, 11, 22, 9, 18, 1)
gf_log = (0, 0, 1, 18, 2, 5, 19, 11, 3, 29, 6, 27, 20, 8, 12, 23, 4, 10,
          30, 17, 7, 22, 28, 26, 21, 25, 9, 16, 13, 14, 24, 15)
initial_codeword = (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
codeword_map = (3, 2, 1, 0, 7, 6, 5, 4, 13, 14, 15, 16, 12, 8, 9, 10, 11)
alphabet = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

initial_codeword_length = len(initial_codeword)
alphabet_length = len(alphabet)

cypher_string_length = 17

base_32_length = 13
base_10_length = 20


class ReedSolomonError(Exception):
    pass


class ReedSolomon:
    @staticmethod
    def gf_mul(a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0

        idx = (gf_log[a] + gf_log[b]) % 31

        return gf_exp[idx]

    def encode(self, plain: str) -> str:
        """
        :param plain: The numeric ID of the account
        :return: The RS encoding of the ID in the form XXXX-XXXX-XXXX-XXXXX
        """
        plain_string = bytearray(plain, "utf-8")
        length = len(plain_string)
        if length > base_10_length or length == 0:
            raise ReedSolomonError

        plain_string_10 = bytearray(base_10_length)
        for x in range(length):
            b = plain_string[x] - ord("0")
            if 0 > b < 256:
                raise ReedSolomonError
            plain_string_10[x] = b

        codeword = bytearray(initial_codeword_length)

        codeword_length = 0
        while length > 0:
            new_length = 0
            digit_32 = 0

            for x in range(length):
                digit_32 = digit_32 * 10 + plain_string_10[x]
                if digit_32 >= 32:
                    plain_string_10[new_length] = digit_32 >> 5
                    digit_32 &= 31
                    new_length += 1
                elif new_length > 0:
                    plain_string_10[new_length] = 0
                    new_length += 1

            length = new_length
            codeword[codeword_length] = digit_32
            codeword_length += 1

        p = bytearray(4)

        for x in range(base_32_length - 1, -1, -1):
            fb = codeword[x] ^ p[3]
            p[3] = p[2] ^ self.gf_mul(30, fb)
            p[2] = p[1] ^ self.gf_mul(6, fb)
            p[1] = p[0] ^ self.gf_mul(9, fb)
            p[0] = self.gf_mul(17, fb)

        # len(initial_codeword) - base_32_length == 17 - 13 == 4
        for x in range(4):
            codeword[x + base_32_length] = p[x]

        cypher_string_builder = ""

        for x in range(cypher_string_length):
            codework_index = codeword_map[x]
            alphabet_index = codeword[codework_index]
            cypher_string_builder += alphabet[alphabet_index]

            if (x & 3) == 3 and x < 13:
                cypher_string_builder += "-"

        return cypher_string_builder

    def decode(self, cypher_string: str) -> str:
        """
        :param cypher_string: The RS encoded address in the form BURST-XXXX-XXXX-XXXX-XXXXX
        :return: The numeric ID of the account
        """
        if cypher_string[:6] == "BURST-":
            cypher_string = cypher_string[6:]

        cypher_string = cypher_string.replace("-", "")

        if len(cypher_string) != cypher_string_length:
            raise ReedSolomonError

        codeword = bytearray(initial_codeword)

        codeword_length = 0
        for x in range(cypher_string_length):
            if cypher_string[x] not in alphabet:
                raise ReedSolomonError
            position_in_alphabet = alphabet.index(cypher_string[x])

            if position_in_alphabet <= -1 or position_in_alphabet > alphabet_length:
                continue

            if codeword_length > 16:
                raise ReedSolomonError("Codeword too long")

            codework_index = codeword_map[codeword_length]
            codeword[codework_index] = position_in_alphabet
            codeword_length += 1

        if codeword_length != 17 or not self.is_codeword_valid(codeword):
            raise ReedSolomonError("Codeword invalid")

        length = base_32_length
        cypher_string_32 = bytearray(length)
        for x in range(length):
            cypher_string_32[x] = codeword[length - x - 1]

        plain_string_builder = bytearray()

        while length > 0:
            new_length = 0
            digit_10 = 0

            for x in range(length):
                digit_10 = digit_10 * 32 + cypher_string_32[x]

                if digit_10 >= 10:
                    cypher_string_32[new_length] = digit_10 // 10
                    digit_10 %= 10
                    new_length += 1
                elif new_length > 0:
                    cypher_string_32[new_length] = 0
                    new_length += 1

            length = new_length
            plain_string_builder.append(digit_10 + ord("0"))

        return plain_string_builder[::-1].decode()

    def is_codeword_valid(self, codeword: bytearray) -> bool:
        c_sum = 0

        for i in range(1, 5):
            t = 0

            for j in range(0, 31):
                if 12 < j < 27:
                    continue

                pos = j
                if j > 26:
                    pos -= 14

                t ^= self.gf_mul(codeword[pos], gf_exp[(i * j) % 31])

            c_sum |= t

        return c_sum == 0
