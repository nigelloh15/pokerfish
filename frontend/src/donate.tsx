import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Money from './donate/money'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Money />
  </StrictMode>,
)
