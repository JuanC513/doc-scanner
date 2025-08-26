#----------------------------------------------------------------
#---------- APPLY OCR ----------
#----------------------------------------------------------------

# Format each value to take data before '/' and remove '.' in prices
def format_data(data):
    for dic in data:
        dic['line'] = dic['line'].split('/')[0]
        dic['subtotal'] = dic['subtotal'].replace('.', '')

    return data


""" def show_dataOld(data, order_number, center_mode, places):
    for line in (data):
        required_fields = ['pedido', 'line', 'solped', 'material', 'cantidad', 'subtotal', 'centro', 'denom']
        required_data = ""
        for field in required_fields:
            new_field = ""

            match field:
                case 'pedido':
                    new_field = order_number
                case 'cantidad':
                    new_field = 2
                case 'centro':
                    new_field = center_mode
                case 'denom':
                    new_field = places[center_mode] if (center_mode in places) else ""
                case _:
                    new_field = f'{line[field]}'
            
            required_data += f'{new_field} '
        normalized_data = ' '.join(required_data.split())
        print(normalized_data) """


# Print the data with certain format
def show_data(data, order_number, center_mode, places):
    def get_denom():
        return places.get(center_mode, "")

    field_map = {
        "pedido": lambda _: order_number,
        "cantidad": lambda _: 2,
        "centro": lambda _: center_mode,
        "denom": lambda _: get_denom(),
    }

    required_fields = ['pedido', 'line', 'solped', 'material', 'cantidad', 'subtotal', 'centro', 'denom']

    for line in data:
        required_data = []
        for field in required_fields:
            if field in field_map:
                new_field = field_map[field](line)
            else:
                new_field = line.get(field, "")
            
            required_data.append(str(new_field))
        print(" ".join(required_data))