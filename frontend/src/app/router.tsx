import { createBrowserRouter } from 'react-router-dom';
import { RootLayout } from './layout/RootLayout';
import { FlowLayout } from './layout/FlowLayout';
import { HomePage } from '../pages/home';
import { CursusDetailPage } from '../pages/cursus-detail';
import { ApplyPage } from '../pages/apply';

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
    children: [
      {
        index: true,
        element: <ApplyPage />,
      },
    ],
  },
]);
