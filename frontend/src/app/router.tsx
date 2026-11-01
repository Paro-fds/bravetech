import { createBrowserRouter, Navigate } from 'react-router-dom';
import { RootLayout } from './layout/RootLayout';
import { FlowLayout } from './layout/FlowLayout';
import { HomePage } from '../pages/home';
import { CursusDetailPage } from '../pages/cursus-detail';
import { ApplyPage } from '../pages/apply';
import { RemplacerPiecePage, SuiviPage } from '../pages/suivi';
import { AdminLayout } from './layout/AdminLayout';
import { AdminLoginPage } from '../pages/admin-login';
import { AdminCandidaturesPage } from '../pages/admin-candidatures';
import { AdminDossierPage } from '../pages/admin-dossier';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <RootLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'cursus/:id',
        element: <CursusDetailPage />,
      },
    ],
  },
  {
    // Tunnel de candidature : mise en page des maquettes, sans menu ni pied de page
    path: '/postuler',
    element: <FlowLayout />,
    handle: { titre: 'Candidature' },
    children: [
      {
        index: true,
        element: <ApplyPage />,
      },
    ],
  },
  {
    // Suivi par référence : même mise en page que le tunnel (maquettes « Suivi » et « Dossier »)
    path: '/suivi',
    element: <FlowLayout />,
    handle: { titre: 'Suivi de dossier' },
    children: [
      { index: true, element: <SuiviPage /> },
      { path: ':reference', element: <SuiviPage /> },
      { path: ':reference/remplacer/:piece', element: <RemplacerPiecePage /> },
    ],
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
    ],
  },
]);
