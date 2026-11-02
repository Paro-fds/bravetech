import assert from 'node:assert/strict';
import { test } from 'node:test';
import { attributTheme, themeEffectif, themeValide } from './theme.ts';

test('sans choix enregistré, le thème suit la préférence système', () => {
  assert.equal(themeEffectif(null, true), 'sombre');
  assert.equal(themeEffectif(null, false), 'clair');
});

test('un choix enregistré l\'emporte sur la préférence système', () => {
  assert.equal(themeEffectif('clair', true), 'clair');
  assert.equal(themeEffectif('sombre', false), 'sombre');
});

test('une valeur mémorisée invalide vaut « pas de choix »', () => {
  assert.equal(themeValide('sombre'), 'sombre');
  assert.equal(themeValide('clair'), 'clair');
  assert.equal(themeValide('dark'), null);
  assert.equal(themeValide(null), null);
  assert.equal(themeValide('{"state":{}}'), null);
});

test('le mode sombre pose data-theme="dark" sur <html>', () => {
  assert.equal(attributTheme('sombre'), 'dark');
  assert.equal(attributTheme('clair'), 'light');
});
