import { QueryClient,QueryClientProvider } from '@tanstack/react-query'
import { fireEvent,render,screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe,expect,it } from 'vitest'
import { UploadPanel } from './UploadPanel'

function renderPanel(){render(<QueryClientProvider client={new QueryClient()}><MemoryRouter><UploadPanel/></MemoryRouter></QueryClientProvider>)}
describe('UploadPanel',()=>{it('rejects unsupported files',()=>{renderPanel();const input=document.querySelector('input[type=file]') as HTMLInputElement;fireEvent.change(input,{target:{files:[new File(['data'],'report.csv',{type:'text/csv'})]}});expect(screen.getByRole('alert')).toHaveTextContent('PDF, TXT, or Markdown')});it('shows a selected valid file',()=>{renderPanel();const input=document.querySelector('input[type=file]') as HTMLInputElement;fireEvent.change(input,{target:{files:[new File(['Revenue was 10.'],'report.txt',{type:'text/plain'})]}});expect(screen.getByText('report.txt')).toBeInTheDocument();expect(screen.getByRole('button',{name:'Upload document'})).toBeEnabled()})})

