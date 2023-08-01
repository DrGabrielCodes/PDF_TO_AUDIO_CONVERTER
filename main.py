# %%
# imports all requirements
import pyttsx3, PyPDF2, os, time

# %%
# Gets an input path from the user
pdf_input = input("Enter the relative path of the pdf file, Eg: './PDF_files/piano_guide.pdf': , ./PDF_files/30-days-of-react-ebook-fullstackio.pdf ")
react_pdf_path = "./PDF_files/30-days-of-react-ebook-fullstackio.pdf"
esotropia_path = "./PDF_files/Accommodative-esotropia.pdf" 

print(pdf_input)

# %%
page_waiting = " Going to the next page in 3 second. "

# A funtion that extracts text from any PDF
def get_text_from_pdf(pdf_path):
    # To open a PDF, do the following
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Code to extract text from PDF
        master_list = []
        for page_num in range( len(pdf_reader.pages)):
            clean_text_list = pdf_reader.pages[page_num].extract_text().strip().replace("\n", " ") #This gets each page  and then extracts its text from it, strippiing down new line marks and unnecessary spaces at end of the page.
            master_list.append(clean_text_list)
            clean_text = page_waiting.join(master_list)
            #print(clean_text)
    return clean_text
print(len(get_text_from_pdf(pdf_input)))


# %%
def get_file_name(pdf_path):
    global name, extenx
    file_name = os.path.basename(pdf_path)
    name, extenx = os.path.splitext(file_name)
    return name


def onEnd_page_waiting(name, completed = True):
    print("finishing: ", name, completed)
    if name == page_waiting:
        time.sleep(3)
    else:
        pass
    
print(get_file_name(pdf_input))

# %%
def create_audio():
    # Next is to call our speaker to read the clean text
    # Intitialize a speaker
    try:
        # Initializes the speaker
        speaker = pyttsx3.init()
        voice_id ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        # Gets the file name and the name to save audio file as
        get_file_name(pdf_input) # returns the name of the file without an extension
        text_to_speak = get_text_from_pdf(pdf_input)
        list_of_text_to_speak = text_to_speak.split(page_waiting)
        audio_file = f"./audios/{name}.mp3"
        # Checks if the audio file exists in the directory and then runs the code for creating one if it doesn't exist
        if os.path.exists(audio_file):
            print(f"An {audio_file} already exists for this PDF in the desired directory.")
        else:
            speaker.setProperty("voice", voice_id)
            speaker.setProperty("rate", 140)
            speaker.connect(page_waiting, onEnd_page_waiting(page_waiting))
            
            speaker.save_to_file(text_to_speak, audio_file)
            speaker.runAndWait()
            speaker.stop()
            print(f"The audio file {audio_file} has been successfully created")
    except Exception as e:
        print(f"Oops! Something went wrong. The audio file {audio_file} can not be created because {e}.")
    finally:
        voices = speaker.getProperty("voices")
        for voice in voices:
            print( "ID: %s" %voice.id)

create_audio()

# %%
