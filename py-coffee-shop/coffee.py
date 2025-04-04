def percentage(percent, whole):
  return (percent * whole) / 100.0

def checkTunai(tunai, bayar):
   if (tunai):
    return True if (tunai > bayar) else False
   else:
    print("Tunai > bayar. Tekan Kembali")
    tunai = input("Tunai: ")  
    tunai = int(tunai)
    return True if (tunai > bayar) else False
    

def add_item(item):
  print("================================================================================================")
  print("Coffee Shop Sederhana")
  print("================================================================================================")
 
  total = (item["harga"] * item["jumla"])
  ppn = percentage(item["ppn"], total)

  print("Menu: ", item["paket"])
  print("Jumla Pesen: ", item["jumla"])
  print("Harga: ", item["harga"])
  print("PPN: ", ppn)
  print("================================================================================================")
  bayar = total + ppn
  print("Jumlah Bayar", bayar)
  print("================================================================================================")
  tunai = input("Tunai: ")

  if not (checkTunai (int(tunai), bayar)):
    checkTunai (int(tunai), bayar)

  kembali = int(tunai) - bayar
  
  print("================================================================================================")
  print("Tunai: ", tunai)
  print("Kembali: ", kembali)
  print("================================================================================================")
  print("Pembelian Selasai! Terimah kasih")
  return False

def main():

  while True:
    # display the menu of options
    print("================================================================================================")
    print("Coffee Shop Sederhana")
    print("================================================================================================")
    print("1. Paket A 50,000")
    print("2. Paket B 60,000")
    print("3. Paket C 70,000")
    print("4. Keluar")
    choice = int(input("Tekan Pilihan Anda: "))

    if choice == 1:
        print("================================================================================================")
        print("Paket A 50,000")
        print("================================================================================================")
        jumla = int(input("Jumla Pesenan: "))
      
        item = {
          "paket": "Paket A 50,000",
          "harga": 50000,
          "ppn": 7,
          "jumla": jumla
        }
        add_item(item)
    elif choice == 2:
        print("================================================================================================")
        print("Paket B 60,000")
        print("================================================================================================")
        jumla = int(input("Jumla Pesenan: "))
      
        item = {
          "paket": "Paket B 60,000",
          "harga": 60000,
          "ppn": 10,
          "jumla": jumla
        }
        add_item(item)
    elif choice == 3:
        print("================================================================================================")
        print("Paket C 70,000")
        print("================================================================================================")
        jumla = int(input("Jumla Pesenan: "))
        item = {
          "paket": "Paket C 70,000",
          "harga": 70000,
          "ppn": 8,
          "jumla": jumla
        }
        add_item(item)
    elif choice == 4:
      # exit the app
      break
    else:
      print("Salah Pilihan! Mohon Ulang Lagi.")

if __name__ == "__main__":
  main()