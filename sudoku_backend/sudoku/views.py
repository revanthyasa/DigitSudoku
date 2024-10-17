import logging
import cv2
import pytesseract
import numpy as np
import os
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .serializers import SudokuSerializer

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\rryasa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Update this path as needed

# Configure logging
logger = logging.getLogger(__name__)

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return thresholded, image

def find_largest_contour(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise Exception("No contours found in the image.")
    largest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    return largest_contour

def extract_sudoku_grid(original_image, contour):
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) != 4:
        raise Exception("Sudoku grid contour not found. Please ensure the image is clear and contains a single Sudoku grid.")
    points = np.array([point[0] for point in approx], dtype='float32')
    s = points.sum(axis=1)
    diff = np.diff(points, axis=1)
    sorted_points = np.array([
        points[np.argmin(s)],
        points[np.argmin(diff)],
        points[np.argmax(s)],
        points[np.argmax(diff)],
    ], dtype='float32')

    side = max([
        np.linalg.norm(sorted_points[0] - sorted_points[1]),
        np.linalg.norm(sorted_points[1] - sorted_points[2]),
        np.linalg.norm(sorted_points[2] - sorted_points[3]),
        np.linalg.norm(sorted_points[3] - sorted_points[0])
    ])
    dst = np.array([[0, 0], [side-1, 0], [side-1, side-1], [0, side-1]], dtype='float32')
    matrix = cv2.getPerspectiveTransform(sorted_points, dst)
    warped = cv2.warpPerspective(original_image, matrix, (int(side), int(side)))
    return warped

def extract_digits_from_cells(warped_image):
    side = warped_image.shape[0]
    cell_side = side // 9
    sudoku_grid = []

    for row in range(9):
        row_cells = []
        for col in range(9):
            x1, y1 = col * cell_side, row * cell_side
            x2, y2 = (col + 1) * cell_side, (row + 1) * cell_side
            cell = warped_image[y1:y2, x1:x2]
            cell = cv2.resize(cell, (50, 50))
            cell = cv2.GaussianBlur(cell, (3, 3), 0)
            _, cell = cv2.threshold(cell, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            kernel = np.ones((3, 3), np.uint8)
            cell = cv2.dilate(cell, kernel, iterations=1)

            try:
                digit = pytesseract.image_to_string(cell, config='--psm 10 -c tessedit_char_whitelist=0123456789', timeout=2)
            except pytesseract.pytesseract.TesseractError:
                digit = ''
            digit = digit.strip()
            row_cells.append(int(digit[-1]) if digit.isdigit() and len(digit) > 0 else 0)
        sudoku_grid.append(row_cells)

    return sudoku_grid

@api_view(['POST'])
def upload_image(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['image']
    file_path = default_storage.save(uploaded_file.name, uploaded_file)
    full_file_path = os.path.join(default_storage.location, file_path)

    try:
        logger.info("Starting image preprocessing.")
        thresholded, original_image = preprocess_image(full_file_path)
        logger.info("Image preprocessing completed.")

        logger.info("Finding largest contour.")
        largest_contour = find_largest_contour(thresholded)
        logger.info("Largest contour found.")

        logger.info("Extracting Sudoku grid.")
        warped_image = extract_sudoku_grid(original_image, largest_contour)
        logger.info("Sudoku grid extracted.")

        logger.info("Extracting digits from cells.")
        sudoku_grid = extract_digits_from_cells(warped_image)

        os.remove(full_file_path)  # Clean up the saved file

        return Response({'grid': sudoku_grid}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error processing the image: {str(e)}")  # Log the error
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SudokuView(APIView):
    def get(self, request):
        sample_sudoku = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

        serializer = SudokuSerializer(data={'grid': sample_sudoku})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
