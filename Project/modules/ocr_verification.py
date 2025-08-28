# required fields: ['pedido', 'posicion', 'solped', 'material', 'cantidad', 'subtotal', 'centro', 'denom']

from . import correct_ocrs

# Receives an ocr input and compares it with the real data in ocrs, to check how accurate it was
def evaluate_ocr(ocr_input, ocr_id):
    is_all_correct = True

    required = ['line', 'solped', 'material', 'quantity', 'subtotal', 'center']
    REAL_OCR = correct_ocrs.ocrs.get(ocr_id, None)
    if (not REAL_OCR):
        return True

    # Check order numbers
    if ocr_input['order_number'] != REAL_OCR['order_number']:
        print("❌ Wrong order number ", end="")
        is_all_correct = False
    else:
        print("✅ Order number ", end="")


    # Check both rows quantity
    REAL_ROWS = REAL_OCR['rows']
    INPUT_ROWS = ocr_input['rows']
    real_rows_quantity = len(REAL_ROWS)
    input_rows_quantity = len(INPUT_ROWS)

    MIN_ROWS = min(real_rows_quantity, input_rows_quantity)
    if real_rows_quantity == input_rows_quantity:
        print("✅ Rows quantity")
    else:
        is_all_correct = False
        print(f'❌ Rows detected: {input_rows_quantity}, real rows: {real_rows_quantity}')

    # Check each atributte for all rows
    for row_i in range(MIN_ROWS):
        print("")
        for att in required:
            if INPUT_ROWS[row_i][att] == REAL_ROWS[row_i][att]:
                print("✅", end="")
            else:
                is_all_correct = False
                print(f'❌ {att}: {INPUT_ROWS[row_i][att]} != {REAL_ROWS[row_i][att]}', end="")
    print("\n")
    return is_all_correct