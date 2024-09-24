from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Document, Dialogue
from .forms import DocumentUploadForm
import re

def extract_proper_nouns(text):
    return re.findall(r'\b[A-Z][a-zA-Z]*\b', text)

def process_document(file, document):
    content = file.read().decode('utf-8')
    
    # splitting the content based on the separator lines
    sections = re.split(r'[-]{4,}', content)  # split on lines of 4 or more dashes
    
    # looping through each section and find the dialogues
    dialogue_started = False  # A flag to indicate when to start parsing dialogues
    for idx, section in enumerate(sections):
        section = section.strip()
        
        if not section:
            continue
        
        # checking if we are in the dialogue section
        if 'Next speaker' in section:
            dialogue_started = True
        
        if dialogue_started:
            # splitting section into dialogues by "Next speaker"
            dialogues = re.split(r'Next speaker:\s*', section, flags=re.IGNORECASE)
            
            # processing each dialogue
            for d_idx, dialogue in enumerate(dialogues):
                dialogue = dialogue.strip()
                
                if dialogue:
                    speaker_match = re.match(r"^([\w\s]+):", dialogue)
                    if speaker_match:
                        speaker = speaker_match.group(1).strip()
                        dialogue_text = dialogue[len(speaker_match.group(0)):].strip()
                        proper_nouns = extract_proper_nouns(dialogue_text)
                        
                        # creating object in sqlite3 db
                        Dialogue.objects.create(
                            document=document,
                            agent=speaker,
                            text=dialogue_text,
                            named_entities=", ".join(proper_nouns),
                            serial_number=d_idx + 1
                        )


def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document_name = form.cleaned_data['document_name']
            document_file = form.cleaned_data['document']

            document = Document.objects.create(name=document_name)

            process_document(document_file, document)
            return redirect('convo_list', document_id=document.id)
    else:
        form = DocumentUploadForm()

    return render(request, 'upload.html', {'form': form})


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})


def conversation_list(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    dialogues = document.dialogues.order_by('serial_number')
    return render(request, 'convo_list.html', {'document': document, 'dialogues': dialogues})
