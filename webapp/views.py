from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError
from django.utils.text import slugify
from django.utils.timezone import make_aware
from .forms import CreateUserForm, LoginForm, AddRecordForm,UpdateRecordForm
from  django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import  csrf_protect
from .models import AssetRecord
from django.contrib import messages
import pandas as pd
import logging

# Create your views here.
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')




# Register a new user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
            
            return redirect('login')
    context = {'form':form}
    return render(request, 'register.html', context)


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form =LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
               
   
            return redirect('dashboard')
    
    context = {'form2':form}        
    
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    
    messages.success(request, 'You are now logged out')
    
    
    return redirect('login')

# Dashboard
@login_required(login_url='login')
def dashboard(request):
    query = request.GET.get('q')
    if query:
        my_records = AssetRecord.objects.filter(
            Q(description__icontains=query) |
            Q(asset_code__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(nomenclature__icontains=query) |
            Q(location__icontains=query) |
            Q(supplier__icontains=query)
        )
    else:
        my_records = AssetRecord.objects.all()

    context = {'my_records': my_records}
    return render(request, 'dashboard.html', context=context)
# create asset record

@login_required(login_url='login')
def create_record(request):

    form = AddRecordForm()
    if request.method == 'POST':
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record was created successfully')
            
            return redirect('dashboard')

    context = {'form':form}
    return render(request, 'create-record.html', context)

# update asset record

@login_required(login_url='login')
def update_record(request, pk):

    record = AssetRecord.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record was updated successfully')
            return redirect('dashboard')

    context = {'form':form}
    return render(request, 'update-record.html', context)

# Read/ view asset record

@login_required(login_url='login')
def singular_record(request, pk):
    all_records = AssetRecord.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'view-record.html', context)

# delete asset record

@login_required(login_url='login')
def delete_record(request, pk):

    record = AssetRecord.objects.get(id=pk)
    
    record.delete()
    messages.success(request, 'Record was deleted successfully')

    return redirect('dashboard')

# webapp/views.py

# webapp/views.py

# webapp/views.py

@csrf_protect
def upload_excel(request):
    if request.method == 'POST':
        logger.debug("Received POST request")
        logger.debug(f"Request Files: {request.FILES}")
        logger.debug(f"Request POST: {request.POST}")

        if 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)
                logger.debug(f"DataFrame loaded: {df.head()}")
                logger.debug(f"Columns in uploaded file: {df.columns}")

                # Define the mapping of Excel columns to model fields
                column_mapping = {
                    'DESCRIPTION': 'description',
                    'ASSET CODE': 'asset_code',
                    'SERIAL NUMBER (T24)': 'serial_number_t24',
                    'NUMENCLATURE': 'nomenclature',
                    'SERIAL NUMBER': 'serial_number',
                    'LOCATION': 'location',
                    'DATE PURCHASE': 'date_purchase',
                    'PRICE': 'price',
                    'UNIT': 'unit',
                    'SUPPLIER': 'supplier',
                    'WARRANTY': 'warranty',
                    'COMMENTS': 'comments',
                }

                # Check if required columns are present
                required_columns = [
                    'DESCRIPTION', 'NUMENCLATURE', 'SERIAL NUMBER', 
                    'LOCATION', 'PRICE', 'UNIT', 'DATE PURCHASE', 
                    'SUPPLIER', 'WARRANTY'
                ]
                missing_columns = [col for col in required_columns if col not in df.columns]

                if missing_columns:
                    error_message = f"Missing required columns: {', '.join(missing_columns)}"
                    logger.error(error_message)
                    return JsonResponse({'status': 'error', 'message': error_message}, status=400)

                # Parse 'DATE PURCHASE' column as date
                df['DATE PURCHASE'] = pd.to_datetime(df['DATE PURCHASE'], errors='coerce').dt.date

                # Handle price column to ensure it's numeric
                df['PRICE'] = pd.to_numeric(df['PRICE'], errors='coerce')

                for index, row in df.iterrows():
                    try:
                        # Use default date if date_purchase is NaT
                        date_purchase = row['DATE PURCHASE']
                        if pd.isna(date_purchase):
                            date_purchase = parse_date('2023-01-01')  # Example default date

                        # Create asset record
                        AssetRecord.objects.create(
                            description=row['DESCRIPTION'],
                            asset_code=row.get('ASSET CODE', ''),
                            serial_number_t24=row.get('SERIAL NUMBER (T24)', 'NOT APPLICABLE'),
                            nomenclature=row['NUMENCLATURE'],
                            serial_number=row['SERIAL NUMBER'],
                            location=row['LOCATION'],
                            price=row['PRICE'] if pd.notna(row['PRICE']) else 0.0,
                            unit=row['UNIT'],
                            date_purchase=date_purchase,
                            supplier=row['SUPPLIER'],
                            warranty=row['WARRANTY'],
                            comments=row.get('COMMENTS', '')
                        )
                    except IntegrityError as e:
                        logger.error(f"Integrity error: {e}")
                        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

                logger.debug("Excel file processed and data saved successfully")
                return redirect('dashboard')  # Redirect to dashboard after successful upload
            except Exception as e:
                logger.error(f"Error processing file: {e}")
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        else:
            logger.warning("No 'excel_file' in FILES")
    else:
        logger.warning("Received non-POST request")

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)