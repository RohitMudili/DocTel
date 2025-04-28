import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import pandas as pd
import os
import openai
import difflib
from dotenv import load_dotenv
from PIL import Image, ImageTk
import base64
from io import BytesIO

# Load environment variables and setup
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the chatbot dataset
df = pd.read_csv("chatbot_qa_data.csv")
df.dropna(subset=['question_text', 'response_text'], inplace=True)
questions = df['question_text'].str.lower().tolist()

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Post-Surgery Recovery Assistant")
        self.root.geometry("1000x800")  # Increased size to accommodate image preview
        
        # Initialize conversation history
        self.conversation_history = []
        self.current_image = None
        self.image_path = None
        
        # Color scheme
        self.colors = {
            'background': '#f5f5f5',
            'chat_bg': '#ffffff',
            'user_bg': '#e3f2fd',
            'bot_bg': '#f3e5f5',
            'input_bg': '#ffffff',
            'button_bg': '#7e57c2',
            'button_fg': '#ffffff',
            'clear_bg': '#ef5350',
            'text': '#333333',
            'alert_bg': '#ffebee',  # Light red background for alerts
            'alert_text': '#d32f2f'  # Red text for alerts
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Create main frame with padding
        self.main_frame = tk.Frame(root, bg=self.colors['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create left and right frames
        self.left_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.right_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        # Title label
        self.title_label = tk.Label(
            self.left_frame,
            text="🩺 Post-Surgery Recovery Assistant",
            font=('Arial', 16, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        self.title_label.pack(pady=(0, 10))
        
        # Chat display area with custom styling
        self.chat_display = scrolledtext.ScrolledText(
            self.left_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            bg=self.colors['chat_bg'],
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.chat_display.pack(pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Image preview area
        self.image_label = tk.Label(
            self.right_frame,
            text="Image Preview",
            bg=self.colors['background'],
            font=('Arial', 10)
        )
        self.image_label.pack(pady=(0, 5))
        
        self.image_preview = tk.Label(
            self.right_frame,
            bg=self.colors['chat_bg'],
            width=30,
            height=15
        )
        self.image_preview.pack(fill=tk.BOTH, expand=True)
        
        # Input area with custom styling
        self.input_frame = tk.Frame(self.left_frame, bg=self.colors['background'])
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Input field with custom styling
        self.user_input = tk.Entry(
            self.input_frame,
            width=60,
            font=('Arial', 10),
            bg=self.colors['input_bg'],
            relief=tk.FLAT,
            insertbackground=self.colors['text']
        )
        self.user_input.pack(side=tk.LEFT, padx=5)
        self.user_input.bind('<Return>', self.send_message)
        
        # Upload Image button
        self.upload_button = tk.Button(
            self.input_frame,
            text="📷 Upload Image",
            command=self.upload_image,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        self.upload_button.pack(side=tk.LEFT, padx=5)
        
        # Send button with custom styling
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            command=self.send_message,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button with custom styling
        self.clear_button = tk.Button(
            self.input_frame,
            text="Clear Chat",
            command=self.clear_chat,
            bg=self.colors['clear_bg'],
            fg=self.colors['button_fg'],
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        self.clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Add welcome message
        self.add_message("Bot", "🩺 Post-Surgery Recovery Assistant\nHow can I help you today?")

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.image_path = file_path
            # Display image preview
            self.display_image_preview(file_path)
            # Add message about image upload
            self.add_message("You", "📷 Image uploaded for analysis")

    def display_image_preview(self, image_path):
        # Open and resize image for preview
        image = Image.open(image_path)
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        max_width = 300
        max_height = 300
        if aspect_ratio > 1:
            new_width = min(max_width, image.width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(max_height, image.height)
            new_width = int(new_height * aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        # Update preview
        self.image_preview.configure(image=photo)
        self.image_preview.image = photo  # Keep a reference
        self.current_image = image

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def search_local_response(self, user_input):
        matches = difflib.get_close_matches(user_input.lower(), questions, n=1, cutoff=0.6)
        if matches:
            match = matches[0]
            response = df[df['question_text'].str.lower() == match]['response_text'].values[0]
            return response
        return None

    def search_openai_response(self, user_input):
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # If there's an image, try to analyze it
            if self.image_path:
                try:
                    base64_image = self.encode_image(self.image_path)
                    response = client.chat.completions.create(
                        model="gpt-4-vision-preview",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a compassionate, professional post-operative support agent specialized in helping breast cancer patients during their recovery phase. Your goal is to provide empathetic, clear, medically-informed guidance, including carefully observing images of recovery areas when shared by patients. Your responsibilities are: Offer emotional reassurance and support without making clinical judgments or definitive diagnoses. Help patients understand and monitor their recovery symptoms (pain, swelling, limited motion, emotional changes, etc.). When an image is provided, carefully review it for signs such as redness, swelling, drainage, bruising, or irregularities. If any concerning signs are observed, kindly and cautiously recommend that the patient consult their healthcare provider promptly. Gently guide patients in wound care, drain care, medication reminders, and self-care practices (nutrition, hydration, physical therapy). Provide clear explanations of what appears normal versus what could be worth medical attention — without diagnosing. Alert patients when symptoms or visual findings may require urgent medical attention (e.g., signs of infection, severe swelling, fever, excessive bleeding) and encourage them to seek professional evaluation. Provide coping strategies for emotional challenges like anxiety, sadness, or frustration. Remind patients to follow up on medical appointments, physiotherapy, or oncology checkups. Always express observations in a supportive and non-alarming tone. Important constraints: Never diagnose, prescribe medications, or suggest altering medical instructions based on images or conversation. If any uncertainty exists, advise the patient to promptly consult their surgeon or healthcare team. Always prioritize patient safety, emotional well-being, and respectful communication. Tone: Warm, supportive, patient, and encouraging. Language: Use simple, non-technical words unless the patient requests detailed medical explanations."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"Please analyze this post-surgery image and provide observations about healing progress, any visible changes, or concerning signs that might need medical attention. User question: {user_input}"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=500
                    )
                    response_text = response.choices[0].message.content.strip()
                    response_text += "\n\n⚠️ IMPORTANT: This is not a medical diagnosis. Please consult your healthcare provider for professional medical advice and confirmation."
                except Exception as e:
                    # If image analysis fails, provide a helpful message
                    response_text = "I understand you've shared an image, but I'm currently unable to analyze it. For your safety and proper medical guidance, I recommend:\n\n1. Consulting your healthcare provider about any concerns\n2. Taking notes about any changes you observe\n3. Keeping track of any symptoms or changes in your recovery\n\nWould you like to discuss your recovery progress or ask any other questions about post-surgery care?"
            
            else:
                # Regular text conversation
                messages = [
                    {"role": "system", "content": "You are a compassionate, professional post-operative support agent specialized in helping breast cancer patients during their recovery phase. Your goal is to provide empathetic, clear, and medically-informed guidance. Your responsibilities are: Offer emotional reassurance and support without making clinical judgments. Help patients understand and monitor their recovery symptoms (pain, swelling, limited motion, emotional changes, etc.). Gently guide patients in wound care, drain care, medication reminders, and self-care practices (nutrition, hydration, physical therapy). Alert patients when symptoms may require urgent medical attention (e.g., signs of infection, severe swelling, fever, excessive bleeding) and advise them to contact their healthcare provider. Provide coping strategies for emotional challenges like anxiety, sadness, or frustration. Remind patients to follow up on medical appointments and therapy (e.g., physiotherapy, oncology follow-up). Adapt your tone: always be kind, respectful, non-judgmental, and calm. Important constraints: Never diagnose, prescribe medication, or suggest altering medical instructions. If a question falls outside general recovery support, encourage the patient to consult their doctor. Always prioritize patient safety and emotional well-being."}
                ]
                messages.extend(self.conversation_history)
                
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=150
                )
                response_text = response.choices[0].message.content.strip()
            
            # Add assistant's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": response_text})
            
            return response_text
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Please try again or contact your healthcare provider for immediate assistance."

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip():
            self.add_message("You", user_message, is_user=True)
            self.user_input.delete(0, tk.END)
            
            # Try local response first
            response = self.search_local_response(user_message)
            if not response:
                self.add_message("Bot", "Let me check that for you...")
                response = self.search_openai_response(user_message)
            
            self.add_message("Bot", response)

    def contains_urgent_medical_alert(self, message):
        # Keywords that indicate urgent medical attention
        alert_keywords = [
            'urgent', 'emergency', 'immediately', 'seek medical attention',
            'call your doctor', 'contact your healthcare provider',
            'seek immediate medical help', 'go to the emergency room',
            'call 911', 'seek emergency care'
        ]
        return any(keyword.lower() in message.lower() for keyword in alert_keywords)

    def add_message(self, sender, message, is_user=False):
        self.chat_display.config(state=tk.NORMAL)
        
        # Configure tags for different message styles
        self.chat_display.tag_configure('user', background=self.colors['user_bg'])
        self.chat_display.tag_configure('bot', background=self.colors['bot_bg'])
        self.chat_display.tag_configure('alert', background=self.colors['alert_bg'], foreground=self.colors['alert_text'])
        
        # Insert message with appropriate styling
        if is_user:
            self.chat_display.insert(tk.END, f"{sender}: ", 'user')
            self.chat_display.insert(tk.END, f"{message}\n\n", 'user')
        else:
            self.chat_display.insert(tk.END, f"{sender}: ", 'bot')
            # Check if message contains urgent medical alert
            if self.contains_urgent_medical_alert(message):
                self.chat_display.insert(tk.END, "⚠️ URGENT: ", 'alert')
                self.chat_display.insert(tk.END, f"{message}\n\n", 'alert')
            else:
                self.chat_display.insert(tk.END, f"{message}\n\n", 'bot')
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        # Clear conversation history and image
        self.conversation_history = []
        self.current_image = None
        self.image_path = None
        self.image_preview.configure(image='')
        self.add_message("Bot", "🩺 Post-Surgery Recovery Assistant\nHow can I help you today?")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop() 