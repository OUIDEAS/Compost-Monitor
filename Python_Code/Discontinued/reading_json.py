# import json
# import datetime

# startTime = datetime.datetime.now()
# with open("/home/dan/Desktop/Overall.json", "r", encoding = 'latin-1') as f:
#     data = json.load(f)
# endTime = datetime.datetime.now()
# totalTime = (endTime - startTime).total_seconds()
# print(totalTime)

# import json
# import datetime

# startTime = datetime.datetime.now()
# with open("/home/dan/Desktop/Overall.json", "r", encoding='latin-1') as f:
#     file_content = f.read()
#     objects = file_content.split('\n')
#     data = [json.loads(obj) for obj in objects if obj.strip()]
# endTime = datetime.datetime.now()
# totalTime = (endTime - startTime).total_seconds()
# print(totalTime)

# import ijson
# import datetime

# startTime = datetime.datetime.now()
# with open("/home/dan/Desktop/Overall.json", "r", encoding="latin-1") as f:
#     data = []
#     parser = ijson.parse(f)
#     for prefix, event, value in parser:
#         if event == 'end_map' and prefix == '':
#             data.append(value)
#     while True:
#         try:
#             next(parser)
#         except StopIteration:
#             break
# endTime = datetime.datetime.now()
# totalTime = (endTime - startTime).total_seconds()
# print(totalTime)

# import jsonlines
# import datetime

# startTime = datetime.datetime.now()
# data = []

# with jsonlines.open("/home/dan/Desktop/Overall.json", "r") as reader:
#     for obj in reader:
#         data.append(obj)

# endTime = datetime.datetime.now()
# totalTime = (endTime - startTime).total_seconds()
# print(totalTime)

# import jsonlines
# import datetime

# startTime = datetime.datetime.now()
# data = []
# batch_size = 1000  # Number of objects to process before dumping to a file
# output_file = "/home/dan/Desktop/processed_data.jsonl"

# def dump_data():
#     with jsonlines.open(output_file, "a") as writer:
#         writer.write_all(data)
#     data.clear()

# with jsonlines.open("/home/dan/Desktop/Overall.json", "r", encoding = 'latin-1') as reader:
#     for i, obj in enumerate(reader):
#         data.append(obj)
#         if i > 0 and i % batch_size == 0:
#             dump_data()

# # Dump any remaining data after processing
# if data:
#     dump_data()

# endTime = datetime.datetime.now()
# totalTime = (endTime - startTime).total_seconds()
# print(totalTime)

# import jsonlines
# import datetime

# startTime = datetime.datetime.now()
# data = []
# batch_size = 1000  # Number of objects to process before dumping to a file
# output_file = "/home/dan/Desktop/processed_data.jsonl"

# def dump_data():
#     with jsonlines.open(output_file, "a") as writer:
#         writer.write_all(data)
#     data.clear()

# with open("/home/dan/Desktop/Overall.json", "r", encoding="latin-1") as file:
#     for i, line in enumerate(file):
#         obj = jsonlines.Reader().loads(line)
#         data.append(obj)
#         if i > 0 and i % batch_size == 0:
#             dump_data()

# # Dump any remaining data after processing
# if data:
#     dump_data()

# endTime = datetime.datetime.now()
# totalTime = (endTime - startTime).total_seconds()
# print(totalTime)

import jsonlines
import datetime
import codecs

startTime = datetime.datetime.now()
data = []
batch_size = 1000  # Number of objects to process before dumping to a file
output_file = "/home/dan/Desktop/processed_data.jsonl"

def dump_data():
    with jsonlines.open(output_file, "a") as writer:
        writer.write_all(data)
    data.clear()

with codecs.open("/home/dan/Desktop/Overall.json", "r", encoding="latin-1") as file:
    reader = jsonlines.Reader(file)
    for line in file:
        obj = reader._loads(line)
        data.append(obj)
        if len(data) >= batch_size:
            dump_data()

# Dump any remaining data after processing
if data:
    dump_data()

endTime = datetime.datetime.now()
totalTime = (endTime - startTime).total_seconds()
print(totalTime)
