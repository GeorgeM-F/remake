import { useState, useEffect } from 'react'
function App() {
  const [posts, setPosts] = useState([])
  const [author, setAuthor] = useState('')
  const [content, setContent] = useState('')
  // Carica i post dal backend
  const fetchPosts = async () => {
    const res = await fetch('http://localhost:8000/posts')
    const data = await res.json()
    setPosts(data)
  }
  useEffect(() => {
    fetchPosts()
  }, [])
  // Invia un nuovo post
  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!author || !content) return
      await fetch('http://localhost:8000/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author, content }),
      })
      setAuthor('')
      setContent('')
      fetchPosts() // Ricarica la lista
  }
  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: 'auto' }}>
    <h1>Mini Forum</h1>
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
    <input
    type="text"
    placeholder="Nome utente"
    value={author}
    onChange={(e) => setAuthor(e.target.value)}
    style={{ display: 'block', marginBottom: '10px', width: '100%' }}
    />
    <textarea
    placeholder="Scrivi un messaggio..."
    value={content}
    onChange={(e) => setContent(e.target.value)}
    style={{ display: 'block', marginBottom: '10px', width: '100%' }}
    />
    <button type="submit">Pubblica</button>
    </form>
    <h2>Discussioni</h2>
    {posts.map((p) => (
      <div key={p.id} style={{ borderBottom: '1px solid #ccc', padding: '10px 0' }}>
      <strong>{p.author}</strong>
      <p>{p.content}</p>
      </div>
    ))}
    </div>
  )
}
export default App
