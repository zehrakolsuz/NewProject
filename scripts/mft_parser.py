# MFT Parser with Python by Zehra Kolsuz
# Bu script, NTFS dosya sisteminin Master File Table (MFT)'sini ayrıştırır.
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to sanitize file paths
def sanitize_path(path):
    return os.path.abspath(os.path.normpath(path))

# Use sanitized path in parse_mft function
def parse_mft(file_path):
    file_path = sanitize_path(file_path)
    try:
        with open(file_path, 'rb') as f:
            mft_data = f.read()
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

    mft_entries = []
    offset = 0
    while offset < len(mft_data):
        try:
            entry = parse_mft_entry(mft_data[offset:offset+1024])
            if entry:
                mft_entries.append(entry)
        except Exception as e:
            logging.error(f"Error parsing MFT entry at offset {offset}: {e}")
        offset += 1024

    return mft_entries
    
def parse_mft(file_path):
    try:
        with open(file_path, 'rb') as f:
            mft_data = f.read()
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

    mft_entries = []
    offset = 0
    while offset < len(mft_data):
        try:
            entry = parse_mft_entry(mft_data[offset:offset+1024])
            if entry:
                mft_entries.append(entry)
        except Exception as e:
        logging.error(f"Error parsing MFT entry at offset {offset}: {e}")
        offset += 1024

    return mft_entries

def parse_mft_entry(entry_data):
    try:
        if len(entry_data) < 48:
            return None

        signature = entry_data[:4].decode('utf-8')
        if signature != 'FILE':
            return None

    # Parse the MFT entry
    fixup_offset, fixup_size = struct.unpack_from('<HH', entry_data, 4)
    if fixup_size > 0:
        fixup_array = entry_data[fixup_offset:fixup_offset+fixup_size*2]
        for i in range(0, len(fixup_array), 2):
            if entry_data[512+i] != fixup_array[i] or entry_data[512+i+1] != fixup_array[i+1]:
                logging.error(f"Fixup check failed at offset {512+i}")
                return None
    lsn = struct.unpack_from('<Q', entry_data, 8)[0]
    sequence_value = struct.unpack_from('<H', entry_data, 16)[0]
    hard_link_count = struct.unpack_from('<H', entry_data, 18)[0]
    first_attribute_offset = struct.unpack_from('<H', entry_data, 20)[0]
    flags = struct.unpack_from('<H', entry_data, 22)[0]
    used_size = struct.unpack_from('<I', entry_data, 24)[0]
    allocated_size = struct.unpack_from('<I', entry_data, 28)[0]
    base_record_reference = struct.unpack_from('<Q', entry_data, 32)[0]
    next_attribute_id = struct.unpack_from('<H', entry_data, 40)[0]
    mft_record_number = struct.unpack_from('<Q', entry_data, 48)[0]

    # Parse attributes
        attributes = []
        offset = first_attribute_offset
        while offset < used_size:
            try:
                attribute_type = struct.unpack_from('<I', entry_data, offset)[0]
                attribute_length = struct.unpack_from('<I', entry_data, offset+4)[0]
                if attribute_length == 0:
                    logging.error(f"Invalid attribute length at offset {offset}")
                    break
                if offset + attribute_length > used_size:
                    logging.error(f"Attribute length exceeds used size at offset {offset}")
                    break
                attribute = parse_attribute(entry_data[offset:offset+attribute_length])
                if attribute:
                    attributes.append(attribute)
            except Exception as e:
                logging.error(f"Error parsing attribute at offset {offset}: {e}")
            offset += attribute_length

    return {
            'signature': signature,
            'sequence_value': sequence_value,
            'hard_link_count': hard_link_count,
            'flags': flags,
            'used_size': used_size,
            'allocated_size': allocated_size,
            'mft_record_number': mft_record_number,
            'attributes': attributes
        }
    except Exception as e:
        logging.error(f"Error parsing MFT entry: {e}")
        return None

def parse_attribute(attribute_data):
    attribute_type = struct.unpack_from('<I', attribute_data, 0)[0]
    attribute_length = struct.unpack_from('<I', attribute_data, 4)[0]
    attribute_type_name = get_attribute_type_name(attribute_type)

    return {
        'type': attribute_type_name,
        'length': attribute_length
    }

def get_attribute_type_name(attribute_type):
    attribute_types = {
        0x10: '$STANDARD_INFORMATION',
        0x20: '$ATTRIBUTE_LIST',
        0x30: '$FILE_NAME',
        0x40: '$OBJECT_ID',
        0x50: '$SECURITY_DESCRIPTOR',
        0x60: '$VOLUME_NAME',
        0x70: '$VOLUME_INFORMATION',
        0x80: '$DATA',
        0x90: '$INDEX_ROOT',
        0xA0: '$INDEX_ALLOCATION',
        0xB0: '$BITMAP',
        0xC0: '$REPARSE_POINT',
        0xD0: '$EA_INFORMATION',
        0xE0: '$EA',
        0xF0: '$PROPERTY_SET',
        0x100: '$LOGGED_UTILITY_STREAM'
    }
    return attribute_types.get(attribute_type, 'UNKNOWN')

def parse_standard_information(attribute_data):
    creation_time = struct.unpack_from('<Q', attribute_data, 24)[0]
    modification_time = struct.unpack_from('<Q', attribute_data, 32)[0]
    mft_modification_time = struct.unpack_from('<Q', attribute_data, 40)[0]
    access_time = struct.unpack_from('<Q', attribute_data, 48)[0]

    return {
        'type': '$STANDARD_INFORMATION',
        'creation_time': convert_windows_time(creation_time),
        'modification_time': convert_windows_time(modification_time),
        'mft_modification_time': convert_windows_time(mft_modification_time),
        'access_time': convert_windows_time(access_time)
    }

def parse_file_name(attribute_data):
    parent_directory = struct.unpack_from('<Q', attribute_data, 24)[0]
    creation_time = struct.unpack_from('<Q', attribute_data, 32)[0]
    modification_time = struct.unpack_from('<Q', attribute_data, 40)[0]
    mft_modification_time = struct.unpack_from('<Q', attribute_data, 48)[0]
    access_time = struct.unpack_from('<Q', attribute_data, 56)[0]
    allocated_size = struct.unpack_from('<Q', attribute_data, 64)[0]
    real_size = struct.unpack_from('<Q', attribute_data, 72)[0]
    file_flags = struct.unpack_from('<I', attribute_data, 80)[0]
    name_length = struct.unpack_from('<B', attribute_data, 84)[0]
    name_type = struct.unpack_from('<B', attribute_data, 85)[0]
    file_name = attribute_data[86:86+name_length*2].decode('utf-16le')

    return {
        'type': '$FILE_NAME',
        'parent_directory': parent_directory,
        'creation_time': convert_windows_time(creation_time),
        'modification_time': convert_windows_time(modification_time),
        'mft_modification_time': convert_windows_time(mft_modification_time),
        'access_time': convert_windows_time(access_time),
        'allocated_size': allocated_size,
        'real_size': real_size,
        'file_flags': file_flags,
        'name_length': name_length,
        'name_type': name_type,
        'file_name': file_name
    }

def convert_windows_time(windows_time):
    # Windows time is in 100-nanosecond intervals since January 1, 1601 (UTC)
    epoch = datetime.datetime(1601, 1, 1)
    return epoch + datetime.timedelta(microseconds=windows_time/10)

import unittest

class TestMFTParser(unittest.TestCase):
    def test_parse_mft_entry(self):
        # Sample MFT entry data
        entry_data = b'FILE' + b'\x00' * 44 + b'\x00' * 1024
        entry = parse_mft_entry(entry_data)
        self.assertIsNotNone(entry)
        self.assertEqual(entry['signature'], 'FILE')

    def test_parse_attribute(self):
        # Sample attribute data
        attribute_data = b'\x10\x00\x00\x00' + b'\x20\x00\x00\x00'  # $STANDARD_INFORMATION
        attribute = parse_attribute(attribute_data)
        self.assertEqual(attribute['type'], '$STANDARD_INFORMATION')
        self.assertEqual(attribute['length'], 32)

if __name__ == "__main__":
    pass
    unittest.main()
