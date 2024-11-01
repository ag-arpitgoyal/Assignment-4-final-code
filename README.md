# Library Digitalization

## Overview
**Library Digitalization** is a Python-based system for efficiently managing a digital library collection. This project demonstrates advanced data retrieval and storage techniques through object-oriented programming and custom hash table implementations, enabling fast keyword searches, book management, and efficient data handling.

## Features
- **Book & Word Management**: Tracks books and unique words for quick retrieval and querying.
- **Custom Collision-Handled Hash Tables**: Uses unique collision-handling methods to optimize data storage and retrieval.
- **Dynamic Resizing**: Automatically resizes hash tables to maintain performance as the collection grows.
- **Efficient Search**: Allows fast, scalable keyword searching across multiple books.

## Project Structure

- **DigitalLibrary** (`digital_library.py`): The abstract base class defining core functionalities for derived library classes.
- **MuskLibrary** (`musk_library.py`): Manages books loaded in bulk with lexicographically sorted words for optimized retrieval.
- **JGBLibrary** (`jgb_library.py`): Manages books added individually, allowing retrieval based on insertion order.
- **HashMap & HashSet** (`hash_map.py`, `hash_set.py`): Custom hash structures implementing collision handling techniques like chaining, linear probing, and double hashing.
- **Dynamic Hash Structures**: Dynamic hash maps and sets that resize based on load factors for consistent performance.

## Installation & Setup
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/Library-Digitalization.git
    cd Library-Digitalization
    ```

2. **Run the main script** to test the system’s capabilities.

## Contribution
Contributions are welcome! Fork, submit pull requests, or open issues to improve features or optimize performance.

## License
Licensed under the MIT License.
