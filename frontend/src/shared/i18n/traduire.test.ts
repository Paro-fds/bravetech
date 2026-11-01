import assert from 'node:assert/strict';
import { test } from 'node:test';
import { codeHtml, interpoler, langueValide, traduire } from './traduire.ts';

const FR = { 'a.titre': 'Bonjour', 'a.compteur': '{n} pièces sur {total}', 'a.seulFr': 'Texte français' };
const KR = { 'a.titre': 'Bonjou', 'a.compteur': '{n} pyès sou {total}' };

test('le français est utilisé quand la langue active est le français', () => {
  assert.equal(traduire('a.titre', 'fr', FR, KR), 'Bonjour');
});

test('le créole est utilisé quand la clé existe', () => {
  assert.equal(traduire('a.titre', 'kr', FR, KR), 'Bonjou');
});

test('une clé manquante en créole retombe sur le français', () => {
  assert.equal(traduire('a.seulFr', 'kr', FR, KR), 'Texte français');
});

test('tant que le dictionnaire créole n\'est pas chargé, le français s\'affiche', () => {
  assert.equal(traduire('a.titre', 'kr', FR, null), 'Bonjour');
});

test('une clé inconnue des deux langues s\'affiche telle quelle', () => {
  assert.equal(traduire('a.inconnue', 'kr', FR, KR), 'a.inconnue');
});

test('les variables sont interpolées dans les deux langues', () => {
  assert.equal(traduire('a.compteur', 'fr', FR, KR, { n: 3, total: 5 }), '3 pièces sur 5');
  assert.equal(traduire('a.compteur', 'kr', FR, KR, { n: 3, total: 5 }), '3 pyès sou 5');
});

test('un marqueur sans valeur est laissé tel quel, et 0 est une valeur', () => {
  assert.equal(interpoler('{a} et {b}', { a: 0 }), '0 et {b}');
});

test('l\'attribut lang du créole haïtien est « ht »', () => {
  assert.equal(codeHtml('kr'), 'ht');
  assert.equal(codeHtml('fr'), 'fr');
});

test('une valeur mémorisée invalide donne le français', () => {
  assert.equal(langueValide('kr'), 'kr');
  for (const v of ['en', '', null, undefined, 42, 'KR']) assert.equal(langueValide(v), 'fr');
});
