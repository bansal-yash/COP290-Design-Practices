import time
import os

def generate(sym, df):
    time_dict = {}
    size_dict = {}

    # .txt format
    file_name = sym + ".txt"
    t1 = time.time()
    df.to_csv(file_name, sep = '\t', index = True)
    t2 = time.time()
    time_dict[".txt"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".txt"] = round(size_bytes/1024, 3)

    # .csv format
    file_name = sym + ".csv"
    t1 = time.time()
    df.to_csv(file_name, index = False)
    t2 = time.time()
    time_dict[".csv"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".csv"] = round(size_bytes/1024, 3)

    # excel format
    file_name = sym + ".xlsx"
    t1 = time.time()
    df.to_excel(file_name, index = True)
    t2 = time.time()
    time_dict[".xlsx"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".xlsx"] = round(size_bytes/1024, 3)

    # feather format
    file_name = sym + ".feather"
    t1 = time.time()
    df.to_feather(file_name)
    t2 = time.time()
    time_dict[".feather"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".feather"] = round(size_bytes/1024, 3)

    # HDF5 format
    file_name = sym + ".h5"
    t1 = time.time()
    df.to_hdf(file_name, key = 'data', mode = 'w')
    t2 = time.time()
    time_dict[".h5"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".h5"] = round(size_bytes/1024, 3)

    # .json format
    file_name = sym + ".json"
    t1 = time.time()
    df.to_json(file_name, orient = 'records', lines = True)
    t2 = time.time()
    time_dict[".json"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".json"] = round(size_bytes/1024, 3)

    # .html format
    file_name = sym + ".html"
    t1 = time.time()
    df.to_html(file_name, index = True)
    t2 = time.time()
    time_dict[".html"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".html"] = round(size_bytes/1024, 3)

    # parquet format
    file_name = sym + ".parquet"
    t1 = time.time()
    df.to_parquet(file_name, engine = 'pyarrow')
    t2 = time.time()
    time_dict[".parquet"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".parquet"] = round(size_bytes/1024, 3)

    # binary format
    file_name = sym + ".pkl"
    t1 = time.time()
    df.to_pickle(file_name)
    t2 = time.time()
    time_dict[".pkl"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".pkl"] = round(size_bytes/1024, 3)

    # xml format
    file_name = sym + ".xml"
    df = df.rename(columns={"NO OF TRADES": "NO_OF_TRADES"})
    t1 = time.time()
    df.to_xml(file_name, index = "True")
    t2 = time.time()
    df = df.rename(columns={"NO_OF_TRADES": "NO OF TRADES"})
    time_dict[".xml"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".xml"] = round(size_bytes/1024, 3)

    # markdown format
    file_name = sym + ".md"
    t1 = time.time()
    df.to_markdown(file_name)
    t2 = time.time()
    time_dict[".md"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".md"] = round(size_bytes/1024, 3)

    # sql format
    file_name = sym + ".sql"
    t1 = time.time()
    df.to_sql(name='your_table_name', con=f'sqlite:///{file_name}', index=False, if_exists='replace')
    t2 = time.time()
    time_dict[".sql"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".sql"] = round(size_bytes/1024, 3)

    # stata format
    file_name = sym + ".dta"
    df = df.rename(columns={"NO OF TRADES": "NO_OF_TRADES"})
    t1 = time.time()
    df.to_stata(file_name, write_index=False)
    t2 = time.time()
    df = df.rename(columns={"NO_OF_TRADES": "NO OF TRADES"})
    time_dict[".dta"] = round((t2-t1)*1000, 3)
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    size_bytes = os.path.getsize(file_path)
    size_dict[".dta"] = round(size_bytes/1024, 3)

    return time_dict, size_dict