from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import BadRequest
import os
import json
import requests
import docx
from io import BytesIO

from django.shortcuts import render
from django.http import HttpResponseBadRequest
import docx
from detector import OpenaiDetector
import re

from django.contrib.auth.decorators import login_required


@login_required
def file_upload(request):
    if request.method == 'POST':
        try:
            avoid_file = request.FILES['avoid_file']
            avoid_file_name = avoid_file.name
            suff = ('.doc', '.docx')
            if avoid_file_name.lower().endswith(suff):
                # Read the document in chunks of 500 words each
                doc = docx.Document(avoid_file)
                chunks = []
                chunk = ''
                for para in doc.paragraphs:
                    # Split the paragraph into words
                    words = para.text.split()
                    for word in words:
                        if len(chunk.split()) < 7000:
                            chunk += ' ' + word
                        else:
                            chunks.append(chunk.strip())
                            chunk = word
                if chunk:
                    chunks.append(chunk.strip())

                # Process each chunk with the detector function
                results = []
                bearer_token = 'Bearer sess-n8NoM0b6HQnaBAr4jvICiKrYpKFKfFsZyhw4upHy'
                od = OpenaiDetector(bearer_token)
                for chunk in chunks:
                    try:
                        response = od.detect(chunk)
                        prob = response['AI-Generated Probability']
                        if re.search(r'\d', str(prob)):
                            # Response contains at least one digit, include it
                            results.append(prob)
                    except:
                        # Skip current chunk if an error occurs
                        pass

                # Calculate the weighted mean average
                total_words = sum(len(chunk.split()) for chunk in chunks)
                avg_prob_fake = round(sum(prob * len(chunk.split()) / total_words for prob in results),1)

                return render(request, 'checker/file_processed.html', {"avg_prob_fake":avg_prob_fake})
            else:
                return HttpResponse('Неверный формат файла')
        except Exception as e:
            return HttpResponseBadRequest(str(e))

    return render(request, 'checker/file_upload.html')



def file_processed(request):
    return render(request, 'checker/file_processed.html')