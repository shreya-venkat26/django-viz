import io
import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from .forms import DocumentUploadForm
from .models import Agent, Dialogue

# Create your views here.
def conversation_list(request):
    dialogues = Dialogue.objects.order_by('timestamp')
    return render(request, 'convo_list.html', {'dialogues': dialogues})

def process_document(file):
    content = file.read().decode('utf-8')
    dialogues = content.split('\n_____________________________\n')

    for dialogue in dialogues:
        lines = dialogue.strip().split('\n')
        if len(lines) > 1:
            agent_name = lines[0].strip()
            text = '\n'.join(lines[1:]).strip()
            agent, created = Agent.objects.get_or_create(name=agent_name)
            Dialogue.objects.create(agent=agent, text=text)

def extract_proper_nouns(text):
    # Simple regex to find capitalized words, which we'll assume are proper nouns
    return re.findall(r'\b[A-Z][a-z]*\b', text)

def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']
            content = document.read().decode('utf-8')

            # Split the content using "Next Speaker" as the delimiter
            speech_segments = content.split("Next Speaker")

            for idx, segment in enumerate(speech_segments, 1):
                segment = segment.strip()  # Clean up white spaces
                if segment:
                    lines = segment.split("\n")
                    dialogue_text = " ".join(lines).strip()

                    # Extract proper nouns from the speech
                    proper_nouns = extract_proper_nouns(dialogue_text)

                    # Create the dialogue entry in the database (no need for agent here)
                    Dialogue.objects.create(
                        agent=None,  # Optional, since we're focusing on text bubbles
                        text=dialogue_text,
                        timestamp=timezone.now(),
                        serial_number=idx,
                        proper_nouns=", ".join(proper_nouns)
                    )

            return redirect('conversation_list')
    else:
        form = DocumentUploadForm()

    return render(request, 'upload_document.html', {'form': form})

def conversation_list(request):
    dialogues = Dialogue.objects.all().order_by('serial_number')  # Fetch by order of speech
    return render(request, 'convo_list.html', {'dialogues': dialogues})