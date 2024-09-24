from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Document, Dialogue
from .forms import DocumentUploadForm
import re

def process_document(file, document):
    content = file.read().decode('utf-8')
    
    sections = re.split(r'[-]{4,}', content)
    print(f"Total sections found: {len(sections)}")
    
    for section_idx, section in enumerate(sections):
        section = section.strip()
        print(f"Processing section {section_idx + 1}...")

        if not section or 'Next speaker' not in section:
            print(f"Skipping section {section_idx + 1}, no 'Next speaker' found.")
            continue
        
        dialogues = re.split(r'Next speaker:\s*', section, flags=re.IGNORECASE)
        
        for idx, dialogue in enumerate(dialogues):
            dialogue = dialogue.strip()
            
            # skip empty dialogues
            if not dialogue:
                continue
            
            # Format 1: 'Next speaker: Hypothesizer'
            # Format 2: 'Hypothesizer (to chat_manager):'
            speaker_match = re.search(r"^(?:Next speaker:\s*)?([\w\s]+)(?:\s*\(.*\))?:", dialogue, flags=re.IGNORECASE)
            if speaker_match:
                speaker = speaker_match.group(1).strip()
                dialogue_text = dialogue[len(speaker_match.group(0)):].strip()
                proper_nouns = extract_proper_nouns(dialogue_text)
                
                # Create a Dialogue entry in the database
                Dialogue.objects.create(
                    document=document,
                    agent=speaker,
                    text=dialogue_text,
                    named_entities=", ".join(proper_nouns),
                    serial_number=idx + 1
                )
                print(f"Dialogue added: Speaker: {speaker}, Text: {dialogue_text[:30]}...")

# Helper function to extract proper nouns
def extract_proper_nouns(text):
    return re.findall(r'\b[A-Z][a-zA-Z]*\b', text)


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
