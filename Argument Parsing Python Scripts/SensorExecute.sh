
python3 ~/WindowsCodeFolder/Methane_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 1 -c /dev/ttyS46 &
# p1pid = $!
python3 ~/WindowsCodeFolder/Methane_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 2 -c /dev/ttyS48 &
# p2pid = $!
python3 ~/WindowsCodeFolder/Methane_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 3 -c /dev/ttyS49 &
# p3pid = $!
python3 ~/WindowsCodeFolder/Methane_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 4 -c /dev/ttyS50 &
# p4pid = $!
python3 ~/WindowsCodeFolder/EZO_O2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 1 -c /dev/ttyS44 &
# p5pid = $!
python3 ~/WindowsCodeFolder/EZO_O2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 2 -c /dev/ttyS59 &
# p6pid = $!
python3 ~/WindowsCodeFolder/EZO_O2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 3 -c /dev/ttyS52 &
# p7pid = $!
python3 ~/WindowsCodeFolder/EZO_O2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 4 -c /dev/ttyS53 &
# p8pid = $!
python3 ~/WindowsCodeFolder/EZO_CO2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 1 -c /dev/ttyS45 &
# p9pid = $!
python3 ~/WindowsCodeFolder/EZO_CO2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 2 -c /dev/ttyS47 &
# p10pid = $!
python3 ~/WindowsCodeFolder/EZO_CO2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 3 -c /dev/ttyS51 &
# p11pid = $!
python3 ~/WindowsCodeFolder/EZO_CO2_Argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 4 -c /dev/ttyS60 &
# p12pid = $!
python3 ~/WindowsCodeFolder/RB_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 1 -c /dev/ttyS43 &
# p13pid = $!
python3 ~/WindowsCodeFolder/PMQ_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 2 -c /dev/ttyS56 &
# p14pid = $!
python3 ~/WindowsCodeFolder/PMQ_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 3 -c /dev/ttyS54 &
# p15pid = $!
python3 ~/WindowsCodeFolder/RB_argparse.py -f /mnt/c/Users/Dan\'s\ Loaner/Documents/Compost\ Monitor/Test\ Data -n 4 -c /dev/ttyS55 &
# p16pid = $!
# cmd.exe /c start cmd.exe /c wsl.exe
# endcommand = input('type "killme" to kill this process')
# if endcommand == "killme"
#     kill p1pid p2pid p3pid p4pid p5pid p6pid p7pid p8pid p9pid p10pid p11pid p12pid p13pid p14pid p15pid p16pid