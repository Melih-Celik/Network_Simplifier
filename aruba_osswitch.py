from netmiko import ConnectHandler
from time import sleep
import re

def config_backup(net_connect):
    print("Yedek alma işlemi başlatıldı...")
    command="show running-config"
    file_name_command="show running-config | include hostname"
    output = net_connect.send_command(command)
    file_name=net_connect.send_command(file_name_command).split()[1].replace('"',"")+".txt"
    open(file_name,"w").write(output)
    print("İşlem tamamlandı.Yedek dosyası oluşturuldu...")
    sleep(3)

def create_vlan(net_connect):
    vlan_id=input("Vlan ID : ")
    ports=input("Portlar : ")
    mode=input("Trunk (T) veya Access (A) : ")
    if mode=="T":
        mode="tagged"
    elif mode=="A":
        mode="untagged"
    vlan_command="""configure terminal
    vlan """+vlan_id+"""
    """+mode+" "+ports+"""
    """
    print("Lütfen Bekleyiniz...")
    try:
        net_connect.send_command(vlan_command) #Connection timeout düzelt
    except:
        pass
    net_connect.send_command("save")

def sum_vlans(net_connect):
    while True:
        vlan_ids=re.findall(r'\d+',net_connect.send_command("show vlans custom id"))
        for i in vlan_ids:
            print("Vlan "+i+" Port Durumları"+"\n-----------------------")
            port_info=net_connect.send_command("show vlans "+i+" | i agged").split()       ##Untagged or tagged
            for x in range(0,len(port_info),4):
                print("Port "+port_info[x]+" "+port_info[x+1])
            print("\n")
        end=input("Çıkmak icin 0 yazınız : ")
        if end=="0":
            print("Ana menüye yönlendiriliyorsunuz.")
            sleep(2)
            break
        else:
            continue
    