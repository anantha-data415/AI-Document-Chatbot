import React, { useState } from 'react'
import { createRoot } from 'react-dom/client'
import './style.css'

const API = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Hi! Upload a PDF or TXT document, then ask a question about it.' }
  ])
  const [busy, setBusy] = useState(false)

  async function upload() {
    if (!file) return setStatus('Choose a PDF or TXT file first.')
    setBusy(true); setStatus('')
    try {
      const body = new FormData()
      body.append('file', file)
      const res = await fetch(`${API}/upload`, { method: 'POST', body })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Upload failed')
      setStatus(`Ready: ${data.filename} (${data.chunks} text sections processed)`)
    } catch (e) {
      setStatus(`${e.message}. Is the FastAPI server running?`)
    } finally { setBusy(false) }
  }

  async function ask(e) {
    e.preventDefault()
    const q = question.trim()
    if (!q || busy) return
    setMessages(prev => [...prev, { role: 'user', text: q }])
    setQuestion(''); setBusy(true)
    try {
      const res = await fetch(`${API}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Could not get an answer')
      const sources = (data.sources || []).map(s => `• ${s.document}, section ${s.section}: ${s.excerpt}`).join('\n')
      setMessages(prev => [...prev, { role: 'assistant', text: `${data.answer}\n\nMode: ${data.mode}${sources ? `\n\nSources:\n${sources}` : ''}` }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', text: `${err.message}. Please check the backend and upload a document.` }])
    } finally { setBusy(false) }
  }

  return <main className="shell">
    <header>
      <div className="logo">D</div>
      <div><p className="eyebrow">DOCUMENT INTELLIGENCE</p><h1>DocuChat</h1></div>
      <span className="pill">AI assistant</span>
    </header>
    <section className="intro">
      <h2>Your documents, easier to explore.</h2>
      <p>Upload a document and ask questions. Answers are based on relevant text found in your file.</p>
    </section>
    <section className="upload panel">
      <div><h3>1. Add a document</h3><p>PDF or TXT · maximum 10 MB</p></div>
      <input type="file" accept=".pdf,.txt" onChange={e => setFile(e.target.files?.[0] || null)} />
      <button onClick={upload} disabled={busy}>{busy ? 'Please wait…' : 'Process document'}</button>
      {status && <p className="status">{status}</p>}
    </section>
    <section className="chat panel">
      <div className="chat-title"><div><h3>2. Ask your document</h3><p>Try a question answered by your file.</p></div><span className="online">● Ready</span></div>
      <div className="messages">
        {messages.map((m, i) => <div className={`message ${m.role}`} key={i}>
          <span className="speaker">{m.role === 'user' ? 'YOU' : 'DOCUCHAT'}</span>
          <p>{m.text}</p>
        </div>)}
        {busy && <div className="message assistant"><p>Working on your question…</p></div>}
      </div>
      <form onSubmit={ask}>
        <input value={question} onChange={e => setQuestion(e.target.value)} placeholder="Ask something about your document…" />
        <button disabled={busy || !question.trim()}>Ask ↗</button>
      </form>
      <p className="note">Demo project: documents are stored temporarily in server memory and are cleared when the server restarts.</p>
    </section>
    <footer>Built as an educational portfolio starter · Do not upload sensitive documents</footer>
  </main>
}

createRoot(document.getElementById('root')).render(<App />)
