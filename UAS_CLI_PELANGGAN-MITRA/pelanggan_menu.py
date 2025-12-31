from utils import clear_screen, press_enter
from database_makanan import load_makanan, linear_search_makanan
from rekomendasi_makanan import menu_rekomendasi
from transaksi import order_makanan
from auth import get_profil_lengkap, edit_profil_lengkap, get_user_by_username

def menu_pelanggan(user):
    while True:
        clear_screen()
        print(f"=== PELANGGAN: {user['nama']} ===")
        print("1. Lihat Profil")
        print("2. Lihat Katalog Makanan")
        print("3. Rekomendasi Makanan")
        print("4. Order Makanan (Simulasi)")
        print("0. Logout")

        pilih = input("Pilih: ").strip()

        if pilih == "1":
            clear_screen()
            from auth import (
                get_profil_lengkap,
                get_user_by_username,
                edit_profil_lengkap
            )
        
            user_baru = get_user_by_username(user["username"])
            profil = get_profil_lengkap(user["username"])
        
            print("=== PROFIL PELANGGAN ===")
            print(f"Nama          : {user_baru['nama']}")
            print(f"Username      : {user_baru['username']}")
        
            if profil:
                print(f"Email         : {profil['email']}")
                print(f"No HP         : {profil['no_hp']}")
                print(f"Alamat        : {profil['alamat']}")
                print(f"Jenis Kelamin : {profil['jenis_kelamin']}")
        
            print("\n1. Lengkapi / Edit Data Diri")
            print("2. Kembali")
            sub = input("Pilih: ").strip()
        
            if sub == "1":
                data = get_profil_lengkap(user["username"])
        
                clear_screen()
                print("=== EDIT DATA DIRI ===")
        
                email = input(f"Email [{data['email']}]: ") or data["email"]
                no_hp = input(f"No HP [{data['no_hp']}]: ") or data["no_hp"]
                alamat = input(f"Alamat [{data['alamat']}]: ") or data["alamat"]
                jk = input(f"Jenis Kelamin [{data['jenis_kelamin']}]: ") or data["jenis_kelamin"]
        
                edit_profil_lengkap(user["username"], {
                    "email": email,
                    "no_hp": no_hp,
                    "alamat": alamat,
                    "jenis_kelamin": jk
                })
        
                user.update(get_user_by_username(user["username"]))
        
                print("\nData diri berhasil diperbarui.")
                press_enter()

        elif pilih == "2":
            clear_screen()
            df = load_makanan()
            if df.empty:
                print("Belum ada data makanan.")
            else:
                print(df[["nama","restoran","kalori","harga"]].assign(no=range(1, len(df) + 1))[["no","nama","restoran","kalori","harga"]].to_string(index=False))
            print("\n1. Cari makanan")
            print("2. Kembali")
            sub = input("Pilih: ").strip()
            if sub == "1":
                keyword = input("Masukkan nama makanan yang dicari: ").strip()
                
                if not keyword:
                    print("Kata kunci pencarian tidak boleh kosong.")
                    press_enter()
                else:
                    hasil = linear_search_makanan(df, keyword)
    
                if hasil.empty:
                    print("Makanan tidak ditemukan.")
                else:
                    print("\nHasil Pencarian:")
                    print(
                        hasil[["nama", "restoran", "kalori", "harga"]]
                        .assign(no=range(1, len(hasil) + 1))
                        [["no", "nama", "restoran", "kalori", "harga"]]
                        .to_string(index=False)
                    )
            
            press_enter()

        elif pilih == "3":
            clear_screen()
            menu_rekomendasi()

        elif pilih == "4":
            clear_screen()
            order_makanan()

        elif pilih == "0":
            break

        else:
            print("Pilihan tidak valid.")
            press_enter()
