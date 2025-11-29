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
        
        # Bei Fehlern (außer Warnungen) wird None zurückgegeben, wenn fail_on_error=True
        if result.stderr and "warning" not in result.stderr.lower():
            if fail_on_error:
                # Wir geben den Fehler hier aus, aber die Funktion kehrt zurück, 
                # was zur Fehlerbehandlung im Hauptteil führt.
                print(f"❌ Fehler bei Ausführung: {result.stderr.strip()}")
                return None, result.stderr.strip() 
        
        # Normaler Rückgabewert (stdout und stderr als Strings)
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        print(f"Ein unerwarteter Systemfehler ist aufgetreten: {e}")
        return None, str(e)

# --- Hauptfunktion zur Missionsladung ---
def mission_control():
    print("-------------------------------------------------------")
    print("💾 1/3: LÖSUNGEN VOM VORTAG SICHERN...")
    print("-------------------------------------------------------")

    # 1. Dateien hinzufügen (add)
    run_git_command("git add .")
    
    # 2. Commit erstellen
    stdout_commit, stderr_commit = run_git_command('git commit -m "Lösung gesichert"', fail_on_error=False)

    if stdout_commit and "nothing to commit" in stdout_commit:
        print("✅ Alles gesichert! Es gab keine neuen Änderungen zum Speichern.")
    elif stderr_commit and "fatal" in stderr_commit:
        # Hier könnten echte Commit-Fehler auftreten
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
    
    # NEU: Wir setzen fail_on_error auf False, da Git die Erfolgsmeldung oft in stderr schreibt.
    stdout_push, stderr_push = run_git_command("git push origin main", fail_on_error=False) 

    # Kombinieren der Ausgaben, um den Status sicher zu prüfen (da Git output auf beiden Kanälen sein kann)
    push_output = (stdout_push or "") + (stderr_push or "")
    
    # Überprüfung des Erfolgsstatus
    if "Everything up-to-date" in push_output or "nothing to commit" in stdout_commit:
        print("✨ Upload bestätigt. Dein Tresor ist aktuell.")
    elif "main -> main" in push_output:
        # Dies fängt die erfolgreiche Meldung ab, die zuvor zum Fehler geführt hat
        print("✨ Upload erfolgreich. Deine Lösung ist gesichert!")
    elif "fatal" in push_output:
        print(f"❌ Upload fehlgeschlagen. Bitte um Hilfe bitten: {push_output}")
        return
    else:
        # Erfolgreicher Push, aber keine spezifische Meldung gefunden
        print("✨ Upload erfolgreich. Deine Lösung ist gesichert!")


    # 4. Neue Mission holen (pull)
    print("\n📡 3/3: NEUE MISSION HERUNTERLADEN & ZUSAMMENFÜHREN (PULL)...")
    
    # FIX: Wir setzen fail_on_error auf False, da Git Pull/Fetch-Meldungen oft in stderr landen.
    stdout_pull, stderr_pull = run_git_command("git pull upstream main", fail_on_error=False)

    # Kombinierte Ausgabe prüfen
    pull_output = (stdout_pull or "") + (stderr_pull or "")
    
    if "Merge made by" in pull_output or "Already up to date" in pull_output:
        # Hier landet die Meldung, wenn es ein Fast-Forward-Merge war oder nichts Neues da war.
        print(pull_output)
        print("\n✅ MISSIONS-UPDATE ERFOLGREICH!")
        print("-------------------------------------------------------")
        print("🚀 Starte mit der neuen Mission! (Ordner: XX_Dezember)")
        print("-------------------------------------------------------")
    elif "FETCH_HEAD" in pull_output and "fatal" not in pull_output.lower():
        # Dies fängt die erfolgreiche Fetch-Meldung ab, die zuvor zum Fehler geführt hat.
        print(pull_output)
        print("\n✅ MISSIONS-UPDATE ERFOLGREICH (Fetch abgeschlossen)! Starte mit der neuen Mission.")
        print("-------------------------------------------------------")
        print("🚀 Starte mit der neuen Mission! (Ordner: XX_Dezember)")
        print("-------------------------------------------------------")
    elif "MERGE_MSG" in pull_output:
        # Dieser Fall tritt auf, wenn es eine manuelle Bestätigung (MERGE_MSG) braucht.
        print(pull_output)
        print("\n⚠️ WICHTIG: Prüfe, ob sich ein 'MERGE_MSG' Fenster geöffnet hat.")
        print("Schließe es, um den Prozess abzuschließen, falls nötig.")
    elif "fatal" in pull_output:
         print(f"❌ FEHLER BEIM HERUNTERLADEN: {pull_output}")
    else:
        # Sonstiger unklarer Status
        print(pull_output)
        print("\n⚠️ Download erfolgreich, aber Status unklar. Prüfe die Ordner!")
    
    print("-------------------------------------------------------")


if __name__ == "__main__":
    # FIX: Sicherstellen, dass die korrekte Funktion aufgerufen wird
    mission_control()