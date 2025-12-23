import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Registerpage from '../Page/Registerpage.jsx'
import Homepage from '../Page/Homepage.jsx'
import Chatpage from '../Page/Chatpage.jsx'
const router = createBrowserRouter([
  {
    path: '/',
    element: <App/>,
  },
  {
    path: 'register',
    element:<Registerpage/>
  },
  {
    path: 'home',
    element:<Homepage/>
  },{
    path: 'chat',
    element:<Chatpage/>
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router ={router}/>
  </StrictMode>,
)
