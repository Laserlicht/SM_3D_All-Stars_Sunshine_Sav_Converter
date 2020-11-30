import binaryfile
import lz4.block
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="filename of the *.raw or *.sav file")
args = parser.parse_args()

#https://switchbrew.org/w/index.php?title=Super_Mario_3D_All-Stars&mobileaction=toggle_view_desktop#Savedata
def hagi_sav(b):
    b.byteorder = 'big'
    b.uint('len', 4)
    b.bytes('data', compressed_data_len)

if args.file.upper().endswith(".RAW") :
    data_decompressed = open(args.file, "rb").read()
    data_compressed = lz4.block.compress(data_decompressed, store_size=False)
    data = { }
    data["len"] = len(data_decompressed)
    data["data"] = data_compressed
    compressed_data_len = len(data_compressed)
    with open(args.file + ".sav", 'wb') as fh:
        binaryfile.write(fh, data, hagi_sav)
    print("Convert: RAW -> SAV: Success!")
elif args.file.upper().endswith(".SAV") :
    with open(args.file, 'rb') as fh:
        fh.seek(0,2)
        compressed_data_len = fh.tell() - 4
        fh.seek(0,0)

        data = binaryfile.read(fh, hagi_sav)
    data_decompressed = lz4.block.decompress(data.data, uncompressed_size=data.len)
    open(args.file + ".raw", 'wb').write(data_decompressed)
    print("Convert: SAV -> RAW: Success!")
else :
    print("Error: no filename!")
