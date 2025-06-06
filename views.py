from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import AssetsForm,AssetTypeForm,BranchForm,DepartmentForm,AllocationForm
from .models import Assets, DamagedAssets,AssetType,Branch,Department,Allocation
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.


def index(request):
    #return HttpResponse("Hello from the Inventory app!")
    return render(request, 'inventory/base.html')

#def signup(request):
    #return render(request, 'inventory/signup.html')

#def login(request):
    #return render(request, 'inventory/login.html')


def add_asset(request):
    if request.method == 'POST':
        form = AssetsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_asset')  # or another page like 'assets_list'
    else:
        form = AssetsForm()

    return render(request, 'inventory/add_asset.html', {'form': form})



def asset_list(request):
    assets = Assets.objects.all()
    return render(request, 'inventory/asset_list.html', {'assets': assets})


@require_POST
def mark_as_damaged(request, asset_id):
    asset = get_object_or_404(Assets, id=asset_id)

    # Copy data to DamagedAssets
    DamagedAssets.objects.create(
        asset_type=asset.asset_type,
        brand_model=asset.brand_model,
        serial_number=asset.serial_number,
        supplier_name=asset.supplier_name,
        contact_name=asset.contact_name,
        contact_cell=asset.contact_cell,
        purchase_date=asset.purchase_date,
        warranty_start_date=asset.warranty_start_date,
        warranty_expiry_date=asset.warranty_expiry_date,
        po_date=asset.po_date,
        comments=asset.comments
    )

    # Delete original asset
    asset.delete()

    return redirect('asset_list')

def damaged_asset_list(request):
    damaged = DamagedAssets.objects.all()
    return render(request, 'inventory/damaged_asset_list.html', {'damaged_assets': damaged})


def add_asset_type(request):
    if request.method == 'POST':
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('asset_type_list')  # or wherever you want
    else:
        form = AssetTypeForm()
    return render(request, 'inventory/add_asset_type.html', {'form': form})


def asset_type_list(request):
    asset_types = AssetType.objects.all()
    return render(request, 'inventory/asset_type_list.html', {'asset_types': asset_types})



def delete_asset_type(request, pk):
    asset_type = get_object_or_404(AssetType, pk=pk)
    asset_type.delete()
    return redirect('asset_type_list')


def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'inventory/branch_list.html', {'branches': branches})

def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = BranchForm()
    return render(request, 'inventory/add_branch.html', {'form': form})



def delete_branch(request, branch_id):
    branch = get_object_or_404(Branch, id=branch_id)
    branch.delete()
    return redirect('branch_list')

def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'inventory/add_department.html', {'form': form})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'inventory/department_list.html', {'departments': departments})


def delete_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    department.delete()
    return redirect('department_list')


from .models import Assets, DamagedAssets, Allocation  # Ensure Allocation is imported

def asset_list(request):
    assets = Assets.objects.all()
    total_assets = assets.count()
    total_damaged = DamagedAssets.objects.count()
    total_allocated = Allocation.objects.count()
    total_all_assets = total_assets + total_damaged + total_allocated

    context = {
        'assets': assets,
        'total_assets': total_assets,
        'total_allocated': total_allocated,
        'total_damaged': total_damaged,
        'total_all_assets': total_all_assets,
    }
    return render(request, 'inventory/asset_list.html', context)


def update_asset(request, asset_id):
    asset = get_object_or_404(Assets, id=asset_id)
    if request.method == 'POST':
        form = AssetsForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('asset_list')
    else:
        form = AssetsForm(instance=asset)

    return render(request, 'inventory/update_asset.html', {'form': form, 'asset': asset})


def delete_asset(request, asset_id):
    asset = get_object_or_404(Assets, id=asset_id)
    asset.delete()
    return redirect('asset_list')



def allocate_asset(request, asset_id):
    asset = get_object_or_404(Assets, id=asset_id)

    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)

            # Copy asset fields to allocation
            allocation.asset_type = asset.asset_type.name
            allocation.brand_model = asset.brand_model
            allocation.serial_number = asset.serial_number
            allocation.supplier_name = asset.supplier_name
            allocation.contact_name = asset.contact_name
            allocation.contact_cell = asset.contact_cell
            allocation.purchase_date = asset.purchase_date
            allocation.warranty_start_date = asset.warranty_start_date
            allocation.warranty_expiry_date = asset.warranty_expiry_date
            allocation.po_date = asset.po_date
            allocation.comments = asset.comments

            allocation.save()
            asset.delete()  # Remove asset from original table

            return redirect('asset_list')
    else:
        form = AllocationForm()

    return render(request, 'inventory/allocate_asset.html', {'form': form, 'asset': asset})

def allocated_assets(request):
    from datetime import date
    allocations = Allocation.objects.all()
    today = date.today()
    return render(request, 'inventory/allocated_assets.html', {'allocations': allocations, 'today': today})




def deallocate_asset(request, allocation_id):
    allocation = get_object_or_404(Allocation, id=allocation_id)

    # Add back to Assets
    asset_type_obj, _ = AssetType.objects.get_or_create(name=allocation.asset_type)

    Assets.objects.create(
        asset_type=asset_type_obj,
        brand_model=allocation.brand_model,
        serial_number=allocation.serial_number,
        supplier_name=allocation.supplier_name,
        contact_name=allocation.contact_name,
        contact_cell=allocation.contact_cell,
        purchase_date=allocation.purchase_date,
        warranty_start_date=allocation.warranty_start_date,
        warranty_expiry_date=allocation.warranty_expiry_date,
        po_date=allocation.po_date,
        comments=allocation.comments
    )

    allocation.delete()
    return redirect('allocated_assets')

def update_maintenance(request, allocation_id):
    allocation = get_object_or_404(Allocation, id=allocation_id)
    if request.method == 'POST':
        form = AllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            return redirect('allocated_assets')
    else:
        form = AllocationForm(instance=allocation)

    return render(request, 'inventory/update_maintenance.html', {'form': form, 'allocation': allocation})



# Permanently delete damaged asset
def delete_damaged_asset(request, asset_id):
    asset = get_object_or_404(DamagedAssets, id=asset_id)
    asset.delete()
    return redirect('damaged_asset_list')

# Move back to Assets table
def restore_damaged_asset(request, asset_id):
    damaged = get_object_or_404(DamagedAssets, id=asset_id)
    
    # Get or create AssetType object
    asset_type_obj, _ = AssetType.objects.get_or_create(name=damaged.asset_type)

    # Create new Asset
    Assets.objects.create(
        asset_type=asset_type_obj,
        brand_model=damaged.brand_model,
        serial_number=damaged.serial_number,
        supplier_name=damaged.supplier_name,
        contact_name=damaged.contact_name,
        contact_cell=damaged.contact_cell,
        purchase_date=damaged.purchase_date,
        warranty_start_date=damaged.warranty_start_date,
        warranty_expiry_date=damaged.warranty_expiry_date,
        po_date=damaged.po_date,
        comments=damaged.comments
    )

    # Delete from DamagedAssets
    damaged.delete()
    return redirect('asset_list')

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('index')  # redirect to dashboard
            else:
                form.add_error(None, "You are not authorized to access the admin section.")
    else:
        form = AuthenticationForm()
    return render(request, 'inventory/admin_login.html', {'form': form})

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep session active
            return redirect('index')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'inventory/change_password.html', {'form': form})

