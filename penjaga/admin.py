from django.contrib import admin
from .models import Penjaga, TongSampah, SesiAbsensi, LogPemilahan

@admin.register(Penjaga)
class PenjagaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'rfid_uid')
    search_fields = ('nama', 'rfid_uid')

@admin.register(TongSampah)
class TongSampahAdmin(admin.ModelAdmin):
    list_display = ('qr_code', 'lokasi_atau_tipe')
    search_fields = ('qr_code', 'lokasi_atau_tipe')

@admin.register(SesiAbsensi)
class SesiAbsensiAdmin(admin.ModelAdmin):
    list_display = ('penjaga', 'tanggal', 'role', 'waktu_mulai', 'waktu_selesai', 'is_submitted')
    list_filter = ('tanggal', 'role', 'is_submitted')
    readonly_fields = ('waktu_mulai', 'waktu_selesai')

@admin.register(LogPemilahan)
class LogPemilahanAdmin(admin.ModelAdmin):
    list_display = ('sesi_absensi', 'tong_sampah', 'waktu_scan')
    list_filter = ('waktu_scan',)