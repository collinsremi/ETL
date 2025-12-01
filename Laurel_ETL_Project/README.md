````markdown
# 🧠 ETL Data Integration Project — Laurel_ETL

## 📋 Overview

This project demonstrates a full **ETL (Extract, Transform, Load)** pipeline built using **Python**, **PonyORM**, and **MySQL**, aimed at integrating and cleaning customer data from multiple file formats — `.csv`, `.json`, `.xml`, and `.txt`.

The main goal is to **consolidate fragmented datasets** into a unified database table called `Customer`, while ensuring that:
- Missing or inconsistent data is cleaned and normalized,
- Duplicates are merged intelligently (based on first and last names),
- The final dataset is stored securely in a local MySQL database for querying or further analysis.

This ETL process ensures accurate and structured data that can be used for reporting, analytics, or data warehousing.

---

## ⚙️ Setup and Installation

### 1. 🧰 Prerequisites

Before running the project, ensure that you have:

- **Python 3.9+**
- **USBWebserver** (for running MySQL locally)
- The following Python libraries installed:

```bash
pip install pony mysql-connector-python
````

> 💡 Tip: You do not need to install heavy MySQL software — USBWebserver provides a lightweight MySQL server and phpMyAdmin in one portable package.

---

### 2. 💽 Setting Up USBWebserver (MySQL Environment)

The project uses **USBWebserver** to provide a local **MySQL** and **PHP** environment that can run without installation.
It’s fast, portable, and perfect for testing ETL pipelines on a local machine.

#### 📥 Download & Installation

1. Download **USBWebserver** from its official site:
   🔗 [https://www.usbwebserver.yura.nl](https://www.usbwebserver.yura.nl)
2. Extract the ZIP file to a convenient location, for example:
   `C:\USBWebserver`
3. Open the extracted folder and double-click **`USBWebserver.exe`**.
4. A small control panel will open. You’ll see green indicators showing that **Apache** and **MySQL** are running successfully.

---

#### ⚙️ Accessing phpMyAdmin

1. In the control panel, click **“phpMyAdmin”**,
   or manually go to: [http://localhost:8080/phpmyadmin/](http://localhost:8080/phpmyadmin/)
2. Log in using the **default credentials**:

   ```
   Username: root
   Password: usbw
   ```
3. Click on **Databases** in the top navigation bar.
4. Create a new database named:

   ```
   laurel_etl
   ```
5. Note the connection details below, as they are used in your Python code:

   ```
   Host: localhost
   Port: 3307
   Username: root
   Password: passord
   Database: laurel_etl
   ```

✅ You now have a running MySQL server ready for your ETL pipeline.

---

### 3. 🔐 Environment Variables (Security Best Practice)

```

In your Python script, the following line reads the value dynamically:

```python
import os
password = os.getenv("DB_PASSWORD", "usbw")
```

This ensures sensitive credentials are not exposed if your code is shared or version-controlled.

---

### 4. 📁 Project Structure

```
📁 laurel_etl_project
 ┣ 📁 data_cetm50
 ┃ ┣ user_data.csv
 ┃ ┣ user_data.json
 ┃ ┣ user_data.xml
 ┃ ┗ user_data.txt
 ┣ 📁 output
 ┃ ┣ customer.csv
 ┣ etl_script.py
 ┗ README.md
 
```

---

## 🧩 ETL Workflow

### 1️⃣ Extract

The program loads data from multiple file formats stored in the `data_cetm50` folder:

| File Type | Description                               | Module Used             |
| --------- | ----------------------------------------- | ----------------------- |
| `.csv`    | Reads tabular data using `csv.DictReader` | `csv`                   |
| `.json`   | Parses JSON objects and arrays            | `json`                  |
| `.xml`    | Reads structured XML data                 | `xml.etree.ElementTree` |
| `.txt`    | Reads unstructured text lines as notes    | `open()`                |

Each extraction step includes **error handling** for missing or corrupted files, printing friendly messages like:

```
❌ CSV file not found. Check your 'data_cetm50' folder path.
```

---

### 2️⃣ Transform

Data transformation ensures all records follow a consistent format.

* **Trimming** whitespace from keys and values
* **Replacing** invalid values like `"N/A"`, `"null"`, or `""` with Python `None`
* **Merging** datasets by matching first and last names
* **Cleaning** final values using a helper function `clean_value()`
* **Normalizing keys** (e.g., “First Name” → “firstName”)

The script uses dictionary comprehensions and helper functions such as:

* `merge_records()` – merges data without overwriting valid fields
* `normalize_key()` – generates a normalized key (e.g., `john_doe`)
* `unify_records()` – combines all input data into one unified dictionary

This logic ensures that missing information in one file (like `salary`) can be filled from another source (like XML or JSON).

---

### 3️⃣ Load

Once all records are cleaned and unified, they are inserted into the **MySQL database** via **PonyORM**.

The `Customer` entity defines all fields as optional (string-based) columns, including:

| Field                           | Example Data                    |
| ------------------------------- | ------------------------------- |
| `firstName`, `lastName`         | John, Doe                       |
| `age`, `sex`                    | 45, Male                        |
| `vehicle_make`, `vehicle_model` | Toyota, Corolla                 |
| `iban`, `credit_card_number`    | GB00BANK123..., 4532-xxxx       |
| `salary`, `pension`, `company`  | 60000, 12000, “TechCorp”        |
| `notes`                         | Unstructured text from TXT file |

Before inserting, the database is reset using:

```python
db.drop_all_tables(with_all_data=True)
db.create_tables()
```

and data insertion is handled inside a `db_session` context:

```python
with db_session:
    Customer(...)
    commit()
```

This ensures transactions are atomic and reliable.

---

## 🧠 Key Techniques and Best Practices

| Technique                      | Description                                             |
| ------------------------------ | ------------------------------------------------------- |
| **PonyORM**                    | Simplifies SQL interactions using Pythonic syntax       |
| **Environment Variables**      | Protect credentials from being hardcoded                |
| **List & Dict Comprehensions** | Improve data merging and cleaning performance           |
| **Exception Handling**         | Prevents program crashes from bad data or missing files |
| **Dynamic Merging**            | Combines data using normalized name keys                |
| **Inline Documentation**       | Each section references Python/PonyORM documentation    |
| **Modular Design**             | Functions can be reused in other ETL projects           |

---

## 🧪 Testing and Verification

1. Run your ETL script:

   ```
   click on the script
   it will open up your default IDE
   click the run button on your IDE
   ```

2. The console will display progress messages like:

   ```
   ✅ Successfully loaded 1000 records from CSV.
   ✅ Unified 993 customer records.
   ✅ All unified customer records inserted into the database successfully.
   ```

3. To verify the data insertion:

   * Open phpMyAdmin at [http://localhost:8080/phpmyadmin/](http://localhost:8080/phpmyadmin/)
   * Select the database `laurel_etl`
   * Run:

     ```sql
     SELECT * FROM Customer;
     ```

   You should see all cleaned and unified records.

---

## 💡 Common Issues & Solutions

| Issue                                         | Cause                           | Solution                                       |
| --------------------------------------------- | ------------------------------- | ---------------------------------------------- |
| **Access denied for user 'root'@'localhost'** | Wrong or missing password       | Ensure you run this command on your power shell: setx DB_PASSWORD "usbw"
| **CSV/JSON file not found**                   | Incorrect folder path           | Ensure all data files are in `data_cetm50/`    |
| **Invalid JSON format**                       | Malformed JSON syntax           | Validate JSON file using an online validator   |
| **XML parsing error**                         | Incorrect XML structure         | Verify closing tags and encoding               |
| **Duplicate name records**                    | Multiple sources with same name | Handled automatically via normalized keys      |

---

## 🔐 Security Considerations

* Credentials are stored securely, **not** hardcoded.
* The database is **local (localhost)** — no remote exposure.
* Sensitive fields like `credit_card_number` are used only for educational demonstration; encryption would be required in production.
* Password defaults to `usbw`, but it can be changed in phpMyAdmin for better security.

---

## 📚 References

* [Python csv Module](https://docs.python.org/3/library/csv.html)
* [Python json Module](https://docs.python.org/3/library/json.html)
* [Python xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)
* [PonyORM Documentation](https://docs.ponyorm.org)
* [USBWebserver Official Site](https://www.usbwebserver.yura.nl)

---

## ✅ Conclusion

This project successfully demonstrates a **real-world ETL pipeline** that unifies data from multiple formats into a **structured MySQL database**, powered by **Python** and **PonyORM**.

It highlights:

* Advanced Python data handling,
* Effective use of external and built-in libraries,
* Secure and maintainable database integration,
* Strong documentation and testing workflow.

The ETL process can be reused or extended for other datasets, showcasing practical data engineering principles in action.

```
