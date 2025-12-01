"""started with importing all built in python modules except for pony.orm"""

from pony.orm import *  # imported every class and module in pony.orm (Ref: https://docs.ponyorm.org/)
import xml.etree.ElementTree as ET  # (Ref: https://docs.python.org/3/library/xml.etree.elementtree.html)
import json  # (Ref: https://docs.python.org/3/library/json.html)
import csv  # (Ref: https://docs.python.org/3/library/csv.html)
import os  # (Ref: https://docs.python.org/3/library/os.html)

db = Database()  # (Ref: https://docs.ponyorm.org/database.html)
password = os.getenv("DB_PASSWORD", "usbw")

db.bind(
    provider='mysql',
    host='localhost', 
    user='root',
    passwd=password,
    db='laurel_etl', 
    port=3307
)

# creating a Customer entity with all fields as Optional strings
class Customer(db.Entity):
    firstName = Optional(str) 
    lastName = Optional(str)
    age = Optional(str, nullable=True)
    sex = Optional(str, nullable=True)
    vehicle_make = Optional(str, nullable=True)
    vehicle_model = Optional(str, nullable=True)
    vehicle_year = Optional(str, nullable=True)
    vehicle_type = Optional(str, nullable=True)
    iban = Optional(str, nullable=True)
    credit_card_number = Optional(str, nullable=True)
    address_city = Optional(str, nullable=True)
    address_postcode = Optional(str, nullable=True)
    retired = Optional(str, nullable=True)
    dependants = Optional(str, nullable=True)
    salary = Optional(str, nullable=True)
    pension = Optional(str, nullable=True)
    company = Optional(str, nullable=True)
    commute_distance = Optional(str, nullable=True)
    notes = Optional(LongStr)

db.generate_mapping(create_tables=True)  # (Ref: https://docs.ponyorm.org/api_reference.html#Database.generate_mapping)


csv_file = os.path.join('data_cetm50', 'user_data.csv')  # (Ref: https://docs.python.org/3/library/os.path.html)
csv_data = []

try:
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # (Ref: https://docs.python.org/3/library/csv.html#csv.DictReader)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() if value.strip() != '' else None
                           for key, value in row.items()}
            csv_data.append(cleaned_row)

    print(f"✅ Successfully loaded {len(csv_data)} records from CSV.")

except FileNotFoundError:
    print("❌ CSV file not found. Check your 'data_cetm50' folder path.")
except Exception as e:
    print(f"⚠️ Error reading CSV: {e}")


json_file = os.path.join('data_cetm50', 'user_data.json') 
json_data = []

try:
    with open(json_file, mode='r', encoding='utf-8') as file:
        data = json.load(file)  
        if isinstance(data, dict):
            data = [data]

        for record in data:
            cleaned_record = {key.strip(): str(value).strip() if value not in [None, ""] else None
                              for key, value in record.items()}
            json_data.append(cleaned_record)

    print(f"✅ Successfully loaded {len(json_data)} records from JSON.")

except FileNotFoundError:
    print("❌ JSON file not found. Check your 'data_cetm50' folder path.")
except json.JSONDecodeError:
    print("⚠️ Error decoding JSON. Make sure the file format is valid JSON.")
except Exception as e:
    print(f"⚠️ Unexpected error reading JSON: {e}")


xml_file = os.path.join('data_cetm50', 'user_data.xml')
xml_data = []

try:
    tree = ET.parse(xml_file)  # (Ref: https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.parse)
    root = tree.getroot()

    for user in root.findall('user'):  # (Ref: https://docs.python.org/3/library/xml.etree.elementtree.html#elementtree-element-findall)
        record = {key.strip(): value.strip() if value.strip() != '' else None
                  for key, value in user.attrib.items()}
        xml_data.append(record)

    print(f"✅ Successfully loaded {len(xml_data)} records from XML.")

except FileNotFoundError:
    print("❌ XML file not found. Check your 'data_cetm50' folder path.")
except ET.ParseError as e:
    print(f"⚠️ XML parsing error: {e}")
except Exception as e:
    print(f"⚠️ Unexpected error reading XML: {e}")


txt_file = os.path.join('data_cetm50', 'user_data.txt')
txt_data = []

try:
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

        content = content.replace('\r\n', '\n').replace('\r', '\n')
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        for line in lines:
            txt_data.append({"notes": line})

    print(f"✅ Successfully loaded {len(txt_data)} text lines from TXT file.")

except FileNotFoundError:
    print("❌ TXT file not found. Check your 'data_cetm50' folder path.")
except Exception as e:
    print(f"⚠️ Error reading TXT file: {e}")


def merge_records(base, new):  # (Ref: https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
    """Merge two records without overwriting existing valid values in base."""
    for k, v in new.items():
        if v in [None, '', 'N/A', 'NA', 'null', 'None']:
            continue
        base_val = base.get(k)
        if base_val in [None, '', 'N/A', 'NA', 'null', 'None']:
            base[k] = v
    return base


def normalize_key(first, last): 
    """Return a normalized key string for a name pair."""
    if not first or not last:
        return None
    f = ' '.join(first.split()).strip().lower()
    l = ' '.join(last.split()).strip().lower()
    return f"{f}_{l}"


def unify_records(csv_data, json_data, xml_data, txt_data):  # (Ref: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
    unified = {}

    def add_or_merge(first, last, record_dict):
        key = normalize_key(first, last)
        if key is None:
            return
        if key not in unified:
            unified[key] = {k: (v if v not in [None, ''] else None) for k, v in record_dict.items()}
        else:
            unified[key] = merge_records(unified[key], record_dict)

    # CSV entries
    for record in csv_data:
        first_name = record.get("First Name") or record.get("firstName") or record.get("first")
        last_name = record.get("Second Name") or record.get("lastName") or record.get("last") or record.get("Surname")
        csv_record = {
            "firstName": first_name,
            "lastName": last_name,
            "age": record.get("Age"),
            "sex": record.get("Sex"),
            "vehicle_make": record.get("Vehicle Make"),
            "vehicle_model": record.get("Vehicle Model"),
            "vehicle_year": record.get("Vehicle Year"),
            "vehicle_type": record.get("Vehicle Type")
        }
        add_or_merge(first_name, last_name, csv_record)

    # JSON entries
    for rec in json_data:
        first_name = rec.get("firstName") or rec.get("First Name") or rec.get("first")
        last_name = rec.get("lastName") or rec.get("Second Name") or rec.get("last") or rec.get("Surname")
        json_record = {
            "firstName": rec.get("firstName"),
            "lastName": rec.get("lastName"),
            "age": rec.get("age"),
            "iban": rec.get("iban"),
            "credit_card_number": rec.get("credit_card_number"),
            "credit_card_security_code": rec.get("credit_card_security_code"),
            "credit_card_start_date": rec.get("credit_card_start_date"),
            "credit_card_end_date": rec.get("credit_card_end_date"),
            "address_main": rec.get("address_main"),
            "address_city": rec.get("address_city"),
            "address_postcode": rec.get("address_postcode"),
        }
        add_or_merge(first_name, last_name, json_record)

    # XML entries
    for rec in xml_data:
        first_name = rec.get("firstName") or rec.get("First Name") or rec.get("first")
        last_name = rec.get("lastName") or rec.get("Second Name") or rec.get("last") or rec.get("Surname")
        xml_record = {
            "firstName": rec.get("firstName"),
            "lastName": rec.get("lastName"),
            "age": rec.get("age"),
            "sex": rec.get("sex"),
            "retired": rec.get("retired"),
            "dependants": rec.get("dependants"),
            "marital_status": rec.get("marital_status"),
            "salary": rec.get("salary"),
            "pension": rec.get("pension"),
            "company": rec.get("company"),
            "commute_distance": rec.get("commute_distance"),
            "address_postcode": rec.get("address_postcode")
        }
        add_or_merge(first_name, last_name, xml_record)

    notes_list = []
    if isinstance(txt_data, list):
        for item in txt_data:
            if isinstance(item, dict) and 'notes' in item:
                notes_list.append(item['notes'])
            elif isinstance(item, str):
                notes_list.append(item)
    elif isinstance(txt_data, str):
        notes_list = [txt_data]

    return unified


unified_data = unify_records(csv_data, json_data, xml_data, txt_data)
print(f"✅ Unified {len(unified_data)} customer records.")


def clean_value(v, field=None):  # (Ref: https://docs.python.org/3/library/functions.html#str)
    """Final cleanup before inserting into DB."""
    if v in [None, '', 'NA', 'N/A', 'null', 'None']:
        return 'N/A'
    return str(v)


db.drop_all_tables(with_all_data=True)  
db.create_tables()  


with db_session:  # (Ref: https://docs.ponyorm.org/transactions.html)
    for key, record in unified_data.items():
        Customer(
            firstName=clean_value(record.get('firstName')),
            lastName=clean_value(record.get('lastName')),
            age=clean_value(record.get('age')),
            sex=clean_value(record.get('sex')),
            vehicle_make=clean_value(record.get('vehicle_make')),
            vehicle_model=clean_value(record.get('vehicle_model')),
            vehicle_year=clean_value(record.get('vehicle_year')),
            vehicle_type=clean_value(record.get('vehicle_type')),
            iban=clean_value(record.get('iban')),
            credit_card_number=clean_value(record.get('credit_card_number')),
            address_city=clean_value(record.get('address_city')),
            address_postcode=clean_value(record.get('address_postcode')),
            retired=clean_value(record.get('retired')),
            dependants=clean_value(record.get('dependants')),
            salary=clean_value(record.get('salary')),
            pension=clean_value(record.get('pension')),
            company=clean_value(record.get('company')),
            commute_distance=clean_value(record.get('commute_distance')),
            notes=clean_value(record.get('notes'))
        )
    commit()  # (Ref: https://docs.ponyorm.org/commit.html)

print("✅ All unified customer records inserted into the database successfully.")
