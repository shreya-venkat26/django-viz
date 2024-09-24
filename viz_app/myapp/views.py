from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Document, Dialogue
from .forms import DocumentUploadForm
import re

def extract_proper_nouns(text):
    return re.findall(r'\b[A-Z][a-zA-Z]*\b', text)

def process_document(file, document):
    content = file.read().decode('utf-8')
    
    # Step 1: Split the content based on separator lines
    sections = re.split(r'[-]{4,}', content)  # Split on lines of 4 or more dashes
    
    dialogue_started = False  # A flag to indicate when to start parsing dialogues
    for section in sections:
        section = section.strip()
        
        if not section:
            continue
        
        # Step 2: Check if the section contains dialogues (looking for 'Next speaker')
        if 'Next speaker' in section:
            dialogue_started = True
        
        # Step 3: If dialogues started, split by "Next speaker" and parse each dialogue
        if dialogue_started:
            dialogues = re.split(r'Next speaker:\s*', section, flags=re.IGNORECASE)
            
            for idx, dialogue in enumerate(dialogues):
                dialogue = dialogue.strip()
                
                if dialogue:
                    # Step 4: Extract the speaker and dialogue text
                    speaker_match = re.match(r"^([\w\s]+):", dialogue)
                    if speaker_match:
                        speaker = speaker_match.group(1).strip()
                        dialogue_text = dialogue[len(speaker_match.group(0)):].strip()
                        proper_nouns = extract_proper_nouns(dialogue_text)
                        
                        # Step 5: Create a Dialogue entry in the database
                        Dialogue.objects.create(
                            document=document,
                            agent=speaker,
                            text=dialogue_text,
                            named_entities=", ".join(proper_nouns),
                            serial_number=idx + 1
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

def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('document_list')
