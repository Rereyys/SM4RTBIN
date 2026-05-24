import os
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.utils import timezone
from django.conf import settings

class Penjaga(models.Model):
    rfid_uid = models.CharField(max_length=50, unique=True, verbose_name="RFID UID")
    nama = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nama} ({self.rfid_uid})"


class TongSampah(models.Model):
    qr_code = models.CharField(max_length=100, unique=True, verbose_name="QR/Barcode ID")
    lokasi_atau_tipe = models.CharField(max_length=100, blank=True, help_text="Misal: Tong Organik Gedung A")
    
    gambar_qr = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"Tong {self.qr_code} - {self.lokasi_atau_tipe}"

    def save(self, *args, **kwargs):
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        
        qr.add_data(self.qr_code)
        qr.make(fit=True)

       
        img = qr.make_image(fill_color="black", back_color="white")
        
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qr-{self.qr_code}.png'
        
        self.gambar_qr.save(filename, File(buffer), save=False)
        
        super().save(*args, **kwargs)


class SesiAbsensi(models.Model):
    ROLE_CHOICES = [
        ('pencatat', 'Pencatat Absensi Siswa'),
        ('pengawas', 'Membantu/Mengawas Pemilahan'),
    ]
    penjaga = models.ForeignKey(Penjaga, on_delete=models.CASCADE, related_name='sesi_berjalan')
    tanggal = models.DateField(default=timezone.now)
    waktu_mulai = models.DateTimeField(auto_now_add=True)
    waktu_selesai = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    foto_bukti = models.ImageField(upload_to='bukti_absensi/', null=True, blank=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"Sesi {self.penjaga.nama} - {self.tanggal}"


class LogPemilahan(models.Model):
    sesi_absensi = models.ForeignKey(SesiAbsensi, on_delete=models.CASCADE, related_name='log_sampah')
    tong_sampah = models.ForeignKey(TongSampah, on_delete=models.CASCADE)
    waktu_scan = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sesi_absensi', 'tong_sampah')