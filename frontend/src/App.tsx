import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { AppLayout } from './layouts/AppLayout'
import { HistoryPage } from './pages/HistoryPage'
import { HowItWorksPage } from './pages/HowItWorksPage'
import { NewReviewPage } from './pages/NewReviewPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ReviewWorkspacePage } from './pages/ReviewWorkspacePage'

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { path: '/', element: <NewReviewPage /> },
      { path: '/history', element: <HistoryPage /> },
      { path: '/how-it-works', element: <HowItWorksPage /> },
      { path: '/reviews/:documentId', element: <ReviewWorkspacePage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export function App() { return <RouterProvider router={router} /> }
