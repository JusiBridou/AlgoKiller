#!/usr/bin/env python3
import argparse
import csv
import os
import random
import smtplib
import ssl
from email.message import EmailMessage
from typing import Dict, List, Tuple


def _normalize(s: str) -> str:
    return (s or "").strip().lower()


def load_participants(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
        reader = csv.DictReader(f, dialect=dialect)
        if not reader.fieldnames:
            raise ValueError("Fichier CSV sans en-têtes.")
        headers = {_normalize(h): h for h in reader.fieldnames}
        name_key = headers.get("name") or headers.get("nom")
        email_key = headers.get("email") or headers.get("mail")
        if not name_key or not email_key:
            raise ValueError("Le CSV doit contenir des colonnes 'name/nom' et 'email/mail'.")
        participants = []
        for row in reader:
            name = (row.get(name_key) or "").strip()
            email = (row.get(email_key) or "").strip()
            if not name or not email:
                continue
            participants.append({"name": name, "email": email})
        if len(participants) < 2:
            raise ValueError("Il faut au moins 2 participants.")
        return participants


def load_missions(missions_path: str) -> List[str]:
    with open(missions_path, "r", encoding="utf-8") as f:
        missions = [line.strip() for line in f if line.strip()]
    if not missions:
        raise ValueError("La liste des missions est vide.")
    return missions


def assign_targets_and_missions(
    participants: List[Dict[str, str]], missions: List[str], rng: random.Random
) -> Tuple[List[Dict[str, str]], Dict[str, str]]:
    if len(missions) < len(participants):
        raise ValueError("Il doit y avoir au moins autant de missions que de cibles.")

    targets = participants[:]  # same people as targets
    rng.shuffle(targets)

    # One single assignment loop. If someone gets themselves, end game.
    for i, participant in enumerate(participants):
        if _normalize(participant["name"]) == _normalize(targets[i]["name"]):
            raise ValueError(
                "Attribution invalide: un participant a obtenu sa propre cible. "
                "Relancez plus tard pour recommencer le jeu."
            )

    rng.shuffle(missions)
    target_to_mission = {t["email"]: missions[i] for i, t in enumerate(targets)}

    assignments = []
    for i, participant in enumerate(participants):
        target = targets[i]
        mission = target_to_mission[target["email"]]
        assignments.append(
            {
                "participant_name": participant["name"],
                "participant_email": participant["email"],
                "target_name": target["name"],
                "mission": mission,
            }
        )

    return assignments, target_to_mission


def build_email(subject: str, sender: str, recipient: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(body)
    return msg


def send_emails(assignments: List[Dict[str, str]], smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str, sender: str, subject: str) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_password)
        for a in assignments:
            body = (
                f"Salut {a['participant_name']},\n\n"
                f"Ta cible: {a['target_name']}\n"
                f"Mission associée à ta cible: {a['mission']}\n\n"
                "Rappel: pas de violence, pas de mise en danger.\n"
            )
            msg = build_email(subject, sender, a["participant_email"], body)
            server.send_message(msg)


def write_assignments_csv(assignments: List[Dict[str, str]], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["participant_name", "participant_email", "target_name", "mission"],
        )
        writer.writeheader()
        writer.writerows(assignments)


def main() -> int:
    parser = argparse.ArgumentParser(description="Générateur de Killer (jeu non-violent)")
    parser.add_argument("--participants", required=True, help="CSV des participants (nom+email)")
    parser.add_argument("--missions", required=True, help="Fichier texte des missions (1 par ligne)")
    parser.add_argument("--seed", type=int, default=None, help="Graine aléatoire optionnelle")
    parser.add_argument("--dry-run", action="store_true", help="N'envoie pas d'email")
    parser.add_argument("--output", help="Chemin CSV pour exporter les attributions")

    parser.add_argument("--smtp-host", default=os.getenv("SMTP_HOST"))
    parser.add_argument("--smtp-port", type=int, default=int(os.getenv("SMTP_PORT", "587")))
    parser.add_argument("--smtp-user", default=os.getenv("SMTP_USER"))
    parser.add_argument("--smtp-password", default=os.getenv("SMTP_PASSWORD"))
    parser.add_argument("--sender", default=os.getenv("SMTP_SENDER"))
    parser.add_argument("--subject", default="Ta cible et ta mission")

    args = parser.parse_args()

    participants = load_participants(args.participants)
    missions = load_missions(args.missions)
    rng = random.Random(args.seed)
    assignments, _ = assign_targets_and_missions(participants, missions, rng)

    if args.output:
        write_assignments_csv(assignments, args.output)

    if args.dry_run:
        print(f"Attributions générées: {len(assignments)} (dry-run)")
        return 0

    missing = [
        name
        for name, value in [
            ("smtp-host", args.smtp_host),
            ("smtp-user", args.smtp_user),
            ("smtp-password", args.smtp_password),
            ("sender", args.sender),
        ]
        if not value
    ]
    if missing:
        raise ValueError(
            "Configuration SMTP incomplète. Utilisez --dry-run ou fournissez: "
            + ", ".join(missing)
        )

    send_emails(
        assignments,
        smtp_host=args.smtp_host,
        smtp_port=args.smtp_port,
        smtp_user=args.smtp_user,
        smtp_password=args.smtp_password,
        sender=args.sender,
        subject=args.subject,
    )

    print(f"Emails envoyés: {len(assignments)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
