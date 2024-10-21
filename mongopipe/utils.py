def compare_entries(source_collection, dest_collection, entry_id):
    old_entry = source_collection.find_one({"id": entry_id})
    new_entry = dest_collection.find_one({"id": entry_id})
    
    if not old_entry or not new_entry:
        print(f"Entry with id {entry_id} not found in one or both collections.")
        return

    print(f"Comparing entries with ID: {entry_id}")
    print("Old entry:")
    print(old_entry)
    print("\nNew entry:")
    print(new_entry)
    print("\nDifferences:")
    
    for key in set(old_entry.keys()) | set(new_entry.keys()):
        if key not in old_entry:
            print(f"Added {key}: {new_entry[key]}")
        elif key not in new_entry:
            print(f"Removed {key}: {old_entry[key]}")
        elif old_entry[key] != new_entry[key]:
            print(f"Changed {key}:")
            print(f"  From: {old_entry[key]}")
            print(f"  To:   {new_entry[key]}")