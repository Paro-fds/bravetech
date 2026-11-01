import React, { useState } from 'react';
import { Check, Clock, Mail, MapPin, Phone, TriangleAlert } from 'lucide-react';
import { contactApi, extraireErreursContact, type ErreursContact } from '../../../entities/contact';
import { ApiError } from '../../../shared/api/client';
import { INSTITUTION } from '../../../shared/config/institution';

const QUESTIONS = [
  { q: 'Dois-je me déplacer pour candidater ?', r: 'Non. Le dossier, les pièces et le suivi se font en ligne.' },
  { q: 'Le paiement est-il réel ?', r: "Non, pour l'instant il s'agit d'une simulation. Aucun argent n'est prélevé." },
  { q: "J'ai perdu ma référence de dossier.", r: "Écrivez-nous avec votre nom et l'email utilisé pour candidater." },
];

const CLASSE_CHAMP =
  'w-full min-h-12 rounded-lg border-[1.5px] bg-white px-3 text-base text-fds-ink focus:outline-none focus:ring-2 focus:ring-fds-navy';

function messageErreur(erreur: unknown): string {
  if (erreur instanceof ApiError) {
    if (erreur.status === 429) return 'Vous avez envoyé plusieurs messages. Patientez quelques minutes avant de réessayer.';
    if (erreur.status === 503) return "Votre message n'a pas pu être envoyé pour le moment. Votre texte est conservé : réessayez dans quelques minutes.";
  }
  return "Envoi impossible. Vérifiez votre connexion : votre texte est conservé, vous pouvez réessayer.";
}

const Coordonnee: React.FC<{ icone: React.ReactNode; titre: string; valeur: string }> = ({ icone, titre, valeur }) => (
  <div className="flex gap-3 items-start">
    <span className="text-fds-navy shrink-0 pt-0.5">{icone}</span>
    <div>
      <div className="font-semibold">{titre}</div>
      <div className="text-sm text-fds-mute">{valeur}</div>
    </div>
  </div>
);

const Champ: React.FC<{ id: string; libelle: string; erreur?: string; children: (p: { id: string; className: string; 'aria-invalid': boolean; 'aria-describedby'?: string }) => React.ReactNode }> = ({
  id,
  libelle,
  erreur,
  children,
}) => (
  <div className="flex flex-col gap-1.5">
    <label htmlFor={id} className="text-[15px] font-semibold">
      {libelle}
    </label>
    {children({
      id,
      className: `${CLASSE_CHAMP} ${erreur ? 'border-fds-bad' : 'border-fds-field'}`,
      'aria-invalid': Boolean(erreur),
      'aria-describedby': erreur ? `${id}-erreur` : undefined,
    })}
    {erreur && (
      <p id={`${id}-erreur`} role="alert" className="text-sm font-semibold text-fds-bad">
        {erreur}
      </p>
    )}
  </div>
);

/** Contact et accès (maquette « Contact »). Les coordonnées non fournies par la Faculté ne sont pas affichées. */
export const ContactPage: React.FC = () => {
  const [nom, setNom] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [robot, setRobot] = useState('');
  const [erreurs, setErreurs] = useState<ErreursContact>({});
  const [erreurGlobale, setErreurGlobale] = useState<string | null>(null);
  const [enCours, setEnCours] = useState(false);
  const [envoye, setEnvoye] = useState(false);

  const envoyer = async (e: React.FormEvent) => {
    e.preventDefault();
    const locales: ErreursContact = {};
    if (nom.trim().length < 2) locales.nom = 'Indiquez votre nom.';
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.trim())) locales.email = 'Indiquez une adresse email valide.';
    if (message.trim().length < 10) locales.message = 'Votre message est trop court (10 caractères minimum).';
    setErreurs(locales);
    setErreurGlobale(null);
    if (Object.keys(locales).length) return;

    setEnCours(true);
    try {
      await contactApi.envoyer({ nom, email, message, site_web: robot });
      setEnvoye(true);
      setNom('');
      setEmail('');
      setMessage('');
    } catch (erreur) {
      // Le texte saisi est conservé : on ne vide rien en cas d'échec
      const champs = extraireErreursContact(erreur);
      if (champs) setErreurs(champs);
      else setErreurGlobale(messageErreur(erreur));
    } finally {
      setEnCours(false);
    }
  };

  return (
    <div className="max-w-3xl w-full mx-auto px-4 py-6 flex flex-col gap-[22px]">
      <section className="flex flex-col gap-2">
        <h1 className="font-fds-serif text-2xl font-bold text-fds-navy-d">Contact et accès</h1>
        <p className="text-fds-mute">Une question sur votre candidature ? Écrivez-nous, vous n'avez pas besoin de venir.</p>
      </section>

      <section className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3.5" aria-label="Coordonnées">
        <Coordonnee icone={<MapPin className="w-5 h-5" aria-hidden="true" />} titre="Adresse" valeur={INSTITUTION.adresse} />
        {INSTITUTION.telephone && <Coordonnee icone={<Phone className="w-5 h-5" aria-hidden="true" />} titre="Téléphone" valeur={INSTITUTION.telephone} />}
        {INSTITUTION.email && <Coordonnee icone={<Mail className="w-5 h-5" aria-hidden="true" />} titre="Email" valeur={INSTITUTION.email} />}
        {INSTITUTION.horaires && <Coordonnee icone={<Clock className="w-5 h-5" aria-hidden="true" />} titre="Horaires du secrétariat" valeur={INSTITUTION.horaires} />}
      </section>

      <section className="flex flex-col gap-3">
        <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">Questions fréquentes</h2>
        {QUESTIONS.map((item) => (
          <div key={item.q} className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-1.5">
            <h3 className="font-semibold">{item.q}</h3>
            <p className="text-sm text-fds-mute">{item.r}</p>
          </div>
        ))}
      </section>

      {envoye ? (
        <section className="rounded-xl border border-[#9bd3b2] bg-fds-ok-bg p-5 flex flex-col gap-2.5 items-start text-fds-ok" role="status">
          <span className="flex items-center gap-2 font-semibold text-lg">
            <Check className="w-6 h-6" aria-hidden="true" />
            Message envoyé
          </span>
          <p className="text-sm">Merci. Le secrétariat vous répondra à l'adresse email indiquée.</p>
          <button type="button" onClick={() => setEnvoye(false)} className="min-h-11 underline font-semibold">
            Écrire un autre message
          </button>
        </section>
      ) : (
        <form onSubmit={envoyer} noValidate className="rounded-xl border border-fds-line bg-white p-4 flex flex-col gap-3.5">
          <h2 className="font-fds-serif text-xl font-bold text-fds-navy-d">Nous écrire</h2>
          <Champ id="contact-nom" libelle="Votre nom" erreur={erreurs.nom}>
            {(p) => <input {...p} autoComplete="name" value={nom} onChange={(e) => setNom(e.target.value)} />}
          </Champ>
          <Champ id="contact-email" libelle="Votre email" erreur={erreurs.email}>
            {(p) => <input {...p} type="email" inputMode="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} />}
          </Champ>
          <Champ id="contact-message" libelle="Votre message" erreur={erreurs.message}>
            {(p) => <textarea {...p} rows={5} maxLength={2000} className={`${p.className} py-2.5 resize-y`} value={message} onChange={(e) => setMessage(e.target.value)} />}
          </Champ>
          {/* Piège à robots : invisible et hors navigation clavier pour les visiteurs */}
          <div aria-hidden="true" className="absolute -left-[9999px]">
            <label htmlFor="contact-site-web">Ne pas remplir</label>
            <input id="contact-site-web" tabIndex={-1} autoComplete="off" value={robot} onChange={(e) => setRobot(e.target.value)} />
          </div>

          {erreurGlobale && (
            <div role="alert" className="flex gap-2.5 items-start rounded-[10px] border border-[#efb1ab] bg-fds-bad-bg px-3.5 py-3 text-sm text-fds-bad">
              <TriangleAlert className="w-5 h-5 shrink-0" aria-hidden="true" />
              <span>{erreurGlobale}</span>
            </div>
          )}
          <button
            type="submit"
            disabled={enCours}
            className="min-h-12 px-4 rounded-lg bg-fds-navy hover:bg-fds-navy-d disabled:opacity-60 text-white font-semibold flex items-center justify-center transition-colors"
          >
            {enCours ? 'Envoi…' : 'Envoyer le message'}
          </button>
        </form>
      )}
    </div>
  );
};
