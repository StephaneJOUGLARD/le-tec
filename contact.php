<?php
// Formulaire de contact TEC — compatible hébergement mutualisé OVH (fonction mail()).
// Adresse de réception à adapter si besoin :
$destinataire = 'contact@le-tec.fr';
$expediteur   = 'no-reply@le-tec.fr'; // doit être une adresse du domaine le-tec.fr

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: contact.html'); exit; }
if (!empty($_POST['site_web'])) { header('Location: merci.html'); exit; } // anti-spam (pot de miel)

function champ($k, $max = 3000) { return trim(mb_substr(strip_tags($_POST[$k] ?? ''), 0, $max)); }
$nom = champ('nom', 120); $societe = champ('societe', 160); $email = champ('email', 160);
$tel = champ('tel', 40); $profil = champ('profil', 120); $mission = champ('mission', 120); $message = champ('message');

if ($nom === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || empty($_POST['rgpd'])) {
  http_response_code(400);
  echo '<!DOCTYPE html><meta charset="utf-8"><p>Merci de renseigner votre nom, un e-mail valide, votre message et d\'accepter la politique de confidentialité. <a href="contact.html">Retour au formulaire</a></p>';
  exit;
}
$sujet = '=?UTF-8?B?' . base64_encode('[le-tec.fr] Demande de ' . $nom . ($societe ? ' — ' . $societe : '')) . '?=';
$corps = "Nouvelle demande depuis le site le-tec.fr\n\n"
       . "Nom : $nom\nSociété : $societe\nE-mail : $email\nTéléphone : $tel\nProfil : $profil\nMission : $mission\n\nMessage :\n$message\n";
$entetes = "From: TEC site web <$expediteur>\r\nReply-To: $email\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n";
@mail($destinataire, $sujet, $corps, $entetes, '-f' . $expediteur);
header('Location: merci.html');
