class Crc:

    def __xor1__(self, a, b):
        result = ""
        n = len(b)
        for i in range(1, n):
            if a[i] == b[i]:
                result += "0"
            else:
                result += "1"
        return result

    def __mod2div__(self, divident, divisor):
        pick = len(divisor)
        tmp = divident[:pick]
        n = len(divident)

        while pick < n:
            if tmp[0] == '1':
                tmp = self.__xor1__(divisor, tmp) + divident[pick]
            else:
                tmp = self.__xor1__('0' * pick, tmp) + divident[pick]
            pick += 1

        if tmp[0] == '1':
            tmp = self.__xor1__(divisor, tmp)
        else:
            tmp = self.__xor1__('0' * pick, tmp)

        return tmp

    def encodeData(self, data, key):
        l_key = len(key)
        appended_data = data + '0' * (l_key - 1)
        remainder = self.__mod2div__(appended_data, key)
        payload = data
        rem = remainder
        codeword = remainder
        return codeword
