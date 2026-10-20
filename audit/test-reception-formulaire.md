# Test de réception du formulaire CWA — à exécuter après autorisation

Aucun envoi externe n'a été effectué pendant les audits. Le fonctionnement local est testé avec interception de l'événement `submit` et blocage des requêtes externes : ces contrôles ne prouvent pas la réception d'un e-mail.

## Préparation

- Confirmer l'autorisation d'envoyer **une demande de test** au formulaire Formspree configuré dans `contact.html` (`https://formspree.io/f/myzwearj`).
- Choisir une adresse e-mail sous le contrôle du propriétaire pour vérifier aussi la possibilité de répondre. Ne pas utiliser une adresse client.
- Prévenir le propriétaire de l'heure prévue et ouvrir la boîte de réception destinataire ainsi que le compte Formspree, si disponible.
- Utiliser le marqueur `TEST-CWA-RECEPTION-20261020` dans le nom et le message pour retrouver la demande.

## Vérification manuelle prévue

1. Ouvrir la page de contact dans un navigateur mobile ou avec une largeur de 390 px. Vérifier que le formulaire et tous ses labels sont visibles.
2. Vérifier les champs obligatoires et le rejet d'une adresse invalide. Puis saisir une demande valide avec les seules coordonnées de test autorisées ; laisser le téléphone facultatif vide.
3. Envoyer une seule fois. Relever l'heure, l'URL affichée après l'envoi et le statut de la requête POST dans les outils réseau. Une page de succès seule ne prouve pas l'arrivée en boîte mail.
4. Vérifier la présence du marqueur dans Formspree et dans la boîte destinataire, y compris les indésirables. Contrôler le nom, l'adresse, l'activité, le message, le choix de rédaction et la localisation.
5. Vérifier que le destinataire de la réponse correspond à l'adresse de test. N'envoyer une réponse que si cela a également été autorisé.
6. Noter le résultat, le délai constaté et les éventuels blocages de quota, d'activation, de filtrage ou de CSP. Supprimer ensuite les données de test selon les pratiques du propriétaire.

## Résultat à compléter

| Élément | Résultat |
|---|---|
| Autorisation et date du test réel | En attente |
| Validation locale du formulaire | Réussie, sans envoi |
| POST accepté par le service | Non testé |
| Demande visible dans Formspree | Non testé |
| E-mail reçu dans la boîte attendue | Non testé |
| Champs et adresse de réponse corrects | Non testé |

La procédure est préparée ; elle n'autorise ni ne déclenche d'envoi automatiquement.
