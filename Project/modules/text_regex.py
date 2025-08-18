import re


# Search order number by pattern
def search_order_number(text):
    order_number = re.search(r'No[:\s]*([0-9]{7,})', text)
    if order_number:
        # print(f"\n✅ Order number detected: {order_number}")
        return order_number.group(1)
    # print("\n⚠️ Order number was not detected.")
    return None


# Search the data rows locating the header first
def search_data_rows(text):
    lines = text.splitlines()

    # List for key words that indicates the header
    first_header_key_words = ["CeCo", "Centro", "Pos", "Material", "Denominacion", "Fecha de", "Valor Unitario"]
    second_header_key_words = ["Lin", "nea", "Serv", "vicio", "Ent", "rega"]

    # Search the first line that containes any of the key words
    start_index = -1
    # Try to find first line of the header
    for i, line in enumerate(lines):
        if any(word in line for word in first_header_key_words):
            start_index = i+1
            break
    # Try to find second line of the header
    for i, line in enumerate(lines):
        if any(word in line for word in second_header_key_words):
            start_index = i
            break

    if start_index == -1:
        raise LookupError(
            "❌ Header line was not found.\n"
        )
    print(f"Header detected in line {start_index}:")
    print(lines[start_index])
    print("\nData rows detected:")
    
    data_rows = lines[start_index+1:]
    for row in data_rows:
        print(row) if row.strip() != "" else None
    return data_rows


def clean_lines(lines):
    
    # Clean the line so it is easier to extract the data
    def clean_line(line):
        # 1. Remove common specific chars due to OCR noise
        line = re.sub(r'[«=+~—_]', '', line)

        # 2. Remove any non alphanumeric char except some specific
        line = re.sub(r'[^\w\s.,/]', '', line)

        # 3. Remove dots alone between spaces " . " → " "
        line = re.sub(r'\s\.\s', ' ', line)

        # 4. Remove dots at the beggining or the end of the line
        line = re.sub(r'^\.\s*|\s*\.$', '', line.strip())

        # 5. Replace multiple spaces for just one
        line = re.sub(r'\s+', ' ', line)
        print(f'Linea limpiada: {line}')
        return line
    
    return map(lambda l: clean_line(l), lines)