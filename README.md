# Rocket Hackathon

## Overview
Chatbot for IBM Redbook documentation

## React Code Rules
Ensure you are following these rules for development:
- Use arrow functions: const fnc = () => {}
- USE MODULE STYLES!!! File names: master.module.css => usage in file: styles.exampleClass => read more here: https://create-react-app.dev/docs/adding-a-css-modules-stylesheet/
- Each component has its own file
- Each component group has its own folder

## Rules
Ensure you are following these rules for development:
- Create a new branch in your computer for each feature
- Branch name: First letter of name + first letter of surname + feature name. Ex.: AB-llama | AB - Aronas Butkevicius
- Do development on that branch
- Push branch to Github
- Open a new Pull Request
- Assign a peer-reviewer
- Each small task has its own branch!

## Installation & Setup
To get started with Rocket Hackathon, follow these steps:

### Clone the Repository
```sh
git clone https://github.com/JonasUrn/RocketHackaton.git
cd RocketHackaton
```

### Create or Switch to a Branch
```sh
git checkout -b [branch_name]
```

### Add and Commit Changes
```sh
git add --all
git commit -m "[Your commit message]"
```

### Push Changes
```sh
git push -u origin [branch_name]
```

## Requirements
Ensure you have the following installed:
- Python
- Ollama
- Llama3.2
- Pip
- Git
- Node.js

## Running the Project
1. Install dependencies:
   ```sh
   - ollama
   - flask: Flask, jsonify, request
   - flask_cors: CORS
   - chromadb
   - sentence_transformers
   - fitz
   - tqdm
   ```
2. Run the main script:
   ```sh
   cd backend
   python app.py
   cd ..
   cd frontend
   npm start
   ```

## Contribution
Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your fork and submit a pull request

## Contact
For questions or contributions, feel free to reach out via [GitHub Issues](https://github.com/JonasUrn/RocketHackaton/issues).