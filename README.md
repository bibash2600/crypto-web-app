# Text Encryption & Decryption Web App

A lightweight, browser-based web application built with Python and Flask that demonstrates how four classical cryptographic algorithms work. 

## Supported Ciphers
* **Caesar Cipher:** Monoalphabetic substitution using a fixed shift.
* **Vigenère Cipher:** Polyalphabetic substitution using a keyword.
* **Rail Fence Cipher:** Transposition using a zig-zag pattern across user-defined rails.
* **Playfair Cipher:** Digraph substitution using a keyword-derived 5x5 matrix.

## Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML, CSS (embedded)

## How to Run Locally
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows)
4. Install Flask: `pip install flask`
5. Run the app: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.
