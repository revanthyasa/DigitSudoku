# DigitSudoku
Sudoku Solver & Interactive Puzzle Web Application: This project is a full-stack web application that allows users to solve and interact with Sudoku puzzles in a dynamic and intuitive interface. The application provides users with multiple functionalities, such as uploading a Sudoku puzzle image, digitizing it, solving it automatically, and playing it interactively. This system leverages advanced Optical Character Recognition (OCR) techniques for digit extraction, allowing users to upload an image of a hand-written or printed Sudoku puzzle, which is then processed to identify and extract the puzzle grid. The application incorporates both front-end and back-end systems to ensure a smooth user experience, data handling, and accurate puzzle solving.

The front end is built with React, providing a clean and responsive user interface for uploading images, displaying Sudoku puzzles, and enabling real-time interaction with the puzzle grid. The interface allows users to manually edit the grid, solve it using an automated algorithm, or verify the extracted grid before proceeding. Users can also interact with the puzzle by placing numbers in empty cells while adhering to Sudoku's rules, with dynamic feedback and validation. Additionally, users are presented with options to undo their moves and receive warnings if they attempt to place invalid numbers.

The back end is powered by a Django Web API that handles image processing and the logic for Sudoku solving. The core image processing functionality is supported by PyTesseract, which extracts digits from the uploaded images and transforms them into a format that can be displayed and edited on the front end. The extracted Sudoku grid can be further verified and corrected by the user before proceeding with solving. The Sudoku solver itself uses a backtracking algorithm to find valid solutions efficiently.

Key features of the application include:

Sudoku Grid Upload: Users can upload an image of a Sudoku puzzle, which the application processes and extracts into a digitized grid.

Grid Verification and Editing: After extracting the grid from the uploaded image, users can verify and manually correct any errors in the OCR-processed grid.

Interactive Sudoku Playing: Users can interact with the Sudoku grid by placing numbers in empty cells, with real-time feedback and validation.

Automated Solver: The app includes a solver that automatically solves the puzzle using backtracking, allowing users to check the solution or solve the entire puzzle at any time.

Dynamic Digit Count: A live count of how many times each number (1–9) has been used in the grid, helping users keep track of available digits.

Undo Functionality: Users can undo their last move if they make a mistake, restoring the previous state of the grid.

User-Friendly Interface: The app is designed to be user-friendly and visually appealing, with responsive layouts and well-organized controls for easy use on various screen sizes.

Backend API for Processing: The Django backend processes the uploaded images and integrates with PyTesseract for digit recognition while also handling the Sudoku-solving logic.

This project offers a rich, interactive experience for Sudoku enthusiasts and provides practical applications in solving and playing Sudoku puzzles. Whether users prefer uploading and solving puzzles automatically or solving them manually, the app provides the tools and flexibility to enjoy Sudoku puzzles at their convenience.
