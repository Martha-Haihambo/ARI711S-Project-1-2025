from load import load_data, scientists, name_to_ids, papers
from search import shortest_path

DATASET_PATH = r"C:\Users\King Don\Desktop\Part 1\dataset"

print("Loading data...")
load_data(DATASET_PATH)
print("Data loaded.")

name1 = input("Enter first scientist's name: ").strip()
name2 = input("Enter second scientist's name: ").strip()

if name1 not in name_to_ids or name2 not in name_to_ids:
    print("Scientist(s) not found in database.")
else:
    source = next(iter(name_to_ids[name1]))
    target = next(iter(name_to_ids[name2]))

   
    path = shortest_path(source, target)

    if path:
        print(f"\n{len(path)} degrees of separation.")
        for i, (paper_id, scientist_id) in enumerate(path, start=1):
            scientist_name = scientists[scientist_id]["name"]
            paper_title = papers[paper_id]["title"]
            print(f"{i}: {scientists[source]['name']} and {scientist_name} co-authored \"{paper_title}\"")
            source = scientist_id 
    else:
        print("No connection found.")
