import subprocess
import os

# --- Hilfsfunktion zum Ausführen von Git-Befehlen ---
def run_git_command(command, fail_on_error=True):
    # Führt einen Git-Befehl aus und gibt die Konsolenausgabe zurück
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=False,
            capture_output=True, 
            text=True
        )
        # Wenn ein Fehler auftritt, der nicht nur eine Warnung ist, geben wir ihn aus
        if result.stderr and "warning" not in result.stderr.lower():
            if fail_on_error:
                print(f"❌ Fehler bei Ausführung: {result.stderr.strip()}")
                return None, result.stderr.strip()
        
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        print(f"Ein unerwarteter Systemfehler ist aufgetreten: {e}")
        return None, str(e)

# --- Hauptfunktion zur Missionsladung ---
def mission_laden():
    print("-------------------------------------------------------")
    print("💾 1/3: LÖSUNGEN VOM VORTAG SICHERN...")
    print("-------------------------------------------------------")

    # 1. Dateien hinzufügen (add)
    run_git_command("git add .")
    
    # 2. Commit erstellen
    stdout_commit, stderr_commit = run_git_command('git commit -m "Lösung gesichert"', fail_on_error=False)

    if "nothing to commit" in stdout_commit:
        print("✅ Alles gesichert! Es gab keine neuen Änderungen zum Speichern.")
    elif stderr_commit:
        # Hier könnten echte Commit-Fehler auftreten (z.B. LFS-Hooks, die hoffentlich weg sind)
        print(f"❌ Fehler beim Commit: {stderr_commit}")
        return
    else:
        # Erfolgreicher Commit
        print("✅ Änderungen wurden lokal gesichert.")

    # 3. Änderungen hochladen (push)
    print("\n🚀 2/3: SYNCHRONISIERE MIT DEM NORDPOL-TRESOR (PUSH)...")
    
    # Git Credential Helper erneut setzen, um Token-Probleme zu vermeiden
    auth_command = "git config credential.helper '!f() { echo \"username=alexfederlin\"; echo \"password=$GITHUB_TOKEN\"; }; f'"
    run_git_command(auth_command)
    
    stdout_push, stderr_push = run_git_command("git push origin main")

    if "Everything up-to-date" in stdout_push or "nothing to commit" in stdout_commit:
        print("✨ Upload bestätigt. Dein Tresor ist aktuell.")
    elif stderr_push and "fatal" in stderr_push:
        print(f"❌ Upload fehlgeschlagen. Bitte um Hilfe bitten: {stderr_push}")
        return
    else:
        print("✨ Upload erfolgreich. Deine Lösung ist gesichert!")

    # 4. Neue Mission holen (pull)
    print("\n📡 3/3: NEUE MISSION HERUNTERLADEN & ZUSAMMENFÜHREN (PULL)...")
    
    # Führt den Pull aus. Dank devcontainer.json wird pull.rebase=false verwendet.
    stdout_pull, stderr_pull = run_git_command("git pull upstream main")
    
    if stdout_pull:
        print(stdout_pull)
        if "Merge made by" in stdout_pull or "Already up to date" in stdout_pull:
            print("\n✅ MISSIONS-UPDATE ERFOLGREICH!")
            print("-------------------------------------------------------")
            print("🚀 Starte mit der neuen Mission! (Ordner: XX_Dezember)")
            print("-------------------------------------------------------")
        elif "MERGE_MSG" in stdout_pull:
            # Dieser Fall sollte nach dem Pull auftreten, wenn es einen Konflikt oder eine manuelle Bestätigung gab.
            print("\n⚠️ WICHTIG: Prüfe, ob sich ein 'MERGE_MSG' Fenster geöffnet hat.")
            print("Schließe es, um den Prozess abzuschließen, falls nötig.")
        else:
            print("\n⚠️ Download erfolgreich, aber Status unklar. Prüfe die Ordner!")
    elif stderr_pull:
        print(f"❌ FEHLER BEIM HERUNTERLADEN: {stderr_pull}")
    
    print("-------------------------------------------------------")


if __name__ == "__main__":
    mission_laden()