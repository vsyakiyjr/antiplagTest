import json

from django.shortcuts import render
from .models import Report
from .models import Comment
from django.http import HttpResponse
from urllib.parse import quote
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
import gzip, os, docx
# from avoid.views import name_the_file

USER_FOLDER = ''
ROOT_FOR_USER_FOLDERS = 'files/user_folders/'


def display_user_reports(request):
    # user = request.user
    file_list = Report.objects.all()[:5]
    return render(request, "reports/reports_list_new.html", {"file_list": file_list})


# def download_file(request, file_id):
#     file = Report.objects.get(id=file_id)
#     response = HttpResponse(file.file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(file.name)}.docx'
#     return response


def download_file(request, report_id):
    report = Report.objects.get(id=report_id)
    file_type = request.POST.get('file_type')
    if file_type == 'original_doc':
        response = HttpResponse(report.original_doc, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    elif file_type == 'report':
        response = HttpResponse(report.report, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    elif file_type == 'file':
        response = HttpResponse(report.file, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    else:
        return HttpResponse('Invalid file type', status=400)
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{quote(report.name)}.docx'
    return response


def unpack_gz_file(report_id):
    report = Report.objects.get(id=report_id)
    gz_file = report.pickles
    with gzip.open(gz_file, "rb") as f:
        pickles = pkl.load(f)
        for filename, data in pickles.items():
            output_filename = USER_FOLDER + filename
            with open(output_filename, "wb") as f:
                pkl.dump(data, f)


def check_AI():
    pass


def check_avoid():
    pass


def check_plagiarism():
    pass


def open_report(request, report_id):
    global USER_FOLDER
    USER_FOLDER = ROOT_FOR_USER_FOLDERS + request.user.username + '/'
    if not os.path.exists(USER_FOLDER):
        os.mkdir(USER_FOLDER)
    report = Report.objects.get(id=report_id)
    #######
    report_id = 474                           # 474 – report.id для теста
    #######
    unpack_gz_file(report_id)
    check_AI()
    check_avoid()
    check_plagiarism()
    with open(USER_FOLDER + 'json_final.pkl', 'rb') as f:
        json_final = pkl.load(f)
        
    # return JsonResponse(json_final)
    doc = docx.Document('media/origianl_docs/Статья_ККСОН_jStCJYh.docx')
    doc_text = ""
    for paragraph in doc.paragraphs:
        doc_text += paragraph.text + " NewParagraph "
        
    with open('output.json', 'w') as file:
        json.dump(doc_text, file)

    json_final['result_json'] = json.loads(json_final['result_json'])
    json_final['spell_check'] = json.loads(json_final['spell_check'])
    json_final['seo_check'] = json.loads(json_final['seo_check'])
    json_final['result_json']['doc_text'] = doc_text
    
    return render(request=request,
                  template_name='reports/report.html',
                  context={'json': json_final})
    


@login_required
@require_POST
def save_comments(request):
    comments = request.POST.getlist('comments')
    if not comments:
        return JsonResponse({'error': 'No comments provided'})
    for comment in comments:
        # if 'id' not in comment or 'text' not in comment or 'report' not in comment or 'position' not in comment or 'deleted' not in comment:
            # return JsonResponse({'error': 'Invalid comment format'})
        id = comment['id']
        text = comment['text']
        report = comment['report']
        position = comment['position']
        deleted = comment['deleted']
        # if not text or position < 0:
            # return JsonResponse({'error': 'Invalid comment data'})
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            comment = Comment(text=text, author=request.user, report=report, position=position, deleted=deleted)
            comment.save()
        else:
            # comment.last_edited_by = request.user
            comment.text = text
            comment.report = report
            comment.position = position
            comment.deleted = deleted
            comment.save()
    return JsonResponse({'success': 'Comments saved'})


@require_GET
def get_comments(request):
    report = request.GET.get('report')
    # if not report:
        # return JsonResponse({'error': 'No report id provided'})
    comments = Comment.objects.filter(report=report, deleted=False)
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'text': comment.text,
            'author': comment.author.username,
            'position': comment.position,
            'deleted': comment.deleted
        })
    return JsonResponse({'comments': comments_data})


import pickle as pkl


def name_the_report(request):
    # date = datetime.now().strftime("%d.%m.%y")
    # client_time = localtime(now()).strftime("%d.%m.%y")
    date = str(request.date)
    USER_FOLDER = 'files/user folders/' + request.user.username
    with open(USER_FOLDER + "file_name.pkl", "rb") as f:
        doc_name = pkl.load(f)
    file_name = ''.join(doc_name.split('.')[:-1]) + ' — ' + date
    return file_name


def create_report(request):
    # input_docx = USER_FOLDER + 'plagiarism_report.docx'
    # doc.save(input_docx)

    # plag_report_name = name_the_file(username, 'plagiarism_report')
    # date_time = datetime.now().strftime("%d.%m.%y %H:%M")
    # # date_time = localtime(now()).strftime("%d.%m.%y %H:%M")
    # report = Report(name=plag_report_name, user=user, date_str=date_time)
    # with open(USER_FOLDER + 'plagiarism_report.docx', 'rb') as f:
    #     report_file = File(f)
    #     report.file.save(plag_report_name + '.docx', report_file)
    #     report_file.close()
    report_name = name_the_report(request)
    Report.objects.create(name=report_name, user=request.user)
    # report = Report(name=report_name, user=request.user)
    # report.save()


def save_report(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        # report_name = request.POST.get('report_name')
        # report_file = request.FILES.get('report_file')
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return HttpResponse('Report not found', status=404)
        # report.name = report_name
        # report.file = report_file
        report.save()
        return HttpResponse('Report saved successfully')
    else:
        return HttpResponse('Method not allowed', status=405)