import { createBrowserRouter } from 'react-router-dom';
import { RootLayout } from './layout/RootLayout';
import { HomePage } from '../pages/home';
import { CursusDetailPage } from '../pages/cursus-detail';

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
]);
