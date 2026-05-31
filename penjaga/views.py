from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import Penjaga, TongSampah, SesiAbsensi, LogPemilahan

def index(request):
    return render(request, 'penjaga/index.html')

def absensi_sukses(request):
    return render(request, 'penjaga/terimakasih.html')

@csrf_exempt
def scan_rfid(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('rfid_uid')
            
            penjaga = Penjaga.objects.get(rfid_uid=uid)
            return JsonResponse({
                'status': 'success',
                'nama': penjaga.nama,
                'penjaga_id': penjaga.id,
                'message': 'RFID Valid. Silahkan pilih role.'
            })
        except Penjaga.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'ID Card tidak terdaftar!'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def start_sesi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            penjaga1_id = data.get('penjaga_id')
            penjaga2_id = data.get('penjaga2_id')
            role_p1 = data.get('role_p1')
            role_p2 = data.get('role_p2')
            
            penjaga1 = Penjaga.objects.get(id=penjaga1_id)
            
            sesi = SesiAbsensi.objects.create(
                penjaga=penjaga1,
                role=role_p1, 
                tanggal=timezone.now().date()
            )
        
            return JsonResponse({
                'status': 'success',
                'sesi_id': sesi.id,
                'message': 'Sesi tim penjagaan berhasil dimulai!'
            })
            
        except Penjaga.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Data penjaga tidak ditemukan di database.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Gagal memproses data: {str(e)}'}, status=500)

@csrf_exempt
def scan_tong(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sesi_id = data.get('sesi_id')
            qr_code = data.get('qr_code')
            
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
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
def submit_sesi(request):
    if request.method == 'POST':
        try:
            sesi_id = request.POST.get('sesi_id')
            foto_file = request.FILES.get('foto_bukti') 
            
            sesi = SesiAbsensi.objects.get(id=sesi_id)
            sesi.waktu_selesai = timezone.now()
            sesi.foto_bukti = foto_file
            sesi.is_submitted = True
            sesi.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Absensi berhasil disubmit! Terima kasih.',
                'redirect_url': reverse('absensi_sukses')
            })
        except SesiAbsensi.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Sesi tidak ditemukan.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)