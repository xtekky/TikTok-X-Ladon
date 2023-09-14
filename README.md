# X-Ladon HTTP Signature (TikTok)

TikTok uses a specific HTTP signature called the X-Ladon. The app's requests to servers have a Ladon signature in their headers. This signature is typically used by the app to ensure the security and integrity of data.

## Introduction

The presented Python script provides the functionality for encrypting TikTok's X-Ladon HTTP signature. The script includes functions for generating a hash table, padding the original data, and encoding the padded data using an internal encryption algorithm, and finally, a Base64-encoded string is returned which forms the X-Ladon HTTP Signature.

## Ladon Encryption Explained

The main function for creating the encryption is `ladon_encrypt`. It accepts three parameters: `khronos`, `lc_id`, and `aid`.

- `khronos` is the current Unix timestamp
- `lc_id` is the client id of a specific application 
- `aid` derives from the TikTok site itself

```python
def ladon_encrypt(khronos: int, lc_id: int = 1611921764, aid: int = 1233) -> str:
    ...
```

The function begins by generating a string of data using these three input parameters, separated by a hyphen:

```python
data = f"{khronos}-{lc_id}-{aid}"
```

The function next creates `keygen` by adding `aid` to a randomly generated 4 bytes string. It then calculates `md5hex`, which is the MD5 hash of the `keygen`.

```python
keygen = urandom(4) + str(aid).encode()
md5hex = md5bytes(keygen)
```
After creating the hash table, the function will apply the PKCS7 padding to the data string to ensure that its length is a multiple of 16 bytes. The padding is performed to align the data to the desired block size and to ensure uniformed data chunks for encryption.

```python
new_size = padding_size(size)
input = bytearray(new_size)
input[:size] = data
pkcs7_padding_pad_buffer(input, size, new_size, 16)
```
Then, the script passes the hash table and the padded input data to the `encrypt_ladon` function. This function generates the encrypted data using a shift-then-xor operation, mimicking a bit rotation operation.

```python
output = encrypt_ladon(md5hex.encode(), data.encode(), size)
```
All output data and random 4 bytes string at the beginning are then Base64-encoded. The result is a string that's ready for inclusion in the header of a TikTok HTTP request:

```python
return base64.b64encode(output).decode()
```

## X-Ladon HTTP Signatures
HTTP signatures are an important security measure commonly used in web applications. By adding an X-Ladon signature to an HTTP header, TikTok helps secure the data and verify the integrity of requests and responses. The hashing mechanism ensures that even a minor change in the request results in a different signature, aiding in the identification of any unauthorized modifications.

## Conclusion
Secure data transmission is a crucial aspect of any application that communicates via HTTP. TikTok uses the X-Ladon HTTP signature as a method of ensuring data integrity during transmission. The Python script provided in this guide decrypts this HTTP signature, providing insights into its inner workings. It showcases how padding, hashing, and bit rotation operations are employed to encrypt the data.
