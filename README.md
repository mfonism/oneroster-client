# OneRoster Client

## 🎉 Welcome to the ultimate data fetching adventure

OneRoster Client is a tool for fetching and organizing teacher and student data from a [OneRoster](https://www.1edtech.org/standards/oneroster)-compliant server like a pro! Whether you're diving into the data sea or just dipping your toes, this client makes data fetching and handling a breeze.

## 🛠️ Prerequisites

Before you embark on this journey, make sure you have these essentials:

- **Python 3.11+**: The backbone of our adventure. [Get it here!](https://www.python.org/downloads/)
- **pip**: Our trusty package installer.
- **Git**: To clone this awesome repository.

## Setting Sail ⛵

### 1. Clone the Repository

Let's kick things off by cloning the repository to your local machine:

```bash
git clone https://github.com/mfonism/oneroster-client.git
cd oneroster-client
```

### 2. Create a Virtual Environment

Create a cozy virtual environment to manage your dependencies:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

- **Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

Time to equip our project with all the necessary tools:

```bash
pip install -r requirements.txt
```

### 5. (Optional) Install Development Dependencies

Feeling adventurous? Contribute or experiment with our development goodies:

```bash
pip install -r requirements-dev.txt
```

Oh, and we've set up automated checks with a `Makefile` to keep everything shipshape. To run all checks, just:

```bash
make all
```

### 6. Set Up Your Environment Variables

Create a `.env` file in the project root. Here's your secret map:

```plaintext
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
TOKEN_URL=https://your-token-url.com/token
BASE_URL=https://your-api-url.com/api
```

Fill in your own credentials and URLs, and you're ready to set sail! 🗺️

## Troubleshooting 🕵️

- **Missing dependencies?** Make sure you've activated your virtual environment.
- **Connection issues?** Double-check your `.env` file settings.

## Contributions Welcome! 🤝

Join our crew! Install development dependencies, run `make all`, and sail into the open seas of contribution.
