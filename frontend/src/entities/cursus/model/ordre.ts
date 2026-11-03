/** Ordre des branches des maquettes ; un cursus absent de la liste passe à la fin, dans l'ordre reçu. */
const ORDRE_BRANCHES = ['genie-civil', 'genie-electromecanique', 'genie-electronique', 'architecture'];

export function trierBranches<T extends { id: string }>(branches: T[]): T[] {
  const rang = (id: string) => {
    const i = ORDRE_BRANCHES.indexOf(id);
    return i === -1 ? ORDRE_BRANCHES.length : i;
  };
  return [...branches].sort((a, b) => rang(a.id) - rang(b.id));
}
