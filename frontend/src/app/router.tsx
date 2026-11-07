import { createBrowserRouter, Navigate } from 'react-router-dom';
import { FlowLayout } from './layout/FlowLayout';
import { HomePage } from '../pages/home';
import { CursusDetailPage } from '../pages/cursus-detail';
import { ApplyPage } from '../pages/apply';
import { RemplacerPiecePage, SuiviPage } from '../pages/suivi';
import { SiteLayout } from './layout/SiteLayout';
import { HistoryPage } from '../pages/histoire';
import { ContactPage } from '../pages/contact';
import { ConfidentialitePage } from '../pages/confidentialite';
import { NotFoundPage } from '../pages/not-found';
import { AdminLayout } from './layout/AdminLayout';
import { AdminLoginPage } from '../pages/admin-login';
import { AdminCandidaturesPage } from '../pages/admin-candidatures';
import { AdminDossierPage } from '../pages/admin-dossier';
import { AdminCalendrierPage } from '../pages/admin-calendrier';
import { AdminSmsPage } from '../pages/admin-sms';
import { AdminUtilisateursPage } from '../pages/admin-utilisateurs';

export const router = createBrowserRouter([
  {
    // Tunnel de candidature : mise en page des maquettes, sans menu ni pied de page
    path: '/postuler',
    element: <FlowLayout />,
    handle: { titre: 'flux.titreCandidature' },
    children: [
      {
        index: true,
        element: <ApplyPage />,
      },
    ],
  },
  {
    // Pages publiques (maquettes « Accueil », « Cursus », « Histoire », « Contact » et « Suivi »)
    element: <SiteLayout />,
    children: [
      { path: '/', element: <HomePage /> },
      { path: '/cursus/:id', element: <CursusDetailPage /> },
      { path: '/histoire', element: <HistoryPage /> },
      { path: '/contact', element: <ContactPage /> },
      // Suivi par référence : en-tête public et pied de page (maquettes « Suivi » et « Dossier », US-022)
      { path: '/suivi', element: <SuiviPage /> },
      { path: '/suivi/:reference', element: <SuiviPage /> },
      // Mentions légales, confidentialité et avertissement anti-fraude
      { path: '/confidentialite', element: <ConfidentialitePage /> },
      // Toute adresse publique inconnue affiche une page 404 explicite
      { path: '*', element: <NotFoundPage /> },
    ],
  },
  {
    // Remplacement d'une pièce : en-tête allégé « Dossier CAN-… » (maquette « Remplacement »)
    path: '/suivi/:reference/remplacer/:piece',
    element: <FlowLayout />,
    handle: { titre: 'flux.titreDossier' },
    children: [{ index: true, element: <RemplacerPiecePage /> }],
  },
  // Espace administration (US-011) : connexion publique, le reste exige une session
  { path: '/admin/login', element: <AdminLoginPage /> },
  {
    path: '/admin',
    element: <AdminLayout />,
    children: [
      { index: true, element: <AdminCandidaturesPage /> },
      { path: 'dashboard', element: <Navigate to="/admin" replace /> },
      { path: 'candidatures/:reference', element: <AdminDossierPage /> },
      // Calendrier d'admission réglable sans toucher au code (US-028)
      { path: 'calendrier', element: <AdminCalendrierPage /> },
      // SMS simulés envoyés aux candidats (US-016)
      { path: 'sms', element: <AdminSmsPage /> },
      // Gestion des accès du personnel (administrateurs et agents du secrétariat)
      { path: 'utilisateurs', element: <AdminUtilisateursPage /> },
    ],
  },
]);
