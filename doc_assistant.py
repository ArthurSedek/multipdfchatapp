'''
    Author: Arthur Sedek
    Email: Arthur.sedek@gmail.com

    DO NOT REMOVE OR MODIFY THE AUTHOR ATTRIBUTION. 
    This attribution acknowledges the efforts of the original developer. 
    Please respect and retain this information when using, modifying, or sharing this code.

    If you have questions or concerns, you're welcome to reach out via the email provided.

'''

import gradio as gr
from askpdf import AskPDF
import fitz
from PIL import Image
import os
import re
import json

class DocumentAssistant:
    def __init__(self, config_filename):
        self.CONFIGS = self.read_json_file(config_filename)
        os.environ["OPENAI_API_KEY"] = self.CONFIGS["openai_api"]
        self.app = AskPDF(self.CONFIGS)

    @staticmethod
    def read_json_file(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def insert_message(chat_log, message: str):
        if not message:
            raise gr.Exception('Provide message')
        chat_log = chat_log + [(message, '')] 
        return chat_log
    
    @staticmethod
    def sanitize_string(s):
        return re.sub('[^a-zA-Z]', '', s)
    
    @staticmethod
    def document_finder(doc_files):
        doc_files_map = {}
        for count, pdf_file in enumerate(doc_files):
            file_name = DocumentAssistant.sanitize_string(str(os.path.basename(pdf_file.name)).split(".pdf")[0])
            doc_files_map[file_name] = count
        return doc_files_map

    def retrieve_reply(self, chat_log, user_input, doc_file):
        if not doc_file:
            raise gr.Exception('Provide a PDF')   
        link_chain = self.app.query_pdf(doc_file)
        outcome = link_chain({"question": user_input, 'chat_history': self.app.conversation_log}, return_only_outputs=True)
        self.app.conversation_log += [(user_input, outcome["answer"])]
        self.app.PageNum = int(os.path.basename(list(outcome['source_documents'][0])[1][1]['source']).split('.txt')[0].split("_")[1])
        document_name = os.path.basename(list(outcome['source_documents'][0])[1][1]['source']).split('.txt')[0].split("_")[0]
        doc_files_map = DocumentAssistant.document_finder(doc_file)
        self.app.DocumentNum = doc_files_map[document_name]
        for char in outcome['answer']:
            chat_log[-1][-1] += char
        return chat_log, ''

    def display_document(self, doc_file):
        return self.show_page(doc_file, self.app.PageNum)

    def show_page(self, doc_file, page_number):
        document = fitz.open(doc_file[self.app.DocumentNum].name)
        individual_page = document[page_number]
        pixmap = individual_page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img_data = Image.frombytes('RGB', [pixmap.width, pixmap.height], pixmap.samples)
        return img_data

    def display_initial(self, doc_file):
        return self.show_page(doc_file, 0), []


    def run(self):
        Stylesheet = """
        img[alt=brandlogo] { width: 178px; height:72px;}
        img[alt=customlogo] { width: 200px; height:125px;}
        footer {visibility: hidden} flex-container {display: flex; justify-content: center; 
        align-items: center;} h1 {margin: 0; } img {margin-left: 10px;}

        """

        with gr.Blocks(css=Stylesheet) as interface:
            gr.Markdown("""![customlogo](file/resource/MYLOGO.png)""")
            
            with gr.Column():
                with gr.Row():           
                    bot_interface = gr.Chatbot(value=[], elem_id='bot_interface', label='Assistant').style(height=650)
                    view_document = gr.Image(label='Source document', tool='select').style(height=680)
            
            with gr.Row():
                with gr.Column(scale=0.80):
                    message_box = gr.Textbox(
                        show_label=False,
                        placeholder="Type here and press enter",
                    ).style(container=False)
                with gr.Column(scale=0.20):
                    upload_btn = gr.UploadButton("📁 Ask a PDF/s", file_types=[".pdf"], file_count="multiple").style()

            upload_btn.upload(fn=self.display_initial, inputs=[upload_btn], outputs=[view_document, bot_interface])
            message_box.submit(
                fn=self.insert_message,
                inputs=[bot_interface, message_box],
                outputs=[bot_interface,]
            ).success(
                fn=self.retrieve_reply,
                inputs=[bot_interface, message_box, upload_btn],
                outputs=[bot_interface, message_box]
            ).success(
                fn=self.display_document,
                inputs=[upload_btn],
                outputs=[view_document]
            )

        interface.queue()
        interface.launch()