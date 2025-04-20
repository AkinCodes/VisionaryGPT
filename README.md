# VisionaryGPT: AI-Powered Movie Poster Generation & Classification

<img width="1073" alt="Screenshot 2025-04-20 at 15 41 48" src="https://github.com/user-attachments/assets/0e73313d-d1e4-4204-a7e1-711d9591f2a7" />
<hr />

Welcome to  **VisionaryGPT**, an AI-powered platform designed to generate, classify, and extract metadata from movie posters. By leveraging the most cutting-edge technologies in computer vision, deep learning, and natural language processing (NLP), VisionaryGPT transforms creative possibilities for media and entertainment into reality. This project demonstrates the seamless integration of powerful AI models with FastAPI for high-performance API deployment.


## Key Features
### **1. Poster Generation**
- **Stable Diffusion**: Utilize **Stable Diffusion**, a powerful **text-to-image generation model**, to create high-quality movie posters based on user-provided prompts.
- Example prompt: "Sci-Fi thriller with a futuristic city."

### **2. Movie Poster Classification**
- **Deep Learning Classification**: Classify movie posters into genres such as **Action**, **Comedy**, **Drama**, **Horror**, **Romance**, and more using a custom-trained **ResNet model** integrated into the FastAPI backend.

### **3. Metadata Generation**
- **CLIP + GPT-4**: Automatically generate detailed movie metadata, including:
    - **Title**
    - **Genre**
    - **Tagline**
    - **Mood**
    - **2-Sentence Summary**
  
  This is based on the visual features of a poster using **CLIP** for image-text matching and **GPT-4** for generating creative and meaningful metadata.

### **4. OCR (Optical Character Recognition)**
- **Text Extraction**: Extract text from movie posters, such as **movie titles**, **quotes**, and **descriptions**, enabling dynamic interaction with textual data embedded in images.

### **5. Face Detection & Recognition**
- **Detect & Recognize Faces**: Detect faces in movie posters using deep learning models. Additionally, the system can optionally recognize and verify identities based on **facial features** to enhance search and categorization.

### **6. Active Learning**
- **Feedback Loop**: Users can provide **feedback** to improve the accuracy of classification models and object detection, enabling the system to adapt and become smarter over time.


## Technologies Used
- **FastAPI**: Backend framework for creating the web API.
- **PyTorch & torchvision**: For training deep learning models and performing image classification.
- **CLIP (Contrastive Language-Image Pretraining)**: For extracting semantic features from images and generating text prompts.
- **GPT-4**: For generating creative metadata descriptions, titles, and summaries based on images.
- **Stable Diffusion**: A text-to-image generation model used to create movie posters based on text prompts.


## Screenshots

<img width="818" alt="Screenshot 2025-04-18 at 16 50 10" src="https://github.com/user-attachments/assets/4bf10aa9-8871-4f1f-a87c-3ca4eb3cf38c" />

<hr />

<img width="1113" alt="Screenshot 2025-04-20 at 15 33 45" src="https://github.com/user-attachments/assets/c1f0b43d-7dcb-4f29-aea8-f41f80a88293" />

<hr />

<img width="1077" alt="Screenshot 2025-04-20 at 06 10 10" src="https://github.com/user-attachments/assets/27b6c172-2e7a-4ab6-b4c2-dbcda4d943e0" />

<hr />





## How to Run Locally

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/visionarygpt.git
   cd visionarygpt
   ```

2. **Set up a Python environment** (using `venv` or `conda`):

   ```bash
   python3 -m venv vision-env
   source vision-env/bin/activate  # On Mac/Linux
   vision-env\Scripts\activate     # On Windows

   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (if required):

   Ensure that you have an OpenAI API key by setting up a `.env` file in the root of your project with the following content:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the FastAPI server**:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

6. **Testing the endpoints**:

## Testing the Endpoints
To test the endpoints, you can use the Swagger UI dashboard at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Here’s how to test them:

1. **POST /classify/**:
   - Input: Provide a movie poster image.
   - Output: Genre classification with confidence score.

2. **POST /metadata/**:
   - Input: Provide a movie poster image.
   - Output: Automatically generated metadata including title, genre, tagline, mood, and summary.

3. **POST /embed/**:
   - Input: Provide a movie poster image.
   - Output: Embedding of the poster in a semantic vector space for further AI tasks.

4. **POST /faces/**:
   - Input: Provide a movie poster image.
   - Output: Detected faces and their bounding boxes with confidence scores.

5. **POST /detect/**:
   - Input: Provide a movie poster image.
   - Output: Detects objects in the poster and returns bounding boxes around identified objects with confidence scores.
  
5. **POST /generate/**:
   - Input: Provide a textual prompt to generate a movie poster, along with any necessary parameters such as an uploaded image 
     file for additional context.
   - Output: A generated movie poster based on the provided prompt and image. The output will include a URL pointing to the 
   generated poster.

**Executing the Requests:**
After entering the necessary information (such as the image file path or uploading the file), click Execute. The response from the API will be displayed on the right side of the screen, showing you the classification, metadata, or results based on your image.


## Contributions
Feel free to fork this project and submit pull requests for improvements! Contributions are welcome in the following areas:
- Improving the performance of classification models.
- Enhancing metadata generation with more complex descriptions.
- Adding new features, such as automatic movie title generation.

---

## Author
**Akin Olusanya**  
iOS Engineer | ML Enthusiast | Full-Stack Creator  
workwithakin@gmail.com  
[LinkedIn](https://www.linkedin.com/in/akindeveloper)  
[GitHub](https://github.com/AkinCodes)

