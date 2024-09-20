import io
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

def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']
            # Read and decode the document (assuming it's a text file)
            content = document.read().decode('utf-8')

            # Split the content based on dashes as the delimiter for speech bubbles
            speech_segments = content.split('Next Speaker')  # Change from underscores to dashes

            for segment in speech_segments:
                # Each segment corresponds to an agent's speech, parse it further if necessary
                lines = segment.strip().split("\n")
                if len(lines) > 1:
                    agent_name = lines[0].strip()  # Assuming the agent's name is in the first line
                    dialogue_text = "\n".join(lines[1:]).strip()  # The rest is dialogue

                    # Create or get the Agent object
                    agent, _ = Agent.objects.get_or_create(name=agent_name)

                    # Save each dialogue as a new entry in the database
                    Dialogue.objects.create(
                        agent=agent,
                        text=dialogue_text,
                        timestamp=timezone.now()
                    )

            return redirect('convo_list')
    else:
        form = DocumentUploadForm()

    return render(request, 'upload.html', {'form': form})

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


