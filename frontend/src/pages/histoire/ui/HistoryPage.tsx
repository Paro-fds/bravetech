import React from 'react';
import { Link } from 'react-router-dom';
import { CONSEIL_DE_DIRECTION } from '../../../shared/config/institution';

const REPERES: { annee: string; texte: string }[] = [
  { annee: '1902', texte: "Création de l'École des Sciences Appliquées." },
  { annee: '1905', texte: "Reconnaissance d'utilité publique." },
  { annee: '1906', texte: "Personnalité civile et droit à une subvention de l'État." },
  { annee: '1945', texte: "Affiliation à la Faculté des Sciences de l'Université d'Haïti, créée en 1944." },
  { annee: '1947', texte: "L'école devient l'École Polytechnique d'Haïti." },
  { annee: '1961', texte: "L'École Polytechnique est absorbée par la Faculté des Sciences." },
  { annee: '1986', texte: 'Passage à une direction collégiale.' },
];

/** Histoire de la Faculté (maquette « Histoire », texte fourni par la Faculté). */
export const HistoryPage: React.FC = () => (
  <>
    <section className="bg-fds-navy text-white">
      <div className="max-w-3xl mx-auto px-4 py-8 flex flex-col gap-2.5">
        <span className="self-start rounded-full bg-white/15 px-2.5 py-0.5 text-[13px] font-semibold">Depuis 1902</span>
        <h1 className="font-fds-serif text-[28px] leading-tight font-bold">Histoire de la Faculté des Sciences</h1>
        <p className="text-[#dbe6f5]">Plus d'un siècle de formation scientifique et technique en Haïti.</p>
      </div>
    </section>

    <div className="max-w-3xl w-full mx-auto px-4 py-6 flex flex-col gap-6">
      <section className="flex flex-col gap-3">
        <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">La fondation</h2>
        <p>
          Fondée en 1902 comme école privée sous le nom d'École des Sciences Appliquées, la Faculté est l'un des plus anciens
          établissements d'enseignement supérieur d'Haïti. Six professionnels haïtiens l'ont créée : l'avocat Auguste Bonamy, les
          ingénieurs Frédéric Doret, Jacques Durocher et Louis-Hérard Roy, l'ingénieur agronome Chavineau Durocher et le professeur
          Horace Ethéart.
        </p>
        <p>Son but : former des conducteurs de travaux et des directeurs d'exploitations industrielles et agricoles.</p>
      </section>

      <section className="flex flex-col gap-3.5" aria-labelledby="reperes">
        <h2 id="reperes" className="font-fds-serif text-xl font-bold text-fds-navy-d">
          Repères
        </h2>
        <ol className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3.5">
          {REPERES.map((r) => (
            <li key={r.annee} className="flex gap-3 items-start">
              <span className="min-w-14 text-center rounded-lg bg-fds-navy text-white text-sm font-bold px-2 py-1">{r.annee}</span>
              <span className="flex-1 text-sm pt-1">{r.texte}</span>
            </li>
          ))}
        </ol>
      </section>

      <section className="flex flex-col gap-3">
        <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">Une offre qui évolue</h2>
        <p>
          Au fil des décennies, la Faculté a adapté ses filières aux besoins du pays : architecture, mécanique et électricité dès
          1947, génie électromécanique (1969), génie électronique (1978), puis filières scientifiques (géologie, mathématiques,
          physique, chimie) dans les années 70-80.
        </p>
        <p>
          Ces évolutions ont accompagné de grands chantiers : barrage de Péligre, prospection minière, drainage de Port-au-Prince,
          routes nationales 1 et 2.
        </p>
      </section>

      <section className="flex flex-col gap-3">
        <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">Une gouvernance participative</h2>
        <p>
          Depuis 1986, la Faculté est dirigée collégialement. Une Assemblée mixte de professeurs et d'étudiants élit le conseil de
          direction.
        </p>
        {CONSEIL_DE_DIRECTION.confirme && (
          <div className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-1.5">
            <div className="text-sm text-fds-mute">Conseil de direction actuel</div>
            {CONSEIL_DE_DIRECTION.membres.map((nom) => (
              <div key={nom} className="font-semibold">
                {nom}
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="rounded-xl border border-[#b9cbe3] bg-fds-navy-t p-4 flex flex-col gap-2.5">
        <h2 className="font-semibold text-lg">Aujourd'hui</h2>
        <p className="text-sm">La Faculté est installée à Delmas 33 et ouvre ses candidatures en ligne.</p>
        <Link to="/postuler" className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d text-white font-semibold flex items-center justify-center">
          Rejoignez la prochaine promotion
        </Link>
        <Link to="/" className="min-h-12 px-4 rounded-lg border-2 border-fds-navy bg-white text-fds-navy font-semibold flex items-center justify-center">
          Voir les cursus
        </Link>
      </section>
    </div>
  </>
);
