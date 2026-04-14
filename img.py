import cv2 as cv
import numpy as np
import os

print("librerias leidas...")

#rango de colores para detectar el color rojo (más permisivos para tiempo real)
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

# Capturar video en tiempo real desde la cámara (0 = cámara por defecto)
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara")
else:
    print("Cámara conectada. Presiona 'q' para salir...")
    
    while True:
        ret, img = cap.read()
        
        if not ret:
            print("Error: No se pudo leer el fotograma")
            break
        
        # Redimensionar el fotograma
        img = cv.resize(img, (400, 400))
        
        # Transformar a escala de grises y detectar color rojo
        imGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imGray = cv.cvtColor(imGray, cv.COLOR_GRAY2BGR)  # Convertir a BGR para mantener la consistencia de canales
        imHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        maskred1 = cv.inRange(imHSV, lower_red, upper_red)
        maskred2 = cv.inRange(imHSV, lower_red2, upper_red2)
        mask = cv.add(maskred1, maskred2)
        
        # Condición: si detecta rojo (más de 100 píxeles rojos), analizar si es octagonal
        red_pixels = cv.countNonZero(mask)
        octagon_detected = False
        if red_pixels > 100:
            # Encontrar contornos en la máscara roja
            contours_red, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            for contour in contours_red:
                epsilon = 0.02 * cv.arcLength(contour, True)
                approx = cv.approxPolyDP(contour, epsilon, True)
                if len(approx) == 8:  # octágono
                    octagon_detected = True
                    break  # suficiente con uno
            if octagon_detected:
                cv.putText(img_with_contours, "OCTAGONO ROJO DETECTADO!", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("Octágono rojo detectado!")
        
        kernel_size = 9 
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (kernel_size, kernel_size))
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        Red_detected = cv.bitwise_and(img, img, mask=mask)
        
        # Fondo de grises
        invMask = cv.bitwise_not(mask)
        grayBackground = cv.bitwise_and(imGray, imGray, mask=invMask)
        
        # Sumatoria del fondo de grises con los rojos
        finalImg = cv.add(grayBackground, Red_detected)
        
        # Otras modificaciones
        imBlur = cv.GaussianBlur(imGray, (7, 7), 0)
        
        # Contorneos
        imCanny = cv.Canny(imBlur, 50, 150)
        contours, hierarchy = cv.findContours(imCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        img_with_contours = img.copy()  # copiar antes de dibujar
        cv.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)
        
        # identificación de polígonos
        for contour in contours:
            shape_name = "Desconocida"  # valor por defecto para evitar NameError
            epsilon = 0.000001 * cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, epsilon, True)
            if len(approx)==8:
                shape_name = "Octagono"
            # else el valor por defecto se mantiene
            M = cv.moments(contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                # solo dibujar texto si identificamos una figura distinta a "Desconocida"
                if shape_name != "Desconocida":
                    cv.putText(img_with_contours, shape_name, (cX - 20, cY - 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        # Visualizaciones en tiempo real
        cv.imshow('mascara roja', mask)
        cv.imshow('imagen canny', imCanny)
        cv.imshow('imagen con contornos', img_with_contours)
        #cv.imshow('imagen borrosa', imBlur)
        #cv.imshow('fondo gris', invMask)
        cv.imshow('imagen final', finalImg)
        
        # Presionar 'q' para salir
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar recursos
    cap.release()
    cv.destroyAllWindows()
