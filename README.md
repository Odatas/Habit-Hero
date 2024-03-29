# Habit Hero

Habit-Hero is an innovative habit-tracking application designed to help you build and maintain positive habits for a healthier, more productive life. At its core, Habit-Hero leverages the power of consistency and accountability to transform your daily routines. Whether you're aiming to exercise more, read regularly, or meditate, our app makes tracking these habits simple and motivating.

What sets Habit-Hero apart is its user-friendly interface and personalized experience. You can easily create, monitor, and adjust your habits as you progress. Moreover, the app offers insightful analytics, allowing you to review your habit streaks and patterns over time. This feature not only encourages you to stay on track but also provides valuable feedback on your journey towards personal growth.

## Python Version

This application is developed using Python 3.9.13. While it is optimized for this version, it may be compatible with other versions of Python as well. We encourage users to experiment with their version of Python, but for the best experience, using Python 3.9.13 is recommended. You can download the required version of Python from the official website: https://www.python.org/downloads/

## Installation and Lunching Instructions

1. **Clone the Repository**
   Clone the repository to your local machine using Git:
   ```bash
   git clone https://github.com/Odatas/Habit-Hero.git
   ```

2. **Navigate to the Project Directory**
   Change to the directory where the project is located:
   ```bash
   cd Habit-Hero
   ```

3. **Install Dependencies**
   Install necessary libraries or frameworks:
   ```bash
   pip install -r requirements.txt
   ```

4. **Running the Application**
   Run the application:
   ```bash
   python orchestrator.py
   ```


## Usage

Once the application is up and running, you can add, edit, or remove habits as per your tracking requirements. The application's user interface is intuitive and user-friendly, providing a seamless experience in managing your daily habits.

Additionally, "Habit-Hero" comes equipped with a dummy user account. This feature allows you to explore various functionalities and get a feel for how the application works without the need to input your data immediately. It's a great way to see the potential of the app in action.

### Dummy data
Habit Hero includes the script savefile_adder.py, which is designed to generate dummy data for the application. This functionality is essential for ensuring that the dummy data remains up-to-date and relevant. By using this script, users can easily simulate a real-world environment with current data, providing a comprehensive preview of how Habit Hero manages and tracks habits over time.

Run this script with:

  ```bash
   python savefile_adder.py
   ```

You will then find a new user created when you start the application. Have fun exploring.
 
 
### Unit Testing

Habit Hero includes a unittest.py script, which provides a suite of unit tests to ensure the application's stability and reliability. Running these tests is highly recommended, especially after making code changes. To execute the unit tests, simply run the unittest.py script. This will verify that all core functionalities are working correctly and that any updates or modifications to the code do not negatively impact the app's performance or functionality.
 
## Contributing

Contributions to Habit Hero are always welcome. Whether it's bug reports, feature requests, or code contributions, feel free to fork the repo and submit a pull request with your changes.

## License

"Habit-Hero" is licensed under the GNU General Public License v3.0. This license allows users to modify, distribute, and use the software freely, but it requires that any modified versions are also open source under the same license. It ensures that end users have the freedom to run, study, share, and modify the software. For more detailed information, please refer to the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

