from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Penjaga, TongSampah, SesiAbsensi, LogPemilahan

def index(name):
    return render(name, 'core/index.html')

def index(request):
    return render(request, 'penjaga/index.html')

@csrf_exempt
def scan_rfid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        uid = data.get('rfid_uid')
        
        try:
            penjaga = Penjaga.objects.get(rfid_uid=uid)
            return JsonResponse({
                'status': 'success',
                'nama': penjaga.nama,
                'penjaga_id': penjaga.id,
                'message': 'RFID Valid. Silahkan pilih role.'
            })
        except Penjaga.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'ID Card tidak terdaftar!'}, status=404)

@csrf_exempt
def start_sesi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        penjaga_id = data.get('penjaga_id')
        role = data.get('role')
        
        penjaga = Penjaga.objects.get(id=penjaga_id)


        sesi = SesiAbsensi.objects.create(
            penjaga=penjaga,
            role=role,
            tanggal=timezone.now().date()
        )
        
        return JsonResponse({
            'status': 'success',
            'sesi_id': sesi.id,
            'message': f'Sesi berhasil dimulai sebagai {sesi.get_role_display()}'
        })

@csrf_exempt
def scan_tong(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sesi_id = data.get('sesi_id')
        qr_code = data.get('qr_code')
        
        try:
            sesi = SesiAbsensi.objects.get(id=sesi_id, is_submitted=False)
            tong = TongSampah.objects.get(qr_code=qr_code)
            
            
            sudah_dipilah = LogPemilahan.objects.filter(sesi_absensi=sesi, tong_sampah=tong).exists()
            
            if sudah_dipilah:
                return JsonResponse({
                    'status': 'warning',
                    'message': f'Peringatan! Tong {tong.lokasi_atau_tipe} ({qr_code}) sudah dipilah sebelumnya!'
                }, status=200) 
                
            
            LogPemilahan.objects.create(sesi_absensi=sesi, tong_sampah=tong)
            
            total_dipilah = LogPemilahan.objects.filter(sesi_absensi=sesi).count()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Tong {tong.lokasi_atau_tipe} berhasil didata.',
                'total_dipilah': total_dipilah
            })
            
        except TongSampah.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'QR Code Tong Sampah tidak dikenal!'}, status=404)
        except SesiAbsensi.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sesi tidak aktif atau sudah di-submit.'}, status=400)

@csrf_exempt
def submit_sesi(request):
    if request.method == 'POST':
        sesi_id = request.POST.get('sesi_id')
        foto_file = request.FILES.get('foto_bukti') 
        try:
            sesi = SesiAbsensi.objects.get(id=sesi_id)
            sesi.waktu_selesai = timezone.now()
            sesi.foto_bukti = foto_file
            sesi.is_submitted = True
            sesi.save()
            
            return JsonResponse({'status': 'success', 'message': 'Absensi berhasil disubmit! Terima kasih.'})
        except SesiAbsensi.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sesi tidak ditemukan.'}, status=404)