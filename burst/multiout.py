import sys
import logging
import struct


class UnpackError(Exception):
    pass


class MultiOutPack(object):
    @staticmethod
    def _unpack_header(data: bytes) -> (int, int):
        headers = struct.unpack("2c", data)

        version = int.from_bytes(headers[0], byteorder=sys.byteorder)
        if version != 1:
            logging.warning("Unknown multiout version: %d, data: %r", version, data)
            raise UnpackError

        nums = int.from_bytes(headers[1], byteorder=sys.byteorder)

        return version, nums

    def unpack_header(self, data: bytes) -> (int, int):
        return self._unpack_header(data[:2])

    def unpack_multi_out(self, data: bytes) -> [int]:
        try:
            version, nums = self._unpack_header(data[:2])
            return struct.unpack("{}P".format(2 * nums), data[2:])
        except struct.error:
            logging.error("Unpack error: %r", data)
            raise UnpackError

    def unpack_multi_out_same(self, data: bytes) -> [int]:
        try:
            version, nums = self._unpack_header(data[:2])
            return struct.unpack("{}P".format(nums), data[2:])
        except struct.error:
            logging.error("Unpack error: %r", data)
            raise UnpackError
