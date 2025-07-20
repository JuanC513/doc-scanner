import cv2
import shutil
import pytesseract
import os

# Intentar usar el tesseract del sistema (en el PATH)
tesseract_en_path = shutil.which("tesseract")

if tesseract_en_path:
    # Opción 1: está en el PATH
    print(f"✅ Usando Tesseract desde el PATH: {tesseract_en_path}")
    pytesseract.pytesseract.tesseract_cmd = tesseract_en_path
else:
    # Opción 2: buscar en ruta local del proyecto
    ruta_local = os.path.join(os.getcwd(), "tesseract", "tesseract.exe")
    if os.path.exists(ruta_local):
        print(f"✅ Usando Tesseract desde ruta local: {ruta_local}")
        pytesseract.pytesseract.tesseract_cmd = ruta_local
    else:
        raise FileNotFoundError(
            "❌ No se encontró Tesseract.\n"
            "Asegúrate de tenerlo instalado y en el PATH, o coloca tesseract.exe en './tesseract/'"
        )

# Configuración opcional para que Tesseract use idioma español
custom_config = r'--oem 3 --psm 6'

# Cambia esto al nombre real de la imagen
nombre_imagen = "prueba2.jpg"
ruta_imagen = os.path.join(os.getcwd(), nombre_imagen)

if not os.path.exists(ruta_imagen):
    raise FileNotFoundError(f"No se encontró la imagen en: {ruta_imagen}")

imagen = cv2.imread(ruta_imagen)
if imagen is None:
    raise ValueError("La imagen no pudo ser cargada. Verifica el formato o permisos.")

# Redimensionar para pruebas si la imagen es muy grande
alto_maximo = 1200
if imagen.shape[0] > alto_maximo:
    scale = alto_maximo / imagen.shape[0]
    imagen = cv2.resize(imagen, None, fx=scale, fy=scale)

# Preprocesamiento básico: escala de grises y binarización
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
_, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Mostrar OCR completo (para ver qué detecta Tesseract)
texto_detectado = pytesseract.image_to_string(binaria, config=custom_config)
print("\n🧾 TEXTO DETECTADO:\n")
print(texto_detectado)

# Buscar el número de pedido por patrones
import re
patron_pedido = re.search(r'No[:\s]*([0-9]{7,})', texto_detectado)
if patron_pedido:
    numero_pedido = patron_pedido.group(1)
    print(f"\n✅ Número de pedido detectado: {numero_pedido}")
else:
    print("\n⚠️ No se detectó número de pedido.")

# Mostrar la imagen preprocesada
cv2.imshow("Imagen binarizada para OCR", binaria)
cv2.waitKey(0)
cv2.destroyAllWindows()