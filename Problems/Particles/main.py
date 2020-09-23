spin = input()
charge = input()

if spin == '1/2':
    if charge == '-1/3':
        print('Strange Quark')
    elif charge == '2/3':
        print('Charm Quark')
    elif charge == '-1':
        print('Electron Lepton')
    elif charge == '0':
        print('Neutrino Lepton')
elif spin == '1':
    if charge == '0':
        print('Photon Boson')
