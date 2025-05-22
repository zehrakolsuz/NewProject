# MFT Parser with Python by Zehra Kolsuz
# Bu script, NTFS dosya sisteminin Master File Table (MFT)'sini ayrıştırır.

def parse_mft(file_path):
    with open(file_path, 'rb') as f:
        mft_data = f.read()

    mft_entries = []
    offset = 0
    while offset < len(mft_data):
        entry = parse_mft_entry(mft_data[offset:offset+1024])
        if entry:
            mft_entries.append(entry)
        offset += 1024

    return mft_entries

def parse_mft_entry(entry_data):
    pass

if __name__ == "__main__":
    pass
