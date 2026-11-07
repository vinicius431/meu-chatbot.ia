import React, { useState, useRef, useEffect } from 'react';

/* 🚨 NÃO REMOVER OU ALTERAR: Importações essenciais para a renderização de Markdown e tabelas */
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'; 

/* 🚨 NÃO REMOVER OU ALTERAR: Integração com o Backend FastAPI */
import { sendMessageToBackend } from './services/api';
import './App.css';

function App() {
  /* 🚨 NÃO REMOVER OU ALTERAR: Estado inicial das mensagens */
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Olá! Sou o teu assistente de IA. Como te posso ajudar hoje?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  /* Estado para gerir a lista de conversas na Sidebar */
  const [chatHistory, setChatHistory] = useState([
    'Conversa Atual'
  ]);

  /* 🚨 NÃO REMOVER OU ALTERAR: Referência para auto-scroll automático */
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  /* 🚨 NÃO REMOVER OU ALTERAR: Hook que força o scroll até ao fundo quando há nova mensagem */
  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  /* 🚨 NÃO REMOVER OU ALTERAR: Função principal de envio e resposta com a API */
  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { sender: 'user', text: userMessage }]);
    setLoading(true);

    const botResponse = await sendMessageToBackend(userMessage);

    setMessages((prev) => [...prev, { sender: 'bot', text: botResponse }]);
    setLoading(false);
  };

  const startNewChat = () => {
    setMessages([
      { sender: 'bot', text: 'Nova conversa iniciada. Como posso ajudar?' }
    ]);
  };

  return (
    <div className="app-layout">
      {/* --- BARRA LATERAL (SIDEBAR) --- */}
      <aside className="sidebar">
        <div className="sidebar-top">
          <button className="new-chat-btn" onClick={startNewChat}>
            <span>+</span> Nova Conversa
          </button>
          
          <div className="sidebar-history">
            <div style={{ fontSize: '12px', color: '#64748b', padding: '4px 12px', fontWeight: '600' }}>
              HISTÓRICO
            </div>
            {chatHistory.map((title, idx) => (
              <div key={idx} className={`history-item ${idx === 0 ? 'active' : ''}`}>
                {title}
              </div>
            ))}
          </div>
        </div>
        
        <div style={{ fontSize: '12px', color: '#64748b', textAlign: 'center', paddingBottom: '4px' }}>
          FastAPI + React v1.0
        </div>
      </aside>

      {/* --- ÁREA PRINCIPAL DO CHAT --- */}
      <main className="chat-main">
        <div className="chat-container">
          <header className="chat-header">
            <h1>Chatbot IA - FastAPI & React</h1>
            <span className="status-badge">Online</span>
          </header>

          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                <div className="message-bubble">
                  {/* 🚨 NÃO REMOVER OU ALTERAR: Renderização condicional com ReactMarkdown + remarkGfm */}
                  {msg.sender === 'bot' ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.text}
                    </ReactMarkdown>
                  ) : (
                    msg.text
                  )}
                </div>
              </div>
            ))}
            
            {/* 🚨 NÃO REMOVER OU ALTERAR: Indicador de carregamento */}
            {loading && (
              <div className="message bot">
                <div className="message-bubble loading">
                  <span>.</span><span>.</span><span>.</span>
                </div>
              </div>
            )}
            
            {/* 🚨 NÃO REMOVER OU ALTERAR: Âncora de Auto-Scroll */}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-wrapper">
            {/* 🚨 NÃO REMOVER OU ALTERAR: Formulário de envio */}
            <form className="chat-input-form" onSubmit={handleSend}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Escreve a tua mensagem..."
                disabled={loading}
              />
              <button type="submit" disabled={loading || !input.trim()}>
                Enviar
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;