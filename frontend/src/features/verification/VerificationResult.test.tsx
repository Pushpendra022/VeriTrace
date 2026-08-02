import { render,screen } from '@testing-library/react'
import { describe,expect,it } from 'vitest'
import { VerificationResult } from './VerificationResult'

describe('VerificationResult',()=>{it('renders verdict and exact evidence',()=>{render(<VerificationResult result={{verification_id:'v',claim_id:'c',verdict:'SUPPORTED',confidence:.94,quote:'Revenue reached $11.4 million.',explanation:'The source directly supports the claim.',source:{document_id:'d',document_name:'summary.pdf',page_number:3,chunk_id:'x',start_char:1,end_char:10},checks:{quote_verified:true,numbers_consistent:true,percentages_consistent:true,dates_consistent:true,currency_consistent:true},metrics:{latency_ms:10,chunks_searched:5,chunks_retrieved:2,context_characters:300,provider:'mock',model:'test',prompt_version:'verification-v1'},created_at:'2026-01-01'}}/>);expect(screen.getByText('SUPPORTED')).toBeInTheDocument();expect(screen.getByText('Revenue reached $11.4 million.')).toBeInTheDocument();expect(screen.getByText('94%')).toBeInTheDocument()})})

