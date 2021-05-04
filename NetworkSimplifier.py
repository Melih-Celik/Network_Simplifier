from netmiko import ConnectHandler
import time
from getpass import getpass
import aruba_osswitch as module

cihaz_menu="""
Hangi cihazda islem yapilacak
1.Aruba Switch
2.Cisco Switch
3.Alcatel Switch\n
Secim : """

islem_menu="""
Yapılacak İşlemi seçin : 
0.Ana Menüye Dön.
1.Config yedek Al.
2.Vlan Ac.
3.Vlan Durumunu özetle.\n
Secim : """

cihazlar={"1":"aruba_osswitch","2":"cisco_ios","3":"alcatel"}
islemler={"1":"config_backup","2":"create_vlan","3":"sum_vlans"}

def space():
    for i in range(20):
        print("\n")

def redir_to_sw(cihaz_secim,ip_address,username,password):
    switch = {
            "device_type": cihaz_secim,
            "ip": ip_address,
            "username": username,
            "password": password,
        }
    print("Bağlantı kuruluyor.")
    net_connect=ConnectHandler(**switch)
    space()
    while True:
        print("İşlem yapılan cihaz : "+ip_address+" "+cihaz_secim)
        islem_secim=input(islem_menu)
        if islem_secim=="0":
            space()
            break
        space()
        method_to_call=getattr(module,islemler[islem_secim])
        method_to_call(net_connect)
        space()

while True:
    cihaz_secim=cihazlar[input(cihaz_menu)]
    space()
    ip_address=input("Ip adresi : ")
    username=input("Username : ")
    password=getpass()
    space()
    redir_to_sw(cihaz_secim,ip_address,username,password)
    print("İşlem tamamlanmıştır.Ana menüye yönlendiriliyorsunuz...")
    time.sleep(3)