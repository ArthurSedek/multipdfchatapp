# Multi-PDF Chat App with OpenAI LLM

![Project Logo/Icon](https://github.com/ArthurSedek/multipdfchatapp/blob/main/resources/MYLOGO.png)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Demo](#demo)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Customization](#customization)
- [Contributing](#contributing)

## Introduction

Welcome to the Multi-PDF Chat App with OpenAI LLM! This application allows users to chat with multiple PDF files simultaneously using the power of OpenAI's Language Model. You can also view images from the PDF files within the app, making it a versatile tool for text and image-based interactions with documents.


## Features

- **Multi-PDF Chat:** Chat with multiple PDF files in real-time.
- **Image Display:** View images contained within the PDF files.
- **OpenAI Integration:** Powered by OpenAI's LLM for natural language understanding.

## Demo

[Insert a link to a live demo or a GIF/video showcasing your app in action.]

## Getting Started

Follow these steps to get the Multi-PDF Chat App up and running on your local machine.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ArthurSedek/multipdfchatapp.git
   ```

2. Change directory to the project folder:

   ```bash
   cd multipdfchatapp
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Certainly! Here's how you can modify the "Usage" section to include instructions on editing the configuration file:

## Usage

To use the Multi-PDF Chat App, you'll need to configure the application by editing the available configuration file. Follow these steps:

1. **Configuration File Setup:**

   - Locate the `configuration.json` file in the project root directory.

   - Open `configuration.json` using a text editor of your choice.

2. **Edit Configuration:**

   - Inside `configuration.json`, you'll find placeholders for various settings such as API keys and other parameters. Edit these fields with your own information:

   ```json
   {
     "openai_api_key": "YOUR_OPENAI_API_KEY",
     "pdf_files_directory": "/path/to/your/pdf/files",
     "output_directory": "/path/to/output/directory",
     "max_chat_history": 3,
     "other_settings": "customize_here"
   }
   ```

   - Replace `"YOUR_OPENAI_API_KEY"` with your actual OpenAI API key.

   - Set `"pdf_files_directory"` to the directory where your PDF files are located.

   - Adjust other settings as needed.

3. **Save Configuration:**

   - Save the `configuration.json` file after making your changes.

4. **Run the App:**

   - Now that you've configured the app, you can run it:

     ```bash
     python app.py
     ```

5. **Using the App:**

   - Once the app is running, follow the on-screen instructions to interact with the PDF files and use the OpenAI LLM model for chat.

6. **Examples:**

   - Here's an example of how your `configuration.json` might look after customization:

   ```json
   {
     "openai_api": "abc123xyz456",
     "model": "gpt-3.5-turbo",
    "tokens_length": 1000,
    "number_of_references": 2,
    "temperature": 0
   }
   ```

   - You can modify the `"model"`, `"tokens length"`, and `"number of references"` settings as per your requirements.

Remember to provide clear instructions within `configuration.json` about the format and expected values for each setting to assist users in configuring the app correctly.


## Contributing

We welcome contributions from the community! If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Create a pull request to submit your changes.
