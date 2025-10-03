import { useState, useEffect, useRef } from 'react';
import ChatHeader from './components/ChatHeader';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import SettingsModal from './components/SettingsModal';
import { Message } from './types/chat';
import { sendMessage } from './services/chatService';
import { Loader2 } from 'lucide-react';

const STORAGE_KEY = 'vishwalpha_api_url';
const DEFAULT_API_URL = 'http://localhost:8000/api/chat';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hello! I'm Vishwalpha Bot. How can I assist you today?",
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [apiUrl, setApiUrl] = useState(() => {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_API_URL;
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending message
  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(content, apiUrl);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: error instanceof Error ? error.message : 'An error occurred',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSaveSettings = (newApiUrl: string) => {
    setApiUrl(newApiUrl);
    localStorage.setItem(STORAGE_KEY, newApiUrl);
  };

  return (
    <div className="fixed bottom-4 right-4 w-96 h-[750px] bg-white shadow-lg rounded-xl flex flex-col z-50 resize overflow-auto transition-all duration-200">
      {/* Header */}
      <ChatHeader onSettingsClick={() => setIsSettingsOpen(true)} />

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-2 bg-gray-50">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex gap-2 p-2 bg-gray-100 rounded-md items-center">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-600 flex items-center justify-center">
              <Loader2 className="w-4 h-4 text-white animate-spin" />
            </div>
            <div className="flex-1 space-y-1">
              <div className="font-medium text-xs text-slate-900">Vishwalpha Bot</div>
              <div className="text-slate-500 text-xs">Thinking...</div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-2 border-t border-gray-300">
        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        apiUrl={apiUrl}
        onSave={handleSaveSettings}
      />
    </div>
  );
}

export default App;
