import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { DocumentViewer } from './DocumentViewer'
import type { Verification } from '../../types'

const pages=[{id:'p1',document_id:'d',page_number:1,text:'Revenue reached $11.4 million.',start_char:0,end_char:30},{id:'p2',document_id:'d',page_number:2,text:'Margin was 67%.',start_char:31,end_char:46}]
const result:Verification={verification_id:'v',claim_id:'c',verdict:'SUPPORTED',confidence:.9,quote:'Revenue reached $11.4 million.',explanation:'Supported.',source:{document_id:'d',document_name:'report.pdf',page_number:1,chunk_id:'x',start_char:0,end_char:30},checks:{quote_verified:true,numbers_consistent:true,percentages_consistent:true,dates_consistent:true,currency_consistent:true},metrics:{latency_ms:1,chunks_searched:2,chunks_retrieved:1,context_characters:30,provider:'mock',model:'mock',prompt_version:'v1'},created_at:'2026-01-01'}
describe('DocumentViewer',()=>{it('highlights exact evidence and supports page navigation',()=>{render(<DocumentViewer pages={pages} result={result}/>);expect(screen.getByText('Revenue reached $11.4 million.').tagName).toBe('MARK');fireEvent.click(screen.getByRole('button',{name:'Next page'}));expect(screen.getByText('Margin was 67%.')).toBeInTheDocument()})})

