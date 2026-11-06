---
created: 2026-11-06T04:00:00Z
updated: 2026-11-06T14:13:35Z
---

# Spécification Technique — WS-05 Notifications

**Réponses :** Comment les emails sont-ils construits, envoyés, et isolés des pannes ?
**Périmètre :** consolidé à la clôture de l'Epic 3 (2026-11-06), d'après US-008, US-010, US-014 et US-019. Comportement : [`ws-func-05-notifications.md`](../functional-specs/ws-func-05-notifications.md).

---

## 1. Port et adaptateurs

| Élément | Couche | Rôle |
|---|---|---|
| `IEmailSender`, `MessageEmail` (`destinataire`, `sujet`, `texte`, `html`, `repondre_a`) | `ports/email_sender.py` | Contrat d'envoi |
| `messages_email.py` (`message_confirmation`, `message_decision`, `message_remplacement`) | `bll/` | Contenu texte + HTML ; le HTML **échappe** prénom, motif et saisie du visiteur (tests à l'appui) |
| `NotifierConfirmationUseCase`, `NotifierDecisionUseCase`, `NotifierRemplacementUseCase` | `bll/` | Construisent le message et **absorbent toute exception** : journal avec la référence, la pièce et le type d'erreur seulement (ni adresse, ni message brut) |
| `ContacterSecretariatUseCase` | `bll/` | Validation, envoi au secrétariat ; l'échec **remonte** (503) |
| `ResendEmailSender` | `dal/email_adapters.py` | API REST de Resend en bibliothèque standard (`urllib`), délai 10 s, `User-Agent: fds-portail/1.0` (Resend refuse celui de urllib) |
| `ConsoleEmailSender` | `dal/email_adapters.py` | Sans `RESEND_API_KEY` : l'email est écrit dans les journaux (développement) |
| `EmailDesactive` | `dal/email_adapters.py` | `EMAIL_ENABLED` à `false`, `0`, `no` ou `non` : aucun envoi |

`creer_email_sender()` (via la dépendance `get_email_sender`) choisit l'adaptateur à chaque requête, d'après les variables d'environnement. `logging.basicConfig(INFO)` dans `main.py` : sans lui, uvicorn masquait les journaux d'envoi.

## 2. Envoi non bloquant

Les routes de soumission (WS-02), de décision (WS-04) et de remplacement (WS-03) ajoutent l'envoi en `BackgroundTasks` **après** l'enregistrement en base : la réponse HTTP part avant l'email, et une exception d'envoi ne peut ni annuler la transaction ni produire une 500 (AGENTS.md, fait critique 2). Une soumission idempotente (déjà soumise) ne renvoie pas d'email ; une décision refusée (409, 422) n'en envoie aucun.

## 3. Configuration

| Variable | Rôle |
|---|---|
| `RESEND_API_KEY` | Clé Resend (« Sending access »). Absente → console |
| `EMAIL_FROM` | Expéditeur. Par défaut `onboarding@resend.dev`, qui n'envoie qu'au titulaire du compte Resend |
| `EMAIL_ENABLED` | Interrupteur général (défaut `true`) |
| `CONTACT_EMAIL` | Secrétariat ; vide → le formulaire de contact répond 503 |
| `APP_BASE_URL` | Base des liens de suivi dans les emails |

**Production (2026-11-05)** : domaine d'envoi `fds.ctpea-prefac.me` vérifié chez Resend (Resend accepte les envois : aucune erreur dans les journaux ; réception confirmée le 2026-11-06) (DKIM `resend._domainkey.fds`, CNAME `send.fds` et `rsend.fds` vers l'infrastructure Resend, DMARC `_dmarc`). Un CNAME ne peut pas cohabiter avec un autre enregistrement de même nom : les anciens TXT et MX de `send.fds` ont dû être supprimés. Les variables sont dans `~/bravetech/.env` sur la VM, jamais dans le dépôt.

## 4. Non livré

SMS (US-016) : aucun port `ISmsSender` n'existe.

---

*ws-tech-05-notifications.md — FDS Portail — Bravetech · GL-EN3-2026*
