import base64
import binascii
import hashlib
import time


def aid_random_md5(buffer):
    return hashlib.md5(buffer).digest()


def ror(x, v):
    a = (x << (64 - v)) | (x >> v)
    return a & 0xffffffffffffffff


def ror_plus(v, shift, x9):
    a = (x9 << (64 - shift)) | (x9 >> shift)
    return (a ^ v) & 0xffffffffffffffff


def validate(num):
    return num & 0xffffffffffffffff


def ladon_calc_1(x8, x9, x22):
    x8 = ror(x8, 0x4)
    x8 = (x8 - x9) ^ x22
    res_1 = x8
    res_2 = ror_plus(x8, 49, x9)
    return res_1, res_2


class XLadon:

    def __init__(self, xk, aid):
        self.make_sig(xk, aid)

    def ladon_2(self, md5_1):
        ror_3d = self.x_2
        x9 = ror(self.r_2, 0x8)
        x8_x9 = ror_3d - x9
        reset_value = x8_x9 ^ md5_1
        for l_value in self.l_value_list:
            ror_x9 = validate(ror(ror_3d, 0x3f))
            ror_3d = validate(reset_value ^ ror_x9)
            x8_ror = validate(ror(reset_value, 0x9))
            and_res = validate(x8_ror + ror_3d)
            reset_value = validate(and_res * l_value)
        x_ladon4 = reset_value
        x_ladon3_ror_3d = validate(ror(ror_3d, 0x3d))
        xladon_3 = validate(x_ladon4 ^ x_ladon3_ror_3d)
        return xladon_3, x_ladon4

    def ladon_1(self, md5_1):
        ror_3d = self.x_1
        x9 = ror(self.r_1, 0x8)  
        x8_x9 = ror_3d + x9
        reset_value = x8_x9 ^ md5_1
        for l_value in self.l_value_list:
            ror_x9 = validate(ror(ror_3d, 0x3f))
            ror_3d = validate(reset_value ^ ror_x9)
            x8_ror = validate(ror(reset_value, 0x4))
            and_res = validate(x8_ror - ror_3d)
            reset_value = validate(and_res ^ l_value)
        x_ladon4 = reset_value
        x_ladon3_ror_3d = validate(ror(ror_3d, 0x3c))
        xladon_3 = validate(x_ladon4 * x_ladon3_ror_3d)
        return xladon_3, x_ladon4

    def make_value_list(self, md5_value):

        a = binascii.hexlify(md5_value[0:4])
        md5_1 = int.from_bytes(a, byteorder='little')
        a = binascii.hexlify(md5_value[4:8])
        md5_2 = int.from_bytes(a, byteorder='little')
        a = binascii.hexlify(md5_value[8:12])
        md5_3 = int.from_bytes(a, byteorder='little')
        a = binascii.hexlify(md5_value[12:16])
        md5_4 = int.from_bytes(a, byteorder='little')
        r0_list = [md5_2, md5_3, md5_4]
        l0_list = [md5_1]
        for i in range(0, 33):
            r_value, l_vaue = ladon_calc_1(r0_list[i], l0_list[i], i)
            l0_list.append(validate(l_vaue))
            r0_list.append(validate(r_value))

        self.l_value_list = l0_list[1:]

    def make_sig(self, x_khons, aid="1128"):
        signature_string = f"{x_khons}-1588093228-{aid}"
        fill_number = 32 - len(list(signature_string.encode()))

        buffer_list = list(signature_string.encode())
        for i in range(fill_number):
            buffer_list.append(fill_number)
        full_buffer = bytearray(buffer_list)
        self.x_1 = int.from_bytes(full_buffer[0:4], byteorder='little')
        self.r_1 = int.from_bytes(full_buffer[8:9], byteorder='little')
        self.x_2 = int.from_bytes(full_buffer[16:24], byteorder='little')
        self.r_2 = int.from_bytes(full_buffer[24:32], byteorder='little')


if __name__ == "__main__":
    x_khons = str(int(time.time()))
    aid = "1233"
    xladon = XLadon(x_khons, aid)
    random_bytes = bytes.fromhex("69 ef fb 61")
    md5_value = aid_random_md5(random_bytes + aid.encode())
    a = binascii.hexlify(md5_value[0:4])
    md5_1 = int.from_bytes(a, byteorder='little')
    xladon.make_value_list(md5_value)

    x_ladon1, x_ladon2 = xladon.ladon_1(md5_1)
    x_ladon3, x_ladon4 = xladon.ladon_2(md5_1)
    buffer = random_bytes + x_ladon1.to_bytes(length=8, byteorder='little') + x_ladon2.to_bytes(length=8, byteorder='little') + x_ladon3.to_bytes(length=8, byteorder='little') + x_ladon4.to_bytes(length=8, byteorder='little')
    res = base64.b64encode(buffer).decode()

    print(res)
