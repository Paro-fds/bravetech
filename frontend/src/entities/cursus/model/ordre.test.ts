import assert from 'node:assert/strict';
import { test } from 'node:test';
import { trierBranches } from './ordre.ts';

const ids = (liste: { id: string }[]) => liste.map((c) => c.id);

test('les branches suivent l\'ordre des maquettes, quel que soit l\'ordre reçu', () => {
  const recues = [{ id: 'architecture' }, { id: 'genie-civil' }, { id: 'genie-electronique' }, { id: 'genie-electromecanique' }];
  assert.deepEqual(ids(trierBranches(recues)), ['genie-civil', 'genie-electromecanique', 'genie-electronique', 'architecture']);
});

test('une branche inconnue passe à la fin sans être perdue', () => {
  const recues = [{ id: 'nouvelle-branche' }, { id: 'architecture' }, { id: 'genie-civil' }];
  assert.deepEqual(ids(trierBranches(recues)), ['genie-civil', 'architecture', 'nouvelle-branche']);
});

test('la liste reçue n\'est pas modifiée', () => {
  const recues = [{ id: 'architecture' }, { id: 'genie-civil' }];
  trierBranches(recues);
  assert.deepEqual(ids(recues), ['architecture', 'genie-civil']);
});
