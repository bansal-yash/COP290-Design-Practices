import shutil
import time
import os

def compress(sym):

    formats = [".txt", ".csv", ".xlsx", ".feather", ".h5", ".json", ".html", ".parquet", ".pkl", ".xml", ".md", ".sql", ".dta"]

    compression_time_dict = {}
    decompression_time_dict = {}
    compressed_size_dict = {}

    for i in formats:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_to_compress = sym + i
        compressed_file_name = f"{file_to_compress}"
        t1 = time.time()
        shutil.make_archive(compressed_file_name, "zip", ".", file_to_compress)
        t2 = time.time()
        compression_time_dict[i] = round((t2-t1)*1000, 3)

        file_path = os.path.join(os.path.dirname(__file__), file_to_compress + ".zip")
        size_bytes = os.path.getsize(file_path)
        compressed_size_dict[i] = round(size_bytes/1024, 3)
        compressed_file_name = file_to_compress + ".zip"
        output_folder = os.path.join(script_directory, "decompressed_folder")
        t1 = time.time()
        shutil.unpack_archive(compressed_file_name, output_folder)
        t2 = time.time()
        decompression_time_dict[i] = round((t2-t1)*1000, 3)

        compress_folder = os.path.join(script_directory, "compressed_folder")
        if not os.path.exists(compress_folder):
            os.makedirs(compress_folder)
        shutil.move(file_path, compress_folder)

    return compression_time_dict, decompression_time_dict, compressed_size_dict