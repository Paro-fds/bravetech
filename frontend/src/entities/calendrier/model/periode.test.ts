import assert from 'node:assert/strict';
import { test } from 'node:test';
import { candidaturesAcceptees, CHAMPS_DATES } from './types.ts';

test('le formulaire est ouvert pendant la période, ou tant qu’aucun calendrier n’est enregistré', () => {
  assert.equal(candidaturesAcceptees('ouverte'), true);
  assert.equal(candidaturesAcceptees('non_definie'), true);
  // Calendrier pas encore chargé : on ne ferme pas le formulaire par erreur, le serveur tranche
  assert.equal(candidaturesAcceptees(undefined), true);
});

test('le formulaire est fermé avant l’ouverture et après la date limite', () => {
  assert.equal(candidaturesAcceptees('a_venir'), false);
  assert.equal(candidaturesAcceptees('fermee'), false);
});

test('les dates sont dans l’ordre chronologique vérifié par le serveur', () => {
  assert.deepEqual(CHAMPS_DATES, ['date_ouverture', 'date_limite', 'date_concours', 'date_resultats', 'date_rentree']);
});
