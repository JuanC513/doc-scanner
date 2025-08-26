# required fields: ['pedido', 'posicion', 'solped', 'material', 'cantidad', 'subtotal', 'centro', 'denom']

from . import correct_ocrs

# Receives an ocr input and compares it with the real data in ocrs, to check how accurate it was
def evaluate_ocr(ocr_input, ocr_id):
    required = ['line', 'solped', 'material', 'quantity', 'subtotal', 'center']
    REAL_OCR = correct_ocrs.ocrs[ocr_id]


    # Check order numbers
    if ocr_input['order_number'] != REAL_OCR['order_number']:
        print("❌ Wrong order number")
    else:
        print("✅ Order number")


    # Check both rows quantity
    REAL_ROWS = REAL_OCR['rows']
    INPUT_ROWS = ocr_input['rows']
    real_rows_quantity = len(REAL_ROWS)
    input_rows_quantity = len(INPUT_ROWS)

    MIN_ROWS = min(real_rows_quantity, input_rows_quantity)
    if real_rows_quantity == input_rows_quantity:
        print("✅ Rows quantity")
    else:
        print(f'❌ Rows detected: {input_rows_quantity}, real rows: {real_rows_quantity}')

    # Check each atributte for all rows
    for row_i in range(MIN_ROWS):
        print("")
        for att in required:
            if INPUT_ROWS[row_i][att] == REAL_ROWS[row_i][att]:
                print("✅", end="")
            else:
                print(f'❌ {att}: {INPUT_ROWS[row_i][att]} != {REAL_ROWS[row_i][att]}', end="")