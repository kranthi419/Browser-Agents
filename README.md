# Browser Agent Project

This project uses a browser automation agent to perform tasks using OpenAI's GPT-4o model. The agent can interact with web pages and perform tasks such as sending messages on LinkedIn.

## Prerequisites

- Python 3.8 or higher
- Google Chrome installed
- `pip` for managing Python packages

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    playwright install
    ```

3. Set up the environment variables in a `.env` file:
    ```dotenv
    ANONYMIZED_TELEMETRY=false
    OPENAI_API_KEY="your-openai-api-key"
    ```

## Usage

1. Ensure Google Chrome is installed and the path to the Chrome executable is correctly set in `main.py`.

2. Run the main script:
    ```sh
    python sample.py
    ```

## Project Structure

- `main.py`: The main script that initializes the browser agent and performs the task.
- `requirements.txt`: Lists the Python dependencies for the project.
- `.env`: Contains environment variables such as the OpenAI API key.

## License

This project is licensed under the MIT License.