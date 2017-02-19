intab = "0123456789abcdef"
outtab = "fghijklmnopqrstu"
trantab = str.maketrans(outtab, intab)

final_out = 'lklgmolnlnmplplrlsmlifififififif'
final_out = final_out.translate(trantab)
print(final_out)
print(bytearray.fromhex(final_out).decode())
