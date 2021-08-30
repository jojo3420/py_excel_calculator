import pandas
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd


# Create your views here.
def calculate(request):
    file = request.FILES['user_input_file']
    df: pandas.DataFrame = pd.read_excel(file, header=0)
    # data = df.loc[[0, 1, 2, 3], ['value']]
    temp_data = {}
    domain_list = []
    for row_t in df.itertuples():
        # print(row_t)
        _idx, grade, name, email, value = row_t
        # print(grade, name, email, value)
        temp_data.setdefault(grade, [])
        temp_data[grade].append(value)
        domain = email.split('@')[1]
        domain_list.append(domain)

    # print(data)
    result = {}
    for grade, values in temp_data.items():
        part = {}
        part['min'] = min(values)
        part['max'] = max(values)
        part['avg'] = sum(values) / len(values)
        result[grade] = part

    print(result)
    data = {'domain_list': domain_list, 'excel_data': result}

    # return HttpResponse('calculate page')
    return render(request, 'main/result.html', data)
