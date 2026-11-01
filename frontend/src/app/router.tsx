import { createBrowserRouter } from 'react-router-dom';
import { RootLayout } from './layout/RootLayout';
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
      {
        path: 'postuler',
        element: <ApplyPage />,
      },
    ],
  },
]);
