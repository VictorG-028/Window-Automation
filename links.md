# Links used to learn something

TODO arrumar isso

""" Links úteis:
Changing working directory to the folder this script is in.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

Como pegar o título de uma janela
    https://superuser.com/questions/378790/how-to-get-window-title-in-windows-from-shell
    Lista de processos -> tasklist /v /FO:CSV
    Todos os títulos de janela existentes -> Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id, Name, mainWindowtitle -AutoSize
    Título da janela com PID -> (Get-Process -id <PID_AKI> -ErrorAction SilentlyContinue).MainWindowTitle
"""
