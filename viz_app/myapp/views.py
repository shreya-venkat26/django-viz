import io
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import DocumentUploadForm
from .models import Agent, Dialogue

# Create your views here.
def conversation_list(request):
    dialogues = Dialogue.objects.order_by('timestamp')
    return render(request, 'conversation_list.html', {'dialogues': dialogues})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['document']
            process_document(file)
            return HttpResponseRedirect(reverse('conversation_list'))
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