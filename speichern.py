import subprocess
import os

# Führt einen Git-Befehl aus und gibt die Konsolenausgabe zurück
def run_git_command(command):
    try:
        # Führen Sie den Befehl aus und erfassen Sie stdout und stderr
        result = subprocess.run(
            command, 
            shell=True, 
            check=False, # Nicht bei Fehler abbrechen, damit wir die Rückgabe prüfen können
            capture_output=True, 
            text=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", f"Ein unerwarteter Fehler ist aufgetreten: {e}"

def speichern():
    print("💾 Mission wird gespeichert...")

    # 1. Dateien hinzufügen (add)
    stdout, stderr = run_git_command("git add .")
    if stderr:
        print(f"❌ Fehler beim Hinzufügen der Dateien: {stderr}")
        return

    # 2. Commit erstellen
    # Das commit-Kommando gibt den Status zurück, den wir prüfen müssen
    stdout, stderr = run_git_command('git commit -m "Lösung gesichert"')

    if "nothing to commit" in stdout:
        print("✅ Alles gesichert! Es gab keine neuen Änderungen zum Speichern.")
    elif stderr:
        # Hier könnten echte Fehler bei der Commit-Erstellung auftreten
        print(f"❌ Fehler beim Commit: {stderr}")
        return
    else:
        # Erfolgreicher Commit
        print("✅ Änderungen wurden lokal gesichert.")

    # 3. Änderungen hochladen (push)
    print("🚀 Synchronisiere mit dem Nordpol-Tresor (Dein GitHub-Repo)...")
    
    # Wir müssen den Credential Helper neu setzen, um sicherzustellen, dass der Token
    # verwendet wird, falls der Codespace neu gestartet wurde. 
    # Wichtig: Wir nutzen den Code, der in publish_day.py funktioniert hat.
    auth_command = "git config credential.helper '!f() { echo \"username=alexfederlin\"; echo \"password=$GITHUB_TOKEN\"; }; f'"
    run_git_command(auth_command)
    
    stdout_push, stderr_push = run_git_command("git push origin main")

    if "Everything up-to-date" in stdout_push:
        # Der Fall, dass bereits alles auf GitHub ist (entsteht nach 'nothing to commit')
        if "nothing to commit" in stdout:
            print("✨ Upload bestätigt. Tresor ist aktuell.")
        else:
            # Sollte nicht passieren, aber als Fallback
            print("⚠️ Hinweis: Lokaler Commit wurde erstellt, aber der Online-Tresor war schon aktuell.")
    elif stderr_push and "fatal" in stderr_push:
        print(f"❌ Upload fehlgeschlagen. Bitte prüfe deine Internetverbindung oder GitHub-Berechtigungen.")
        print(f"   Details: {stderr_push}")
    else:
        # Erfolgreicher Push
        print("✨ Upload erfolgreich. Deine Lösung ist gesichert!")

    print("\nDu bist bereit für die nächste Mission!")


if __name__ == "__main__":
    # Dieses Skript ist nur für das Child-Repo gedacht.
    # Wir können annehmen, dass die Authentifizierung über den Codespace-Token läuft,
    # den wir hier nicht sehen, aber das Git-Kommando trotzdem ausführt.
    speichern()