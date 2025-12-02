from reedsolo import RSCodec
import random

n = 16
message = "Vladyslav"
msgBytes = bytearray(message, 'utf-8')

k = len(msgBytes)

t = (n - k) // 2

rs = RSCodec(n - k)

print(f"Your original message: '{message}'")
print(f"Your original message length k: {k}")
print(f"Can correct up to t: {t} errors")

encodedmsg = rs.encode(msgBytes)
print(f"Encoded Message: {list(encodedmsg)}")

positions = random.sample(range(n), t)
values = [random.randint(1, 255) for _ in range(t)]

corruptedmsg = bytearray(encodedmsg)
for p, v in zip(positions, values):
    corruptedmsg[p] ^= v


print(f"Corrupted Message: {list(corruptedmsg)}")
print(f"Positions of mistakes: {positions}")
print(f"Values if mistakes: {values}")

try:
    decodedmsg = rs.decode(corruptedmsg)[0]
    decodedtxt = decodedmsg.decode('utf-8')

    print(f"Restored message: '{decodedtxt}'")

    if decodedtxt == message:
        print("\nYour message has been successfully recovered!")
    else:
        print("\nCouldn't recover your message")

except Exception as e:
    print(f"\nAn error occurred during decoding: {e}")
    print("Couldn't recover your message (too many errors or other issue).")