# Meme Lingo

Meme Lingo is a fun and interactive meme translation tool built during the AGIHouse Hackathon. It allows users to translate text in memes to different languages while maintaining the meme's visual context.

## Features

- Upload meme images
- Detect text in memes using Google's Gemini Vision API
- Translate meme text to multiple languages
- Generate captioned images with translations
- User-friendly interface

## Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS

### Backend
- FastAPI
- Python
- Google Gemini API
- Pillow (PIL) for image processing

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js
- Google Gemini API key

### Installation

1. Clone the repository
2. Install backend dependencies
```
cd fastapi_services
pip install -r requirements.txt
```
3. Install frontend dependencies
```
cd ..
npm install
```

4. Set up environment variables
Create a `.env` file in the `fastapi_services` directory:

### Running the Application

1. Start the backend server
```bash
cd fastapi_services
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Start the frontend development server
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

1. Upload a meme image
2. Select the target language for translation
3. Submit and receive the translated meme with caption

## Built for AGIHouse Hackathon

This project was developed during the AGIHouse Hackathon, showcasing the integration of modern AI capabilities with practical applications in content localization and meme culture.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


